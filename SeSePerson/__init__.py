from pathlib import Path
from time import sleep

import nonebot
import nonebot.adapters.onebot.v12 as onebot
from nonebot import logger

from SeSePerson.utils import config


def asgi():
    return nonebot.get_asgi()


def driver():
    return nonebot.get_driver()


def init():
    bot_config = config.get_config("nonebot", nonebot.config.Config)
    onebot_config = config.get_config("onebot", onebot.adapter.Config)

    nonebot.init(**bot_config.dict(), **onebot_config.dict())
    # nonebot.init()

    driver().register_adapter(onebot.Adapter)
    nonebot.load_plugins("SeSePerson/plugins")


def run():
    nonebot.run()
