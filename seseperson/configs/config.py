from pathlib import Path
from time import sleep

import yaml

from .create import init_config
from .models import ConfigModel, BotConfig, RuntimeConfig

_DEFAULT_CONFIG_PATH = Path(__file__) / ".." / "default_config.yml"


class Config:
    def __init__(self, config_path: Path):
        if not config_path.is_file():
            init_config(config_path, _DEFAULT_CONFIG_PATH)
            sleep(3)

        raw_conf = yaml.safe_load(_DEFAULT_CONFIG_PATH.read_bytes())
        conf = yaml.safe_load(config_path.read_bytes())

        if raw_conf.get("ConfigVersion") != conf.get("ConfigVersion"):
            print("!!! 你的 config.yml 文件已废弃, 请 删除/备份 并重新启动")
            sleep(3)
            exit(-1)

        self.config = conf

    def parse(self) -> ConfigModel:
        return ConfigModel.parse_obj(self.config)

    def get_runtime_conf(self) -> dict:
        bot_conf = BotConfig.parse_obj(self.config["BotConfig"])

        return RuntimeConfig(
            host=bot_conf.host,
            port=bot_conf.port,
            debug=bot_conf.debug,
            superusers=bot_conf.superusers,
            nickname=bot_conf.nickname,
            onebot_access_token=bot_conf.access_token,
            command_start=bot_conf.command_start,
            command_sep=bot_conf.command_sep,
            session_expire_timeout=bot_conf.session_expire_timeout,
        ).dict()
