from __future__ import annotations

import os
from pathlib import Path

import frontmatter

from . import constants


class Article:
    def __init__(self, article_path: Path):
        self.article_path = article_path
        self._raw_article = frontmatter.load(article_path)

    @property
    def title(self) -> str:
        return self._raw_article["title"]

    @property
    def tags(self) -> list:
        return self._raw_article["tags"]

    @property
    def series(self) -> list | None:
        return self._raw_article.get("series")

    @property
    def embed_code(self) -> str | None:
        if "video" in self._raw_article.keys():
            return self._raw_article["video"].split("/")[-1]

    @property
    def content(self) -> str:
        return self._raw_article.content

    @property
    def canonical_url(self):
        # Remove the "content" part of the path.
        path_parts = self.article_path.split("/")[1:]
        base_name = os.path.splitext(path_parts[-1])[0]
        # Strip off the date. Expects "YYYY-MM-DD-".
        path_parts[-1] = base_name[11:]
        path = "/".join(path_parts)
        return f"{constants.WEBSITE_URL}/{path}/"
