from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from tools import fetch_text_from_url
from dotenv import load_dotenv

load_dotenv()
model = init_chat_model(
    "openai:gpt-5.5",
    temperature=0.5,
    max_tokens=25000,
    timeout=300
)
SYSTEM_PROMPT = """
Your role:You are a Literary Research Agent.

## Capabilities

- Use tool named "fetch_text_from_url" to fetch text from a given URL.
## Rules

- Do not guess the line count or position of the text in the URL. Always use the tool to fetch the text.
- Always rely on using retrieved document content
"""

checkpointer = InMemorySaver()
agent = create_agent(
    model=model,
    tools=[fetch_text_from_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer
)

print("Literary Research Agent created successfully!")