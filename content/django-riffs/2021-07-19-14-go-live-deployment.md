---
title: "Episode 14 - Going Live"
aliases:
 - /django-riffs/14
 - /djangoriffs/14
 - /django-riffs/14.
 - /djangoriffs/14.
description: >-
    On this episode,
    we will look
    at what it takes
    to go live
    and how to prepare your Django project
    for the internet.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - deployment
nofluidvids: true

---

On this episode,
we will look
at what it takes
to go live
and how to prepare your Django project
for the internet.

Listen at {{< extlink "https://open.spotify.com/episode/5ZFl9yvSuiiIXVrpFdl38x" "Spotify" >}}.

## Last Episode

On the last episode,
we discussed how you can verify
that your site works
and continues to work.
We dug into automated testing
and how to write tests
for your Django apps.

## Pick A Python Application Server

When you begin to learn Django,
the documentation will instruct you
to use `./manage.py runserver`
to interact with your application locally.
`runserver` is a great tool
for getting started
because you can avoid extra software
from the outset
of your Django journey.

While great,
the `runserver` command is not designed
for handling a lot of web traffic.
`runserver` is explicitly intended
for a development-only setting.
Aside from a lack of performance tuning options,
the server doesn't receive the same security scrutiny
as other Python web application servers.

These factors add up
to make the `runserver` command unsuitable
for handling your live site.
What should you use instead?
When you read the {{< extlink "https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/" "deployment documentation" >}},
you'll find many possible Python web application servers listed.
Gunicorn, uWSGI, Apache with mod_wsgi, Daphne, Hypercorn, and Uvicorn
are all presented as available options.
That's way too much choice.

> Use {{< extlink "https://gunicorn.org/" "Gunicorn" >}}.

Gunicorn (which stands for "Green Unicorn") is a very simple web application server
to start using.
In my experience,
Gunicorn *stays* easy to use
and works for projects that receive a ton of traffic.
I've used some of the other options presented
for Django apps,
and few are as simple
to use as Gunicorn.

```bash
$ gunicorn project.wsgi
```

By default,
Gunicorn will only create a single worker process.
The Gunicorn documentation recommends picking a number
that is two to four times larger
than the number
of CPU cores available
to your machine.

The number of workers is a large determining factor
in how many requests
that your Django app can handle
at once.
The number of requests processed is usually called *traffic*
by web developers.
The idea of handling more traffic
by creating more processes (i.e., Gunicorn workers)
is called *horizontal scaling*.
In contrast,
*vertical scaling* handles more traffic
by using a better individual computer.
A faster processor with a single CPU can handle more requests.
When thinking about performance,
horizontal scaling is often a far easier approach.

```bash
$ gunicorn project.wsgi --workers 2 --log-file -
```

## Pick Your Cloud

Once you know which application server to use
and how to use it,
you need to run your code somewhere.
Again,
you can be paralyzed
by the sheer volume
of choices available to you.
AWS, GCP, Azure, Digital Ocean, Linode, Heroku, PythonAnywhere,
and so many other cloud vendors are out there
and able to run your application.

If you're getting started,
use a Platform as a Service (PaaS) option.
Specifically,
I think Heroku is a great platform
for applications.
A PaaS removes loads
of operational complexity
that you may be unequipped
to handle initially
if you're newer to web development.

Think you want to run your application
on a general cloud provider like AWS?
You can certainly do that,
but you'll potentially need to be prepared for:

* Setting up machines
* Getting TLS certificates for https
* Doing database backups
* Using configuration management tools to automate deployment
* And loads more!

Let's contrast this
with Heroku.
Because Heroku is a PaaS,
they deal with the vast majority
of the setup and coordination
of machines in their cloud.
Your experience as a developer primarily moves
to a single command:

```bash
$ git push heroku main
```

## Project Preconditions

Django has a few preconditions
that it expects
before running your application
in a live setting.
If you've listened to the previous episodes,
then you've actually heard most
of these preconditions by now,
but we'll group them together in this section
so you can see the complete picture.

One that we haven't discussed
is the `DJANGO_SETTINGS_MODULE` environment variable.
This is one critical element
to your application
because the variable signals
to your Django application
where the settings module is located.
If you have different settings modules
for different configurations
(e.g., a live site configuration versus a unit testing configuration),
then you may need to specify
which settings module
that Django should use when running.

The next important precondition
for your app is keeping your database
in sync using migrations.
As mentioned
in the models episode,
we make migrations
when making model changes.
These migrations generate instructions
for your relational database,
so that Django can match the database schema.

```bash
$ ./manage.py migrate
```

Heroku uses a `Procfile` to set
which machines and commands to run
so my `Procfile` looks like:

```yaml
release: python manage.py migrate
web: gunicorn project.wsgi --workers 2 --log-file -
```

Another precondition needed
for your app
is static files.
We saw in the static files episode
that Django looks
for static files
in a single directory
for performance reasons.
That requires running a command
to put those files
in the expected location.

```bash
$ ./manage.py collectstatic
```

## Protecting Your Site

Django includes a command
that provides a set
of instructive safety messages
for things that you should apply
to your site
that are important.
Thankfully,
ignoring these messages is unlikely
to affect your personal health,
but the messages are valuable
to help you combat the bad forces
that exist
on the public internet.

To view these important messages,
run:

```bash
$ ./manage.py check --deploy --fail-level WARNING
SystemCheckError: System check identified some issues:

WARNINGS:
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS
  setting. If your entire site is served only over SSL, you may want to
  consider setting a value and enabling HTTP Strict Transport Security.
  Be sure to read the documentation first; enabling HSTS carelessly can
  cause serious, irreversible problems.
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True.
  Unless your site should be available over both SSL and non-SSL connections,
  you may want to either set this setting True or configure a load balancer
  or reverse-proxy server to redirect all connections to HTTPS.
?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a
  secure-only session cookie makes it more difficult for network traffic
  sniffers to hijack user sessions.
?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware'
  in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True.
  Using a secure-only CSRF cookie makes it more difficult for network traffic
  sniffers to steal the CSRF token.
?: (security.W018) You should not have DEBUG set to True in deployment.
?: (security.W020) ALLOWED_HOSTS must not be empty in deployment.

System check identified 6 issues (0 silenced).
```

The items reported by the checklist are often about settings
that could be configured better.
These checks are created
by the {{< extlink "https://docs.djangoproject.com/en/3.1/topics/checks/" "System check framework" >}}
that comes with Django.

Some of these checks are too modest about their importance.
For instance, `security.W018` is the warning
that tells you that `DEBUG` is set to `True`
in the settings.
`DEBUG = True` is *TERRIBLE*
for a live site
since it can *trivially* leak loads of private data.

If HSTS is handled elsewhere,
you could set the `SILENCED_SYSTEM_CHECKS` setting
to tell Django
that you took care of it.

```python
# project/settings.py

SILENCED_SYSTEM_CHECKS = ["security.W004"]
```

## Prepare For Errors

Dealing with a live site brings a new set
of challenges.
Try as we might to consider every possible action
that our users do,
we'll never get them all.
There are lots
of ways
that a site can have errors
from things that we failed
to consider.
Since errors *will* happen
with a large enough product
and large enough customer base,
we need some plan to manage them.

We can consider a few strategies:

#### 1. Do nothing.

While I don't recommend this strategy,
you *could* wait for your customers
to report errors to you.
Some portion of customers might actually write to you
and report a problem,
but the vast majority won't.
What's worse is that some
of these customers may abandon your product
if the errors are bad enough or frequent enough.

> Using your customers to learn about errors makes for a poor user experience.

#### 2. Use error emails.

The Django deployment documentation highlights Django's ability
to send error information
to certain email addresses.
*I don't recommend this strategy either.*
Why?

* Setting up email properly can be a very tricky endeavor
    that involves far more configuration
    than you may realize.
    You may need email for your service,
    but setting it up for error info alone is overkill.
* The error emails can include Python tracebacks to provide context,
    but other tools can provide much richer context information
    (e.g., the browser used when a customer experiences an error).
* If you have a runaway error
    that happens constantly on your site,
    you can say "bye, bye"
    to your email inbox.
    A flood of emails is a quick way to get email accounts flagged
    and hurt the deliverability of email.

#### 3. Use an error tracking service.

Error tracking services are specifically designed
to collect context about errors,
aggregate common errors together,
and generally give you tools
to respond to your site's errors appropriately.

In the Django world,
I generally hear about two
of these error tracking services:
{{< extlink "https://rollbar.com/" "Rollbar" >}}
and {{< extlink "https://sentry.io/welcome/" "Sentry" >}}.
I've used both of these error trackers,
and I think they are both great.
For my personal projects,
I happen to pick Rollbar
by default,
so I'll describe
that service
in this section
as an example.

The flow for installing Rollbar is:

1. Create a Rollbar account on their site.
2. Install the `rollbar` package.
3. Set some settings in a `ROLLBAR` dictionary.

```python
# project/settings.py

ROLLBAR = {
    "enabled": env("ROLLBAR_ENABLED"),
    "access_token": env("ROLLBAR_ACCESS_TOKEN"),
    "environment": env("ROLLBAR_ENVIRONMENT"),
    "branch": "master",
    "root": BASE_DIR,
}
```

Once you set this up,
how can you tell that it's working?
Like a musician tapping a microphone
to see if it's working,
I like to add a view to my code
that let's me test
that my error tracking service is operational.

```python
# application/views.py

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def boom(request):
    """This is for checking error handling (like Rollbar)."""
    raise Exception("Is this thing on?")
```

With error tracking set up,
you'll be in a good position
to see errors when they happen
on your site.
In fact,
a great way to win the favor
of customers can be to fix errors proactively
and reach out to them.
Most people don't enjoy contacting support
and would be surprised and delighted
if you tell them
that you fixed their problem immediately.

## Summary

In this episode,
we learned the things
to consider when deploying a site
to the internet.
We examined:

* Deploying your application with a Python web application server
    (i.e., `./manage.py runserver` isn't meant for deployed apps)
* Running your app on a cloud vendor
* Deployment preconditions
    for managing settings, migrations, and static files
* A checklist to confirm that your settings are configured
    with the proper security guards
* Monitoring your application for errors

## Next Time

On the next episode,
we are going to look at session data.
Sessions are a way to keep a bit of data
for each visitor to your site.
We'll see why sessions are critical
to most Django apps
and what that data is used for.

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
