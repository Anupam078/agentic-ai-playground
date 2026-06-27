#Foundation of LangGraph Framework - Single node State Graph
from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    name: str
    greeting: str

def greeting_agent(state: AgentState)-> AgentState:
    state['greeting'] = f"Hello, {state['name']}!"
    return state

builder = StateGraph(AgentState)
builder.add_node("greet", greeting_agent)

builder.set_entry_point("greet")
builder.set_finish_point("greet")

graph = builder.compile()

if __name__ == "__main__":
   result = graph.invoke({"name": "Shyni"})
   print(result["greeting"])
for name in ["Alice", "Bob", "VIT Student"]:
   output = graph.invoke({"name": name})
   print(output["greeting"])

