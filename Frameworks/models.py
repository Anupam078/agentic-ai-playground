from langchain_ollama import ChatOllama

# temperature=0 → deterministic, best for agents
# temperature=0.7 → creative, for content generation

llm = ChatOllama(
    model="llama3.1",  # Ollama model name
    temperature=0,
    num_predict=512  # max tokens per response
)

# Basic invocation
response = llm.invoke("What is an AI Agent?")
print(response.content)