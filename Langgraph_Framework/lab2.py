#Ai powered customer suppport router using langgraph
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph
from typing import TypedDict

class CustomerSupportState(TypedDict):
    customer_query: str
    predicted_category: str
    final_response: str


llm_model=ChatOllama(
    model = 'llama3.1',
    temperature = 0
)

def predict_category(State: CustomerSupportState) -> CustomerSupportState:
    prompt = f"Classify the following customer query into one of the following categories: Billing, Technical Support, General Inquiry. Query: {State['customer_query']}"
    response = llm_model.invoke(prompt)
    State['predicted_category'] = response
    return State

def billing_agent(State: CustomerSupportState) -> CustomerSupportState:
    prompt = f"Provide a response to the following billing query: {State['customer_query']}"
    response = llm_model.invoke(prompt)
    State['final_response'] = response
    return State

def technical_support_agent(State: CustomerSupportState) -> CustomerSupportState:
    prompt = f"Provide a response to the following technical support query: {State['customer_query']}"
    response = llm_model.invoke(prompt)
    State['final_response'] = response
    return State

def general_inquiry_agent(State: CustomerSupportState) -> CustomerSupportState:
    prompt = f"Provide a response to the following general inquiry: {State['customer_query']}"
    response = llm_model.invoke(prompt)
    State['final_response'] = response
    return State

def route_query(State: CustomerSupportState) -> str:
    category = State['predicted_category'].lower()
    if category == "billing":
        return "billing_agent"
    elif category == "technical support":
        return "technical_support_agent"
    elif category == "general inquiry":
        return "general_inquiry_agent"
    else:
        return "general_inquiry_agent"  # Default route
    
builder = StateGraph(CustomerSupportState)
builder.add_node("predict_category", predict_category)
builder.add_node("billing_agent", billing_agent)
builder.add_node("technical_support_agent", technical_support_agent)
builder.add_node("general_inquiry_agent", general_inquiry_agent)
builder.add_node("route_query", route_query)
builder.add_conditional_edge("predict_category",
                             route_query,
                             {
                                "billing_agent": "billing_agent",
                                "technical_support_agent": "technical_support_agent",
                                "general_inquiry_agent": "general_inquiry_agent"
                             }
)
builder.set_entry_point("predict_category")
builder.set_finish_point("billing_agent")
builder.set_finish_point("technical_support_agent")
builder.set_finish_point("general_inquiry_agent")

graph = builder.compile()

test_queries = [
 "My payment failed yesterday and I was charged twice",
 "The app crashes every time I try to login from my iPhone",
 "What are your office hours?",
 "I need a refund for my last invoice",
 "How do I reset my password? The reset email never arrives",
 "Do you offer student discounts?",
]
if __name__ == "__main__":
  console.print("\n[bold magenta]=== AI Customer Support Router ===[/bold magenta]\n")
  for query in test_queries:
    console.print(f"\n[bold white]Customer:[/bold white] {query}")
  result = graph.invoke({
    "query": query,
    "category": "",
    "answer": ""
    })
  console.print(Panel(
   result["answer"],
   title=f"[bold green]Response ({result['category'].upper()})[/bold green]",
   border_style="green"
   ))
  console.print("\n[bold yellow]All queries routed successfully.[/bold yellow]")

