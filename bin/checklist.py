#!/usr/bin/env python

from pathlib import Path

import typer


def main(article: Path = typer.Argument(..., exists=True)):
    if article.suffix != ".md":
        typer.echo("The provided article path is not a Markdown file.")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
