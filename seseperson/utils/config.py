from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel

BASE_CONFIG_DIR = (Path(__file__).parents[2] / "configs").resolve()
BASE_CONFIG_DIR.mkdir(exist_ok=True)


def get_config_path(name: str):
    return BASE_CONFIG_DIR / f"{name}.json"


def create_default_config(path: Path, model: Type[BaseModel]) -> None:
    path.write_text(model().json(by_alias=True, ensure_ascii=False, indent=2), encoding="utf-8")


T = TypeVar('T', bound=BaseModel)


def get_config(name: str, model: Type[T]) -> T:
    config_path = get_config_path(name)

    if not config_path.is_file():
        create_default_config(config_path, model)
    return model.parse_raw(config_path.read_text(encoding="utf-8"))
