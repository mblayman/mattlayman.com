import typer

import make_youtube_article

app = typer.Typer()

app.command("yt")(make_youtube_article.main)
