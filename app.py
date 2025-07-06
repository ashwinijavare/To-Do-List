from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/add", methods=["POST"])
def add_task():
    data = request.json
    tasks = load_tasks()
    tasks.append({"task": data["task"], "done": False})
    save_tasks(tasks)
    return jsonify(success=True)

@app.route("/delete", methods=["POST"])
def delete_task():
    data = request.json
    tasks = load_tasks()
    del tasks[data["index"]]
    save_tasks(tasks)
    return jsonify(success=True)

@app.route("/done", methods=["POST"])
def mark_done():
    data = request.json
    tasks = load_tasks()
    tasks[data["index"]]["done"] = True
    save_tasks(tasks)
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
