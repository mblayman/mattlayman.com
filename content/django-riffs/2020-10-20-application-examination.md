---
title: "Episode 9 - Application Examination"
aliases:
 - /django-riffs/9
 - /djangoriffs/9
 - /django-riffs/9.
 - /djangoriffs/9.
description: >-
    On this episode,
    we will study the structure
    of a Django application.
    Applications are the core components
    that make up a Django project.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - applications

---

On this episode,
we will study the structure
of a Django application.
Applications are the core components
that make up a Django project.

Listen at {{< extlink "https://djangoriffs.com/episodes/application-examination" "djangoriffs.com" >}}.

## Last Episode

On the last episode,
we focused
on the built-in Django administrator's site.
We'll saw what it is,
how you can configure it,
and how you can customize it
to serve your needs.

## What Is An Application?

In Django parlance,
a "web application" is a Django *project*.
All of the pieces
that come together to make a website
are a project.
The primary components
within the project
are called *applications*.
In other words,
a Django project is built
from one or more Django applications.

> Your "web application" is a Django **project**
composed of one more Django **applications**.

## Application Structure

An application usually tries
to capture a core concept
within your system.
For this episode,
we will use movies
as the concept we want to model.

```bash
(venv) $ ./manage.py startapp movies
(venv) $ tree movies
movies
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

`admin.py`:
This file is where all your `ModelAdmin` classes live
to power how the movies app will appear
in the Django admin.

`apps.py`:
This file is for the `AppConfig`
of the application.
We will discuss the `AppConfig`
and how to use it
later in this article.

`migrations`:
This directory is where all database migrations are stored
for the application.
Any model changes for this app will generate a migration
and created a numbered migration file
in this directory.

`models.py`:
This file is the home
for all the Django `Model` classes
in the application.
The models represent all your database data.

`tests.py`:
This file is for automated tests.
We'll cover automated tests
in Django
in a future article.
For now,
you can know that I *always* **delete** this file
and replace it with a `tests` package.
A `tests` package is superior
because you can split out to more focused files
like `test_models.py`
to know where the appropriate tests are.

`views.py`:
This file is where Django view functions or classes go.
Views are the glue code
that connect your URL routes
to your database models.

That's everything
that comes
with a generated app,
but what other files are missing
that you will commonly see
in a Django application?

`urls.py`:
This file is often used
to create routes
that logically group
all movie related functionality.
The `urls.py` file would power all the routes
in something
like `www.mysite.com/movies/`.

`forms.py`:
When you use Django `Form` classes
to interact with users,
this is the file
where forms are stored.

`templatetags`:
This directory is a Python package
that would include a module
like `movies_tags.py`
where you'd define any custom template tags
to use when rendering your templates.

`templates`:
This directory can store templates
that the application will render.
I personally prefer
using a project-wide `templates` directory,
but `templates` directories are commonly found,
especially for third party applications
that you may pull into your project.

`static`:
For static files
that you want to display
like images,
you can use the `static` directory.

`management`:
Users can extend Django
with custom commands
that can be called via `manage.py`.
Those commands are stored
in this package.

`locale`:
When doing translations and internationalization,
the translation files must have a home.
That's the purpose
of the `locale` directory.

`managers.py`:
This file is not always used,
but if your application has a lot
of custom managers,
then you may want
to separate them
from your models
in this file.

Here's what our final sample tree
would look like.

```bash
(venv) $ tree movies
movies
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── locale
│   └── es
│       └── LC_MESSAGES
│           ├── django.mo
│           └── django.po
├── management
│   ├── __init__.py
│   └── commands
│       ├── __init__.py
│       └── do_movie_stuff.py
├── managers.py
├── migrations
│   ├── 0001_initial.py
│   └── __init__.py
├── models.py
├── static
│   └── movies
│       └── moviereel.png
├── templates
│   └── movies
│       ├── index.html
│       └── movie_detail.html
├── templatestags
│   ├── __init__.py
│   └── movies_tags.py
├── tests
│   ├── __init__.py
│   ├── test_models.py
│   └── test_views.py
├── urls.py
└── views.py
```

## Loading applications

We've now seen
what's in a Django application
and have an idea
of an app's composition.
How does Django load applications?

Django does *not* do automatic discovery
of Django applications
within your project.
If you want Django
to include an app
in your project,
you *must* add the app
to your `INSTALLED_APPS` list
in the settings file.

When Django starts,
it will initialize the system
by doing the following:

* Load the settings
* Configure logging (a topic we'll explore in the future)
* Initialize an application registry
* Import each package from the `INSTALLED_APPS`
* Import a models module for each application
* Invoke the `ready` method of every `AppConfig` discovered

## Ecosystem Applications

An application is an important tool
for grouping the different logical components
in your project,
but apps also serve another purpose.
Apps are the basis
for most of the 3rd party extensions
in the Django ecosystem.

A big reason to use Django is
that the framework takes a "batteries included" approach.
Most of the tools
that you need to build a website are baked directly
into the framework.
This is a vastly different approach compared
to {{< extlink "https://flask.palletsprojects.com/en/1.1.x/" "Flask" >}}
which provides a relatively small API
and depends heavily
on third party libraries.

Even though Django includes most
of the major pieces
for a web application,
the framework doesn't include *everything*.
When you want to include more features,
Django apps fill in the gaps.

Apps are contained and reusable modules.
Because they have a fairly standard structure,
a project can integrate a new app quickly.
This means you can leverage the knowledge
and experience
(read: battle scars)
of other web developers.
The apps all play
by the same rules
so you,
as the developer,
spend less time gluing the app
into your project
and more time benefiting
from what it does.

All in all,
Django applications make working
with the Django ecosystem
a more enjoyable experience.

## Summary

On this episode,
we studied the structure
of a Django application.

We examined:

* The files and usage that exists within an application
* How an application loads when Django starts
* Why applications are important to the Django ecosystem

## Next Time

In the next episode,
we will dive into
the authentication system.
Django's built-in auth system comes
from a powerful Django application
that includes all the components you need
to manage users and their permissions
in your web app.

You can follow the show
on {{< extlink "https://djangoriffs.com" "djangoriffs.com" >}}.
Or follow me or the show
on Twitter
at
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}
or
{{< extlink "https://twitter.com/djangoriffs" "@djangoriffs" >}}.

Please rate or review
on Apple Podcasts, Spotify,
or from wherever you listen to podcasts.
Your rating will help others discover the podcast,
and I would be very grateful.

Django Riffs is supported by listeners like *you*.
If you can contribute financially
to cover hosting and production costs,
please check out my {{< extlink "https://www.patreon.com/mblayman" "Patreon page" >}}
to see how you can help out.
