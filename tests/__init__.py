from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", '"bird" in this case means 原神'),
    ("user", "{input}")
])
llm = ChatOpenAI(openai_api_key="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",
                 openai_api_base="https://api.openai-proxy.com/v1")

chain = prompt | llm
# llm.openai_proxy = "http://127.0.0.1:10809"
# llm.request_timeout = 1
print(chain.invoke({"input": "is bird genshin?"}))
