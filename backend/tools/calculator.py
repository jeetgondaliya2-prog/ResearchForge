from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Example:
    1000 * 0.18
    """

    try:

        result = eval(
            expression,
            {
                "__builtins__": {}
            }
        )

        return str(result)

    except Exception as e:

        return f"Calculation error: {str(e)}"