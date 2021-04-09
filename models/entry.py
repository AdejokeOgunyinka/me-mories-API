from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from .category import Category
from .user import User


class Entry(Model):
    id = fields.UUIDField(pk=True)
    # fields.ForeignKeyField('models.Tournament', related_name='events')
    category= fields.ForeignKeyField( 'models.Category', related_name='entry')
    user = fields.ForeignKeyField( 'models.User', related_name='entries')
    title = fields.CharField(255)
    content = fields.CharField(255)
    images = fields.JSONField(null=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    class PydanticMeta:
        exclude = ['created_at', 'updated_at']


Entry_Pydantic = pydantic_model_creator(Entry, name='Entry')
EntryIn_Pydantic = pydantic_model_creator(Entry, name='EntryIn', exclude_readonly=True)
