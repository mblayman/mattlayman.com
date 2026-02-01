---
title: "Middleware Do You Go?"
description: >-
    The topic for this Understand Django article
    is middleware.
    We'll see what middleware is,
    what it is used for
    in a Django project,
    and how to write your own.
image: /static/img/django.png
slug: middleware-do-you-go
date: 2020-12-16
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - middleware
series: "Understand Django"

---

In the previous
[Understand Django](/understand-django/about)
article,
we covered the built-in auth system.
That article gave you a chance
to see the `User` model,
ways to login users
with Django's authentication tools,
and the features
that make the authorization controls work.
In that topic,
middleware came up
as an integral component.
Now we're going to learn more
about middleware
and its function
within a Django project.

1. [From Browser To Django](/understand-django/browser-to-django)
2. [URLs Lead The Way](/understand-django/urls-lead-way)
3. [Views On Views](/understand-django/views-on-views)
4. [Templates For User Interfaces](/understand-django/templates-user-interfaces)
5. [User Interaction With Forms](/understand-django/user-interaction-forms)
6. [Store Data With Models](/understand-django/store-data-with-models)
7. [Administer All The Things](/understand-django/administer-all-the-things)
8. [Anatomy Of An Application](/understand-django/anatomy-of-an-application)
9. [User Authentication](/understand-django/user-authentication)
10. Middleware Do You Go?
11. [Serving Static Files](/understand-django/serving-static-files)
12. [Test Your Apps](/understand-django/test-your-apps)
13. [Deploy A Site Live](/understand-django/deploy-site-live)
14. [Per-visitor Data With Sessions](/understand-django/sessions)
15. [Making Sense Of Settings](/understand-django/settings)
16. [User File Use](/understand-django/media-files)
17. [Command Your App](/understand-django/command-apps)
18. [Go Fast With Django](/understand-django/go-fast)
19. [Security And Django](/understand-django/secure-apps)
20. [Debugging Tips And Techniques](/understand-django/debugging-tips-techniques)

## How Should I Think About Middleware?

To start this topic,
let's figure out
where middleware exists
in a Django project.

Middleware is code that exists
in the middle.
"In the middle of what?"
you might ask.
The "middle" is the code that executes between
when an `HttpRequest`
is created
by the framework
and when the code you wrote is called
by Django.
The "middle" can also refer
to code that executes
*after* your view completes
but before Django translates the `HttpResponse`
to bytes
to send it over the network
to a browser.

Have you ever eaten an Everlasting Gobstopper?
No,
I don't mean the one
from Willy Wonka
that will last forever.
An Everlasting Gobstopper is a hard, layered candy
that changes colors and flavors
as you keep it in your mouth
until you finally get to a soft center.

Middleware is kind of like those candy layers
and your view code is like the soft center.
My analogy breaks down when you think
about how someone eats the candy.

With the candy,
you experience one layer at a time
until you get to the middle
and you're done.
A more apt comparison to middleware would be
to burrow *through* the layers
and come out the other side,
experiencing the same layers
in the opposite order
as the way you came in.

What's shown below is a diagram
of all the default middleware
that is included
when you run the `startproject` command.
If you're a visual learner
who didn't find my gobstopper analogy helpful,
then I hope this picture will be more illustrative.

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
We will cover application servers in a later topic,
but, for now, know that an application server can run your Django app.
If your project directory containing your settings file
is called `project`,
then calling Gunicorn looks like:

```bash
$ gunicorn project.wsgi
```

You'd have this setup if you ran `django-admin startproject project .`
(including the last dot),
but what's really needed by the application server is wherever your `wsgi.py`
file is located in your project,
*in module path form*.
Adjust accordingly for your needs.

Remember way back
in the first article
of the series
that WSGI stands
for the Web Server Gateway Interface
and is the common layer
that synchronous Python web apps must implement
in order to work
with Python application servers.
Inside this `project.wsgi` module
is a function called `get_wsgi_application`,
imported from `django.core.wsgi`.

`get_wsgi_application` does two things:

* Calls `django.setup` which does all the startup configuration
    that we saw in the last article
* Returns a `WSGIHandler` instance

As you might guess,
the `WSGIHandler` is designed
to make the WSGI interface work,
but it is also a subclass
of `django.core.handlers.base.BaseHandler`.
This base handler class is where Django handles middleware setup.

The base handler includes a `load_middleware` method.
This method has the job
of iterating through all the middleware listed
in your `MIDDLEWARE` setting.
As it iterates through the `MIDDLEWARE`,
the method's primary objective is
to include each middleware
in the *middleware chain*.

> The middleware chain is the Django gobstopper.

The chain represents each instance of Django middleware,
layered together,
to produce the desired effect
of allowing a request and response
to pass through each middleware.

Aside from building the middleware chain,
`load_middleware` must do some other important configuration.

* The method handles synchronous and asynchronous middleware.
    As Django increases its support
    of async development,
    the internals of Django need to manage the differences.
    `load_middleware` makes some alterations
    depending on what it can discover about a middleware class.
* The method registers a middleware with certain *sets*
    of middleware
    based on the presence
    of various hook methods.
    We'll discuss those hooks later in this article.

That explains middleware's structure
and how all the middleware interacts
with the request and response lifecycle,
but what does middleware do?

We can use middleware
for a wide variety
of purposes.
Because of the middleware chain,
a successful HTTP request will pass
through every middleware.
This property of middleware makes it ideal
for code that we want to execute globally
for our Django project.

For instance,
think back to our last article
on
[User Authentication](/understand-django/user-authentication).
In that article,
we observed
that Django's auth system is dependent
on the `AuthenticationMiddleware`.
This middleware has the singular job
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

*Why?*
Again,
the answer is related
to the middleware chain.
Since the HTTP request will pass through every middleware
in the chain,
then we can see
that *every middleware will execute
for every request.*
In other words,
each middleware carries a performance overhead
for each request.

There **is** an exception to this behavior
of the chain.
A middleware early
in the chain
can prevent middleware later
in the chain
from running.

For example,
the `SecurityMiddleware` is first
in the default middleware chain
from a `startproject` generated project.
This middleware is designed to do some checks
to keep the application secure.
One check is to look for a secure connection
(i.e., a request using HTTPS)
if HTTPS is configured.
If a request comes to the application
and uses HTTP
instead of HTTPS,
the middleware can return an `HttpResponsePermanentRedirect`
that redirects to the same URL
with `https://`
and prevents the rest of the chain
from running.

Aside from this exceptional behavior
in middleware,
it's important
to remember that,
in most circumstances,
each middleware will run
for each request.
We should be aware
of that performance aspect
when creating our own middleware.

Now we're ready to learn
about how we can create our own middleware!

## How Can I Write My Own Custom Middleware?

Let's assume that you've found a good case
to create a middleware.
You need something that happens
with every request
and that functionality has a narrow goal.

You can begin
with an empty middleware definition.
In my example,
we're going to put the middleware
in a `middleware.py` file.

```python
# project/middleware.py
class AwesomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(
            request
        )
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

*That's it!*
This custom middleware doesn't do anything
except slow performance slightly
because it's an extra method call
on every request.
Since I put the middleware at the end
of the `MIDDLEWARE` list,
it will be the last middleware
to run before a view receives a request
and the first middleware
with the chance
to process a response.

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

Let's say we want our example middleware
to record some timing information.
We might update the code
to look like:

```python
# project/middleware.py
import logging
import time

logger = logging.getLogger(__name__)


class AwesomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        before_timestamp = time.time()
        logger.info(
            f"Tracking {before_timestamp}"
        )

        response = self.get_response(request)

        after_timestamp = time.time()
        delta = after_timestamp - before_timestamp
        logger.info(
            f"Tracking {after_timestamp} for a delta of {delta}"
        )

        return response
```

We still haven't covered logging yet,
but you can understand it
as recording messages
to some output source
like a file.

This example acts as a crude performance monitor.
If you wanted to measure the response time
of a view,
this middleware would do that.
The downside is that it wouldn't tell you *which* view is recorded.
Hey, give me a break,
this is a silly example! 🤪

Hopefully,
you're beginning
to see how middleware can be useful.
But wait!
There's more that middleware can do.

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

Returning to our silly example,
we can make it less silly
by using the `process_view` hook.
Let's see what we can do:

```python
# project/middleware.py
import logging
import time

logger = logging.getLogger(__name__)


class AwesomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        before_timestamp = time.time()
        logger.info(
            f"Tracking {before_timestamp}"
        )

        response = self.get_response(request)

        after_timestamp = time.time()
        delta = after_timestamp - before_timestamp
        logger.info(
            f"Tracking {after_timestamp} for a delta of {delta}"
        )

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        logger.info(
            f"Running {view_func.__name__} view"
        )
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

This middleware could still benefit
from a lot of polish,
but you can see how the hooks make it possible
for a middleware to have more advanced functionality.

As an example of the `process_exception` middleware,
consider a service
that collects and reports exceptions
to track the health
of your application.
There are many of these services
like
[Rollbar](https://rollbar.com/)
and
[Sentry](https://sentry.io/welcome/).
I happen to be a Rollbar user
so I'll comment
on that one.
You can see from the
[pyrollbar code](https://github.com/rollbar/pyrollbar/blob/8d116a374f2c54da886972f7da7c289e317bbd8a/rollbar/contrib/django/middleware.py#L268)
that the service sends exception information
from the `process_exception` hook
to Rollbar
via their `rollbar.report_exc_info` function.
Without middleware,
capturing and reporting exceptions would be *significantly* harder.

Want to learn more about hooks?
You can see all the details
about these hooks
in the [middleware documentation](https://docs.djangoproject.com/en/4.1/topics/http/middleware/#other-middleware-hooks).

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
in the [middleware reference](https://docs.djangoproject.com/en/4.1/ref/middleware/).
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

Remember,
middleware comes with a performance cost
so avoid the temptation
to stuff too much functionality
into the middleware chain.
As long as you're aware
of the tradeoffs,
middleware is a great tool
for your toolbelt.

## Summary

In this article,
we saw Django's middleware system.

We discussed:

* The mental model for considering middleware
* How to write your own middleware
* Some of the middleware classes that come with Django

Next time we'll dig into static files.
Static files are all the images,
JavaScript,
CSS,
or other file types
that your application serves, unmodified,
to a user.
We need to understand:

* How to configure static files
* The way to work with static files
* How to handle static files
    when deploying your site
    to the internet

If you have questions,
you can reach me online
on X
where I am
[@mblayman](https://x.com/mblayman).
&nbsp;
