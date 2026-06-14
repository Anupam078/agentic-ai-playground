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