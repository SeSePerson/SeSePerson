import hashlib
from pathlib import Path
from typing import Annotated

from nonebot import on_message, logger, require, on_command
from nonebot.adapters.onebot import v12 as onebot
from nonebot.params import EventPlainText
from nonebot.rule import to_me

from SeSePerson.utils.config import get_config
from .config import Config
from .model import Contact
from .session import Session
from ...utils.cache import FileCache

RES_DIR = Path(__file__).resolve().parent / "resource"

config = get_config("chat", Config)
require("database")

session = Session(openai_key=config.openai_key,
                  template=config.template,
                  max_history=config.max_history,
                  time_limit=config.time_limit)


def is_text(text: Annotated[str, EventPlainText()]) -> bool:
    return bool(text)


chat = on_message(rule=to_me() & is_text, block=True, priority=100)
brainwash = on_command("brainwash", aliases={"洗脑"}, block=True, priority=99)


def get_contact_id(event: onebot.MessageEvent) -> str:
    if isinstance(event, onebot.GroupMessageEvent):
        return event.group_id
    else:
        return event.get_session_id()


@chat.handle()
async def _(bot: onebot.Bot, event: onebot.MessageEvent, text: Annotated[str, EventPlainText()]):
    contact_id = get_contact_id(event)
    user_name = (await bot.get_user_info(user_id=event.get_user_id())).get("user_name", None)

    async with session.talk(contact_id, text, user_name) as stream:
        async for s in stream:
            await chat.send(s)


@brainwash.handle()
async def _(bot: onebot.Bot, event: onebot.MessageEvent):
    contact_id = get_contact_id(event)
    await session.cut_history(contact_id)

    file_id = await FileCache.upload_file(path=RES_DIR / "brainwash.png", bot=bot)

    message = onebot.MessageSegment("wx.emoji", {"file_id": file_id})
    await brainwash.finish(message)
