---
title: "Episode 11 - Here, There, Middleware"
aliases:
 - /django-riffs/11
 - /djangoriffs/11
 - /django-riffs/11.
 - /djangoriffs/11.
description: >-
    On this episode,
    we will investigate Django middleware
    and see where it goes in your project.
    In the process,
    you'll see why middleware is useful
    and how you can work with it.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - middleware

---

On this episode,
we will investigate Django middleware
and see where it goes in your project.
In the process,
you'll see why middleware is useful
and how you can work with it.

Listen at {{< extlink "https://djangoriffs.com/episodes/here-there-middleware" "djangoriffs.com" >}}.

## Last Episode

On the last episode,
we're going to look
at working with users
in a Django project.
We'll see Django's tools
for identifying users
and checking what those users are permitted
to do
on your website.

## How Should I Think About Middleware?

Middleware is code that exists
in the middle.
"In the middle of what?"
you might ask.
The "middle" is the code between
when an `HttpRequest`
is created
by the framework
to the time
where your view code is called
by Django.
The "middle" can also refer
to the time
*after* your view completes
but before the `HttpResponse`
is translated to bytes
by Django
to send over the network
to a browser.

What's shown below is a diagram
of all the default middleware
that is included
when you run the `startproject` command.

```text
               +--------- SecurityMiddleware --------------+
               |+-------- SessionMiddleware --------------+|
               ||+------- CommonMiddleware --------------+||
               |||+------ CsrfViewMiddleware -----------+|||
               ||||+----- AuthenticationMiddleware ----+||||
               |||||+---- MessageMiddleware ----------+|||||
               ||||||+--- XFrameOptionsMiddleware ---+||||||
               |||||||                               |||||||
HttpRequest =================> view function ==================> HttpResponse
               |||||||                               |||||||
```

How does Django make this layering work?
When you start Django
with an application server
like Gunicorn,
you have to give the application server the path
to your WSGI module.
If your project directory containing your settings file
is called `project`,
then calling Gunicorn looks like:

```bash
$ gunicorn project.wsgi
```

Remember way back
in the first episode
that WSGI stands
for the Web Server Gateway Interface
and is the common layer
that synchronous Python web apps must implement
in order to work
with Python application servers.
Inside this `project.wsgi` module
is a function called `get_wsgi_application`.

`get_wsgi_application` does two things:

* Calls `django.setup` which does all the startup configuration
    that we saw in the last article
* Returns a `WSGIHandler` instance

The base handler includes a `load_middleware` method.
This method has the job
of iterating through all the middleware listed
in your `MIDDLEWARE` setting.
As it iterates through the `MIDDLEWARE`,
the method's primary objective is
to include each middleware
in the *middleware chain*.

The chain represents each instance of Django middleware,
layered together,
to produce the desired effect
of allowing a request and response
to pass through each middleware.

Aside from building the middleware chain,
`load_middleware` must do some other important configuration.

* The method handles synchronous and asynchronous middleware.
    As Django increases its support
    of async development (a future topic in this series),
    the internals of Django need to manage the differences.
    `load_middleware` makes some alterations
    depending on what it can discover about a middleware class.
* The method registers a middleware with certain *sets*
    of middleware
    based on the presence
    of various hook methods.
    We'll discuss those hooks later in this article.

`AuthenticationMiddleware` has the singular job
of adding a `user` property
to every `HttpRequest` object
that passes through the application
before the request gets
to view code.

The `AuthenticationMiddleware` highlights some qualities
that are good for middleware
in Django.

* A middleware should ideally have a narrow or singular objective.
* A middleware should run a minimal amount of code.

## How Can I Write My Own Custom Middleware?

You can begin
with an empty middleware definition.
In my example,
we're going to put the middleware
in a `middleware.py` file.

```python
class AwesomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
```

After creating the middleware,
you add it to your settings.

```python
# project/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    ...,
    'middleware.AwesomeMiddleware',
]
```

We can break down how this class works.

* The `__init__` method gets a callable
    that is conventionally named `get_response`.
    The middleware is created during `load_middleware`
    and the callable is a key part
    of what makes the middleware chain work.
    The callable will either call the next middleware
    or the view
    depending on where the current middleware is
    in the chain.
* The `__call__` method transforms the middleware instance itself
    into a callable.
    The method must call `get_response`
    to ensure that the chain is unbroken.

If you want to do extra work,
you can make changes
to the `__call__` method.
You can modify `__call__`
to process changes
before or after the call
of `get_response`.
In the request/response lifecycle,
changes before `get_response`
occur before the view is called
while changes after `get_response`
can handle the `response` itself
or any other post-request processing.

```python
import logging
import time

logger = logging.getLogger(__name__)


class AwesomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        before_timestamp = time.time()
        logger.info(f"Tracking {before_timestamp}")

        response = self.get_response(request)

        after_timestamp = time.time()
        delta = after_timestamp - before_timestamp
        logger.info(f"Tracking {after_timestamp} for a delta of {delta}")

        return response
```

A Django middleware can define any
of three different hook methods
that Django will run
at different parts of the request/response lifecycle.
The three methods are:

* `process_exception` - This hook is called
    whenever a view raises an exception.
    This could include an uncaught exception
    from the view,
    but the hook will also receive exceptions
    that are intentionally raised
    like `Http404`.
* `process_template_response` - This hook is called
    whenever a view returns a response
    that looks like a template response
    (i.e., the response object has a `render` method).
* `process_view` - This hook is called
    right before the view.

```python
import logging
import time

logger = logging.getLogger(__name__)


class AwesomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        before_timestamp = time.time()
        logger.info(f"Tracking {before_timestamp}")

        response = self.get_response(request)

        after_timestamp = time.time()
        delta = after_timestamp - before_timestamp
        logger.info(f"Tracking {after_timestamp} for a delta of {delta}")

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        logger.info(f"Running {view_func.__name__} view")
```

Now our middleware uses Python's reflection capabilities
to record the view's name.
If accessing the Django admin
with an unauthenticated user,
the log might record something like:

```text
Tracking 1607438038.232886
Running login view
Tracking 1607438038.261855 for a delta of 0.02896881103515625
```

Want to learn more about hooks?
You can see all the details
about these hooks
in the {{< extlink "https://docs.djangoproject.com/en/3.1/topics/http/middleware/#other-middleware-hooks" "middleware documentation" >}}.

## What Middleware Does Django Include?

We've looked at the mental model
for middleware
and all the details
of how an individual middleware works.
What middleware does Django include
in the framework?

The full list
of built-in middleware
is available
in the {{< extlink "https://docs.djangoproject.com/en/3.1/ref/middleware/" "middleware reference" >}}.
I'll describe what I think are the most common
or useful middleware classes
that Django includes.

* `AuthenticationMiddleware` - We've already encountered this middleware
    in the exploration of the auth system.
    The job of this middleware is
    to add the `user` attribute
    to an `HttpRequest` object.
    That one little `user` attribute powers many
    of the features of the auth system.
* `CommonMiddleware` - The common middleware is a bit of an oddball.
    This middleware handles a variety
    of Django settings
    to control certain aspects
    of your project.
    For instance,
    the `APPEND_SLASH` setting will redirect a request
    like `example.com/accounts`
    to `example.com/accounts/`.
    This setting only works
    if the `CommonMiddleware` is included.
* `CsrfViewMiddleware` - In the forms article,
    I mentioned the CSRF token.
    As a reminder,
    this is a security feature
    that helps protect your project against malicious sources
    that want to send bad data
    to your site.
    The `CsrfViewMiddleware` ensures
    that the CSRF token is present and valid
    on form submissions.
* `LocaleMiddleware` - This middleware is for handling translations
    if you choose to internationalize your project.
    We'll look into internationalization
    in a future article.
* `MessageMiddleware` - The message middleware is for "flash messages."
    These are one-time messages
    that you'd likely see
    after submitting a form,
    though they can be used
    in many places.
    We'll discuss messages more
    when we get to the sessions topic.
* `SecurityMiddleware` - The security middleware includes a number
    of checks
    to help keep your site secure.
    We saw the example of checking for HTTPS earlier
    in this article.
    This middleware also handles things like XSS, HSTS,
    and a bunch of other acronyms (😛)
    that will be seen
    with the future security topic.
* `SessionMiddleware` - The session middleware manages
    session state
    for a user.
    Sessions are crucial
    for many parts of Django
    like user auth.

As you can see
from this incomplete list,
Django's middleware can do a lot
to enrich your project
in a wide variety
of ways.
Middleware is an extremely powerful concept
for Django projects
and a great tool
to extend your application's request handling.

## Summary

In this episode,
we explored middleware.

That exposed you to:

* The mental model for considering middleware
* How to write your own middleware
* Some of the middleware classes that come with Django

## Next Time

On the next episode,
I'll chat about static files.
Static files are CSS, JavaScript, images, and the like.
We will look at how Django works
with those kinds of files
in your project.

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
