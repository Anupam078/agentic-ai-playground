from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


root = Path(".")
text_files = sorted(root.glob("*.txt"))
if not text_files:
    raise FileNotFoundError(
        "No .txt documents were found in the workspace root to index."
    )

# Load documents from the existing policy / JD files in the workspace.
documents = []
for file_path in text_files:
    loader = TextLoader(str(file_path), encoding="utf-8")
    documents.extend(loader.load())

print(f"Loaded {len(documents)} documents")

# Split documents into searchable chunks.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# Create embeddings and persist the FAISS vector store.
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_db = FAISS.from_documents(chunks, embeddings)

output_dir = Path("hr_vector_db")
output_dir.mkdir(exist_ok=True)

vector_db.save_local(str(output_dir))

print(f"Vector Database Created at {output_dir.resolve()}")