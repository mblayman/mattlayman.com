from pathlib import Path

WEBSITE_URL = "https://www.mattlayman.com"

root = Path(__file__).resolve().parent.parent.parent
content_dir = root / "content"
static_dir = root / "static"
templates_dir = root / "bin" / "templates"
