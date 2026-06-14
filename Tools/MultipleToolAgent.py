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