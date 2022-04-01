import datetime
import os
from pathlib import Path

import pyperclip
import typer
from jinja2 import Environment, FileSystemLoader

from . import constants
from .article import Article
from .mailchimp import MailchimpGateway


def default_month() -> datetime.datetime:
    return datetime.datetime.now()


def main(
    month: datetime.datetime = typer.Argument(default=default_month, formats=["%Y-%m"])
):
    """Generate a monthly newsletter for Mailchimp"""
    month_content = get_month_content(month)
    articles = [Article(article_path) for article_path in month_content]
    html = render_newsletter(articles)
    pyperclip.copy(html)
    print("Newsletter copied to clipboard.")

    mailchimp = MailchimpGateway()
    month_name = f"{month:%B %Y}"
    campaign = mailchimp.create_campaign(
        month_name,
        f"What did you miss from {month_name}?",
        "In case you missed it, here are some software developer topics "
        "that I covered this past month.",
    )
    mailchimp.open_campaign(campaign["web_id"])


def get_month_content(month: datetime.datetime) -> list[Path]:
    month_str = f"{month:%Y-%m}"

    month_content = []
    for dirpath, _, filenames in os.walk(constants.content_dir):
        for filename in filenames:
            if filename.startswith(month_str):
                month_content.append((dirpath, filename))

    return [
        Path(dirpath).relative_to(constants.root) / filename
        for dirpath, filename in sorted(month_content, key=lambda v: v[1])
    ]


def render_newsletter(articles: list[Article]) -> str:
    env = Environment(
        loader=FileSystemLoader(str(constants.templates_dir)), autoescape=False
    )
    template = env.get_template("newsletter.html")
    return template.render(articles=articles)
