#Calculator Tool
def calculate(expression: str) -> dict:
    try:
        allowed_set = set("0123456789+-*/(). ")
        if not all(char in allowed_set for char in expression):
            return {"error": "Invalid characters in expression."}
        result = eval(expression)
        return {"expression": expression, "result": result, "Status": "Success"}
    except Exception as e:
        return {"error": str(e), "Status": "Failure"}
    
    # Tool 3: Time Converter

def convert_time(time_str: str, from_timezone: str, to_timezone: str) -> dict:
    """Converts time between Indian cities / timezones (mock)."""

    offsets = {
        "IST": 5.5, "india": 5.5,
        "UTC": 0, "gmt": 0,
        "EST": -5, "usa": -5,
        "PST": -8,
        "CET": 1, "europe": 1
    }

    try:
        hour, minute = map(
            int,
            time_str.replace(":", " ").split()[:2]
        )

        from_off = offsets.get(
            from_timezone.upper(),
            offsets.get(from_timezone.lower(), 0)
        )

        to_off = offsets.get(
            to_timezone.upper(),
            offsets.get(to_timezone.lower(), 0)
        )

        diff = to_off - from_off

        new_hour = int((hour + diff) % 24)

        return {
            "original": f"{time_str} {from_timezone}",
            "converted": f"{new_hour:02d}:{minute:02d} {to_timezone}",
            "difference_hours": diff,
            "status": "success"
        }

    except:
        return {
            "status": "error",
            "message": "Could not parse time"
        }
    
def get_weather(city: str) -> dict:

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

ALL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city in India.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["city"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations. Use for any arithmetic, percentage, or formula.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression e.g. '45 * 12 + 300'"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "convert_time",
            "description": "Convert time between timezones. IST, UTC, EST, PST, CET supported.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_str": {
                        "type": "string",
                        "description": "Time in HH:MM format e.g. '09:00'"
                    },
                    "from_timezone": {
                        "type": "string",
                        "description": "Source timezone e.g. IST"
                    },
                    "to_timezone": {
                        "type": "string",
                        "description": "Target timezone e.g. EST"
                    }
                },
                "required": [
                    "time_str",
                    "from_timezone",
                    "to_timezone"
                ]
            }
        }
    }
]

Tool_MAP = {
    "get_weather": get_weather,
    "calculate": calculate,
    "convert_time": convert_time
}


class WeatherChatbot:
    """A stateful chatbot - remembers the conversation (short-term memory)"""

    def __init__(self):
        self.history = []

        self.system = (
            "You are a helpful weather assistant for India. "
            "When asked about weather, always use the get_weather tool. "
            "Remember what city the user mentioned earlier in the conversation."
        )

    def chat(self, user_input: str):

        print(f"\n👤 You : {user_input}")

        # Store user message in memory
        self.history.append({
            "role": "user",
            "content": user_input
        })

        messages = [
            {
                "role": "system",
                "content": self.system
            }
        ] + self.history

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=weather_tool_schema,
            tool_choice="auto"
        )

        msg = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls" and msg.tool_calls:

            tool_call = msg.tool_calls[0]

            tool_args = json.loads(
                tool_call.function.arguments
            )

            tool_result = get_weather(**tool_args)

            print(
                f" [Tool called: get_weather({tool_args})]"
            )

            self.history.append(msg)

            self.history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })

            messages = [
                {
                    "role": "system",
                    "content": self.system
                }
            ] + self.history

            final = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )

            reply = final.choices[0].message.content

            self.history.append({
                "role": "assistant",
                "content": reply
            })

        else:

            reply = msg.content

            self.history.append({
                "role": "assistant",
                "content": reply
            })

        print(f"🤖 Agent : {reply}")
        print(
            f" [Memory: {len(self.history)} messages stored]"
        )

        return reply


bot = WeatherChatbot()

bot.chat("Hi! I live in Coimbatore.")

bot.chat("What's the weather like today?")

bot.chat("Should I take an umbrella when I go out?")
