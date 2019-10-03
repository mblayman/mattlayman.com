---
title: "Bring in the WhiteNoise, Bring in Da Funk - Building SaaS #34"
description: >-
  In this episode,
  we added WhiteNoise to the app as a tool for handling static assets.
  This lets us move away from depending on Nginx
  for the task and gives shiny new features like Brotli support.
type: video
image: img/2019/white-noise.jpg
video: https://www.youtube.com/embed/P1rssIETizc
aliases:
 - /building-saas/34
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - WhiteNoise

---

In this episode,
we added WhiteNoise to the app as a tool for handling static assets.
This lets us move away from depending on Nginx
for the task and gives shiny new features like Brotli support.

We installed WhiteNoise
into the `requirements.in` file
and used `pip-tools`
to generate a new `requirements.txt`.

```text
whitenoise[brotli]==4.1.4
```

Once WhiteNoise was installed,
it needed two primary settings changes.

1. Add a new middleware.
2. Change the `STATICFILES_STORAGE`.

```python
MIDDLEWARE = [
    ...
    "whitenoise.middleware.WhiteNoiseMiddleware",
    ...
]

STATICFILES_STORAGE = \
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

This was enough to get WhiteNoise working.
We checked the local development server,
and the site continued to operate normally.

Unfortunately,
the configuration was not enough to make static assets work
with the Shiv app.
Since `STATIC_ROOT` used a relative value
of `static`,
Shiv couldn't find the static files.
This relative pathing was the same problem I faced
when getting the templates directory working
with the Shiv app.
We used the same solution
and switched to:

```python
import conductor

conductor_dir = os.path.dirname(conductor.__file__)
STATIC_ROOT = os.path.join(conductor_dir, "static")
```

Finally,
we needed to make the conductor package hold the collected static files.
We could do this by tweaking `MANIFEST.in`
with the following addition:

```text
recursive-include conductor/static *
```

On the next stream,
we'll make some CI changes
and update deployment
to discontinue use
of Nginx
for serving static files.
