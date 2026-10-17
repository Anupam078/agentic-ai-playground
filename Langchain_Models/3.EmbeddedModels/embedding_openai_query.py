from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
#dimensions decide the size of the embedding vector. The larger the dimensions, the more information can be captured in the embedding, but it also requires more computational resources and memory. A dimension of 32 is a good balance for many applications, providing sufficient detail while remaining efficient.
embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=32)
#performing embedding on a String query. The embed_query method is used to generate an embedding for a single piece of text, which can then be used for various tasks such as semantic search, clustering, or similarity comparisons.
result = embedding.embed_query("Delhi is the capital of India")

print(str(result))