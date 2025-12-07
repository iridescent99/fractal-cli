import typer
import re
from state import tasktree, taskengine
from tasknode import TaskNode

app = typer.Typer()


@app.command()
def task(title: str, property: str):
    key, value = property.split(" ", 1)
    task = tasktree.find_task(title)
    if task:
        task.update(key, value)
        taskengine._db_handler.write_tasks(tasktree.to_dict())
    else:
        # TODO: print fuzzy matches
        typer.prompt("Can't find task. Did you spell that correctly?")
