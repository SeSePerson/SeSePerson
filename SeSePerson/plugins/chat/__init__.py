from typing import Annotated

from nonebot import on_message, logger, require
from nonebot.adapters.onebot import v12 as onebot
from nonebot.params import EventPlainText
from nonebot.rule import to_me

from SeSePerson.utils.config import get_config
from .config import Config
from .model import Contact
from .session import Session

config = get_config("chat", Config)
require("database")

session = Session(openai_key=config.openai_key,
                  template=config.template,
                  max_history=config.max_history)


async def is_text(text: Annotated[str, EventPlainText()]) -> bool:
    return bool(text)


chat = on_message(rule=to_me() & is_text, block=True, priority=100)


@chat.handle()
async def _(bot: onebot.Bot, event: onebot.MessageEvent, text: Annotated[str, EventPlainText()]):
    if isinstance(event, onebot.GroupMessageEvent):
        contact_id = event.group_id
    else:
        contact_id = event.get_session_id()

    user_name = (await bot.get_user_info(user_id=event.get_user_id())).get("user_name", None)

    async with session.talk(contact_id, text, user_name) as stream:
        async for s in stream:
            await chat.send(s)
