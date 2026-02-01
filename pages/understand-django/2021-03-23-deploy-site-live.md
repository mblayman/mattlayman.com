---
title: "Deploy A Site Live"
description: >-
    You're ready to take the site you developed
    and share it with the world.
    What steps should you take
    to prepare your Django project
    for life on the web?
    That's the focus
    of this article.
image: /static/img/django.png
slug: deploy-site-live
date: 2021-03-23
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - deployment
series: "Understand Django"

---

In the previous
[Understand Django](/understand-django/about)
article,
we looked at automated testing
and how writing tests
to check your Django project
can be very valuable,
saving you time
and making sure your site works
for your users.
Next,
we're going to look into
how to share your site
on the internet
by understanding what it means
to *deploy* a Django project.
Deployment is the act
of making your application live
to your audience,
and this article explains the actions
you should consider
to deploy effectively.

1. [From Browser To Django](/understand-django/browser-to-django)
2. [URLs Lead The Way](/understand-django/urls-lead-way)
3. [Views On Views](/understand-django/views-on-views)
4. [Templates For User Interfaces](/understand-django/templates-user-interfaces)
5. [User Interaction With Forms](/understand-django/user-interaction-forms)
6. [Store Data With Models](/understand-django/store-data-with-models)
7. [Administer All The Things](/understand-django/administer-all-the-things)
8. [Anatomy Of An Application](/understand-django/anatomy-of-an-application)
9. [User Authentication](/understand-django/user-authentication)
10. [Middleware Do You Go?](/understand-django/middleware-do-you-go)
11. [Serving Static Files](/understand-django/serving-static-files)
12. [Test Your Apps](/understand-django/test-your-apps)
13. Deploy A Site Live
14. [Per-visitor Data With Sessions](/understand-django/sessions)
15. [Making Sense Of Settings](/understand-django/settings)
16. [User File Use](/understand-django/media-files)
17. [Command Your App](/understand-django/command-apps)
18. [Go Fast With Django](/understand-django/go-fast)
19. [Security And Django](/understand-django/secure-apps)
20. [Debugging Tips And Techniques](/understand-django/debugging-tips-techniques)

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
When you read the [deployment documentation](https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/),
you'll find many possible Python web application servers listed.
Gunicorn, uWSGI, Apache with mod_wsgi, Daphne, Hypercorn, and Uvicorn
are all presented as available options.
That's way too much choice.

> Use [Gunicorn](https://gunicorn.org/).

Gunicorn (which stands for "Green Unicorn") is a very simple web application server
to start using.
In my experience,
Gunicorn *stays* easy to use
and works for projects that receive a ton of traffic.
I've used some of the other options presented
for Django apps,
and few are as simple
to use as Gunicorn.

To use Gunicorn,
we need to point the `gunicorn` command
to the WSGI application
that Django projects have.
If you recall,
WSGI is the Web Server Gateway Interface.
WSGI is the protocol that permits Django apps
to talk to any of these web application servers.

If you ran the `startproject` command
and named your Django project as "project,"
the WSGI application should be in a file
like `project/wsgi.py`.
Gunicorn is aware that Django conventionally calls
the WSGI application in that module `application`,
so your only action is to point Gunicorn
to the module
with Python's dotted syntax.
Here's the most basic setup.

```bash
$ gunicorn project.wsgi
```

Gunicorn works by starting a main process
that will listen
for HTTP requests
on the local machine
at port 5000
by default.
As each request reaches the main process,
the request routes to an available worker process.
The worker process executes your Django app code
to provide the response data
to the user.

By default,
Gunicorn will only create a single worker process.
The Gunicorn documentation recommends picking a number
that is two to four times larger
than the number
of CPU cores available
to your machine.

The number of workers is a large determining factor
in how many requests
your Django app can handle
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

One of my projects
has a small amount of traffic
and runs on a single CPU
on its hosting provider.
In that scenario,
I use two workers
which looks like:

```bash
$ gunicorn project.wsgi --workers 2
```

The only other option you may require is an option
to handle where logging data goes.
I haven't covered logging in depth yet,
but recall from previous articles
that logging allows you to record information
about what your application is doing
while it's running.

Some hosting providers expect monitoring output
like logging
to go to stdout or stderr.
stdout stands for "standard output"
and stderr is "standard error."
stdout is where data appears
in your terminal
when you use `print`.
To tell Gunicorn to log
to stderr,
you can use a dash as the value
to the `log-file` option.
My full Gunicorn command looks like:

```bash
$ gunicorn project.wsgi \
    --workers 2 \
    --log-file -
```

A note about ASGI:
I am assuming that your use of Django will use WSGI
and its synchronous mode.
In recent years,
Django added support for asynchronous Python.
Asynchronous Python brings the promise
of higher performance
with the tradeoff of some implementation complexity.
For learning Django initially,
you don't need to understand asynchronous Python
and the Asynchronous Server Gateway Interface (ASGI).

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

You may be using Django to learn those skills.
If so,
that's awesome and good luck!
But if your primary goal is to get your application out
into the world,
then these tasks are a huge drag
on your productivity.

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

The Heroku instructions have you set up a Git remote.
That remote is the place you push your code to
and let Heroku handle the deployment
of your application.
Heroku manages this by cleverly detecting Django applications
and applying the correct commands.
We'll see some of those required commands
when looking at the preconditions.

To be really clear,
this is not an ad for Heroku.
I have personal experience with most of the cloud vendors
that I listed earlier
in this section.
I have found that a PaaS like Heroku is far and away an easier option
to apply for my own projects.
That's why I recommend the service so strongly.

## Project Preconditions

Django has a few preconditions
that it expects
before running your application
in a live setting.
If you've read the previous articles,
then you've actually seen most
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
Django should use when running.

In a future article,
we'll focus on how to manage your settings modules.
At that time,
you'll see how using some particular techniques diminish the need
for multiple modules.
For now,
keep in mind `DJANGO_SETTINGS_MODULE` for deployments,
and you should be good.

The next important precondition
for your app is keeping your database
in sync using migrations.
As mentioned
in the models article,
we make migrations
when making model changes.
These migrations generate instructions
for your relational database,
so that Django can match the database schema.

Without the migration system,
Django would be unable to communicate effectively
with the database.
Because of that,
you need to ensure
that you have applied all migrations
to your application
before running your app.

For whatever cloud you're using,
you need to make sure
that when you deploy,
your deployment scripts run:

```bash
$ ./manage.py migrate
```

For instance,
with my Heroku setup,
Heroku lets me define a "release" command
that they guarantee to run
before launching the new version
of the app.
Heroku uses a `Procfile` to set
which machines and commands to run
so my `Procfile` looks like:

```yaml
release: python manage.py migrate
web: gunicorn project.wsgi --workers 2 --log-file -
```

This file tells Heroku
to run migrations before launching,
then run gunicorn
as the web process
for the application.

Another precondition needed
for your app
is static files.
We saw in the static files article
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

In my deployment process
for Heroku,
this is a step that Heroku automatically does
because it can detect a Django project.

These items are the required preconditions
to run your application.
Django also has steps
that aren't strictly required
to make your app work,
but are very beneficial.
Let's look at how to address those next.

## Protecting Your Site

"Put on your seat belt."
The average person knows
that it's wise
to wear a seat belt
in a car.
The statistical data is overwhelming
that a seat belt can help save your life
if you're ever
in a car accident.
Yet,
a seat belt is not strictly necessary
(aside from a legal perspective)
to operate a vehicle.

Django includes a command
that produces a set of instructive safety messages
for important site settings and configurations.
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
```

On a little sample project
that I created,
the (slightly reformatted for the article) output looks like:

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
by the [System check framework](https://docs.djangoproject.com/en/4.1/topics/checks/)
that comes with Django.

You should review each of the checks
and learn about the changes
that the check recommends.
The items that appear with the `--deploy` flag are usually quite important
and fixing them can greatly improve the safety
and security
of your application.

Some of these checks are too modest about their importance.
For instance, `security.W018` is the warning
that tells you that `DEBUG` is set to `True`
in the settings.
`DEBUG = True` is *TERRIBLE*
for a live site
since it can *trivially* leak loads of private data.

As a *warning*,
`security.W018` will *not* fail the deploy check
because `./manage.py check` defaults
to failing
on things that are errors.
If you want to make sure
that your site is sufficiently protected,
I strongly encourage you
to add the `--fail-level WARNING` flag
so that the check will give those warnings the weight
that they likely deserve.

What do you do if the check is handled
by some other part
of your system?
For example,
maybe you've set up a secure configuration
with HTTPS,
and you've set HSTS headers
with a reverse proxy
like Nginx
(this was one of the configurations
that I mentioned
in the static files article).
If HSTS is handled elsewhere,
you could set the `SILENCED_SYSTEM_CHECKS` setting
to tell Django
that you took care of it.

```python
# project/settings.py

SILENCED_SYSTEM_CHECKS = [
    "security.W004"
]
```

Once you have finished the checklist,
your application will be much better equipped
to handle the hostile internet,
but things can still go wrong.
What should you do about errors
that happen on your live site?
Let's look at that next.

## Prepare For Errors

If an error happens on a live site
and the site administrator (i.e., *you*) didn't hear it,
did it really happen?
**Yes, yes it did.**

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

This brings us to the final strategy
that I'll cover.

#### 3. Use an error tracking service.

Error tracking services are specifically designed
to collect context about errors,
aggregate common errors together,
and generally give you tools
to respond to your site's errors appropriately.

**I find that error tracking services are the best tools
to understand what's going wrong
on your live site**
because the tools are purpose-built
for detailing error behavior.

Many of these services are not complicated
to get installed and configured,
and the services often have an extremely generous free tier
to monitor your application.

In the Django world,
I generally hear about two
of these error tracking services:
[Rollbar](https://rollbar.com/)
and [Sentry](https://sentry.io/welcome/).
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

That's it!

My Rollbar configuration
for one of my projects looks like:

```python
# project/settings.py

ROLLBAR = {
    "enabled": env("ROLLBAR_ENABLED"),
    "access_token": env("ROLLBAR_ACCESS_TOKEN"),
    "environment": env("ROLLBAR_ENVIRONMENT"),
    "branch": "main",
    "root": BASE_DIR,
}
```

In this example,
everything coming from `env` is from an environment variable
that we'll discuss more when we focus on settings management
in Django.

The `enabled` parameter can quickly turn Rollbar on and off.
This is good for local development
so you're not sending data to the service when working on new features.

The `access_token` is the secret that Rollbar will provide
in your account
to associate your app's error data
with your account
so you can see problems.

The `environment` setting lets Rollbar split your errors
into different groupings.
You can use this to separate different configurations
that you put on the internet.
For instance,
the software industry likes to call live sites "production."
You may also have a separate site
that is available privately
to a team
that you might call "development."

The other settings tell Rollbar information
that can help map errors back to your code repository.

Once you set this up,
how can you tell that it's working?
Like a musician tapping a microphone
to see if it's working,
I like to add a view to my code
that lets me test
that my error tracking service is operational.

```python
# application/views.py

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def boom(request):
    """This is for checking error handling (like Rollbar)."""
    raise Exception("Is this thing on?")
```

I connect this view to a URL configuration,
then check it after I deploy Rollbar
for the first time.
Importantly,
don't forget to include a `staff_member_required` decorator
so that random people
on the internet can't trigger errors
on your server on a whim!

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

In this article,
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

In the next article,
we'll look at Django's tools
for managing shorter term user data
like authentication info
with Django sessions.
We'll see the different modes
that Django provides
and how to use sessions
to support your project.
You'll learn about:

* What sessions are and how they work
* Ways that Django uses sessions
* How to use sessions in your apps

If you have questions,
you can reach me online
on X
where I am
[@mblayman](https://x.com/mblayman).
&nbsp;
