import typer
from commands import show, add, update, delete
from state import tasktree, taskengine
from fractalcli import ERRORS, __app_name__, __version__, config, database
from pathlib import Path

app = typer.Typer()
app.add_typer(add.app, name="add")
app.add_typer(show.app, name="show")
app.add_typer(update.app, name="update")
app.add_typer(delete.app, name="delete")


@app.callback()
def main(verbose: bool = typer.Option(False, "--verbose", "-v")):
    tasktree.verbose = verbose
    tasktree.serialize(taskengine._db_handler.read_tasks().todo_list)


@app.command()
def init(
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
            prompt="to-do database location?",
        ),
) -> None:
    """Initialize the to-do database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)
