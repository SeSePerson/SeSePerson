import random

from nonebot import on_command, logger
from nonebot.internal.adapter import MessageTemplate
from nonebot.internal.params import ArgStr, ArgPlainText
from nonebot.typing import T_State

from SeSePerson.utils.config import get_config
from .config import Config

ANS = 'ans'
config = get_config("katakana", Config)
katakana2rom = list(config.katakana2rom.items())

katakana = on_command("katakana", aliases={"kata", "jap"}, block=True, priority=10)


@katakana.handle()
async def _(state: T_State):
    q, a = random.choice(katakana2rom)
    state["question"] = q
    state["right_ans"] = a
    state["try"] = 0
    await katakana.send(q)


@katakana.got("ans")
async def _(state: T_State, ans: str = ArgPlainText()):
    # last_ans = state["last_ans"]
    if ans.strip() == state["right_ans"]:
        await katakana.finish(MessageTemplate('答对啦awa~ "{question}"的罗马音就是"{right_ans}"呢~'))
    elif ans in config.hint_key:
        if state.get("hinted", False):
            await katakana.reject(MessageTemplate('駄目です~ 已经提示过了啊~'))
        else:
            right_ans = state["right_ans"]
            i = random.randint(0, len(right_ans) - 1)
            hint = "?" * i + right_ans[i] + "?" * (len(right_ans) - i - 1)
            await katakana.reject(MessageTemplate(f'ヒントです~ "{state["question"]}"的罗马音提示是"{hint}"~'))
    elif state["try"] <= config.max_try and (ans not in config.break_key):
        state["try"] += 1
        state["last_ans"] = ans
        await katakana.reject(MessageTemplate('不对哦awa~ "{question}"的罗马音不是"{last_ans}"哦~'))
    else:
        await katakana.finish(MessageTemplate('残念です~ "{question}"的正确罗马音是"{right_ans}"欸~'))
