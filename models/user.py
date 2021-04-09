from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt


class User(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(255, unique=True)
    username = fields.CharField(50, unique=True)
    password = fields.CharField(200)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    def verify_password(self, my_password):
        return bcrypt.verify(my_password, self.password)
