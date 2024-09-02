import json
from pathlib import Path
from typing import Type, TypeVar
from pydantic import BaseModel
from pydantic_yaml import parse_yaml_raw_as, to_yaml_file

BASE_CONFIG_DIR = (Path(__file__).parents[2] / "configs").resolve()
BASE_CONFIG_DIR.mkdir(exist_ok=True)


def get_config_path(name: str) -> Path:
    return BASE_CONFIG_DIR / f"{name}.yaml"


T = TypeVar('T', bound=BaseModel)


def create_default_config(path: Path, model: Type[T]) -> None:
    # 创建一个模型实例并保存为 YAML 文件
    to_yaml_file(path, model())


def get_config(name: str, model: Type[T]) -> T:
    config_path = get_config_path(name)

    if not config_path.is_file():
        # check old format
        try:
            migrate_config(name, model)
        except FileNotFoundError:
            create_default_config(config_path, model)

    # 从 YAML 文件中解析配置
    with config_path.open('r', encoding='utf-8') as file:
        return parse_yaml_raw_as(model, file.read())


def migrate_config(name: str, model: Type[T]) -> None:
    yaml_path = get_config_path(name)
    json_path = yaml_path.with_suffix(".json")

    if not json_path.is_file():
        raise FileNotFoundError(f"The JSON configuration file does not exist: {json_path}")
    elif yaml_path.is_file():
        raise FileExistsError(f"The YAML configuration file already exists and cannot be overwritten: {yaml_path}")
    else:
        with json_path.open('r', encoding='utf-8') as file:
            config_data = model.parse_raw(file.read())

        # 将模型实例保存为新的 YAML 文件
        to_yaml_file(yaml_path, config_data)

        # 删除旧的 JSON 文件
        json_path.unlink()
