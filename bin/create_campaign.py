#!/usr/bin/env python
import os
import sys
import webbrowser

from dotenv import load_dotenv
import requests


mc_url = "https://us19.api.mailchimp.com/3.0"
mc_campaign_url = "https://us19.admin.mailchimp.com/campaigns/edit?id="


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
    data = {
        "type": "regular",
        "recipients": {"list_id": list_id},
        "settings": {
            "from_name": "Matt Layman",
            "reply_to": os.environ["MAILCHIMP_REPLY_TO"],
            "title": article["title"],
            "subject_line": article["title"],
            "preview_text": article["description"],
        },
    }
    response = session.post(f"{mc_url}/campaigns", json=data)
    response.raise_for_status()
    return response.json()


def open_campaign(campaign_web_id):
    """Open a browser to the campaign page."""
    webbrowser.open(f"{mc_campaign_url}{campaign_web_id}")


if __name__ == "__main__":
    load_dotenv()

    # TODO: Parse from HTML file.
    article = {
        "title": "Test title",
        "description": "X" * 200,
        "html_content": "<p>hello world</p>",
    }

    session = requests.Session()
    session.auth = ("me", os.environ["MAILCHIMP_API_KEY"])

    list_id = get_list_id(session)
    campaign = create_campaign(session, list_id, article)
    open_campaign(campaign["web_id"])
