import json
from pathlib import Path
from types import ModuleType
from typing import Iterable, Union, Optional

from nonebot import get_driver, logger
from tortoise import Tortoise

BASE_DATABASE_DIR = (Path(__file__).parent.parent.parent / "database").resolve()
BASE_DATABASE_DIR.mkdir(exist_ok=True)

TORTOISE_CONFIG = {
    "connections": {},
    "apps": {},
    "use_tz": True,
    "timezone": "Asia/Shanghai",
}

driver = get_driver()


def _add_app(name: str, models: Iterable[Union[ModuleType, str]], connection: Optional[str] = None) -> None:
    if connection is None:
        connection = name
    TORTOISE_CONFIG["apps"][name] = {
        'models': models,
        'default_connection': connection,
    }


def _add_connection(name: str, path: Optional[Path] = None) -> None:
    if path is None:
        path = BASE_DATABASE_DIR / f"{name}.db"
    TORTOISE_CONFIG["connections"][name] = f"sqlite://{path}"


def add_plugin(name: str, models: Iterable[Union[ModuleType, str]]) -> None:
    _add_connection(name)
    _add_app(name, models, name)


@driver.on_startup
async def connect():
    logger.debug("参数预览\n" + json.dumps(TORTOISE_CONFIG, ensure_ascii=False, indent=4))

    await Tortoise.init(TORTOISE_CONFIG)
    await Tortoise.generate_schemas()


@driver.on_shutdown
async def disconnect():
    await Tortoise.close_connections()
    logger.opt(colors=True).success("数据库断开链接")
