from flask import Flask, jsonify, request
from .utilsl import json_parsing

app = Flask(__name__)


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route("/computation_example", methods=["POST"])
def computation_example():
    request_data = request.get_json()
    res = json_parsing(request_data)()
    return jsonify({"array result": res.tolist()})
