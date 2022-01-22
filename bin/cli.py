import typer

import checklist

app = typer.Typer()

app.command("checklist")(checklist.main)


@app.command("other")
def other():
    pass
