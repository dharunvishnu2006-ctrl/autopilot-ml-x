from flask import Flask, request, jsonify
import pandas as pd
from src.profiler import profile
import os

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    allowed = {"csv", "json", "xlsx"}
    ext = file.filename.rsplit(".", 1)[-1].lower()

    if ext not in allowed:
        return jsonify({"error": "Invalid file type"}), 400

    if ext == "csv":
        df = pd.read_csv(file)
    elif ext == "json":
        df = pd.read_json(file)
    else:  # xlsx
        df = pd.read_excel(file)

    report = profile(df)
    return jsonify(report)


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug, use_reloader=False)
