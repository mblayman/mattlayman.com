---
title: "Episode 2 - Enter With URLs"
aliases:
 - /django-riffs/2
 - /djangoriffs/2
 - /django-riffs/2.
 - /djangoriffs/2.
description: >-
    On this episode,
    we discuss Django's front door, URLs.
    We talk about what URLs are,
    how to build them in Django,
    and the functions Django provides
    to work with URLs.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - URLs

---

On this episode,
we discuss Django's front door, URLs.
We talk about what URLs are,
how to build them in Django,
and the functions Django provides
to work with URLs.

Listen at {{< extlink "https://open.spotify.com/episode/0k7fpDbuAEUp2I8Rnm3yep" "Spotify" >}}.

## What's a URL?

A URL is a Uniform Resource Locator.
It is the full address that goes into a browser.

Consider `https://www.mattlayman.com/django-riffs/`.
Here are the parts:

* Scheme, `https://`
* Domain name:
  * Top Level Domain (TLD), `com`
  * Domain, `mattlayman`
  * Subdomain, `www`
  * Path or route, `/django-riffs/`

## URLconf

Every route for Django to handle goes into a URL configuration,
URLconf for short and in the documentation.

* The main URLconf is defined by the `ROOT_URLCONF` settings.
* Set to the `project/urls.py` file by the `startproject` command.

What is a URLconf? A Python module with a special list in it.

Open the file and find `urlpatterns` list at module level scope.
This list is the rules that Django will follow
to route user's to your code.

* Each type of route will have a `path` rule in the list.
* Django will match from top to bottom.
* When matching, hand off to your code that you'll define in *views*.

Here's an example URLconf.

```python
# project/urls.py
from django.urls import path

from application import views

urlpatterns = [
    path("", views.home),
    path("about/", views.about),
]
```

* Empty route matches `/`.
* `about/` does a literal match to `example.com/about/`.
* Django URLs end with a slash as a design choice.
  This is controlled by the `APPEND_SLASH` setting.

## `path`

`path` is the key function for defining individual routes.
The first parameter is the route string.
Routes are more than strings only.
They can contain *converters*.
A converter looks like:

```python
    path("blog/<int:year>/", views.blog_by_year),
```

A converter's job is to extract information
from a URL.
This would pull out an integer
from `mattlayman.com/blog/2020/`
and provide a 2020 value
to the view code.

Order matters!
In the following code,
the first ordering will never call `blog_for_twenty_twenty`
because Django will stop as soon as it finds a match.

```python
    path("blog/<int:year>/", views.blog_by_year),
    path("blog/2020/", views.blog_for_twenty_twenty),

# vs.

    path("blog/2020/", views.blog_for_twenty_twenty),
    path("blog/<int:year>/", views.blog_by_year),
```

## View Basics

A view is code that takes an `HttpRequest` and returns an `HttpResponse`

```python
# application/views.py
from django.http import HttpResponse

def blog_by_year(request, year):
    # ... some code to handle the year
    return HttpResponse('some response')
```

This view function pairs with the converter example above.
The converter passes the extracted `year`
to the view.
Django did all the hard work
of parsing the year for us!

## `re_path`

More complicated URLs can be represented
with `re_path`
which gives the full power
of Python's *regular expression* engine.
Check out [URLs Lead The Way]({{< ref "/understand-django/2020-01-22-urls-lead-way.md" >}}) article
to learn more.

## Grouping

Django's tool for grouping is the `include` function.
Let's think about a website devoted to some fantasy adventure.

```python
# project/urls.py
from django.urls import path

from heroes import views as heroes_views

urlpatterns = [
    path("heroes/", heroes_views.index),
    path("heroes/<int:hero_id>/", heroes_views.hero_detail),
]
```

Project has to know the details of the views for `heroes`.
That's not cool.
Here's an alternate version
that uses `include`.

```python
# project/urls.py
from django.urls import include, path

urlpatterns = [
    path("heroes/", include("heroes.urls")),
]
```

```python
# heroes/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("<int:hero_id>/", views.hero_detail),
]
```

The URL configurations function like a tree.
Lower level configurations do not need to handle earlier parts
of the route.

## Naming

How can we reference URLs in code?
We could hardcode a `/heroes/` string.
What if we change to `/champions/`?
That could be a lot of editing.

Django lets us name URLs.
This is a layer of indirection.

```python
# heroes/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

To use this, we need a new tool, the `reverse` function.

```python
>>> from django.urls import reverse
>>> reverse("index") == "/heroes/"
True
```

## Namespacing

There's a problem with `index` as the name of the URL.
What if another view in a different app (like villains) also wanted to use the name `index`?
There's a conflict. Who wins? The name `index` becomes ambiguous.

How can we get around that?
We create a namespace!

```bash
$ python
>>> import this
The Zen of Python, by Tim Peters

...
Namespaces are one honking great idea -- let's do more of those!
```

We could do a manual namespace
by renaming to `heroes_index`.
Plenty of Django developers do this!

But Django gives us another tool.

```python
# heroes/urls.py
from django.urls import path

from . import views

app_name = "heroes"
urlpatterns = [
    path("", views.index, name="index"),
]
```

We added `app_name` to give the app a namespace.
We need a small tweak to how we use `reverse`.

```python
>>> from django.urls import reverse
>>> reverse("heroes:index") == "/heroes/"
True
```

## Next Time

In the next episode,
we'll look at views,
the different kinds of views,
and tools to help build them.

You can follow the show
on {{< extlink "https://open.spotify.com/show/1RtdveQIz5m5MqLKPWbhnD" "Spotify" >}}.
Or follow me or the show
on X
at
{{< extlink "https://x.com/mblayman" "@mblayman" >}}
or
{{< extlink "https://x.com/djangoriffs" "@djangoriffs" >}}.

Please rate or review
on iTunes, Spotify,
or from wherever you listen to podcasts.
Your rating will help others discover the podcast,
and I would be very grateful.

Django Riffs is supported by listeners like *you*.
If you can contribute financially
to cover hosting and production costs,
please check out my {{< extlink "https://www.patreon.com/mblayman" "Patreon page" >}}
to see how you can help out.
