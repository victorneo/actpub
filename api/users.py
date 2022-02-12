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


base_url = ''
url = 'https://' + base_url + '/users/vic'


@router.get('/.well-known/webfinger')
async def webfinger(resource: str):
    return {
        "subject": "acct:vic@"+base_url,
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


@router.get("/users/{username}", response_class=JSONLDResponse)
async def get_user(username: str):
    return {
        "@context": ["https://www.w3.org/ns/activitystreams"],
        "type": "Person",
        "id": url,
        "following": url + '/following',
        "followers": url + '/followers',
        "liked": url + '/liked',
        "inbox": url + '/inbox',
        "outbox": url + '/outbox',
        "preferredUsername": "victorneo",
        "name": "Victor Neo",
        "summary": "Dummy profile",
        "icon": [
        ],
    }


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