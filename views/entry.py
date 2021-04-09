from pydantic import BaseModel
from fastapi import FastAPI, Depends
from typing import List
from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi import APIRouter
from models.entry import EntryIn_Pydantic, Entry_Pydantic, Entry


router = APIRouter()


class Status(BaseModel):
    message: str

@router.get('/entries')
async def get_my_entries():
    pass

@router.get('/entry/{title}')
async def get_one_entry():
    pass

@router.post('/entries')
async def create_entry():
    pass

@router.put('/entry/{title}')
async def edit_entry():
    pass

@router.delete('/entry/{title}')
async def delete_entry():
    pass
