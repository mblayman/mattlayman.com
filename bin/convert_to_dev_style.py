#!/usr/bin/env python
import os
import re
import sys

import frontmatter
from dotenv import load_dotenv

from devto import DEVGateway

EXTLINK_PATTERN = re.compile(r'.*({{< extlink "(.*)" "(.*)" >}}).*')
EXTLINE_REPLACEMENT_PATTERN = re.compile(r"{{< extlink .* >}}")
REF_PATTERN = re.compile(r'.*{{< ref "(.*?)" >}}.*')
REF_REPLACEMENT_PATTERN = re.compile(r"{{< ref .* >}}")
YOUTUBE_IFRAME_PATTERN = re.compile(r'.*youtube.com/embed/(.*?)".*')
WEBSITE_URL = "https://www.mattlayman.com"


def main():
    if len(sys.argv) < 1:
        sys.exit("Provide the path to the Markdown article.")

    load_dotenv()

    article_path = sys.argv[1]
    article = frontmatter.load(article_path)
    output = []

    if "video" in article.keys():
        embed_code = article["video"].split("/")[-1]
        output.extend([f"{{% youtube {embed_code} %}}", ""])

    state = "unknown"
    for line in article.content.splitlines():
        previous_state = state
        state = check_state(previous_state, line)
        # print(f"{previous_state} -> {state}")
        run_state(previous_state, state, line, output)

    dev_markdown = "\n".join(output)
    # print(dev_markdown)
    canonical_url = get_canonical_url(article_path)
    create_article(article, dev_markdown, canonical_url)


def check_state(current_state, line):
    if current_state == "unknown":
        if line:
            return check_starting_line_state(line)
        else:
            return "empty_line"
    elif current_state == "paragraph":
        if line:
            return "paragraph"
        else:
            return "empty_line"
    elif current_state == "empty_line":
        if line:
            return check_starting_line_state(line)
        else:
            return "empty_line"
    elif current_state == "fenced":
        if line != "```":
            return "fenced"
        else:
            return "empty_line"
    elif current_state == "list":
        if line:
            return "list"
        else:
            return "empty_line"
    elif current_state == "blockquote":
        if line:
            return "blockquote"
        else:
            return "empty_line"

    raise Exception(f"unhandled state: {current_state} with line: {line}")


def check_starting_line_state(line):
    """Check the starting line looks like some Markdown type.

    Assumes the line has content.
    """
    if line.startswith("```"):
        return "fenced"
    elif line.startswith("> "):
        return "blockquote"
    elif line.strip().startswith("* "):
        return "list"
    return "paragraph"


def run_state(previous_state, state, line, output):
    return globals()[f"process_{state}"](previous_state, line, output)


def process_blockquote(previous_state, line, output):
    line = process_line(line)
    if previous_state != "blockquote":
        output.append(line)
    else:
        output[-1] = output[-1] + " " + line.lstrip("> ")


def process_empty_line(previous_state, line, output):
    output.append(line)


def process_fenced(previous_state, line, output):
    output.append(line)


def process_list(previous_state, line, output):
    line = process_line(line)
    if line.strip().startswith("* "):
        output.append(line)
    else:
        output[-1] = output[-1] + " " + line.lstrip()


def process_paragraph(previous_state, line, output):
    line = process_line(line)
    if previous_state != "paragraph":
        output.append(line)
    else:
        output[-1] = output[-1] + " " + line


def process_line(line):
    line = convert_extlink(line)
    line = convert_ref(line)
    line = convert_youtube_embed(line)
    return line


def convert_extlink(line):
    if "{{< extlink" in line:
        match = EXTLINK_PATTERN.match(line)
        link = match.group(2)
        text = match.group(3)
        return EXTLINE_REPLACEMENT_PATTERN.sub(f"[{text}]({link})", line)
    return line


def convert_ref(line):
    if "{{< ref" in line:
        match = REF_PATTERN.match(line)
        ref_path = match.group(1)
        if "_index.md" in ref_path:
            ref_url = f"{WEBSITE_URL}{ref_path.replace('_index.md', '')}"
            return REF_REPLACEMENT_PATTERN.sub(ref_url, line)
        else:
            raise Exception(f"unhandled ref style: {ref_path}")
    return line


def convert_youtube_embed(line):
    if "iframe" in line and "youtube" in line:
        match = YOUTUBE_IFRAME_PATTERN.match(line)
        embed_code = match.group(1)
        return f"{{% youtube {embed_code} %}}"
    return line


def get_canonical_url(article_path):
    # Remove the "content" part of the path.
    path_parts = article_path.split("/")[1:]
    base_name = os.path.splitext(path_parts[-1])[0]
    # Strip off the date. Expects "YYYY-MM-DD-".
    path_parts[-1] = base_name[11:]
    path = "/".join(path_parts)
    return f"{WEBSITE_URL}/{path}/"


def create_article(article, dev_markdown, canonical_url):
    dev_gateway = DEVGateway()
    data = dev_gateway.create_article(
        title=article["title"],
        body=dev_markdown,
        tags=article["tags"],
        series=article.get("series"),
        canonical_url=canonical_url,
    )
    print(f"New article ID: {data['id']}")


if __name__ == "__main__":
    main()
