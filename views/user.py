from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from tortoise.contrib.fastapi import HTTPNotFoundError
from passlib.hash import bcrypt
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter
from models import UserIn_Pydantic, User_Pydantic, User


router = APIRouter()


class Status(BaseModel):
    message: str

JWT_SECRET = 'myjwtsecret'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password=password):
        return False
    return user

@router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        return {'error': 'Invalid Credentials'}
    
    user_obj = await User_Pydantic.from_tortoise_orm(user) 
    user_obj.id = str(user_obj.id)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {'access_token': token, 'token_type': 'bearer'}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    return await User_Pydantic.from_tortoise_orm(user)

@router.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user

@router.get('/users', response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(User.all())

@router.get('/user/{email}')
async def get_user(user_email: str):
    try:
        return await User_Pydantic.from_queryset_single(User.get(email=user_email))
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with email-{user_email} not found'
        )

@router.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    # user_obj = await User.create(**user.dict(exclude_unset=True))
    existing_user_email = await User.filter(email=user.email)
    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'Email already exists.'
        )
    
    existing_user_username = await User.filter(username=user.username)
    if existing_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'Username already exists.'
        )

    user_obj = User(username=user.username, email=user.email, password=bcrypt.hash(user.password))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@router.put('/user/{email}', response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def edit_user(user_email: str, username: str, password: str):
    # await User.filter(email=user_email).update(**user.dict(exclude_unset=True))
    try:
        await User.filter(email=user_email).update(username=username, password=bcrypt.hash(password))
        return await User_Pydantic.from_queryset_single(User.get(email=user_email))
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with email-{user_email} not found'
        )


@router.delete('/user/{email}', response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_email: str):
    deleted_count = await User.filter(email=user_email).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User with email {user_email} not found")
    return Status(message=f"Deleted user with email: {user_email}")
