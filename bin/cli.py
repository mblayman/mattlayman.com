import typer

import create_campaign
import make_youtube_article
from tools import newsletter

app = typer.Typer()

app.command("campaign")(create_campaign.main)
app.command("newsletter")(newsletter.main)
app.command("yt")(make_youtube_article.main)
