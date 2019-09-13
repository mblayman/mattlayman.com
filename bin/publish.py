"""Publish scheduled articles to DEV."""
import datetime
import logging

import requests
from dateutil.parser import parse

from devto import DEVGateway


dev_gateway = DEVGateway()
logger = logging.getLogger(__name__)


def publish_scheduled_articles():
    published_articles = dev_gateway.get_published_articles()
    published_article_ids = set([article["id"] for article in published_articles])

    scheduled_articles = get_scheduled_articles()
    for scheduled_article in scheduled_articles:
        if should_publish(scheduled_article, published_article_ids):
            article_id = scheduled_article["id"]
            logger.info(f"Publishing article with id: {article_id}")
            dev_gateway.publish(article_id)


def get_scheduled_articles():
    """Get the schedule from GitHub."""
    logger.info("Fetch schedule.")
    url = "https://raw.githubusercontent.com/mblayman/mattlayman.com/master/devto-schedule.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def should_publish(article, published_article_ids):
    """Check if the article should be published.

    This depends on if the date is in the past
    and if the article is already published.
    """
    publish_date = parse(article["publish_date"])
    now = datetime.datetime.now(datetime.timezone.utc)
    return publish_date < now and article["id"] not in published_article_ids


if __name__ == "__main__":
    publish_scheduled_articles()
