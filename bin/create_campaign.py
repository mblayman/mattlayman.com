#!/usr/bin/env python
import os
import sys
import time
import webbrowser

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pyperclip
import requests


mc_url = "https://us19.api.mailchimp.com/3.0"
mc_campaign_url = "https://us19.admin.mailchimp.com/campaigns/edit?id="


def parse_article(article_path):
    """Parse the content of the article into a dict."""
    with open(article_path, "r") as f:
        article_html = f.read()

    soup = BeautifulSoup(article_html, "html.parser")
    title = soup.find("h1", class_="post-full-title")
    description = soup.find("meta", attrs={"name": "description"})
    content = soup.find("div", class_="kg-card-markdown")

    return {
        "title": title.string,
        "description": description.attrs["content"],
        "html_content": content.encode_contents().decode("utf-8"),
    }


def get_list_id(session):
    """Get the list ID from the name."""
    response = session.get(f"{mc_url}/lists")
    response.raise_for_status()
    lists_data = response.json()

    list_id = ""
    for l in lists_data.get("lists"):
        if l.get("name") == "Matt Layman":
            list_id = l.get("id")

    if not list_id:
        sys.exit("No list found.")

    return list_id


def create_campaign(session, list_id, article):
    """Create a new campaign for the post."""
    template_id = get_one_column_template_id(session)
    data = {
        "type": "regular",
        "recipients": {"list_id": list_id},
        "settings": {
            "from_name": "Matt Layman",
            "reply_to": os.environ["MAILCHIMP_REPLY_TO"],
            "title": article["title"],
            "subject_line": article["title"],
            "preview_text": article["description"],
            "template_id": template_id,
        },
    }
    response = session.post(f"{mc_url}/campaigns", json=data)
    response.raise_for_status()
    return response.json()


def get_one_column_template_id(session):
    """Get the template ID of the 1-Column style."""
    response = session.get(
        f"{mc_url}/templates", params={"count": "40", "type": "base"}
    )
    response.raise_for_status()
    data = response.json()
    for template in data["templates"]:
        if template.get("name") == "1 Column":
            return template.get("id")

    sys.exit("Failed to find 1 Column template.")


def open_campaign(campaign_web_id):
    """Open a browser to the campaign page."""
    webbrowser.open(f"{mc_campaign_url}{campaign_web_id}")


if __name__ == "__main__":
    load_dotenv()

    if len(sys.argv) < 1:
        sys.exit("Provide the path to the HTML article.")

    article_path = sys.argv[1]
    article = parse_article(article_path)

    session = requests.Session()
    session.auth = ("me", os.environ["MAILCHIMP_API_KEY"])

    list_id = get_list_id(session)
    campaign = create_campaign(session, list_id, article)
    pyperclip.copy(article["html_content"])
    print("Article copied to clipboard.")
    time.sleep(1)
    open_campaign(campaign["web_id"])
