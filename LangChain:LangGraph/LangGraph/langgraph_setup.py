from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
import operator

llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

# State schema (from Exercise 3)
class PublishingState(TypedDict):
    topic: str
    content_type: str
    draft: str
    final_content: str
    edit_log: Annotated[list, operator.add]

# Shared draft node (from Exercise 3)
def draft_node(state: PublishingState):
    result = llm.invoke(f"Write a short {state['content_type']} post (2-3 paragraphs) on: {state['topic']}")
    return {"draft": result.content, "edit_log": [f"Draft created"]}