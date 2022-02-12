from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from db.db import async_session
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User


router = APIRouter()


class JSONLDResponse(JSONResponse):
    media_type = "application/activity+json"


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
            "subject": resource,
            "aliases": [
                url,
            ],
            "links": [
                {
                "rel": "self",
                "type": "application/activity+json",
                "href": url
                },
            ]
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/users/{username}", response_class=JSONLDResponse)
async def get_user(username: str):
    async with async_session() as s:
        statement = select(User).where(User.username == username)
        results = await s.execute(statement)
        user = results.first()
    
    if user:
        user = user[0]
        url = base_url + 'users/' + user.username
        return {
            '@context': ["https://www.w3.org/ns/activitystreams"],
            'type': 'Person',
            'id': url,
            'following': url + '/following',
            'followers': url + '/followers',
            'liked': url + '/liked',
            'inbox': url + '/inbox',
            'outbox': url + '/outbox',
            'preferredUsername': username,
            'name': user.first_name,
            'summary': '',
            'icon': [],
        }

    raise HTTPException(status_code=404, detail="User not found")


@router.get("/users/id/{user_id}")
async def get_user(user_id: int, response: Response):
    user = None

    async with async_session() as s:
        statement = select(User).where(User.id == user_id)
        results = await s.execute(statement)
        user = results.first()

    if user:
        user = user[0]
        return {"id": user.id, "first_name": user.first_name}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}