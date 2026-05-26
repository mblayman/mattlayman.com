# Agent Guide

This repository powers https://www.mattlayman.com. It is a custom Lua site that runs on Nibiru, with Markdown content rendered through HTML templates.

## Start Here

- Read `README.md` for the human-facing quickstart.
- Use `app/entry.lua` as the route map and application entrypoint.
- Use `app/pages.lua` to understand how Markdown files are loaded and validated.
- Check `app/blog/pages.lua` and `app/understand_django/pages.lua` for content collection requirements.
- Check `templates/` before changing rendered markup.
- Check `static/site.css` before changing layout or styling.

## Project Map

- `app/entry.lua` defines the Nibiru application routes.
- `app/responders.lua` handles the home page and health check.
- `app/blog/responders.lua` renders blog entries from `pages/blog/`.
- `app/understand_django/responders.lua` renders book chapters from `pages/understand-django/`.
- `app/pages.lua` loads Markdown files, parses frontmatter, validates required keys, detects duplicate slugs, and sorts pages by date descending.
- `app/template_functions.lua` registers template helper functions.
- `templates/` contains the Nibiru/Jinja-style HTML templates.
- `static/` contains CSS, JavaScript, images, and other static assets.
- `pages/blog/` contains blog Markdown content.
- `pages/understand-django/` contains Understand Django Markdown content.

## Common Commands

- `make deps` installs Nibiru into `.rocks` with LuaRocks.
- `make local` runs `air` for local development.
- `make image` builds the Docker image as `lua-app`.
- `docker compose up --build` builds and runs the app with port `8080` exposed.

The Docker runtime command is `/srv/rocks/bin/nibiru run app.entry:app`.

## Content Conventions

Markdown pages in `pages/blog/` and `pages/understand-django/` must include these frontmatter keys:

- `slug`
- `title`
- `date`

Most existing pages also include `description`, `image`, and `tags`. Preserve nearby file patterns when adding or editing content. Slugs must be unique within their collection because `app/pages.lua` raises an error for duplicates.

## Editing Guidance

- Keep changes narrow. This is a content-heavy personal site, so avoid broad rewrites unless explicitly requested.
- Do not modify generated or vendor-like assets such as `static/js/prism.js`, `static/js/two.min.js`, or Prism CSS unless the task is specifically about those assets.
- For route changes, update `app/entry.lua` and the matching responder/template files together.
- For template changes, inspect `templates/base.html` first because most pages extend it.
- For visual changes, check both light and dark color-scheme behavior because `templates/base.html` defines theme variables and Prism CSS is split by media query.
- There is no test suite in this repo currently. Validate by running the app when possible and manually checking affected routes.

## Verification Checklist

- For Lua or routing changes, start the app with `make local` or Docker and request the affected route.
- For content changes, confirm required frontmatter is present and the route uses the intended slug.
- For template or CSS changes, check the home page, a blog entry, and an Understand Django chapter.
- For documentation-only changes, review the rendered Markdown structure and keep docs consistent with the current Makefile and Dockerfile.
