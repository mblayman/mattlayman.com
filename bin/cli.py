import typer

import checklist
import create_campaign
import make_youtube_article
from tools import newsletter

app = typer.Typer()

app.command("campaign")(create_campaign.main)
app.command("checklist")(checklist.main)
app.command("newsletter")(newsletter.main)
app.command("yt")(make_youtube_article.main)
