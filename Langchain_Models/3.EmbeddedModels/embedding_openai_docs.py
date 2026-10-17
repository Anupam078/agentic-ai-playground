from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=32)

documents = [
    "Delhi is the capital of India",
    "Kolkata is the capital of West Bengal",
    "Paris is the capital of France"
]
#performing embedding on a list of documents. The embed_documents method is used to generate embeddings for multiple pieces of text, which can then be used for various tasks such as semantic search, clustering, or similarity comparisons.
result = embedding.embed_documents(documents)

print(str(result))