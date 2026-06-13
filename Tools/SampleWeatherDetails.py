GROQ_API_KEY = "xxxx"

from groq import Groq
client = Groq(api_key=GROQ_API_KEY)
MODEL  = "llama-3.1-8b-instant"

questions = [
    "What is the weather in Chennai right now?",
    "What is today's date?",
    "What is the current price of gold in India?"
]

print(" Model WITHOUT Tools\n" + "="*50)

for q in questions:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": q}],
        max_tokens=80
    )
    answer = response.choices[0].message.content.strip()
    print(f"\n❓ {q}")
    print(f"🤖 {answer[:200]}")
    print("-"*50)

    import json


def get_weather(city: str) -> dict:
    """
    Simulates a Weather API call.
    In real life this would call OpenWeatherMap API.
    """

    weather_data = {
        "chennai":   {"temp": 34, "condition": "Sunny",  "humidity": 78, "unit": "°C"},
        "mumbai":    {"temp": 29, "condition": "Cloudy", "humidity": 85, "unit": "°C"},
        "delhi":     {"temp": 38, "condition": "Hazy",   "humidity": 45, "unit": "°C"},
        "bangalore": {"temp": 24, "condition": "Rainy",  "humidity": 90, "unit": "°C"},
        "coimbatore":{"temp": 31, "condition": "Partly Cloudy", "humidity": 70, "unit": "°C"},
        "kolkata":   {"temp": 32, "condition": "Humid",  "humidity": 88, "unit": "°C"},
    }
    key = city.lower().strip()
    if key in weather_data:
        data = weather_data[key]
        return {
            "city": city.title(),
            "temperature": f"{data['temp']}{data['unit']}",
            "condition": data["condition"],
            "humidity": f"{data['humidity']}%",
            "status": "success"
        }
    return {"status": "error", "message": f"City '{city}' not found in database"}



print("Testing tool function directly:")
print(get_weather("Chennai"))
print(get_weather("Mumbai"))

weather_tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for any city in India. Returns temperature, condition and humidity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city (e.g. Chennai, Mumbai, Delhi)"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

print(" Tool schema defined!")
print("   Tool name :", weather_tool_schema[0]["function"]["name"])
print("   Description:", weather_tool_schema[0]["function"]["description"])

def weather_agent(user_question: str, verbose: bool = True):
    """Weather agent that uses tool calling to answer weather questions."""

    if verbose:
        print(f"\n{'='*55}")
        print(f" STEP 1 — User Input: {user_question}")
        print(f"{'='*55}")

    messages = [{"role": "user", "content": user_question}]


    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=weather_tool_schema,
        tool_choice="auto"
    )

    msg         = response.choices[0].message
    finish_reason = response.choices[0].finish_reason

    if verbose:
        print(f"\n STEP 2 — Model Decision: finish_reason = '{finish_reason}'")


    if finish_reason == "tool_calls" and msg.tool_calls:
        tool_call = msg.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        if verbose:
            print(f" STEP 3 — Tool Invoked : {tool_name}")
            print(f"            Arguments   : {tool_args}")


        tool_result = get_weather(**tool_args)

        if verbose:
            print(f" STEP 4 — Tool Result  : {tool_result}")


        messages.append(msg)
        messages.append({
            "role":         "tool",
            "tool_call_id": tool_call.id,
            "content":      json.dumps(tool_result)
        })


        final = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        final_answer = final.choices[0].message.content

    else:

        final_answer = msg.content

    if verbose:
        print(f"\nSTEP 5 — Final Answer:")
        print(f"   {final_answer}")

    return final_answer


print(" weather_agent() function ready!")

weather_agent("What is the weather like in Chennai today?")
