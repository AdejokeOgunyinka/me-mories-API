from tortoise.models import Model
from tortoise import fields
from .entry import Entry


class Category(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(255)
    entry: fields.ReverseRelation["Entry"]
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = field.DatetimeField(null=True, auto_now=True)
