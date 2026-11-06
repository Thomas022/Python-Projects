# langchain_setup.py

# Import required modules
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

# File path to the sample document
file_path = "sample_document.txt"

# Load the document
loader = TextLoader(file_path)
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)

# Embed and store in vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_documents(chunks, embeddings)

# Create a retriever from the vector store
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Create a web search tool
search_engine = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """Search the web for current information.

    Use this tool when you need to find recent news,
    look up facts, or get current information.

    Args:
        query: The search terms to look up
    """
    return search_engine.run(query)

# Setup function to return all components
def setup():
    """
    Return all components for the Agent + RAG hybrid pipeline.
    """
    return {
        "retriever": retriever,
        "web_search": web_search,
    }

# To prevent automatic execution in Jupyter Notebooks
if __name__ == '__main__':
    print("LangChain setup module loaded successfully")
