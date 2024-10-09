"""
Provides a FastAPI router for managing tasks.

The `tasks_router` handles the following API endpoints:

- `POST /`: Creates a new task.
- `GET /{task_id}`: Retrieves a task by its ID.
- `GET /`: Retrieves a list of all tasks.
- `PUT /{task_id}`: Updates an existing task by its ID.
- `DELETE /{task_id}`: Deletes a task by its ID.
- `DELETE /all`: Deletes all tasks (requires confirmation).

The router uses the `db` module to interact with the task data storage.
"""
from fastapi import APIRouter, HTTPException, Query
from ..models import Task, UpdateTaskModel, TaskList
from ..db import db

tasks_router = APIRouter()

@tasks_router.post("/", response_model=Task)
async def create_task(task: Task):
    return db.add_task(task)


@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks_router.get("/", response_model=TaskList)
async def get_tasks():
    tasks = db.get_tasks()
    return TaskList(tasks=tasks)


@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: UpdateTaskModel):
    updated_task = db.update_task(task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@tasks_router.delete("/all", response_model=dict)
async def delete_all_tasks(confirm: bool = Query(False, description="Confirmar eliminación de todas las tareas")):
    if not confirm:
        raise HTTPException(status_code=400, detail="Confirmación requerida para eliminar todas las tareas")
    db.delete_all_tasks()
    return {"message": "Todas las tareas han sido eliminadas exitosamente"}

@tasks_router.delete("/{task_id}")
async def delete_task(task_id: int):
    db.delete_task(task_id)
    return {"message": "Task deleted successfully"}