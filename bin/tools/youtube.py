import os

import googleapiclient.discovery


def build_youtube_client():
    return googleapiclient.discovery.build(
        "youtube", "v3", developerKey=os.environ["YOUTUBE_API_KEY"]
    )
