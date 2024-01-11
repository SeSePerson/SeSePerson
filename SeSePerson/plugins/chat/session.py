import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional

import aiohttp
from nonebot import logger

from SeSePerson.plugins.chat import Contact
from SeSePerson.plugins.chat.model import Message, MessageRole


@dataclass
class SessionData:
    history: List[Dict[str, str]] = field(default_factory=list)
    extra_template: List[Dict[str, str]] = field(default_factory=list)
    length_limit: int = 1000


class Session:
    def __init__(self, openai_key: str, template: str, max_history: int,time_limit:int):
        self.openai_key: str = openai_key
        self.template: str = template
        self.max_history: int = max_history
        self.time_limit: int = time_limit

    def talk(self, contact_id: str, text: str, name: Optional[str]):
        # logger.debug(self.template)
        # now = datetime.now()
        # template = self.template.format(date=now.strftime("%Y-%m-%d %H:%M"))
        if name is not None:
            text = f"{name}: {text}"
        # logger.debug(template)
        out = self

        class AnswerStream:
            def __init__(self):
                self.ans = ""
                self.buffer = ""

            async def __aenter__(self):
                now = datetime.now(timezone.utc)
                # 查询记录
                self.contact = (await Contact.get_or_create(id=contact_id))[0]
                await Message.create(
                    contact=self.contact,
                    role=MessageRole.USER,
                    content=text
                )
                history = await Message.filter(
                    contact=self.contact,
                    time__gte=max(now - timedelta(hours=out.time_limit), self.contact.cutoff)
                ).order_by('-time').limit(out.max_history + 1)
                history = [{"role": msg.role.value, "content": msg.content} for msg in reversed(history)]
                history.insert(0, {"role": "system", "content": out.template})

                logger.debug(json.dumps(history, ensure_ascii=False, indent=2))

                self.session = aiohttp.ClientSession()
                self.response = await self.session.post(
                    "https://api.openai-proxy.com/v1/chat/completions",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {out.openai_key}", },
                    json={
                        "model": "gpt-4-1106-preview",
                        "messages": history,
                        "temperature": 1,
                        "frequency_penalty": 0.3,
                        "max_tokens": 1024,
                        "stream": True,  # 启用流式API
                    },
                    timeout=60,
                ).__aenter__()
                # await self.response.content.readline()
                # logger.debug(self.response)
                return self

            async def __aexit__(self, exc_type, exc, tb):
                if self.ans:
                    await Message.create(
                        contact=self.contact,
                        role=MessageRole.AI,
                        content=self.ans
                    )
                await self.response.__aexit__(exc_type, exc, tb)
                await self.session.close()

            def __aiter__(self):
                return self

            async def __anext__(self):
                while "\n" not in self.buffer:
                    chunk = await self.response.content.readline()
                    if chunk:
                        chunk = chunk.decode('utf-8')
                        if chunk == '\n' or chunk == "data: [DONE]\n":
                            # logger.debug("跳过了啊")
                            continue
                        elif chunk.startswith('data: '):
                            # 去掉 'data: ' 前缀
                            chunk = chunk[len('data: '):]
                        # logger.debug(chunk)
                        try:
                            chunk_data = json.loads(chunk)
                        except json.JSONDecodeError:
                            logger.debug(chunk)
                            continue
                        content = chunk_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                        self.buffer += content
                    else:
                        # 如果没有新的chunk读取，并且buffer中没有换行符，
                        # 说明所有的数据都已经接收完毕，可以返回剩余的buffer内容
                        if self.buffer:
                            break
                            # self.buffer = out.ans_dispose(self.buffer)
                            # self.ans += self.buffer
                            # buffer_to_return = self.buffer
                            # self.buffer = ''  # 清空buffer以指示所有内容都已返回
                            # return buffer_to_return
                        else:
                            # 如果buffer也为空，说明所有的内容都已经返回完毕，可以终止迭代
                            raise StopAsyncIteration

                # 如果buffer中包含换行符，那么返回换行符之前的内容，并更新buffer
                self.buffer = out.ans_dispose(self.buffer)
                self.ans += self.buffer
                line, _, self.buffer = self.buffer.partition("\n")
                return line

        return AnswerStream()

    @staticmethod
    async def cut_history(contact_id: str, time: datetime = datetime.now()):
        contact = await Contact.get_or_none(id=contact_id)
        if contact is None:
            return
        contact.cutoff = time
        await contact.save()

    @staticmethod
    def ans_dispose(msg: str):
        msg = msg.strip()
        msg = re.sub("^(?:SeSePerson|涩涩人).?[:：]", "", msg)
        return msg.strip()
