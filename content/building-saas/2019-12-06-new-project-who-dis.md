---
title: "New Project, Who Dis? - Building SaaS #38"
description: >-
  In this episode,
  we started a brand new project!
  I had some internet troubles so this "stream" is actually a local recording
  from my computer.
  We created a new Django project from scratch
  and set up Heroku to handle deployments.
type: video
image: img/2019/heroku.png
video: https://www.youtube.com/embed/0RV11k2lkFs
aliases:
 - /building-saas/38
categories:
 - Twitch
 - Python
 - Django
tags:
 - Django
 - Heroku

---

In this episode,
we started a brand new project!
I had some internet troubles so this "stream" is actually a local recording
from my computer.
We created a new Django project from scratch
and set up Heroku to handle deployments.

In spite of the streaming trouble,
we were able to get a bunch done.
We started the project from scratch
so we made a repository
on GitHub
with some `.gitignore` settings tailored
for Python projects.

The first step in the process was to get a tool
to help manage packages.
I chose {{< extlink "https://github.com/jazzband/pip-tools" "pip-tools" >}}
to make this process easier.
After creating a virtual environment with:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

I added `pip-tools` to a `requirements-dev.txt` file
and installed it.

```bash
(venv) $ pip install -r requirements-dev.txt
```

Then we put Django into `requirements.in`
(with Django 3.0, yay!)
and let `pip-tools` generate our `requirements.txt` file.

```bash
(venv) $ pip-compile --output-file requirements.txt requirements.in
```

Finally, we installed Django.

```bash
(venv) $ pip install -r requirements.txt
```

This process might seem roundabout,
but it will ensure that we have exactly the packages we expect
as we make future updates.

I took some time to explain some naming conventions
and places where we have choice in the structure
of our projects.
Ultimately, I picked the name of `project`
to store my settings and WSGI files.
To do that, I used `django-admin`.

```bash
(venv) $ django-admin startproject project .
```

*Note the period at the end of that command! It's important.*

The next step was to fire up the site
and check it out.

```bash
(venv) $ ./manage.py runserver
```

Not much there yet,
but it was a start.
I added all of this to source control
as a checkpoint
before we moved on.

For this project,
I'm using {{< extlink "https://www.heroku.com/" "Heroku" >}}
as a Platform as a Service (PaaS)
to host my application.
Prior to the stream,
I followed the Heroku tutorial
and set up the command line tools.

To try to run Django
locally with Heroku's tools,
I ran:

```bash
(venv) $ heroku local
```

This failed because the project was missing a `Profile`.
So, we created a `Profile`
to run the app
with this line
(and added an installation
of {{< extlink "https://gunicorn.org/" "gunicorn" >}}
into our virtual environment).

```Procfile
web: gunicorn project.wsgi --log-file -
```

Now `heroku local` would start,
but we immediately hit an error
because of the `http://0.0.0.0:5000` URL
(which is the default
for gunicorn).
The failure is that the gunicorn default URL
is not in the `ALLOWED_HOSTS` setting.

Instead of changing `ALLOWED_HOSTS`,
I installed the `django-heroku` package
and added the following to the settings file.

```python
import django_heroku
django_heroku.settings(locals())
```

This amount of work tweaks the settings
to make Django cooperate
with Heroku better.
We then verified that `heroku local` worked
and were ready to deploy online.

Deploying an app to Heroku
for the first time is done in two command.
Two commands!
*That's amazing!*

```bash
(venv) $ heroku create
(venv) $ git push heroku master
```

The final result made it to Heroku
on a randomly assigned domain name.
We successfully deployed an awesome web framework
on the internet
in under an hour
(with me explaining everything along the way).

That's great progress,
but there is a lot of work left to do
to make the site ready
for general use!
On the next stream,
we'll add `django-allauth`
to make it painless
for users to sign up on the site.
