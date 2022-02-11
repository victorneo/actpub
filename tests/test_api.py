import pytest
from fastapi.testclient import TestClient
from db.db import get_session
from models.users import User
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
    u = User(first_name='a', last_name='b', email='a@b.com', password='123')
    session = await get_session()
    session.add(u)
    await session.commit()

    response = client.get('/users/id/{}'.format(u.id))
    assert response.status_code == 200