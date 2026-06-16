import ollama

REACT_SYSTEM = """You are a ReAct (Reasoning + Acting) AI Agent.

For EVERY question, you MUST respond using this exact format - never skip a step:

THOUGHT: [Analyze what the question is really asking. What do you know about this topic?]

PLAN: [Describe your step-by-step approach to answer this well.]

ACTION: [Execute your plan. Work through the answer in detail. Show your thinking.]

FINAL ANSWER: [Write a clear, concise summary answer in 2-3 sentences maximum.]

Rules:
- Never answer directly without going through all 4 steps
- THOUGHT must be at least 2 sentences
- ACTION must show actual work/reasoning
- FINAL ANSWER must be short and clear
"""

chat_history = [
    {
        'role': 'system',
        'content': REACT_SYSTEM
    }
]

print("=" * 50)
print(" ReAct Reasoning Agent (Llama 3.1)")
print("=" * 50)
print("I reason through questions step-by-step to provide clear, well-thought-out answers.")
print("Type 'exit' to end the conversation.")

question_count = 0

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == 'exit':
        print(f"Goodbye! You asked {question_count} questions.")
        break

    if not user_input:
        print("Please enter a valid question.")
        continue

    question_count += 1

    chat_history.append({'role': 'user', 'content': user_input})

    response = ollama.chat(
        model='llama3.1',
        messages=chat_history
    )

    ai_message = response['message']['content']
    chat_history.append({'role': 'assistant', 'content': ai_message})

    print("AI Agent Response:")
    print(ai_message)
    print("-" * 50)