import json
import os
from pathlib import Path

import requests

from make_youtube_article import get_video, fetch_thumbnail, generate_article

processed_videos = Path(__file__).parent / "processed_videos.json"


def main():
    api_video_ids = get_api_video_ids()
    processed_video_ids = get_processed_video_ids()
    missing_video_ids = set(api_video_ids) - set(processed_video_ids)
    for video_id in missing_video_ids:
        video = get_video(video_id)

        # The API sometimes has other videos in it that weren't meant for publishing.
        # This attribute seems to be the right one to check against.
        if video.live_broadcast_content == "none":
            fetch_thumbnail(video)
            generate_article(video)

        processed_video_ids.append(video_id)

    with open(processed_videos, "w") as f:
        f.write(json.dumps(sorted(processed_video_ids), indent=2))


def get_processed_video_ids():
    with open(processed_videos, "r") as f:
        return json.load(f)


def get_api_video_ids():
    response = requests.get(
        f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=UUA-ORpF9LEgECmkP3nvVLXQ&key={os.environ['YOUTUBE_API_KEY']}"
    )
    data = response.json()
    video_ids = []

    for item in data["items"]:
        video_ids.append(item["contentDetails"]["videoId"])

    return video_ids


if __name__ == "__main__":
    main()
