from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time

# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0,
    num_predict=512
)

# --------------------------------------------------
# Prompt Template
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert {domain} engineer. Be concise."),
    ("human", "Explain {topic} with a real-world example.")
])

# --------------------------------------------------
# LCEL Chain
# --------------------------------------------------

chain = prompt | llm | StrOutputParser()

# --------------------------------------------------
# Invoke
# --------------------------------------------------

result = chain.invoke({
    "domain": "cloud",
    "topic": "microservices"
})

print("\n=== INVOKE OUTPUT ===")
print(result)

# --------------------------------------------------
# Stream
# --------------------------------------------------

print("\n=== STREAM OUTPUT ===")

for chunk in chain.stream({
    "domain": "AI",
    "topic": "agents"
}):
    print(chunk, end="", flush=True)

print()

# --------------------------------------------------
# Batch
# --------------------------------------------------

inputs = [
    {
        "domain": "AI",
        "topic": "Machine Learning"
    },
    {
        "domain": "AI",
        "topic": "Deep Learning"
    },
    {
        "domain": "AI",
        "topic": "Reinforcement Learning"
    }
]

t0 = time.time()

results = chain.batch(inputs)

print(f"\nBatch time: {time.time() - t0:.1f}s ({len(results)} results)")

for i, r in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(r[:120])