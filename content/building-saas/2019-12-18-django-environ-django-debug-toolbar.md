---
title: "django-environ and django-debug-toolbar - Building SaaS #39"
description: >-
  In this episode,
  we set up a couple of tools that will be at the base of development.
  The first tool was django-environ to control Django settings
  from environment variables.
  The second tool was the django-debug-toolbar to help with debugging pages
  in future work.
type: video
image: img/2019/environ.jpg
video: https://www.youtube.com/embed/_KJnLWXqgbQ
aliases:
 - /building-saas/39
categories:
 - Twitch
 - Python
 - Django
tags:
 - Django
 - django-environ
 - django-debug-toolbar

---

In this episode,
we set up a couple of tools that will be at the base of development.
The first tool was django-environ to control Django settings
from environment variables.
The second tool was the django-debug-toolbar to help with debugging pages
in future work.

We started the stream with an upgrade
to Django 3.0.1
because of a security release
that was announced today.
For a new project,
I don't recommend upgrading packages all the time,
but security releases are my exception to that rule.

After that,
we installed {{< extlink "https://django-environ.readthedocs.io/en/latest/" "django-environ" >}}
in `requirements.in`.

```text
django-environ==0.4.5
```

Then installed it
into the virtual environment.

```bash
(venv) $ pip-compile --output-file=requirements.txt requirements.in
(venv) $ pip install -r requirements.txt
```

django-environ lets us control settings
from environment variables.
We'll use it much more
in the future,
but, for this stream,
I wanted to control the `DEBUG` and `SECRET_KEY` settings
to help secure the Heroku deployment.

In the project's `settings.py` file,
we added:

```python
import environ

# <snip other settings>

env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)

# <snip>

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
```

Because the `env` object received a default `DEBUG`,
that environment variable is optional.
By declaring `SECRET_KEY` without a default,
the application will fail
if the `SECRET_KEY` environment variable is not defined.

We're using django-environ
because Heroku works
by communicating settings and secrets
(set via the Heroku dashboard)
as environment variables available
to the Heroku dyno
that runs the app.

The process of adding this tool showed a couple
of things:

1. To use an `.env` file
    at the project root,
    we needed to explicitly provide the path.
    Without the path,
    it attempted to find an `.env` file
    within the project's package.
2. You can set the cast function
    to coerce an environment variable string
    into a data type of your choice.
    For instance `DEBUG=(bool, False)` tries to use the `bool` function
    to cast a string to a boolean value.
    What was surprising was that strings *don't* follow Python truthiness rules
    and only evaluate to `True`
    for {{< extlink "https://django-environ.readthedocs.io/en/latest/#environ.environ.Env.BOOLEAN_TRUE_STRINGS" "certain strings" >}}.

The second package that we installed in `requirements.in` was {{< extlink "https://django-debug-toolbar.readthedocs.io/en/stable/index.html" "django-debug-toolbar" >}}.

```text
django-debug-toolbar==2.1
```

The debug toolbar is a useful tool
for analyzing aspects
of a Django view
(like templates used, context, or database queries).

We configured the toolbar
so that it will only appear in debug mode.
To be clear,
I didn't intuit how to do this.
We followed the {{< extlink "https://django-debug-toolbar.readthedocs.io/en/stable/installation.html" "installation documentation" >}}.

In `settings.py`:

```python
# Enable the debug toolbar only in DEBUG mode.
if DEBUG and DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]
```

and in `urls.py`:

```python
# Enable the debug toolbar only in DEBUG mode.
if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] \
                + urlpatterns
```

We also took the step to make the toolbar configurable
with a `DEBUG_TOOLBAR` setting
because I noticed some poor performance
on some requests coming from Gunicorn,
and I didn't want to dig into the core problem.

To cap off the night,
I deployed to Heroku again
to show how the new settings were required
as environment variables.

I generated a new secret key using the tools
that come with Django.

```python
>>> from django.core.management import utils
>>> utils.get_random_secret_key()
'3dg^)!ijawvq_%#c^6pav)#kpn4jc4t$7lgzb@=75$c+5+6r2q'  # This is an example!
```

Now that we have some basic tooling in place,
the next stream will focus
on adding accounts
with {{< extlink "https://django-allauth.readthedocs.io/en/latest/" "django-allauth" >}}.
