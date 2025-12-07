import typer
import re
from state import tasktree, taskengine
from tasknode import TaskNode

app = typer.Typer()


@app.command()
def task(title: str, property: str):
    key, value = property.split(" ")
    task = tasktree.find_task(title)
    if task:
        task.update(key, value)
        taskengine._db_handler.write_tasks(tasktree.to_dict())
    else:
        print("Task not found")
