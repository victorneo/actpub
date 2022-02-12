from dotenv import load_dotenv
from typing import Optional
from fastapi import Depends, FastAPI
from sqlmodel import Session
from sqlmodel.sql.expression import Select, SelectOfScalar
from db.db import engine
from api import users


load_dotenv()

# https://github.com/tiangolo/sqlmodel/issues/189
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

app = FastAPI()
app.include_router(users.router)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/")
async def read_root():
    return {"Hello": "World"}