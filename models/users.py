from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, VARCHAR, Column
from pydantic import EmailStr


class UserGroup(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

    users: List["User"] = Relationship(back_populates="group")


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column('username', VARCHAR, unique=True))
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    public_key: str
    private_key: str
    profile_pic: Optional[str]
    is_staff: bool = Field(default=False)

    group_id: Optional[int] = Field(foreign_key="usergroup.id")
    group: Optional[UserGroup] = Relationship(back_populates="users")


def generate_new_pk() -> RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=4096)


def load_pk(pkstr: str) -> RSAPrivateKey:
    loaded_pk = serialization.load_pem_private_key(pkstr, password=None)


def create_user(username: str, password: str, email: str, first_name: str, last_name: str, profile_pic: Optional[str]) -> User:
    user = User(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        profile_pic=profile_pic,
    )

    pk = generate_new_pk()
    pub_key = pk.public_key()

    user.public_key = pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode('utf-8')

    user.private_key = pk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    return user