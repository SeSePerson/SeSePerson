from pathlib import Path
from time import sleep

import nonebot
from nonebot.adapters.onebot.v12 import Adapter as OneBotV12Adapter

from .configs import Config

__conf_path = Path("") / "configs.yml"
__conf = Config(__conf_path)

conf = __conf.parse()


def asgi():
    return nonebot.get_asgi()


def driver():
    return nonebot.get_driver()


def init():
    nonebot.init(**__conf.get_runtime_conf())
    driver().register_adapter(OneBotV12Adapter)
    nonebot.load_plugins("SeSePerson/plugins")
    sleep(3)


def run():
    log_level = "debug" if conf.BotConfig.debug else "warning"
    nonebot.run(log_level=log_level)
