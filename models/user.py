from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(255, unique=True)
    username = fields.CharField(50, unique=True)
    password = fields.CharField(200)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = field.DatetimeField(null=True, auto_now=True)

