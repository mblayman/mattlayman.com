#!/usr/bin/env python
import os
import string
import sys
from dataclasses import dataclass
from pathlib import Path

import googleapiclient.discovery
import requests
from dateutil import parser
from dotenv import load_dotenv

root = Path(__name__).resolve().parent
static_dir = root / "static"
templates_dir = root / "bin" / "templates"


@dataclass
class Video:
    youtube_id: str
    title: str
    description: str
    published_at_str: str
    image_url: str
    tags: list

    @property
    def published_at(self):
        return parser.parse(self.published_at_str)

    @property
    def image_filename(self):
        _, extension = os.path.splitext(self.image_url)
        filename = self.youtube_id + extension
        return static_dir / "img" / str(self.published_at.year) / filename


def main():
    if len(sys.argv) < 2:
        sys.exit("Missing YouTube URL")

    url = sys.argv[1]
    video_id = url.split("=")[1]
    video = get_video(video_id)
    fetch_thumbnail(video)
    generate_article(video)


def get_video(video_id):
    youtube = build_youtube_client()
    request = youtube.videos().list(part="snippet", id=video_id)
    snippet = request.execute()["items"][0]["snippet"]
    return Video(
        video_id,
        snippet["title"],
        snippet["description"],
        snippet["publishedAt"],
        snippet["thumbnails"]["maxres"]["url"],
        snippet["tags"],
    )


def build_youtube_client():
    return googleapiclient.discovery.build(
        "youtube", "v3", developerKey=os.environ["YOUTUBE_API_KEY"]
    )


def fetch_thumbnail(video):
    response = requests.get(video.image_url)
    response.raise_for_status()

    with open(video.image_filename, "wb") as f:
        f.write(response.content)


def generate_article(video):
    template_filename = templates_dir / "article.md"
    with open(template_filename) as f:
        template = string.Template(f.read())

    title = slugify(video.title)
    filename = f"{video.published_at:%Y-%m-%d}-{title}.md"
    filepath = root / "content" / "blog" / filename
    with open(filepath, "w") as f:
        short_description = video.description.split("\n")[0]
        mapping = {
            "title": video.title.replace('"', "'"),
            "description": short_description.replace('"', "'"),
            "image_filename": video.image_filename.relative_to(static_dir),
            "youtube_id": video.youtube_id,
            "tags": repr(video.tags),
        }
        content = template.substitute(mapping)
        f.write(content)


def slugify(title):
    parts = title.split(" ")
    parts = [part for part in parts if part != "-"]
    title = "-".join(parts)
    title = title.replace("#", "")
    return title.lower()


if __name__ == "__main__":
    load_dotenv()
    main()
