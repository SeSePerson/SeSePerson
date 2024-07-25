import hashlib
from pathlib import Path
from typing import Optional

from nonebot.adapters.onebot.v12 import Bot, ActionFailed
from tortoise import Model
from tortoise.exceptions import DoesNotExist
from tortoise.fields import CharField, UUIDField

from seseperson.plugins.database import add_plugin

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
    async def upload_file(cls, path: Path | str, bot: Bot) -> str:
        data = path.read_bytes()
        return await cls.upload_bytes(data=data, name=path.name, bot=bot)

    @classmethod
    async def upload_bytes(cls, data: bytes, name: str, bot: Bot) -> str:
        # 计算数据的SHA256哈希值
        sha256 = hashlib.sha256(data).hexdigest()
        # 尝试从缓存中获取文件ID
        cache = await cls.get_or_none(sha256=sha256)
        if cache is not None:
            # 检验文件是否仍在缓存中
            try:
                await bot.get_file(type="path", file_id=str(cache.fileid))
            except ActionFailed:
                cache = None  # 如果检验失败，设置为缓存失效

        if cache is None:
            # 如果缓存中没有找到文件，上传文件
            fileid = (await bot.upload_file(type="data", name=name, data=data, sha256=sha256))["file_id"]
            # 保存新上传的文件ID到数据库
            await cls.save_fileid(sha256, fileid)
        else:
            # 如果缓存中存在，直接使用缓存的文件ID
            fileid = str(cache.fileid)

        return fileid
