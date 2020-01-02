---
title: "Make A Custom User Model - Building SaaS #40"
description: >-
    In this episode,
    we started a users app and hook up the custom user model feature of Django
    to unlock the full extensibility of that model in the future.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/I2pG21ol_KU
aliases:
 - /building-saas/40
categories:
 - Twitch
 - Python
 - Django
tags:
 - Django
 - auth

---

In this episode,
we started a users app and hook up the custom user model feature of Django
to unlock the full extensibility of that model in the future.
The stream was cut short this week because of some crashing issues
in the OBS streaming software.

The goal of the episode was to add
{{< extlink "https://django-allauth.readthedocs.io/en/latest/" "django-allauth" >}}
so that users can sign into the service
with an email and password
instead of the default username and password combination.
We're using {{< extlink "https://wsvincent.com/django-login-with-email-not-username/" "Will Vincent's guide" >}}
on this topic
as an aide
for this implementation (thanks Will!).

django-allauth makes it possible
to add a variety of authentication options
like Google or Facebook sign in.
My app is not using those modes,
but it is taking advantage
of the "email as username" feature
that the package can provide.

Before getting to the django-allauth integration,
we first needed to create a custom `User` model.
This isn't strictly necessary,
but it unlocks a lot of future potential
and is a hard change to make later
in a project.

I started with the creation
of a new Django app
for the `User` model to reside in.

```bash
(venv) $ python manage.py startapp users
```

From there,
I discussed some code organization ideas
and explained why I'm making the choice
to put all of my app code into a single, top-level package
called `homeschool`.
It's mostly a personal preference issue,
but I did talk through some justification
for my decision.

```bash
(venv) $ mkdir homeschool
(venv) $ touch homeschool/__init__.py
(venv) $ mv users homeschool
```

With the app
in the location I wanted,
we put in the list
of installed applications
in the settings.

```python
# project/settings.py

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "homeschool.users",
]
```

Next,
we needed to create the model
and set it
in the settings.

```python
# homeschool/users/models.py
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """A custom user for extension"""

# project/settings.py
AUTH_USER_MODEL = "users.User"
```

Finally,
we generate the migration
to make use of the setup.

```bash
(venv) $ python manage.py makemigrations
(venv) $ python manage.py migrate
```

Unfortunately,
that's where the stream ended
for the night.
My recent upgrade to macOS Catalina
was not playing nicely
with the OBS streaming software
and OBS crashed **hard**.
Interestingly,
I was able to get OBS
to crash
every time I tried to log in
to the Django admin in Firefox.
It was super weird.

Next time,
we will continue to work through the django-allauth addition
with a (hopefully) more stable streaming setup.
