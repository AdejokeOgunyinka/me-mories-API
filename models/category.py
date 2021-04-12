from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Category(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(255, unique=True)
    # entry: fields.ReverseRelation['Entry']
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    class PydanticMeta:
        exclude = ['created_at', 'updated_at']


Category_Pydantic = pydantic_model_creator(Category, name='Category')
CategoryIn_Pydantic = pydantic_model_creator(Category, name='CategoryIn', exclude_readonly=True)
