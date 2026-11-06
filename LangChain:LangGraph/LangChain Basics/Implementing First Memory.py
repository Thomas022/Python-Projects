from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

import os
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]


# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5
)

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful personal assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

base_chain = prompt | llm | StrOutputParser()

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

session_config = {"configurable": {"session_id" : "user-101"}}

# Turn 1
response = conversation_chain.invoke(
    {"input": "Hi! My name is Alex and I work as a data scientist."},
    config=session_config
)
print("User: Hi! My name is Alex and I work as a data scientist.")
print(f"Assistant: {response}\n")

# Turn 2
response = conversation_chain.invoke(
    {"input": "I'm working on a project about predicting customer churn."},
    config=session_config
)
print("User: I'm working on a project about predicting customer churn.")
print(f"Assistant: {response}\n")

# Turn 3
response = conversation_chain.invoke(
    {"input": "I'm using random forests and gradient boosting."},
    config=session_config
)
print("User: I'm using random forests and gradient boosting.")
print(f"Assistant: {response}\n")

response = conversation_chain.invoke({"input": "Whats my name and what do i do?"}, config=session_config)
print("User : Whats my name and what do i do?")