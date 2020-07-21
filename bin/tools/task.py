import typer


class Task:
    prompt = "Ask a yes/no question."
    start = "Starting the task..."

    def handle(self, *args, **kwargs):
        typer.echo("Handling the task.")
        return False
