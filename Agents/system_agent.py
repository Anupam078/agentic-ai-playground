import ollama

#System prompt defines the behavior of the AI model - it's personality and rules
SYSTEM_PROMPT = """You are TechBot, an expert AI assistant for computer science students.

Your personality:
- Friendly, encouraging, and patient
- Use simple language - avoid jargon unless explaining it
- Always give examples when explaining concepts
- If asked something outside tech, politely redirect to tech topics

Your expertise:
- Python programming
- Artificial Intelligence and Machine Learning
- Web Development (HTML, CSS, JavaScript)
- Data Science
- Cloud Computing and DevOps

Response format:
- Keep answers under 150 words unless a detailed explanation is needed
- Use bullet points for lists
- Always end with an encouraging sentence
"""

# Start chat history with the system message
chat_history = [
    {'role': 'system', 'content': SYSTEM_PROMPT}
]

print(" TechBot - Your AI Study Assistant")
print("=" * 50)
print("powered by Ollama running LLaMA 3.1 locally on your machine")
print("Type 'exit' to end the conversation.")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == 'exit':
        print("Goodbye! Keep learning and coding!")
        break

    if not user_input:
        print("Please enter a valid question.")
        continue

    # Add user message to chat history
    chat_history.append({'role': 'user', 'content': user_input})

    # Get response from Ollama API
    response = ollama.chat(
        model='llama3.1',
        messages=chat_history
    )

    ai_message = response['message']['content']
    
    # Add AI response to chat history
    chat_history.append({'role': 'assistant', 'content': ai_message})

    print("TechBot: " + ai_message)
    print("-" * 50)

