import os
import sys
import webbrowser

import requests


class MailchimpGateway:
    mc_url = "https://us19.api.mailchimp.com/3.0"
    mc_campaign_url = "https://us19.admin.mailchimp.com/campaigns/edit?id="

    def __init__(self):
        self.session = requests.Session()
        self.session.auth = ("me", os.environ["MAILCHIMP_API_KEY"])

    def create_campaign(self, title, subject_line, preview_text):
        """Create a new campaign for the post."""
        template_id = self._get_one_column_template_id()
        data = {
            "type": "regular",
            "recipients": {"list_id": self._get_list_id()},
            "settings": {
                "from_name": "Matt Layman",
                "reply_to": os.environ["MAILCHIMP_REPLY_TO"],
                "title": title,
                "subject_line": subject_line,
                "preview_text": preview_text,
                "template_id": template_id,
            },
        }
        response = self.session.post(f"{self.mc_url}/campaigns", json=data)
        response.raise_for_status()
        return response.json()

    def _get_one_column_template_id(self):
        """Get the template ID of the 1-Column style."""
        response = self.session.get(
            f"{self.mc_url}/templates", params={"count": "40", "type": "base"}
        )
        response.raise_for_status()
        data = response.json()
        for template in data["templates"]:
            if template.get("name") == "1 Column":
                return template.get("id")

        sys.exit("Failed to find 1 Column template.")

    def _get_list_id(self):
        """Get the list ID from the name."""
        response = self.session.get(f"{self.mc_url}/lists")
        response.raise_for_status()
        lists_data = response.json()

        list_id = ""
        for lists in lists_data.get("lists"):
            if lists.get("name") == "Matt Layman":
                list_id = lists.get("id")

        if not list_id:
            sys.exit("No list found.")

        return list_id

    def open_campaign(self, campaign_web_id):
        """Open a browser to the campaign page."""
        webbrowser.open(f"{self.mc_campaign_url}{campaign_web_id}")
