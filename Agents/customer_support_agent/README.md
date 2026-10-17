AI-Powered Customer Support Automation System

1. Background

This project is an automated customer support system built for ABC Technologies using LangGraph. It automatically ingests customer queries, classifies their intent, routes them to specialized AI agents, fetches context using RAG, and includes a persistent memory checkpointer (SQLite) to remember past interactions. Furthermore, it incorporates an enterprise-grade Human-in-the-Loop (HITL) approval process for high-risk operations like refunds.

2. Setup Instructions

Prerequisites

Ensure you have Python 3.9+ installed.

Installation

Run the following command to install the necessary dependencies:

pip install langgraph langchain-openai langchain pydantic


Configuration

Open main.py.

Locate line 18: os.environ["OPENAI_API_KEY"] = "sk-proj-YOUR_API_KEY_HERE"

Replace the placeholder with your actual OpenAI API Key.

3. How to Run

Execute the python script from your terminal:

python main.py


The application will automatically run through the 5 required test queries, demonstrating routing, RAG retrieval, Human-in-the-Loop interruption, and memory recall.

4. Architecture / Workflow Overview

START: Ingests HumanMessage.

Intent Classifier: Pydantic structured output model assigns a routing category (Sales, Technical, Billing, Account, or MemoryRecall).

RAG Agents: For standard queries, context is retrieved from the Mock Knowledge Base, and a specialized LLM generates a response.

Risk Assessment: Scans queries for words like "refund". If found, sets requires_approval = True.

Human Approval: Using LangGraph's interrupt_before, the execution halts and waits for manual state update (approved: True).

Memory Recall: Directly answers questions about previous conversations by accessing SQLite graph history.

Supervisor: Formats the final response, adding Supervisor tags if a manual override occurred.

5. Artifacts included in this package

main.py: Full source code.

README.md: This document.

memory.db: SQLite Checkpointer database (auto-generated upon running).