from uuid import uuid4
from flask import Flask, jsonify, request
from models.task import Task


app = Flask(__name__)

tasks = []


@app.get("/tasks")
def get_all_tasks():
    tasks_list = [task.to_dict() for task in tasks]
    return jsonify({
        "tasks": tasks_list,
        "total_tasks": len(tasks_list)
    })


@app.get("/tasks/<uuid:id>")
def get_task(id: str):
    for task in tasks:
        if task.id == id:
            return jsonify({ "task": task.to_dict() })

    return jsonify({"message": "Task not found"})


@app.post("/tasks")
def create_task():
    data = request.get_json()
    task = Task(id=uuid4(), title=data.get('title'), description=data.get('description', ''))
    tasks.append(task)
    return jsonify({
        "message": "Task created",
        "task": task.to_dict()
    }), 201


@app.put("/tasks/<uuid:id>")
def complete_task(id: str):
    for task in tasks:
        if task.id == id:
            task.is_completed = True
            return jsonify({ "success": "OK" })

    return jsonify({ "message": "Task not found" })


@app.delete("/tasks/<uuid:id>")
def delete_task(id: str):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
    
    return jsonify({
        "message": "Task deleted"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
