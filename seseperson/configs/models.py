from pydantic import BaseModel


class BotConfig(BaseModel):
    host: str
    port: int
    debug: bool
    superusers: set
    nickname: set
    command_start: set
    command_sep: set
    session_expire_timeout: int
    access_token: str
    proxy: str
    request_timeout: int


class ConfigModel(BaseModel):
    ConfigVersion: str


class RuntimeConfig(BaseModel):
    host: str
    port: int
    debug: bool
    superusers: set
    nickname: set
    onebot_access_token: str
    command_start: set
    command_sep: set
    session_expire_timeout: int
