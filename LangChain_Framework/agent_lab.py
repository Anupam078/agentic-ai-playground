from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain_ollama import ChatOllama

# Import tools from customtools.py
from customtools import calculator, student_lookup

# ===================================================
# LLM
# ===================================================

llm = ChatOllama(
    model="llama3.1",
    temperature=0
)

# ===================================================
# TOOLS
# ===================================================

tools = [
    calculator,
    student_lookup
]

# ===================================================
# MEMORY
# ===================================================

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    k=5
)

# ===================================================
# CONVERSATIONAL AGENT
# ===================================================

conv_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    max_iterations=5
)

# ===================================================
# TURN 1
# ===================================================

r1 = conv_agent.invoke({
    "input": "Look up Priya"
})

print("\n=== TURN 1 ===")
print(r1["output"])

# ===================================================
# TURN 2
# ===================================================

r2 = conv_agent.invoke({
    "input": "What is 10% of her CGPA?"
})

print("\n=== TURN 2 ===")
print(r2["output"])

# ===================================================
# MEMORY CONTENT
# ===================================================

print("\n=== MEMORY ===")

msgs = memory.chat_memory.messages

for m in msgs:
    print(f"[{m.type.upper()}] {m.content}")