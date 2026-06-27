from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Initialize the LLM (Project Spec: qwen2.5:3b)
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0 # Great choice keeping this at 0 for factual HR answers
)

# 2. Create a dynamic prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an HR Recruitment Assistant."),
    ("human", "{input}") # Using a placeholder for dynamic queries
])

# 3. Initialize the parser
parser = StrOutputParser()

# 4. Build the LCEL Chain
chain = prompt | llm | parser

# 5. Invoke the chain with a dynamic input
print("Thinking...\n")
result = chain.invoke({
    "input": "What does a software engineer do?"
})

print("=== INVOKE OUTPUT ===")
print(result)
