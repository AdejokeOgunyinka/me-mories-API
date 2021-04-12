from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi import APIRouter
import fastapi.openapi.utils as fastapi_utils
from models.entry import EntryIn_Pydantic, Entry_Pydantic, Entry
from models.user import User
from models.category import Category, Category_Pydantic
from .user import get_current_user, get_user


router = APIRouter()

# and override the schema

class Status(BaseModel):
    message: str

@router.get('/entries', response_model=List[Entry_Pydantic])
async def get_my_entries(current_user: User = Depends(get_current_user)):
    return await Entry_Pydantic.from_queryset(Entry.filter(user=current_user.username))

@router.get('/entry/{title}', response_model=Entry_Pydantic)
async def get_one_entry(entry_title: str, current_user: User = Depends(get_current_user)):
    try:
        return await Entry_Pydantic.from_queryset_single(Entry.get(user=current_user.username, title=entry_title))
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Diary entry with title-{entry_title} does not exist.'
        )

@router.post('/entries', response_model=Entry_Pydantic)
async def create_entry(entry: EntryIn_Pydantic, current_user: User = Depends(get_current_user)):
    category_instance = await Category.filter(name=entry.category.title())
    if category_instance:
        entry_obj = Entry(category=category_instance.name, user=current_user.username, title=entry.title, content=entry.content, images=entry.images)
        await entry_obj.save()
        return await Entry_Pydantic.from_tortoise_orm(entry_obj)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Diary entry with category-{entry.category} does not exist.'
        )

@router.put('/entry/{title}', response_model=Entry_Pydantic)
async def edit_entry(entry_title: str, new_entry_title: str, new_entry_content: str, new_entry_images: dict, current_user: User = Depends(get_current_user)):
    try:
        await Entry.filter(user=current_user.username, title=entry_title).update(title=new_entry_title, content=new_entry_content, images=new_entry_images)
        return await Entry_Pydantic.from_queryset_single(Entry.get(title=new_entry_title))
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Diary entry with title-{entry_title} does not exist.'
        )

@router.delete('/entry/{title}')
async def delete_entry(entry_title: str, current_user: User = Depends(get_current_user)):
    deleted_count = await Entry.filter(user=current_user.username, title=entry_title).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Entry with title {entry_title} not found")
    return Status(message=f"Deleted entry with title: {entry_title}")
