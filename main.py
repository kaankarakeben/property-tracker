import typer
from rich.console import Console

from property_tracker.commands import finance, investor, property, simulate

app = typer.Typer()
console = Console()

app.add_typer(investor.app, name="investor")
app.add_typer(property.app, name="property")
app.add_typer(finance.app, name="finance")
app.add_typer(simulate.app, name="simulate")


@app.callback()
def callback():
    """
    This applications helps you to create tasks and manage them.
    """


if __name__ == "__main__":
    app()
