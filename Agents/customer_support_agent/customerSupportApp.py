import os
import sqlite3
from typing import TypedDict, List, Literal, Optional, Any, Dict
from typing_extensions import Annotated
from pydantic import BaseModel, Field

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

# ==========================================
# 0. SETUP AND CONFIGURATION
# ==========================================

# Initialize SQLite memory checkpointer
conn = sqlite3.connect("memory.db", check_same_thread=False)
memory_checkpointer = SqliteSaver(conn)

# Initialize the LLM
llm = ChatOllama(model="llama3.1", temperature=0)

# ==========================================
# 1. STATE DEFINITION (Task 2)
# ==========================================
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    query_type: Optional[str]
    retrieved_context: Optional[str]
    requires_approval: bool
    approved: Optional[bool]
    final_response: Optional[str]

# ==========================================
# 2. INTENT CLASSIFIER NODE (Task 3)
# ==========================================
class IntentClassification(BaseModel):
    category: Literal["Sales", "Technical", "Billing", "Account", "MemoryRecall"] = Field(
        description="The department suited for the query. Use 'MemoryRecall' if the user asks about previous history."
    )

def intent_classifier_node(state: AgentState) -> dict:
    last_user_message = state["messages"][-1].content
    
    # Enhanced prompt to help Llama 3.1 accurately classify the intents
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert triage agent. Classify the user query into exactly one of these categories:
- Sales: For questions about pricing, plans, or buying software.
- Technical: For bugs, app crashes, or errors.
- Billing: For refunds, invoices, or payments.
- Account: For password resets, login issues, or profile updates.
- MemoryRecall: ONLY for questions asking about past history or previous issues."""),
        ("human", "{query}")
    ])
    
    classifier_chain = prompt | llm.with_structured_output(IntentClassification)
    result = classifier_chain.invoke({"query": last_user_message})
    
    print(f"--> [Intent Classifier] Query routed to: {result.category}")
    
    # Force string cast and RESET the human-in-the-loop flags for every new query
    # so approvals don't accidentally leak from previous conversational turns!
    return {
        "query_type": str(result.category),
        "requires_approval": False,
        "approved": None
    }

# ==========================================
# 3. MOCK RAG PIPELINE (Task 6)
# ==========================================
KNOWLEDGE_BASE = {
    "Sales": "Pricing Guide: Basic plan is $10/mo, Pro is $25/mo. Annual subscriptions get 20% off.",
    "Technical": "Technical Manual: If app crashes on upload, clear cache and ensure file is under 50MB.",
    "Billing": "Policy Document: Refunds are available within 30 days of purchase for annual plans only.",
    "Account": "FAQ: To reset password, click 'Forgot Password' on login screen to receive an email link."
}

def retrieve_context(category: str) -> str:
    """Simulates a Vector Database retrieval."""
    return KNOWLEDGE_BASE.get(category, "No specific documents found.")

# ==========================================
# 4. SPECIALIZED AGENTS (Task 5)
# ==========================================
def department_agent_node(state: AgentState) -> dict:
    # Use .get() with a fallback to avoid KeyErrors on fresh runs
    department = state.get("query_type", "Sales") 
    last_message = state["messages"][-1].content
    
    # RAG Retrieval
    context = retrieve_context(department)
    print(f"--> [{department} Agent] Retrieved Context: {context}")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a {dept} support agent. Use the context to answer: {context}"),
        ("human", "{query}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"dept": department, "context": context, "query": last_message})
    
    return {"messages": [response], "retrieved_context": context}

# ==========================================
# 5. MEMORY RECALL NODE (Task 7)
# ==========================================
def memory_recall_node(state: AgentState) -> dict:
    """Answers queries about past interactions by reading the SQLite state history."""
    print("--> [Memory Node] Analyzing past conversational context...")
    
    # Filter out only user messages from the past, excluding the current one
    past_user_messages = [msg.content for msg in state["messages"][:-1] if isinstance(msg, HumanMessage)]
    
    if not past_user_messages:
        response = AIMessage(content="You don't have any previous support requests in my memory.")
    else:
        history = "\n".join(past_user_messages)
        prompt = f"Summarize the user's past issues based on this history:\n{history}"
        response = llm.invoke(prompt)
        
    return {"messages": [response]}

# ==========================================
# 6. HUMAN-IN-THE-LOOP & SUPERVISOR (Tasks 8 & 9)
# ==========================================
def risk_assessment_node(state: AgentState) -> dict:
    user_query = state["messages"][-2].content.lower() # User query is right before Agent response
    high_risk_keywords = ["refund", "cancel", "closure", "compensation"]
    
    requires_approval = any(word in user_query for word in high_risk_keywords)
    if requires_approval:
        print("--> [Risk Assessor] HIGH RISK DETECTED. Flagging for Human Approval.")
        
    return {"requires_approval": requires_approval}

def human_approval_node(state: AgentState) -> dict:
    # Execution pauses BEFORE this node. We just pass through when resumed.
    return {} 

def supervisor_node(state: AgentState) -> dict:
    print("--> [Supervisor] Reviewing final response...")
    requires_approval = state.get("requires_approval", False)
    approved = state.get("approved")
    
    if requires_approval and not approved:
        final_text = "Your request requires manual manager review. We will email you shortly."
    elif requires_approval and approved:
        final_text = f"[SUPERVISOR APPROVED]: {state['messages'][-1].content}"
    else:
        final_text = state["messages"][-1].content
        
    return {"final_response": final_text}

# ==========================================
# 7. GRAPH ROUTING & COMPILATION (Tasks 1 & 4)
# ==========================================
def route_after_classification(state: AgentState) -> str:
    # Use .get() to safely check the state
    if state.get("query_type") == "MemoryRecall":
        return "memory_recall"
    return "department_agent"

def route_after_risk(state: AgentState) -> str:
    if state.get("requires_approval"):
        return "human_approval"
    return "supervisor"

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("classifier", intent_classifier_node)
workflow.add_node("department_agent", department_agent_node)
workflow.add_node("memory_recall", memory_recall_node)
workflow.add_node("risk_assessment", risk_assessment_node)
workflow.add_node("human_approval", human_approval_node)
workflow.add_node("supervisor", supervisor_node)

# Add Edges
workflow.add_edge(START, "classifier")
workflow.add_conditional_edges("classifier", route_after_classification)
workflow.add_edge("department_agent", "risk_assessment")
workflow.add_conditional_edges("risk_assessment", route_after_risk)
workflow.add_edge("human_approval", "supervisor")
workflow.add_edge("memory_recall", "supervisor") # Memory skips risk assessment
workflow.add_edge("supervisor", END)

# Compile with Memory and HITL breakpoint
app = workflow.compile(
    checkpointer=memory_checkpointer, 
    interrupt_before=["human_approval"]
)

# ==========================================
# 8. DEMONSTRATION RUNNER (Task 10)
# ==========================================
if __name__ == "__main__":
    # Changed thread_id to bypass corrupted memory from previous runs
    config = {"configurable": {"thread_id": "customer_david_002"}}
    
    queries = [
        "What are the pricing plans available for your software?",
        "I forgot my account password.",
        "My application crashes whenever I upload a file.",
        "I need a refund for my annual subscription.",
        "What was my previous support issue?"
    ]

    print("\n" + "="*50)
    print("STARTING CUSTOMER SUPPORT AUTOMATION DEMONSTRATION")
    print("="*50)

    for i, query in enumerate(queries, 1):
        print(f"\n\n--- [Query {i}] ---")
        print(f"Customer: {query}\n")
        
        # 1. Stream the graph execution
        for event in app.stream({"messages": [HumanMessage(content=query)]}, config):
            pass # The print statements inside nodes will show the progress
        
        # 2. Check if the graph paused for Human-in-the-Loop
        snapshot = app.get_state(config)
        if snapshot.next and snapshot.next[0] == "human_approval":
            print("\n!!! EXECUTION PAUSED BY LANGGRAPH !!!")
            print("--> Waiting for Human Supervisor input...")
            
            # Simulate a human clicking "Approve" in a dashboard
            print("--> Human clicked [APPROVE]. Resuming graph execution...\n")
            
            # Update state with human decision and resume
            app.update_state(config, {"approved": True}, as_node="human_approval")
            for event in app.stream(None, config):
                pass
                
        # 3. Print Final Output
        final_state = app.get_state(config).values
        print(f"\nFINAL SYSTEM RESPONSE:\n{final_state.get('final_response')}")
        
    print("\n\nDemonstration complete. Memory saved to memory.db.")