import os
import string
from dataclasses import dataclass

import requests
from dateutil import parser

from tools import constants
from tools.youtube import build_youtube_client


@dataclass
class Video:
    youtube_id: str
    title: str
    description: str
    published_at_str: str
    image_url: str
    tags: list
    live_broadcast_content: str

    @property
    def published_at(self):
        return parser.parse(self.published_at_str)

    @property
    def image_filename(self):
        _, extension = os.path.splitext(self.image_url)
        filename = self.youtube_id + extension
        img_year_dir = constants.static_dir / "img" / str(self.published_at.year)
        img_year_dir.mkdir(exist_ok=True)
        return img_year_dir / filename


def main(url: str):
    """Generate an article from a YouTube video URL."""
    video_id = url.split("=")[1]
    video = get_video(video_id)
    fetch_thumbnail(video)
    generate_article(video)


def get_video(video_id):
    youtube = build_youtube_client()
    request = youtube.videos().list(part="snippet", id=video_id)
    snippet = request.execute()["items"][0]["snippet"]
    thumbnail = None
    for size in ["maxres", "standard", "high"]:
        if size in snippet["thumbnails"]:
            thumbnail = snippet["thumbnails"][size]
            break
    if thumbnail is None:
        print(snippet["thumbnails"])
        raise Exception("Failed to find a size")

    print(snippet["title"])
    return Video(
        video_id,
        snippet["title"],
        snippet["description"],
        snippet["publishedAt"],
        thumbnail["url"],
        snippet["tags"],
        snippet["liveBroadcastContent"],
    )


def fetch_thumbnail(video):
    response = requests.get(video.image_url)
    response.raise_for_status()

    with open(video.image_filename, "wb") as f:
        f.write(response.content)


def generate_article(video):
    template_filename = constants.templates_dir / "article.md"
    with open(template_filename) as f:
        template = string.Template(f.read())

    title = slugify(video.title)
    filename = f"{video.published_at:%Y-%m-%d}-{title}.md"
    filepath = constants.root / "content" / "videos" / filename
    with open(filepath, "w") as f:
        short_description = video.description.split("\n")[0]
        mapping = {
            "title": video.title.replace('"', "'"),
            "description": short_description.replace('"', "'"),
            "image_filename": video.image_filename.relative_to(constants.static_dir),
            "youtube_id": video.youtube_id,
            "tags": repr(video.tags),
        }
        content = template.substitute(mapping)
        f.write(content)


def slugify(title):
    parts = title.split(" ")
    # Replace any slashes *within* a word (e.g., `ci/cd`)
    parts = [part.replace("/", "-") for part in parts if part != "-" and part != "/"]
    title = "-".join(parts)
    title = title.replace("#", "")
    return title.lower()
