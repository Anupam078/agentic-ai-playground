from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain_ollama import ChatOllama

# ===================================================
# LLM
# ===================================================

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# ===================================================
# HELPERS
# ===================================================

def clean_input(text: str) -> str:
    return (
        text.replace("expression=", "")
        .replace("name=", "")
        .replace('"', "")
        .replace("'", "")
        .strip()
    )

# ===================================================
# DATABASE
# ===================================================

STUDENT_DB = {
    "priya": {
        "department": "Cyber Security",
        "cgpa": 9.1,
        "risk": "Low"
    },
    "arjun": {
        "department": "AI & ML",
        "cgpa": 6.8,
        "risk": "Medium"
    },
    "deepika": {
        "department": "Data Science",
        "cgpa": 8.5,
        "risk": "Low"
    }
}

# ===================================================
# CALCULATOR TOOL
# ===================================================

@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.

    Example:
    2 + 2 * 3
    """

    expression = clean_input(expression)

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception as e:
        return f"Error: {e}"

# ===================================================
# STUDENT LOOKUP TOOL
# ===================================================

@tool
def student_lookup(name: str) -> str:
    """
    Lookup a student by name.
    Returns department, CGPA and risk level.
    """

    name = clean_input(name).lower()

    student = STUDENT_DB.get(name)

    if not student:
        return f"Student '{name}' not found."

    return (
        f"Department: {student['department']} | "
        f"CGPA: {student['cgpa']} | "
        f"Risk: {student['risk']}"
    )

# ===================================================
# TEST TOOLS
# ===================================================

print("\n=== CALCULATOR ===")

print(
    calculator.invoke({
        "expression": "(88+92+76+85+90)/5"
    })
)

print(
    calculator.invoke({
        "expression": "1/0"
    })
)

print("\n=== STUDENT LOOKUP ===")

print(
    student_lookup.invoke({
        "name": "Priya"
    })
)

print(
    student_lookup.invoke({
        "name": "Ravi"
    })
)

# ===================================================
# AGENT
# ===================================================

tools = [
    calculator,
    student_lookup
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=5
)

# ===================================================
# RUN
# ===================================================

response = agent.invoke({
    "input": "What is Priya's CGPA and what is 15% of it?"
})

print("\n=== FINAL ANSWER ===")
print(response["output"])