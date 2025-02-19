from .model import FileCache

import json
from pathlib import Path
from typing import Type, TypeVar
from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as, to_yaml_file

BASE_CACHE_DIR = (Path(__file__).parents[2] / "caches").resolve()
BASE_CACHE_DIR.mkdir(exist_ok=True)


def get_cache_path(name: str) -> Path:
    path = BASE_CACHE_DIR / f"{name}"
    path.mkdir(exist_ok=True)
    return path