# langchain_setup.py

# Import required modules
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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

# Setup function to return all components
def setup():
    """
    Return all components for the document loading and splitting pipeline.
    """
    return {
        "file_path": file_path,
        "documents": documents,
        "text_splitter": text_splitter,
        "chunks": chunks,
    }

# To prevent automatic execution in Jupyter Notebooks
if __name__ == '__main__':
    print("LangChain setup module loaded successfully")
    print(f"Loaded {len(documents)} document(s), split into {len(chunks)} chunks.")
