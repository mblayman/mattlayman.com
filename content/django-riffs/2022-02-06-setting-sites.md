---
title: "Episode 16 - Setting Your Sites"
aliases:
 - /django-riffs/16
 - /djangoriffs/16
 - /django-riffs/16.
 - /djangoriffs/16.
description: >-
    On this episode,
    we look at how to manage settings
    on your Django site.
    What are the common techniques
    to make this easier to handle?
    Let's find out!
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - settings
nofluidvids: true

---

On this episode,
we look at how to manage settings
on your Django site.
What are the common techniques
to make this easier to handle?
Let's find out!

Listen at {{< extlink "https://open.spotify.com/episode/5jYVhLg90B720l0fpcF2TS" "Spotify" >}}
or with the player below.

## Last Episode

On the last episode,
we dug
into sessions
and how Django uses that data storage technique
for visitors
to your site.

## How Is Django Configured?

To run properly,
Django needs to be configured.
We need to understand
where this configuration comes from.
Django has the ability
to use default configuration values
or values set
by developers like yourself,
but where does it get those from?

Early in the process
of starting a Django application,
Django will internally import the following:

```python
from django.conf import settings
```

### Sidebar: Environment Variables

Environment variables are not a Django concept.
When any program runs
on a computer,
the operating system makes certain data available
to the running program.
This set of data is called the program's "environment,"
and each piece of data
in that set
is an environment variable.

```bash
$ export HELLO=world
```

If you create a Django project
with `startproject`
and use `project` as the name,
then you will find a generated file called `project/settings.py`
in the output.
When Django runs,
you could explicitly instruct Django with:

```bash
$ export DJANGO_SETTINGS_MODULE=project.settings
```

You may not actually need
to set `DJANGO_SETTINGS_MODULE` explicitly.
If you stick with the same settings file
that is created by `startproject`,
you can find a line
in `wsgi.py`
that looks like:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
```

Once Django reads the global settings
and any user defined settings,
we can get any configuration
from the `settings` object
via attribute access.
This convention of keeping all configuration
in the `settings` object
is a convenient pattern
that the framework,
third party library ecosystem,
and *you* can depend on.

```python
$ ./manage.py shell
>>> from django.conf import settings
>>> settings.SECRET_KEY
'a secret to everybody'
```

## Settings Module Patterns

### Multiple Modules Per Environment

A Django settings module is a Python module.
Nothing is stopping us
from using the full power
of Python
to configure that module the way we want.

Minimally, you will probably have at least two environments
where your Django app runs:

* On your local machine while developing
* On the internet for your live site

You might have modules like:

* `project.settings.dev`
* `project.settings.stage`
* `project.settings.production`

These examples would be for a local development environment
on your laptop,
a staging environment
(which is a commonly used pattern
for testing a site
that is as similar to the live site as possible
without *being* the live site),
and a production environment.
As a reminder from the deployment article,
the software industry like to call the primary site
for customers "production."

You could use a common module.
The advantage to this form is that the common settings can be
in a single location.
The environment specific files only need to record the *differences*
between the environments.
The disadvantage is that it is harder to get a clear picture
of all the settings of that environment.

For your local development environment
on your laptop,
you could use `project.settings.dev`.
This settings module would look like:

```python
# project/settings/dev.py

from project.settings.base import *

DEBUG = True

# Define any other settings that you want to override.
...
```

By using the `*` import in the `dev.py` file,
all the settings from `base.py` are pulled
into the module level scope.
Where you want a setting to be different,
you set the value in `dev.py`.
When Django starts using `DJANGO_SETTINGS_MODULE`
of `project.settings.dev`,
all the values from `base.py` will be used
via `dev.py`.

*Don't commit secret data to your code repository!*
Adding secrets to your source control tool
like Git
is usually not a good idea.
This is especially true
if you have a public repository
on GitHub.
Think no one is paying attention to your repo?
Think again!
There are tools out there
that scan *every public commit* made to GitHub.
These tools are specifically looking
for secret data
to exploit.

If you can't safely add secrets
to your code repo,
where can we add them instead?
You can use environment variables!
Let's look at another scheme
for managing settings
with environment variables.

### Settings Via Environment Variables

In Python,
you can access environment variables
through the `os` module.
The module contains the `environ` attribute,
which functions like a dictionary.

By using environment variables,
your settings module can get configuration settings
from the external environment
that is running the Django app.
This is a solid pattern because it can accomplish two things:

* Secret data can be kept out of your code
* Configuration differences between environments
  can be managed by changing environment variable values

Here's an example of secret data management:

```python
# project/settings.py

import os

SECRET_KEY = os.environ['SECRET_KEY']

...
```

On one of my projects,
I use the excellent {{< extlink "https://anymail.readthedocs.io/en/stable/" "Anymail" >}} package
to send emails
via an email service provider
(of the ESPs, I happen to use {{< extlink "https://sendgrid.com/" "SendGrid" >}}).
When I'm working with my development environment,
I don't want to send real email.
Because of that,
I use an environment variable
to set Django's `EMAIL_BACKEND` setting.
This let's me switch between the Anymail backend
and Django's built-in
`django.core.mail.backends.console.EmailBackend`
that prints emails to the terminal instead.

If I did this email configuration with `os.environ`,
it would look like:

```python
# project/settings.py

import os

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', "anymail.backends.sendgrid.EmailBackend")

...
```

We need to be aware of a big gotcha
with using environment variables.
*Environment variables* are only available as a `str` type.
This is something to be aware
because there will be times when you want a boolean settings value
or some other *type* of data.
In a situation
where you need a different type,
you have to coerce a `str`
into the type you need.
In other words,
don't forget that every string
except the empty string is truthy
in Python:

```python
>>> not_false = "False"
>>> bool(not_false)
True
```

Note:
As you learn more about settings,
you will probably encounter advice
that says to avoid using environment variables.
This is well intentioned advice
that highlights
that there *is* some risk
with using environment variables.
With this kind of advice,
you may read a recommendation
for secrets management tools
like {{< extlink "https://www.vaultproject.io/" "HashiCorp Vault" >}}.
These are good tools,
but consider them a more advanced topic.
In my opinion,
using environment variables for secrets management
is a reasonably low risk storage mechanism.

## Settings Management Tools

The built-in tool that is available to you
is the `diffsettings` command.
This tool makes it easy
to see the computed settings
of your module.
Since settings can come
from multiple files
(including Django's `global_settings.py`)
or environment variables,
inspecting the settings output
of `diffsettings` is more convenient
than thinking through how a setting is set.

Here's an example
of some of the security settings
by running `./manage.py diffsettings --output unified`
for one of my projects.

```diff
- SECURE_HSTS_INCLUDE_SUBDOMAINS = False
+ SECURE_HSTS_INCLUDE_SUBDOMAINS = True
- SECURE_PROXY_SSL_HEADER = None
+ SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

Finally,
I'll note that you can actually compare two separate settings modules.
Let's say you wanted to compare settings
between your development mode
and your live site.
Assuming your settings files are names
like I described earlier,
you could run something like:

```bash
$ ./manage.py diffsettings \
    --default project.settings.dev \
    --settings project.settings.production \
    --output unified
```

{{< extlink "https://django-environ.readthedocs.io/en/latest/" "django-environ" >}}
primarily does two important things
that I value:

* The package allows you coerce strings into a desired data type.
* The package will read from a file
  to load environment variables into your environment.

What does type coercion look like?
With `django-environ`,
you start with `Env` object.

```python
# project/settings.py

import environ

env = environ.Env()
```

If you want to be able to control `DEBUG`
from an environment variable,
the settings would be:

```python
# project/settings.py

import environ

env = environ.Env(
    DEBUG=(bool, False),
)

DEBUG = env("DEBUG")
```

With this setup,
your app will be safe by default
with `DEBUG` set to `False`,
but you'll be able to override
that via the environment.
`django-environ` works with a handful
of strings that it will accept as `True`
such as "on", "yes", "true", and others
(see the documentation for more details).

```env
# .env
DEBUG=on
```

Back in the settings file, you'd include `read_env`:

```python
# project/settings.py

import environ

environ.Env.read_env()
env = environ.Env(
    DEBUG=(bool, False),
)

DEBUG = env("DEBUG")
```

## My Preferred Settings Setup

For the majority of uses,
I find that working with `django-environ`
in a single file is the best pattern
in my experience.

When I use this approach,
I make sure that all of my settings favor a safe default configuration.
This minimizes the configuration
that I have to do for a live site.

Overall,
I like the environment variable approach,
but I do use more than one settings file
for one important scenario: testing.

When I run my unit tests,
I want to guarantee
that certain conditions are always true.
There are things
that a test suite should never do
in the vast majority of cases.
Sending real emails is a good example.
If I happen to configure my `.env`
to test real emails for the local environment,
I don't want my tests
to send out an emails accidentally.

Thus,
I create a separate testing settings file
and configure my test runner (pytest)
to use those settings.
This settings file *does* mostly use the base environment,
but I'll override some settings with explicit values.
Here's how I protect myself
from accidental live emails:

```python
# project/testing_settings.py

from .settings import *

# Make sure that tests are never sending real emails.
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
```

The combination of a single file
for most settings sprinkled
with a testing settings file
for safety
is the approach
that has worked the best for me.

## Summary

In this episode,
we learned about Django settings
and how to manage the configuration
of your application.
We covered:

* How Django is configured
* Patterns for working with settings in your projects
* Tools that help you observe and manage settings

## Next Time

On the next episode,
we'll talk about user uploaded files.
How *does* that profile picture work?
Where does that data go?
We'll answer those kinds of questions next time.

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
