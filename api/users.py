import os
import base64
from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from db.db import async_session
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from activitypub.activitystreams import ActivityTypes
from activitypub.server import send_activity
from models.users import User


router = APIRouter()


class JSONLDResponse(JSONResponse):
    media_type = 'application/activity+json'


domain = ''
base_url = 'https://' + domain + '/'


@router.get('/.well-known/webfinger')
async def webfinger(resource: str):
    email = resource.split(':')[1]
    async with async_session() as s:
        statement = select(User).where(User.email == email)
        results = await s.execute(statement)
        user = results.first()
    
    if user:
        user = user[0]
        url = base_url + 'users/' + user.username
        return {
            'subject': resource,
            'links': [
                {
                'rel': 'self',
                'type': 'application/activity+json',
                'href': url
                },
            ]
        }
    else:
        raise HTTPException(status_code=404, detail='User not found')


@router.get('/users/{username}', response_class=JSONLDResponse)
async def get_user(username: str):
    async with async_session() as s:
        statement = select(User).where(User.username == username)
        results = await s.execute(statement)
        user = results.first()
    
    if user:
        user = user[0]
        url = base_url + 'users/' + user.username
        return {
            '@context': ['https://www.w3.org/ns/activitystreams', 'https://w3id.org/security/v1'],
            'type': 'Person',
            'id': url,
            'followers': url + '/followers',
            'inbox': url + '/inbox',
            'preferredUsername': user.username,
            'publicKey': {
                'id': url + '#main-key',
                'owner': url,
                'publicKeyPem': user.public_key,
            },
        }

    raise HTTPException(status_code=404, detail='User not found')


@router.get('/users/{username}/following', response_class=JSONLDResponse)
async def get_user_following(username: str):
    return {
        '@context': ['https://www.w3.org/ns/activitystreams'],
        'type': 'OrderedCollection',
        'totalItems': 0,
        'orderedItems': [],
    }


@router.get('/users/{username}/followers', response_class=JSONLDResponse)
async def get_user_followers(username: str):
    return {
        '@context': ['https://www.w3.org/ns/activitystreams'],
        'type': 'OrderedCollection',
        'totalItems': 0,
        'orderedItems': [],
    }


@router.get('/users/{username}/inbox', response_class=JSONLDResponse)
async def get_user_inbox(username: str):
    return {
        '@context': ['https://www.w3.org/ns/activitystreams'],
        'type': 'OrderedCollection',
        'totalItems': 0,
        'orderedItems': [],
    }


@router.post('/users/{username}/inbox', response_class=JSONLDResponse)
async def post_user_inbox(username: str, request: Request, response: Response):
    req = await request.json()

    async with async_session() as s:
        statement = select(User).where(User.username == username)
        results = await s.execute(statement)
        user = results.first()

    if user:
        user = user[0]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}

    if req['type'] == ActivityTypes.FOLLOW.value:
        follower = req['actor']
        actor_id = base_url + 'users/' + user.username

        body = {
            '@context': 'https://www.w3.org/ns/activitystreams',
            'id': base_url + base64.b64encode(os.urandom(16)).hex(),
            'type': 'Accept',
            'actor': actor_id,
            'object': req,
        }

        await send_activity(user.private_key, actor_id, follower, body)

        response.status_code = status.HTTP_201_CREATED
        return {}

    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return {}


@router.get('/users/{username}/outbox', response_class=JSONLDResponse)
async def get_user_outbox(username: str):
    return {
        '@context': ['https://www.w3.org/ns/activitystreams'],
        'type': 'OrderedCollection',
        'totalItems': 0,
        'orderedItems': [],
    }


@router.get('/users/id/{user_id}')
async def get_user(user_id: int, response: Response):
    user = None

    async with async_session() as s:
        statement = select(User).where(User.id == user_id)
        results = await s.execute(statement)
        user = results.first()

    if user:
        user = user[0]
        return {'id': user.id, 'first_name': user.first_name}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}