import pytest
from models.users import User, create_user


def test_create_user():
    user = create_user('username', 'pw', 'a@b.com', 'FN', 'LN', None)
    assert user.private_key
    assert user.public_key