import ollama
print("Welcome to the Ollama Chatbot!")
print("You can ask any question and press Enter")
print("Type 'exit' to end the conversation.")

message_count = 0

while True:
    #Get input from User
    user_input = input("You: ").strip()

    #Exit Condition
    if user_input.lower() == 'exit':
        print(f"Goodbye! you asked {message_count} questions.")
        break

    #Skip empty input
    if not user_input:
        print("Please enter a valid question.")
        continue

    message_count += 1

    #Send the message to the Ollama API
    response= ollama.chat(
        model='llama3.1',
        messages=[
            { 
                "role": "user",
             
                "content": user_input
            
            }
        ]
    )

    #Print the response
    print("AI: " + response['message']['content'])
    print("-" * 50)



    
    