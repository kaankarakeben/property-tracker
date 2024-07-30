import typer
from rich.console import Console

from property_tracker.commands import add_investor

# Set up application
app = typer.Typer()
console = Console()


app.add_typer(add_investor.app, name="add-investor")


@app.callback()
def callback():
    """
    This applications helps you to create tasks and manage them.
    """


if __name__ == "__main__":
    app()
