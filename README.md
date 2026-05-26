# mattlayman.com

This repository is the source for https://www.mattlayman.com. The site is a custom Lua application that runs on [Nibiru](https://github.com/mblayman/nibiru), loads Markdown content, and renders pages through HTML templates.

For AI-agent-specific guidance, start with `AGENTS.md`.

## Project Layout

- `app/entry.lua` is the application entrypoint and route map.
- `app/pages.lua` loads Markdown files, parses frontmatter, validates required fields, and sorts pages by date.
- `app/blog/` contains blog page registration and responders.
- `app/understand_django/` contains Understand Django page registration and responders.
- `templates/` contains the HTML templates used by responders.
- `pages/blog/` contains blog posts.
- `pages/understand-django/` contains Understand Django chapters.
- `static/` contains CSS, JavaScript, images, and other static assets.

## Local Development

Install dependencies with LuaRocks:

```sh
make deps
```

Run the app locally with:

```sh
make local
```

`make local` runs `air`, so the local workflow expects `air` to be installed.

## Docker

Build the image directly with:

```sh
make image
```

Or run the app with Docker Compose:

```sh
docker compose up --build
```

The Compose service exposes port `8080`.

## Content

Blog posts and Understand Django chapters are Markdown files with YAML frontmatter. The loader requires these fields:

- `slug`
- `title`
- `date`

Existing content commonly includes `description`, `image`, and `tags` too. Follow nearby files when adding or editing pages.

## Prism Config

- Languages selected on the Prism builder page are embedded in the link at the top of `static/js/prism.js`.
- The CSS files are separate because the previous Automad site did not use `prefers-color-scheme` for theme selection. The links for those files are also at the top of each CSS file.
