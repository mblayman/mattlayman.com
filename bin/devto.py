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
