import base64
from enum import Enum

from seseperson.plugins.database import add_plugin
from tortoise import Model
from tortoise.fields import CharField, IntField, ForeignKeyField, TextField, DatetimeField, CharEnumField, BinaryField

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
    image = BinaryField(null=True)
    content = TextField()  # 消息内容
    time = DatetimeField(auto_now_add=True)  # 消息发送时间

    def to_dict(self, enable_image: bool = False) -> dict:
        return {
            "role": self.role.value,
            "content": (
                self.content
                if (self.image is None) or not enable_image
                else [
                    {"type": "text", "text": self.content},
                    {"type": "image_url", "image_url":
                        {"url": f"data:image/jpeg;base64,{base64.b64encode(self.image).decode('utf-8')}"}}
                ]
            )
        }
