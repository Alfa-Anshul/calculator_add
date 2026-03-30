from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def parse_operands(payload: dict) -> tuple[float, float]:
    if not isinstance(payload, dict):
        raise ValueError("JSON body is required.")

    try:
        first = float(payload.get("a"))
        second = float(payload.get("b"))
    except (TypeError, ValueError) as exc:
        raise ValueError("Both a and b must be valid numbers.") from exc

    return first, second


def build_result(operation: str, first: float, second: float, result: float) -> dict:
    symbol = "+" if operation == "add" else "-"
    return {
        "operation": operation,
        "a": first,
        "b": second,
        "result": result,
        "formula": f"{first} {symbol} {second} = {result}",
    }


@app.get("/api/health")
def health() -> tuple[dict, int]:
    return {"status": "ok", "service": "calculator-backend"}, 200


@app.post("/api/add")
def add() -> tuple[dict, int]:
    try:
        first, second = parse_operands(request.get_json(silent=True))
    except ValueError as exc:
        return {"error": str(exc)}, 400

    return jsonify(build_result("add", first, second, first + second)), 200


@app.post("/api/subtract")
def subtract() -> tuple[dict, int]:
    try:
        first, second = parse_operands(request.get_json(silent=True))
    except ValueError as exc:
        return {"error": str(exc)}, 400

    return jsonify(build_result("subtract", first, second, first - second)), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
