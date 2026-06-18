from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert {domain} engineer. Be concise."),
    ("human", "Explain {topic} with a real-world example.")
])

# Preview the formatted prompt
formatted = prompt.format_messages(
    domain="AI",
    topic="React agent pattern"
)

print(formatted)