from dotenv import load_dotenv
from typing import Optional
from fastapi import Depends, FastAPI
from sqlmodel import Session
from db.db import init_db, get_session
from api import users


load_dotenv()


app = FastAPI()
app.include_router(users.router)


@app.get("/")
async def read_root(session: Session = Depends(get_session)):
    return {"Hello": "World"}