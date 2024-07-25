from enum import Enum

from tortoise import Model
from tortoise.fields import CharField, IntField, ForeignKeyField, TextField, DatetimeField, CharEnumField

from seseperson.plugins.database import add_plugin

APP_NAME = "chat"
add_plugin(APP_NAME, [__name__])


class Contact(Model):
    id = CharField(max_length=20, pk=True)
    cutoff = DatetimeField(null=True)


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    AI = "assistant"


class Message(Model):
    id = IntField(pk=True)
    contact = ForeignKeyField(f'{APP_NAME}.Contact', related_name='messages')
    # username = CharField(max_length=20)  # 发送者的用户名
    role = CharEnumField(MessageRole)
    content = TextField()  # 消息内容
    time = DatetimeField(auto_now_add=True)  # 消息发送时间
