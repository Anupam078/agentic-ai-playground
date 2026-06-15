import ollama

response = ollama.chat(
    model="llama3.1",
    messages=[
        {"role": "user", 
         "content": "What is Artificial Intelligence? Expplain in 3 sentences."
        } 
    ]
)

print("AI Response:")
print(response['message']['content'])
print("Done!")