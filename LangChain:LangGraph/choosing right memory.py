from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

import os
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

from langchain_setup import (
conversation_chain,
get_session_history,
store,
trim_to_window
)

summarizer = ChatOpenAI(model="gpt-3.5-turbo", temperature = 0)

test_messages = [
    "I need a dessert recipe.",
    "I`m allergic to peanuts",
    "Something chocolate would be great",
    "How long does it take?",
    "Can I make it the day before?",
    "What ingredients do I need?"
]

#Configuration for buffer-based session
config_buffer = {"configurable": {"session_id": "recipe_buffer"}}

print("BUFFER MEMORY")
for i, msg in enumerate(test_messages, 1):
    reponse = conversation_chain.invoke({"input": msg}, config=config_buffer)
    if i == 2: #Show the Allergy mention
        print(f"Turn {i}: \n User: {msg}")
        print(f"Assistant: {reponse}\n")
    else:
        print(f"Turn {i}: check")

#Configuration for Window-based session
confi_window = {"configurable": {"session_id": "recipe_buffer"}}

print("\nWINDOW MEMORY (k=3):")
for i, msg in enumerate(test_messages, 1):
    response = conversation_chain.invoke({"input": msg}, config=confi_window)
    trim_to_window(store["recipe_buffer"], k=3)
    if i == 2:
        print(f"Turn {i}: \n User: {msg}")
        print(f"Assistant: {response}\n")
    else:
        print(f"Turn {i}: check")

#Creating a conversation summary
def create_sumamry(messages):
    conversation_text = "\n\n".join(
        f"{message.type}\n{message.content}"
        for message in messages
    )

    summary_prompt = (
        "Summarize the following conversation"
        "Preserve important facts, preferences and restrictions \n\n"
        f"{conversation_text}"
    )

    summary = summarizer.invoke([
        SystemMessage(content=summary_prompt)
    ]
    )
    return conversation_text

testar = create_sumamry([
    HumanMessage(content="Hoje eu estou feliz")])
print(testar)

