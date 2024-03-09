from typing import Dict, Any, List

from langchain.globals import set_verbose
from langchain.memory import ConversationSummaryBufferMemory, ConversationBufferMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory.prompt import SUMMARY_PROMPT
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.language_models import BaseChatModel, BaseLanguageModel
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, BasePromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

set_verbose(True)

class UserMessage(HumanMessage):
    user_id:str

class Memory(BaseChatMessageHistory):
    llm: BaseLanguageModel
    prompt: BasePromptTemplate = SUMMARY_PROMPT
    recent_messages:List[BaseMessage]
    summary:str = ""
    def add_message(self, message: BaseMessage) -> None:
        self.recent_messages.append(message)

    async def summarize(self):




    def clear(self) -> None:
        pass


    # async def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
    #     token=self.llm.get_num_tokens_from_messages()
    #
    # @property
    # def memory_variables(self) -> List[str]:
    #     pass
    #
    # summary_threshold: int = 2048
    # retain_rounds: int = 3
    #
    # def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
    #     input_str, output_str = self._get_input_output(inputs, outputs)





prompt = "You are a transgender"
template = ChatPromptTemplate.from_messages([
    ('system', prompt),
    ("system", "info: \n{info}"),
    # ("system", "current situation: \n{cur}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
chat = ChatOpenAI(openai_api_base="https://api.openai-proxy.com/v1",
                  openai_api_key="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")

history = ChatMessageHistory()
history.add_user_message("hello")
history.add_ai_message("hi.")

chain = template | chat
print(chain.invoke({
    "info": "trans often play maimai DX",
    "history": history.messages,
    "input": "What do you like to play?"
}))
RunnableWithMessageHistory
ConversationBufferMemory
