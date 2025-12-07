from state import tasktree, taskengine
import typer

app = typer.Typer()


@app.command()
def tasks():
    tasktree.print()

