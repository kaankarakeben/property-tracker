import typer
from rich.console import Console

from property_tracker.commands import investor, property

app = typer.Typer()
console = Console()

app.add_typer(investor.app, name="investor")
app.add_typer(property.app, name="property")


@app.callback()
def callback():
    """
    This applications helps you to create tasks and manage them.
    """


if __name__ == "__main__":
    app()
