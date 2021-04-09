from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI()

register_tortoise(
    app,
    db_url='sqlite://memories_db',
    modules={'models': ['models']},
    generate_schemas=True, #generate the schema if it does not exist or find it if it does exist.
    add_exception_handlers=True
)
