---
title: "Episode 15 - User Session Data"
aliases:
 - /django-riffs/15
 - /djangoriffs/15
 - /django-riffs/15.
 - /djangoriffs/15.
description: >-
    On this episode,
    we will dig
    into a data storage technique
    that Django makes heavy use of
    for visitors
    to your site.
    This category of data is called *session* data.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - sessions
nofluidvids: true

---

On this episode,
we will dig
into a data storage technique
that Django makes heavy use of
for visitors
to your site.
This category of data is called *session* data.

Listen at {{< extlink "https://open.spotify.com/episode/6lUub9mrEKOJDnvpYqqAop" "Spotify" >}}.

## Last Episode

On the last episode episode,
we looked
at what it takes
to go live
and how to prepare your Django project
for the internet.

## What Is A Session?

> A session is a set of data
that is available to users
that Django can use over multiple requests.

From a development perspective,
the data is different
from the regular data
that you would store in a database
with Django models.
When working with session data,
you don't query the database
using the ORM.
Instead,
you can access session content
via the `request.session` attribute.

```python
# application/views.py

from django.http import HttpResponse

def a_session_view(request):
    request.session['data_to_keep'] = 'store this'
    return HttpReponse('')
```

### The "What is JSON?" Sidebar

JSON is a data format.
JSON is a way of describing data
so that the data can be stored
or transmitted.
The definition of that format is listed
on the official {{< extlink "https://www.json.org/json-en.html" "JSON website" >}}
and can be understood
in probably 10 minutes or less.

The Python standard library includes a module
for working with JSON data.
Here's an example to give you an idea
of what JSON output looks like.

```python
>>> import json
>>> data = {'hello': 'world'}
>>> json.dumps(data)
'{"hello": "world"}'
>>> json_string = json.dumps(data)
>>> parsed_data = json.loads(json_string)
>>> parsed_data
{'hello': 'world'}
>>> data == parsed_data
True
```

JSON is an extremely versatile format
and is used all over the internet.
Getting back to sessions,
JSON is a good fit
because there are multiple places
where Django can store session data.
Let's look at those next.

## Session Storage

When you start a new Django project
with the `startproject` command,
the session engine will be set
to `django.contrib.sessions.backends.db`.
This is because the `SESSION_ENGINE` setting will be unset
in your settings module,
and Django will fall back to the default.

With this engine,
Django will store session data
in the database.
Because `startproject` includes the `django.contrib.sessions` app
in `INSTALLED_APPS`,
you'd probably see the following stream by
when you migrate your database
for the first time.

```text
(venv) $ ./manage.py migrate
  ...
Running migrations:
  ...
  Applying sessions.0001_initial... OK
```

The `Session` model stores three things:

* A session key that uniquely identifies the session
  in the storage engine
* The actual session data,
  stored in JSON format,
  in a `TextField`
* An expiration date for the session data

Why is the session engine configurable?
Django's session storage is configurable
to manage tradeoffs.
The default storage of a database engine
is a safe default
and the easiest to understand.
The answer to "Where is my app's session data?"
is "In the database with all of my other application data."

This is where other storage engines might be better
for your application.
One method to improve performance is
to switch to an engine
that uses caching.
If you have set up the caching system
with a technology
like {{< extlink "https://redis.io/" "Redis" >}}
or {{< extlink "https://memcached.org/" "Memcached" >}},
then a lot of session load
on the database
can be pushed to the cache service.
Caching is a topic we will explore more
in a future article,
so if this doesn't make too much sense right now,
I apologize for referencing concepts
that I haven't introduced yet.
For the time being,
understand that caching can improve session performance.

Another session storage engine
that can remove load
from a database
uses the browser's cookie system.
This system will certainly remove database load
because the state will stored
with the browser,
but this strategy comes
with its own set
of tradeoffs.
With cookie-base storage:

* The storage could be cleared at any time
  by the user.
* The storage engine is limited to a small amount
  of data storage
  by the browser,
  based on the maximum allowed size
  of a cookie
  (commonly, only 4kB).

## How Does The Session System Identify Visitors?

When a visitor comes to your site,
Django needs to associate the session data
to the visitor.
To do this association,
Django will store a session identifier
in a cookie
on the user's browser.

On the first visit,
the session storage engine will look
for a cookie
with the name `sessionid` (by default).
If the application doesn't find that cookie,
then the session storage will generate a random ID
and ensure that the random ID doesn't conflict
with any other session IDs
that already exist.

From there, the storage engine will store some session data
via whatever mechanism that engine uses
(e.g., the database engine will create a new session row
in the table).

The session ID is added
to the user's browser cookies
for your site's domain.
Cookies are stored in a secured manner
so only that browser will have access
to that randomly generated value.
The session ID is very long (32 characters),
and the session will expire after a given length of time.
These characteristics make session IDs quite secure.

## What Uses Sessions?

Sessions can store all kinds of data,
but what are some real world use cases?
You can look
in Django's source code
to find some immediate answers!

If you look into the session data
after you've authenticated,
you'll find three pieces of information:

* The user's ID (stored in `_auth_user_id`)
* The user's hash (stored in `_auth_user_hash`)
* The string name of the auth backend used 
  (stored in `_auth_user_backend`)

The auth system will read which backend is used
and load that backend if possible.
The backend is used to load the specific user record
from the ID found
in the session.
Finally,
that user is used to check
if the hash provided validates
when compared to the user's hashed password
(there is some extra hashing involved
to ensure that the user's password hash is not stored directly
in the session).
If the comparison checks out,
the user is authenticated
and the request proceeds as an authenticated request.

As a final example,
we can look
at the `messages` application.
The `messages` app can store "flash" messages.
A flash messages is the kind
of message
that you'd expect to see
on a single page view.
For instance,
if you have a message
that you'd like to display
to a user upon some action,
you might use a flash message.
Perhaps your application has some "Contact Us" form
to receive customer feedback.
After the customer submits the form,
you might want the application
to flash "Thank you for the feedback!"

```python
# application/views.py

from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy

from .forms import ContactForm

class ContactView(FormView):
    form_class = ContactForm
    success_url = reverse_lazy("application:index")

    def form_valid(self, form):
        messages.info(self.request, "Thank you for the feedback!")
        return super().form_valid(form)
```

In the default setup,
Django will attempt to store the flash message
in the request's cookies,
but, as we saw earlier,
browsers constrain the maximum cookie size.
If the flash messages will not fit in the request's cookies,
then the `messages` app will switch
to the session as a more robust alternative.
Observe that this might run into problems
if you are using the session's cookie storage engine!

## Summary

In this episode,
we learned session data
and its use.
We covered:

* What sessions are and the interface they expose as `request.session`
* How JSON is used to manage session data
* Different kinds of session storage
    that are available to your site
* The way that Django recognizes a user's session in the browser
* Examples within `django.contrib`
    of how sessions get used by Django's built-in apps.

## Next Time

On the next episode,
we are going to spend time focusing
on settings in Django.
Settings are how you control your Django app,
and there are a variety of techniques
that make settings more manageable.

You can follow the show
on {{< extlink "https://open.spotify.com/show/1RtdveQIz5m5MqLKPWbhnD" "Spotify" >}}.
Or follow me or the show
on X
at
{{< extlink "https://x.com/mblayman" "@mblayman" >}}
or
{{< extlink "https://x.com/djangoriffs" "@djangoriffs" >}}.

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
