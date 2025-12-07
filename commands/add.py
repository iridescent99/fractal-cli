import typer
import re
from state import tasktree, taskengine

app = typer.Typer()


@app.command()
def task(task: str):
    chain = re.split(r'>', task)
    prev_task = None
    for task in chain:
        taskobj = tasktree.add(prev_task, task, 0)
        prev_task = taskobj
    taskengine._db_handler.write_tasks(tasktree.to_dict())