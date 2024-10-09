import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Task, UpdateTaskModel, TaskList
from app.db import db

client = TestClient(app)

def test_create_task():
    task_data = {"title": "New Task", "description": "Test Description", "completed": False}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    created_task = response.json()
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]
    assert created_task["completed"] == task_data["completed"]
    assert "id" in created_task

def test_get_task():
    task = Task(title="Test Task", description="Test Description", completed=False)
    added_task = db.add_task(task)
    response = client.get(f"/tasks/{added_task.id}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["id"] == added_task.id
    assert retrieved_task["title"] == added_task.title
    assert retrieved_task["description"] == added_task.description
    assert retrieved_task["completed"] == added_task.completed

def test_get_task_not_found():
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_get_tasks():
    db.delete_all_tasks()
    task1 = Task(title="Task 1", description="Description 1", completed=False)
    task2 = Task(title="Task 2", description="Description 2", completed=True)
    db.add_task(task1)
    db.add_task(task2)
    response = client.get("/tasks/")
    assert response.status_code == 200
    task_list = response.json()
    assert len(task_list["tasks"]) == 2
    assert task_list["tasks"][0]["title"] == "Task 1"
    assert task_list["tasks"][1]["title"] == "Task 2"

def test_update_task():
    task = Task(title="Original Task", description="Original Description", completed=False)
    added_task = db.add_task(task)
    update_data = {"title": "Updated Task", "description": "Updated Description", "completed": True}
    response = client.put(f"/tasks/{added_task.id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["id"] == added_task.id
    assert updated_task["title"] == update_data["title"]
    assert updated_task["description"] == update_data["description"]
    assert updated_task["completed"] == update_data["completed"]

def test_update_task_not_found():
    update_data = {"title": "Updated Task"}
    response = client.put("/tasks/9999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task():
    task = Task(title="Task to Delete", description="Will be deleted", completed=False)
    added_task = db.add_task(task)
    response = client.delete(f"/tasks/{added_task.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"
    assert db.get_task(added_task.id) is None

def test_delete_all_tasks_without_confirmation():
    response = client.delete("/tasks/all")
    assert response.status_code == 400
    assert response.json()["detail"] == "Confirmación requerida para eliminar todas las tareas"

def test_delete_all_tasks_with_confirmation():
    task1 = Task(title="Task 1", description="Description 1", completed=False)
    task2 = Task(title="Task 2", description="Description 2", completed=True)
    db.add_task(task1)
    db.add_task(task2)
    response = client.delete("/tasks/all?confirm=true")
    assert response.status_code == 200
    assert response.json()["message"] == "Todas las tareas han sido eliminadas exitosamente"
    assert len(db.get_tasks()) == 0
