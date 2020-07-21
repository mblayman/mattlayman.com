#!/usr/bin/env python

import json
from pathlib import Path

import typer

ROOT_DIR = Path(__file__).parent.parent
CHECKLIST_ITEMS = ("dev",)


def main(article: Path = typer.Argument(..., exists=True)):
    if article.suffix != ".md":
        typer.echo("The provided article path is not a Markdown file.")
        raise typer.Exit(code=1)

    checklist = Checklist(article)
    checklist.load(CHECKLIST_ITEMS)

    for item in checklist:
        print(item)
    # TODO: Use the checklist.

    checklist.write()


class Checklist:
    """A container to track which checklist items are processed."""

    checklists_dir = ROOT_DIR / "checklists"

    def __init__(self, article):
        self.article = article
        self.items = {}

    def __iter__(self):
        return iter(self.items.keys())

    @property
    def path(self):
        article_path = str(self.article.relative_to("content").with_suffix(".json"))
        article_path = article_path.replace("/", "_")
        return self.checklists_dir / article_path

    def load(self, checklist_items):
        try:
            with self.path.open() as f:
                self.items = json.load(f)
        except FileNotFoundError:
            self.items = {item: False for item in checklist_items}

    def write(self):
        """Store the checklist for any future use."""
        with self.path.open("w") as f:
            json.dump(self.items, f, sort_keys=True, indent=2)


if __name__ == "__main__":
    typer.run(main)
