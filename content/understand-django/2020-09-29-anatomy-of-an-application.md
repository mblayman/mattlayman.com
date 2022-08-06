---
title: "Anatomy Of An Application"
description: >-
    This article explores applications.
    Applications are core structural elements
    of a Django project.
    We will see the composition
    of an app
    and how to use them effectively.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - applications
series: "Understand Django"

---

{{< web >}}
In the previous
[Understand Django]({{< ref "/understand-django/_index.md" >}})
article,
we got deep
into the Django administrators site.
We saw what the site was
and how to configure and customize it.
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
we will examine what goes into an application.
Applications are core elements
of a Django project.

{{< understand-django-series "apps" >}}

## What Is An Application?

Before getting to what a Django application **is**,
we probably need to start with what it **is not**
because the terminology is confusing.
In the world of web development,
developers may call a website a "web application."

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

This situation is quite similar
to Python packages.
The software industry
often describes the software unit
as a "package."
We think
of `pip`,
`npm`,
or `apt`
as "package" managers.
This leads to a similar naming problem
because Python also calls any directory
with a `__init__.py` file a "package" as well.

In reality,
the code that you download
using pip is technically called a "{{< extlink "https://packaging.python.org/overview/" "distribution" >}}."
Even though we colloquially talk about Python downloads
from PyPI
as packages,
we're really talking about distributions,
and a distribution is a unit
that contains one or more Python packages.

Hopefully,
you now understand
the relationship
of applications
in Django.

> Your "web application" is a Django **project**
composed of one or more Django **applications**.

## Application Structure

Let's look at a fully loaded Django application
to see the fairly standard structure
that you will encounter
in Django projects.

An application usually tries
to capture a core concept
within your system.
{{< web >}}
For this article,
{{< /web >}}
{{< book >}}
For this chapter,
{{< /book >}}
we will use movies
as the concept we want to model.

Let's see what a default scaffold includes,
then build it up
with all the extras.

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
{{< web >}}
You can learn more about the admin
in [Administer All The Things]({{< ref "/understand-django/2020-08-26-administer-all-the-things.md" >}}).
{{< /web >}}

`apps.py`:
This file is for the `AppConfig`
of the application.
We will discuss the `AppConfig`
and how to use it
{{< web >}}
later in this article.
{{< /web >}}
{{< book >}}
later in this chapter.
{{< /book >}}

`migrations`:
This directory is where all database migrations are stored
for the application.
Any model changes for this app will generate a migration
and create a numbered migration file
in this directory.
{{< web >}}
More info about migrations is
in [Store Data With Models]({{< ref "/understand-django/2020-06-25-store-data-with-models.md" >}}).
{{< /web >}}

`models.py`:
This file is the home
for all the Django `Model` classes
in the application.
The models represent all your database data.
{{< web >}}
Learn more about models
in [Store Data With Models]({{< ref "/understand-django/2020-06-25-store-data-with-models.md" >}}).
{{< /web >}}

`tests.py`:
This file is for automated tests.
We'll cover automated tests
in Django
{{< web >}}
in a future article.
{{< /web >}}
{{< book >}}
in a future chapter.
{{< /book >}}
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
{{< web >}}
I wrote about views
in [Views On Views]({{< ref "/understand-django/2020-03-03-views-on-views.md" >}}).
{{< /web >}}

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
{{< web >}}
Information
on URLs is
in [URLs Lead The Way]({{< ref "/understand-django/2020-01-22-urls-lead-way.md" >}}).
{{< /web >}}

`forms.py`:
When you use Django `Form` classes
to interact with users,
this is the file
where forms are stored.
{{< web >}}
You can discover more on forms
in [User Interaction With Forms]({{< ref "/understand-django/2020-05-05-user-interaction-forms.md" >}}).
{{< /web >}}

`templatetags`:
This directory is a Python package
that would include a module
like `movies_tags.py`
where you'd define any custom template tags
to use when rendering your templates.
{{< web >}}
Custom tags are a topic
in [Templates For User Interfaces]({{< ref "/understand-django/2020-04-02-templates-user-interfaces.md" >}}).
{{< /web >}}

`templates`:
This directory can store templates
that the application will render.
I personally prefer
using a project-wide `templates` directory
as discussed
{{< web >}}
in [Templates For User Interfaces]({{< ref "/understand-django/2020-04-02-templates-user-interfaces.md" >}}),
{{< /web >}}
{{< book >}}
in the templates chapter,
{{< /book >}}
but `templates` directories are commonly found,
especially for third party applications
that you may pull into your project.

`static`:
For static files
that you want to display
like images,
you can use the `static` directory.
We'll discuss static files more
{{< web >}}
in a future article.
{{< /web >}}
{{< book >}}
in a future chapter.
{{< /book >}}

`management`:
Users can extend Django
with custom commands
that can be called via `manage.py`.
Those commands are stored
in this package.
Custom commands are a future topic
{{< web >}}
in this series.
{{< /web >}}
{{< book >}}
in this book.
{{< /book >}}

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
{{< web >}}
Managers are a topic
in [Store Data With Models]({{< ref "/understand-django/2020-06-25-store-data-with-models.md" >}}).
{{< /web >}}

Most applications will *not* have all
of these pieces,
but this should give you an idea
of what things are when you are exploring
Django apps in the wild
on your own.
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

This is a good example
of Django following the Python ethos
of favoring explicit
over implicit.
By being explicit,
your project is not in danger
of including apps
that you don't expect.
That might seem silly
for apps that you write yourself,
but you'll be thankful
that's the case when some third party package
in your virtual environment
happens to have a Django app
that you don't want
in your project.

On startup,
when an application is
in `INSTALLED_APPS`,
Django will look
for an `AppConfig` class.
This class is stored
in `apps.py`
from the `startapp` command
and contains metadata
about the application.

When Django starts,
it will initialize the system
by doing the following:

* Load the settings
* Configure logging (a topic we'll explore in the future)
* Initialize an application registry
* Import each package from the `INSTALLED_APPS`
* Import a models module for each application
* Invoke the `ready` method of every `AppConfig` discovered

The `ready` method is a useful hook
for taking action
at startup.
Since models are already loaded
by the time the method is called,
it's a safe place
to interact with Django.

If you attempt to run setup code
before Django is ready,
and you try to do something
like use the ORM
to interact with database data,
you'll probably get an `AppRegistryNotReady` exception.
Most apps won't directly need to run startup code,
but knowing about the `ready` hook
is a useful piece
of knowledge
to keep in your back pocket.

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

Before you go out to PyPI,
we need look no further
than the `django.contrib` package.
When you run the `startproject` command,
Django will include a variety
of built-in applications
that perform different functions.
If you don't need some of the functionality,
you can opt out
by removing the app
from your list
in `INSTALLED_APPS`.

I think this is the big difference
in philosophy
behind the framework.
Some developers like starting
from an extremely minimal kernel
of functionality
and build it up
based on their needs.
Django's philosophy seems to be
that you start
with an opinionated baseline
and pare down what you don't require.

From my point of view,
I think the Django philosophy is the right one
(shocking, isn't it!? 🤪).
The benefit of the Django philosophy is
that you leverage the knowledge
of people who have built web apps
for a very long time.
Not only do you leverage that knowledge,
you benefit from the polishing
applied by the Django developers
to integrate the different major systems
into a consistent whole.
What you're left with is a framework
that feels like it belongs together,
and I think that is a positive impact
on your productivity.

When you build from a minimal kernel
and work up,
you depend on knowing everything
that's required to put something
on the web.
That means that you know all the pieces
and how to bolt them together.
But most people *don't* know all the pieces
(because there are so many!).

If you start minimally
and don't know the pieces,
you'll learn along the way,
but what happens when you encounter a new concept
that doesn't fit
into your original mental model?
For instance,
security is a critical part
that can destroy your mental model
when you learn
of a class of vulnerabilities
that can restrict what is possible
to do safely.
When you follow this building from scratch approach,
I think the final result will naturally be your own custom framework.
If that's your thing, awesome.
Go for it.
For me,
I want a framework
that is a commodity
and commonly understood
by many people.

Ok, so, what does this have to do with Django apps?
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

I think this standard structure also makes it easier
to experiment
with new apps.
When I need some new functionality,
I will often check
{{< extlink "https://djangopackages.org/" "Django Packages" >}}
to look
for apps
that could meet my needs.
In my experience,
adding a new app is,
in many cases,
little more
than installing the package,
adding the app
to the `INSTALLED_APPS` list,
and putting an `include`
in my `urls.py` file.
Some packages require more configuration
than that,
but I think
that the integration cost is low enough
for me to experiment rapidly
and back out my decision
if I discover
that an app won't do
what I need.

All in all,
Django applications make working
with the Django ecosystem
a more enjoyable experience.

## Summary

{{< web >}}
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
we studied
Django applications.

We saw:

* What a Django application is
* How a Django application is structured
* How the Django ecosystem benefits
    from a common format
    that creates reusable components

{{< web >}}
Next time we will look into authentication
{{< /web >}}
{{< book >}}
Next, we will look into authentication
{{< /book >}}
in Django.
We will study:

* How users are created and managed
* How to deal with permissions for users
* How to work with users in your views and templates

{{< web >}}
If you'd like to follow along
with the series,
please feel free to sign up
for my newsletter
where I announce all of my new content.
If you have other questions,
you can reach me online
on Twitter
where I am
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
{{< /web >}}
