from __future__ import annotations

from pathlib import Path

import frontmatter
from bs4 import BeautifulSoup

from . import constants


class Article:
    def __init__(self, article_path: Path):
        self.article_path = article_path
        self._raw_article = frontmatter.load(article_path)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Article: {self.title}>"

    @property
    def title(self) -> str:
        return self._raw_article["title"]

    @property
    def description(self) -> str:
        return self._raw_article["description"]

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
    def html_content(self) -> str:
        with open(self._output_path, "r") as f:
            article_html = f.read()

        soup = BeautifulSoup(article_html, "html.parser")
        content = soup.find("div", class_="article-content")
        return content.encode_contents().decode("utf-8")

    @property
    def _output_path(self):
        return constants.public_dir / self._slug_path / "index.html"

    @property
    def _slug_path(self):
        path = self.article_path.relative_to(constants.content_dir)
        path_parts = list(path.parts)

        # Strip off the date. Expects "YYYY-MM-DD-".
        path_parts[-1] = path.stem[11:]

        # Articles in the main blog area include the year in the path.
        if path_parts[0] == "blog":
            path_parts = ["blog", path.stem[:4]] + path_parts[1:]

        return "/".join(path_parts)

    @property
    def canonical_url(self):
        return f"{constants.WEBSITE_URL}/{self._slug_path}/"
