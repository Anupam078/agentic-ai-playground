from datetime import datetime
from typing import List

from pydantic import BaseModel
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool

# ==========================================
# 1. INITIALIZATION & MEMORY
# ==========================================
llm = ChatOllama(model="qwen2.5:3b", temperature=0)

# Load the Vector Database from Task 2
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_db = FAISS.load_local(
    "hr_vector_db", 
    embeddings, 
    allow_dangerous_deserialization=True # Required by FAISS to load local files
)
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

# ==========================================
# 2. STRUCTURED OUTPUT (RESUME PARSING)
# ==========================================
class Candidate(BaseModel):
    name: str
    experience: int
    skills: List[str]

structured_llm = llm.with_structured_output(Candidate)

# ==========================================
# 3. TOOLS
# ==========================================
@tool
def experience_calculator(start_year: int) -> str:
    """Calculate candidate experience"""
    return str(datetime.now().year - start_year)

@tool
def eligibility_checker(skills: str) -> str:
    """Check candidate eligibility"""
    required = {"python", "sql", "git"}
    candidate = {skill.strip().lower() for skill in skills.split(",")}
    missing = required - candidate
    if len(missing) == 0:
        return "Eligible"
    return "Not Eligible. Missing: " + ", ".join(missing)

@tool
def company_policy_search(question: str) -> str:
    """Search company documents"""
    docs = retriever.invoke(question) 
    context = "\n".join(doc.page_content for doc in docs)
    prompt = f"Answer only from context.\n\nContext:\n{context}\n\nQuestion:\n{question}"
    return llm.invoke(prompt).content

@tool
def interview_questions(skills: str) -> str:
    """Generate interview questions"""
    prompt = f"Generate 5 interview questions for: {skills}"
    return llm.invoke(prompt).content

tools = [experience_calculator, eligibility_checker, company_policy_search, interview_questions]

# ==========================================
# 4. AGENT SETUP
# ==========================================
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an HR Recruitment Assistant. Use tools whenever required."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}") # Lowercase 'placeholder'
])

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# ==========================================
# 5. MAIN CHAT LOOP
# ==========================================
print("=" * 60)
print("HR RECRUITMENT ASSISTANT (Type 'exit' to quit)")
print("=" * 60)

while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() == "exit":
        print("Shutting down assistant...")
        break
        
    # Intercept Resume Parsing
    if user_input.lower().startswith("resume:"):
        resume_text = user_input[7:].strip() 
        
        print("Parsing resume...")
        extraction_prompt = f"Extract Name, Experience, Skills\n\nResume:\n{resume_text}"
        
        candidate_details = structured_llm.invoke(extraction_prompt)
        print("\n--- Structured Candidate Data ---")
        print(candidate_details)
        continue
        
    # Standard Agent Queries
    print("Thinking...")
    response = agent_executor.invoke({"input": user_input})
    print(f"\nAssistant: {response['output']}")