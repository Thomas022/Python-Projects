# langchain_setup.py

# Import required modules
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

# Single memory store for all sessions
store = {}

def get_session_history(session_id):
    """Retrieve or create a chat history for a given session."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def trim_to_window(history, k=3):
    """Keep only the last k exchanges (k*2 messages)"""
    if len(history.messages) > k * 2:
        recent_messages = history.messages[-(k * 2):]
        history.clear()
        for msg in recent_messages:
            history.add_message(msg)

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5
)

# Create prompt template 
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful cooking assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Create conversation chain 
conversation_chain = RunnableWithMessageHistory(
    prompt | llm | StrOutputParser(),
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

def clear_session(session_id):
    """Clear the history for a specific session."""
    if session_id in store:
        store[session_id].clear()
        print(f"✓ Session '{session_id}' cleared")
    else:
        print(f"⚠ Session '{session_id}' not found")

def clear_all_sessions():
    """Clear all session histories."""
    store.clear()
    print("✓ All sessions cleared")

# Setup function to return all components
def setup():
    """
    Return all components for LangChain conversation with memory.
    """
    return {
        "llm": llm,
        "prompt": prompt,
        "conversation_chain": conversation_chain,
        "store": store,
        "get_session_history": get_session_history,
        "trim_to_window": trim_to_window,
        "clear_session": clear_session,
        "clear_all_sessions": clear_all_sessions,
    }

# To prevent automatic execution in Jupyter Notebooks
if __name__ == '__main__':
    print("LangChain setup module loaded successfully")