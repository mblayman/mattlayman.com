import datetime
import os
from pathlib import Path

import typer

from . import constants


def default_month() -> datetime.datetime:
    return datetime.datetime.now()


def main(
    month: datetime.datetime = typer.Argument(default=default_month, formats=["%Y-%m"])
):
    """Generate a monthly newsletter for Mailchimp"""
    month_str = f"{month:%Y-%m}"

    month_content = []
    for dirpath, _, filenames in os.walk(constants.content_dir):
        for filename in filenames:
            if filename.startswith(month_str):
                month_content.append((dirpath, filename))

    for dirpath, filename in sorted(month_content, key=lambda v: v[1]):
        path = Path(dirpath) / filename
        print(path)
