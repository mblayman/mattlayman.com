import time
from pathlib import Path

import pyperclip
import typer
from dotenv import load_dotenv

from tools.article import Article
from tools.mailchimp import MailchimpGateway


def main(article_path: Path = typer.Argument(..., exists=True)):
    """Create a Mailchimp campaign for an article."""
    load_dotenv()

    article = Article(article_path)

    mailchimp = MailchimpGateway()
    campaign = mailchimp.create_campaign(
        article.title, article.title, article.description
    )

    pyperclip.copy(article.html_content)
    print("Article copied to clipboard.")
    time.sleep(1)

    mailchimp.open_campaign(campaign["web_id"])
