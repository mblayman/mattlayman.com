import typer

import checklist
import make_youtube_article

app = typer.Typer()

app.command("checklist")(checklist.main)
app.command("yt")(make_youtube_article.main)
