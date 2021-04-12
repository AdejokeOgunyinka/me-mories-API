from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from .category import Category
from .user import User


class Entry(Model):
    id = fields.UUIDField(pk=True)
    category= fields.CharField(255)
    user = fields.CharField( 255)
    title = fields.CharField(255)
    content = fields.CharField(255)
    images = fields.JSONField(null=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    class PydanticMeta:
        exclude = ['created_at', 'updated_at', 'user']


Entry_Pydantic = pydantic_model_creator(Entry, name='Entry')
EntryIn_Pydantic = pydantic_model_creator(Entry, name='EntryIn', exclude_readonly=True)
