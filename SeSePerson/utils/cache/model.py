import hashlib
from pathlib import Path
from typing import Optional

from nonebot.adapters.onebot.v12 import Bot, ActionFailed
from tortoise import Model
from tortoise.exceptions import DoesNotExist
from tortoise.fields import CharField, UUIDField

from SeSePerson.plugins.database import add_plugin

APP_NAME = "cache"
add_plugin(APP_NAME, [__name__])


class FileCache(Model):
    sha256 = CharField(pk=True, max_length=64)
    fileid = UUIDField()

    @classmethod
    async def save_fileid(cls, sha256: str, fileid: str) -> None:
        try:
            cache = await cls.get(sha256=sha256)
            cache.fileid = fileid
        except DoesNotExist:
            cache = cls(sha256=sha256, fileid=fileid)
        await cache.save()

    @classmethod
    async def get_fileid(cls, sha256: str) -> Optional[str]:
        try:
            return str((await cls.get(sha256=sha256)).fileid)
        except DoesNotExist:
            return None

    @classmethod
    async def upload_file(cls, path: Path, bot: Bot) -> str:
        data = path.read_bytes()
        sha256 = hashlib.sha256(data).hexdigest()
        cache = await cls.get_or_none(sha256=sha256)
        if cache is not None:
            # 检验
            try:
                await bot.get_file(type="path", file_id=str(cache.fileid))
            except ActionFailed:
                cache = None

        if cache is None:
            # 上传文件
            fileid = (await bot.upload_file(type="data", name=path.name, data=data, sha256=sha256))["file_id"]
            await cls.save_fileid(sha256, fileid)
        else:
            fileid = str(cache.fileid)

        return fileid
