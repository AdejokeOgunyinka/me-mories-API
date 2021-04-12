from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi import APIRouter
from models import Category,  CategoryIn_Pydantic, Category_Pydantic


router = APIRouter()

class Status(BaseModel):
    message: str

@router.get('/categories', response_model=List[Category_Pydantic])
async def get_categories():
    return await Category_Pydantic.from_queryset(Category.all())

@router.get('/category/{name}')
async def get_category(category_name: str):
    try:
        return await Category_Pydantic.from_queryset_single(Category.get(name=category_name.title()))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with name- {category_name} does not exist.")

@router.post('/categories', response_model=Category_Pydantic)
async def create_category(category: CategoryIn_Pydantic):
    try:
        category_obj = Category(name=category.name.title())
        await category_obj.save()
        return await Category_Pydantic.from_tortoise_orm(category_obj)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category with name- {category.name} already exists.")


@router.put('/category/{name}', response_model=Category_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def edit_category(category_name: str, new_category_name: str):
    try:
        await Category.filter(name=category_name.title()).update(name=new_category_name.title())
        return await Category_Pydantic.from_queryset_single(Category.get(name=new_category_name.title()))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with name- {category_name} does not exist.")

@router.delete('/category/{name}', response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_category(category_name: str):
    deleted_count = await Category.filter(name=category_name.title()).delete()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with name- {category_name} not found")
    return Status(message=f"Deleted category with name: {category_name}")
