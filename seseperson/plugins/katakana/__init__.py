import asyncio
import random
from typing import Optional

from nonebot import on_command, logger
from nonebot.internal.adapter import MessageTemplate
from nonebot.internal.params import ArgPlainText
from nonebot.typing import T_State

from seseperson.utils.config import get_config
from .config import Config
from nonebot.adapters.onebot import v12 as onebot

from .model import User

ANS = 'ans'
config = get_config("katakana", Config)
katakana2rom = list(config.katakana2rom.items())


async def get_user_name(bot, user_id) -> str:
    user_info = await bot.get_user_info(user_id=user_id)
    return user_info.get("user_name", "Unknown")


async def format_rank(bot: onebot.Bot, user_id: str) -> str:
    s = ""
    top = await User.top_rank()
    tasks = [get_user_name(bot, user.id) for user in top]
    names = await asyncio.gather(*tasks)
    for rk, user in enumerate(top, start=1):
        s += f'{rk}.{names[rk - 1]} | {user.score}P\n'

    user = (await User.get_or_create(id=user_id))[0]
    if user not in top:
        rk = await user.get_rank()
        name = await get_user_name(bot, user_id)
        s += f'{rk}.{name} | {user.score}P\n'
    return s[:-1]


katakana = on_command("katakana", aliases={"kata", "jap"}, block=True, priority=10)
rank = on_command("rank", block=True, priority=10)


@katakana.handle()
async def start(state: T_State, event: onebot.MessageEvent):
    state["user"] = (await User.get_or_create(id=event.get_user_id()))[0]
    q, a = random.choice(katakana2rom)
    state["question"] = q
    state["right_ans"] = a
    state["try"] = 0
    await katakana.send(q)


@katakana.got("rep")
async def reply(state: T_State, rep: str = ArgPlainText()):
    rep = rep.lower()
    user: User = state["user"]
    # last_ans = state["last_ans"]
    if rep.strip() == state["right_ans"]:
        await user.right()
        await katakana.send(MessageTemplate('答对啦awa~ "{question}"的罗马音就是"{right_ans}"呢~'))
    elif rep in config.hint_key:
        if state.get("hinted", False):
            await katakana.reject(MessageTemplate('駄目です~ 已经提示过了啊~'))
        else:
            right_ans = state["right_ans"]
            i = random.randint(0, len(right_ans) - 1)
            hint = "?" * i + right_ans[i] + "?" * (len(right_ans) - i - 1)
            await user.hint()
            await katakana.reject(MessageTemplate(f'ヒントです~ "{state["question"]}"的罗马音提示是"{hint}"~'))
    elif state["try"] <= config.max_try and (rep not in config.break_key):
        state["try"] += 1
        state["last_ans"] = rep
        await user.wrong()
        await katakana.reject(MessageTemplate('不对哦awa~ "{question}"的罗马音不是"{last_ans}"哦~'))
    else:
        await user.wrong()
        await katakana.send(MessageTemplate('残念です~ "{question}"的正确罗马音是"{right_ans}"欸~'))


@katakana.handle()
async def finish(state: T_State):
    user: User = state["user"]
    if user.combo <= 1:
        await katakana.finish(f'目前的分数是: {user.score}P, 杂鱼~杂鱼~')
    else:
        await katakana.finish(f'{user.combo}连击! 目前的分数是: {user.score}P~')


@rank.handle()
async def _(bot: onebot.Bot, event: onebot.MessageEvent):
    await rank.finish(await format_rank(bot, event.get_user_id()))
