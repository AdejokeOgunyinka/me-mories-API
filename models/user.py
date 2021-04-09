from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(255, unique=True)
    username = fields.CharField(50, unique=True)
    password = fields.CharField(200)
    # entries: fields.ReverseRelation['Entry']
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    def verify_password(self, my_password):
        return bcrypt.verify(my_password, self.password)

    class PydanticMeta:
        exclude = ['created_at', 'updated_at']



User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
