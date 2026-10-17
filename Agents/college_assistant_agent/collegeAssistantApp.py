import os
from langchain_groq import ChatGroq
from typing import List
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

# ==========================================
# 0. Mock Database for Student Information
# ==========================================
# This dictionary simulates a backend database for the Bonus Challenge
STUDENT_DATABASE = {
    "24BCE10746": {
        "name": "Anupam Ojha",
        "department": "Computer Science Engineering",
        "year": "2nd Year",
        "hostel_room": "302-B"
    },
    "24BCE10636": {
        "name": "Rashi Bhatt",
        "department": "Computer Science Engineering",
        "year": "2nd Year",
        "hostel_room": "104-A"
    }
}

# ==========================================
# 1. Defining Tools via @tool Decorator
# ==========================================

@tool
def attendance_calculator(total_classes: int, attended_classes: int) -> str:
    """
    Calculates the student's attendance percentage and determines exam eligibility.
    Use this tool when a user asks about attendance, class percentage, or exam eligibility.
    """
    if total_classes <= 0:
        return "Error: Total classes must be greater than zero."
    
    percentage = (attended_classes / total_classes) * 100
    eligible = percentage >= 75
    status = "Eligible for Exam" if eligible else "Not Eligible for Exam"
    
    return f"Attendance: {percentage:.2f}%. Status: {status}."


@tool
def result_calculator(marks: List[float]) -> str:
    """
    Calculates average marks, assigns a letter grade, and checks pass/fail status for exactly 5 subjects.
    Use this tool when a user provides a list of marks or scores and asks for a grade or result summary.
    """
    if len(marks) != 5:
        return f"Error: Please provide marks for exactly 5 subjects. Received: {len(marks)}"
    
    average_marks = sum(marks) / 5
    
    # Grade assignment logic
    if average_marks >= 90:
        grade = "A"
    elif 75 <= average_marks <= 89:
        grade = "B"
    elif 60 <= average_marks <= 74:
        grade = "C"
    else:
        grade = "D"
        
    pass_fail = "Pass" if average_marks >= 50 else "Fail"
    
    return f"Average Marks: {average_marks:.2f}, Grade: {grade}, Status: {pass_fail}"


@tool
def fee_balance_calculator(total_course_fee: float, amount_paid: float) -> str:
    """
    Calculates the pending course fee balance.
    Use this tool when a user asks about pending fees, due balances, or outstanding tuition payments.
    """
    pending_fee = total_course_fee - amount_paid
    return f"Pending Fee Amount: ₹{pending_fee:.2f}"


@tool
def library_fine_calculator(delayed_days: int) -> str:
    """
    Calculates the library fine based on the number of delayed days.
    Use this tool when a user mentions a late, delayed, or overdue library book return.
    """
    fine_rate = 5
    total_fine = delayed_days * fine_rate
    return f"Library Fine Amount: ₹{total_fine} (Calculated at ₹{fine_rate}/day for {delayed_days} days)"


@tool
def hostel_fee_calculator(monthly_hostel_fee: float, months_stayed: int) -> str:
    """
    Calculates the total hostel fee accumulated over a period of months.
    Use this tool when a user asks about hostel dues, room rents, or stay expenses.
    """
    total_hostel_fee = monthly_hostel_fee * months_stayed
    return f"Total Hostel Fee: ₹{total_hostel_fee:.2f} for a stay of {months_stayed} months."


@tool
def student_information_tool(student_id: str) -> str:
    """
    Retrieves personal data and registration records of a student using their Student ID string.
    Use this tool whenever a user asks for details about a specific student ID or profile lookups.
    """
    # Standardizing uppercase formatting for ID matching
    clean_id = student_id.strip().upper()
    student_data = STUDENT_DATABASE.get(clean_id)
    
    if student_data:
        return (f"Student Record Found -> Name: {student_data['name']}, "
                f"Dept: {student_data['department']}, Year: {student_data['year']}, "
                f"Hostel Room: {student_data['hostel_room']}")
    else:
        return f"Error: No student profile found matching ID '{student_id}'."


# ==========================================
# 2. Main Agent Assembly and Setup
# ==========================================

def main():
    print("Initializing College Assistant Agent...")
    
    # Bundling all tools into a list for the agent
    tools = [
        attendance_calculator,
        result_calculator,
        fee_balance_calculator,
        library_fine_calculator,
        hostel_fee_calculator,
        student_information_tool
    ]
    
    # Initializing the cloud-based Groq LLM using the massive 70B model
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.0)
    
    # Defining a structured system prompt template to govern agent behavior
    # Defining a structured system prompt template to govern agent behavior
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful and precise College Assistant AI. Your task is to look at the user's inquiry, "
            "identify which tools are necessary, call them with the correct parsed parameters, and summarize "
            "the results cleanly. If multiple tools are required, execute them systematically before answering."
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Constructing the Native Tool Calling Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Creating the runtime executor. verbose=True is set to display the chain of thought log.
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # ==========================================
    # 3. Automated Execution of Test Cases
    # ==========================================
    test_queries = [
        # Query 1

        "I attended 72 classes out of 90. Am I eligible for exams?",

        # Query 2

        "My marks are 95, 90, 88, 91 and 87. What is my grade?",

        # Query 3

        "My course fee is 50000 and I have paid 35000. How much fee is pending?",

        # Query 4

        "I returned a library book 8 days late. What is the fine amount?",

        # Query 5

        "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",
        # Multi-Tool Challenge
        "Please provide a complete consolidated report for this student profile:\n"
        "- I attended 80 classes out of 100.\n"
        "- My marks are 90, 85, 88, 92 and 95.\n"
        "- My course fee is 60000 and I paid 45000.",

        
        # Bonus Challenge Demonstration

        "Can you look up the student profile records for ID: 24BCE10746?"
        
    ]
    
    print("\n--- Starting Verification Execution Loop ---\n")
    
    for idx, query in enumerate(test_queries, 1):
        print("\n" + "="*60)
        print(f"RUNNING TEST CASE {idx}")
        print("="*60)
        print(f"User Query: {query}\n")
        
        # Invoking agent execution
        response = agent_executor.invoke({"input": query})
        
        print("\n" + "-"*40)
        print(f"Final Answer (Test Case {idx}):")
        print(response["output"])
        print("-"*40 + "\n")


if __name__ == "__main__":
    main()