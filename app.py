from flask import Flask, render_template, request


app = Flask(__name__)


ALLOWED_CHARACTERS = set("0123456789+-*/.() ")


def safe_evaluate(expression: str) -> str:
    expression = expression.strip()
    if not expression:
        return "0"

    if any(character not in ALLOWED_CHARACTERS for character in expression):
        raise ValueError("Unsupported characters in expression.")

    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except ZeroDivisionError as exc:
        raise ValueError("Cannot divide by zero.") from exc
    except Exception as exc:  # noqa: BLE001
        raise ValueError("Invalid expression.") from exc

    return str(result)


@app.route("/", methods=["GET", "POST"])
def index():
    expression = ""
    result = "0"
    error = ""

    if request.method == "POST":
        expression = request.form.get("expression", "")
        try:
            result = safe_evaluate(expression)
        except ValueError as exc:
            error = str(exc)
            result = "Error"

    return render_template(
        "index.html",
        expression=expression,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
