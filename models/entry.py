from tortoise.models import Model
from tortoise import fields
from .category import Category


class Entry(Model):
    id = fields.UUIDField(pk=True)
    category = fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        'models.Category', related_name='entry'
    )
    title = fields.CharField(255)
    content = fields.CharField(255)
    images = fields.JSONField()
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = field.DatetimeField(null=True, auto_now=True)
