import os

import requests


class DEVGateway:
    url = "https://dev.to/api"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {"api-key": os.environ["DEV_API_KEY"]}

    def get_published_articles(self):
        """Get all the published articles."""
        response = self.session.get(
            f"{self.url}/articles/me/published", params={"per_page": 1000}
        )
        response.raise_for_status()
        return response.json()

    def publish(self, article_id):
        """Publish the article."""
        data = {"article": {"published": True}}
        response = self.session.put(f"{self.url}/articles/{article_id}", json=data)
        response.raise_for_status()

    def create_article(
        self, *, title, body, tags, canonical_url, series=None, published=False
    ):
        """Create an article on DEV."""
        data = {
            "article": {
                "title": title,
                "published": published,
                "body_markdown": body,
                "tags": [tag.lower() for tag in tags],
                "canonical_url": canonical_url,
            }
        }
        if series:
            data["article"]["series"] = series

        response = self.session.post(f"{self.url}/articles", json=data)
        response.raise_for_status()
        return response.json()
