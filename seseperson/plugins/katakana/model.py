from enum import Enum

from tortoise import Model
from tortoise.fields import CharField, IntField, ForeignKeyField, TextField, DatetimeField, CharEnumField

from seseperson.plugins.database import add_plugin
from . import Config
from seseperson.utils.config import get_config

APP_NAME = "katakana"
add_plugin(APP_NAME, [__name__])

config = get_config("katakana", Config)
base = config.base_point
bonus = config.bonus
hint_cost = config.hint_cost
allow_neg = config.allow_neg
max_rank = config.max_rank


class User(Model):
    id = CharField(max_length=20, pk=True)
    score = IntField(default=0, index=True)
    combo = IntField(default=0)

    async def right(self):
        old_score = self.score  # 保存原始分数
        self.score += base + self.combo * bonus
        if self.score < 0 and not allow_neg:
            self.score = 0
        self.combo += 1
        await self.save()
        return self.score - old_score  # 返回分数变化值

    async def wrong(self):
        old_score = self.score  # 保存原始分数
        self.score -= base
        if self.score < 0 and not allow_neg:
            self.score = 0
        self.combo = 0
        await self.save()
        return self.score - old_score  # 返回分数变化值

    async def hint(self):
        old_score = self.score  # 保存原始分数
        self.score -= hint_cost
        if self.score < 0 and not allow_neg:
            self.score = 0
        await self.save()
        return self.score - old_score  # 返回分数变化值

    @classmethod
    async def top_rank(cls, k: int = max_rank):
        return await cls.all().order_by('-score').limit(k)

    # @classmethod
    async def get_rank(self):
        # 计算排名
        higher_score_count = await self.filter(score__gt=self.score).count()
        return higher_score_count + 1

