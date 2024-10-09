import pytest
from app.db import FakeDB
from app.models import Task, UpdateTaskModel

@pytest.fixture
def fake_db():
    return FakeDB()

def test_add_task(fake_db):
    task = Task(title="Test Task", description="Test Description", completed=False)
    added_task = fake_db.add_task(task)
    assert added_task.id == 1
    assert added_task.title == "Test Task"
    assert added_task.description == "Test Description"
    assert added_task.completed == False

def test_get_task(fake_db):
    task = Task(title="Test Task", description="Test Description", completed=False)
    added_task = fake_db.add_task(task)
    retrieved_task = fake_db.get_task(added_task.id)
    assert retrieved_task == added_task

def test_get_task_not_found(fake_db):
    assert fake_db.get_task(999) is None

def test_get_tasks(fake_db):
    task1 = Task(title="Task 1", description="Description 1", completed=False)
    task2 = Task(title="Task 2", description="Description 2", completed=True)
    fake_db.add_task(task1)
    fake_db.add_task(task2)
    tasks = fake_db.get_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"

def test_update_task(fake_db):
    task = Task(title="Original Task", description="Original Description", completed=False)
    added_task = fake_db.add_task(task)
    update = UpdateTaskModel(title="Updated Task", description="Updated Description", completed=True)
    updated_task = fake_db.update_task(added_task.id, update)
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated Description"
    assert updated_task.completed == True

def test_update_task_not_found(fake_db):
    update = UpdateTaskModel(title="Updated Task")
    assert fake_db.update_task(999, update) is None

def test_delete_task(fake_db):
    task = Task(title="Test Task", description="Test Description", completed=False)
    added_task = fake_db.add_task(task)
    fake_db.delete_task(added_task.id)
    assert fake_db.get_task(added_task.id) is None

def test_delete_all_tasks(fake_db):
    task1 = Task(title="Task 1", description="Description 1", completed=False)
    task2 = Task(title="Task 2", description="Description 2", completed=True)
    fake_db.add_task(task1)
    fake_db.add_task(task2)
    fake_db.delete_all_tasks()
    assert len(fake_db.get_tasks()) == 0
