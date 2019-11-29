"""Publish scheduled articles to DEV."""
import datetime
import json
import logging
import sys

from dateutil.parser import parse

from devto import DEVGateway

logger = logging.getLogger(__name__)


def publish_scheduled_articles():
    dev_gateway = DEVGateway()
    published_articles = dev_gateway.get_published_articles()
    published_article_ids = set([article["id"] for article in published_articles])

    scheduled_articles = get_scheduled_articles()
    for scheduled_article in scheduled_articles:
        if should_publish(scheduled_article, published_article_ids):
            article_id = scheduled_article["id"]
            logger.info(f"Publishing article with id: {article_id}")
            dev_gateway.publish(article_id)


def get_scheduled_articles():
    """Get the schedule."""
    logger.info("Read schedule.")
    with open("devto-schedule.json", "r") as f:
        return json.load(f)


def should_publish(article, published_article_ids):
    """Check if the article should be published.

    This depends on if the date is in the past
    and if the article is already published.
    """
    publish_date = parse(article["publish_date"])
    now = datetime.datetime.now(datetime.timezone.utc)
    return publish_date < now and article["id"] not in published_article_ids


if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s: %(message)s", level=logging.INFO, stream=sys.stdout
    )
    import requests

    logger.info("test with cache")
    logger.info(requests.__file__)
    publish_scheduled_articles()
