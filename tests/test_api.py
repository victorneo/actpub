import pytest
from fastapi.testclient import TestClient
from db.db import async_session
from models.users import User, create_user
from app import app


client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'Hello': 'World'}


@pytest.mark.asyncio
async def test_get_user():
    response = client.get('/users/id/91919')
    assert response.status_code == 404
    u = create_user(username='username', first_name='a', last_name='b', email='a@b.com', password='123', profile_pic=None)

    async with async_session() as s:
        s.add(u)
        await s.commit()

    response = client.get('/users/id/{}'.format(u.id))
    assert response.status_code == 200