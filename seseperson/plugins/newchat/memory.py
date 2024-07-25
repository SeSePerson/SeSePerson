from typing import List

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.memory import BaseMemory

from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from langchain_core.messages import BaseMessage
# class ChatMessageHistory(BaseChatMessageHistory):

from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from pydantic import Field


class Memory:
    summary: str = Field(default_factory=str)
    messages: List[BaseMessage] = Field(default_factory=list)


    