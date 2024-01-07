import nonebot
from nonebot.adapters import onebot

from .utils import config


def asgi():
    return nonebot.get_asgi()


def driver():
    return nonebot.get_driver()


def init():
    bot_config = config.get_config("nonebot", nonebot.config.Config)
    onebot_config = config.get_config("onebot", onebot.v12.adapter.Config)

    nonebot.init(**bot_config.dict(by_alias=True), **onebot_config.dict(by_alias=True))
    # nonebot.init()

    driver().register_adapter(onebot.V12Adapter)
    nonebot.load_plugins("SeSePerson/plugins")


def run():
    nonebot.run()
