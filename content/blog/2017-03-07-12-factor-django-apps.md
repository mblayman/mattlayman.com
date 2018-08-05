---
title: 12-factor Django apps
description: >-
  Twelve-factor applications
  are a pattern
  that can be applied to web applications
  for making deployment easier.
  Learn what a twelve-factor app is
  and some things to consider
  when applying the pattern
  to Django applications.
image: img/2017/django.png
type: post
aliases:
 - /2017/12-factor-django-apps.html

---

Deployment of web applications
has many considerations.
Most web applications must handle sensitive data.
To handle increased traffic,
the app should be scalable.
If a crash occurs
in the app,
no data should be lost.
These are only a few things
that need to be considered.
*Twelve-factor applications address a lot
of these issues,
and I'll show how to make a Django web application
behave as a twelve-factor app.*

The {{< extlink "https://12factor.net/" "twelve-factor application" >}} methodology
is a pattern popularized by {{< extlink "https://www.heroku.com/" "Heroku" >}}
with an aim
to handle many of the biggest considerations
in web application deployment.
Twelve-factor applications operate differently
from a more traditional web application.
In a traditional environment,
the state of the system
is often baked in
to the deployed software.
This state could include information
like:

* database connections
* routes to other services such as Memcached
* tokens to connect with external services like Stripe

Including this kind of data
in the web application
reduces its flexibility
and is potentially unsafe
as it essentially stores secrets
in the app.

In contrast,
a twelve-factor app is **stateless**.
All state and configuration that can change dynamically
is injected via environment variables.
By pushing the environment settings
to environment variables,
a twelve-factor app can be deployed
to a variety of environments
merely by changing settings.
Do you want to deploy your app to a staging environment
and a production environment?
Change the environment variables
and your app is now configured for the new setting!

The decoupling of state from function
unlocks a number of new possibilities.

* With great ease,
  a team can scale their application horizontally
  by increasing the number of application servers
  to handle additional load.
* Apps can migrate to new environments quickly.
  Because the applications are stateless,
  they can be discarded in an old environment
  and provisioned again in a new environment
  without losing data.

There are other benefits documented
on the twelve-factor app website
and I strongly suggest that you read it
to see some of the other ideas
for these kinds of applications.

## 12-factor and Django

I've worked on a few Django apps
in my career.
These apps have mostly *not* been twelve-factor apps,
but my latest project,
{{< extlink "https://www.collegeconductor.com/" "College Conductor" >}},
uses the twelve-factor app pattern.
A Django app requires very little extra work
to make it a twelve-factor app.
The biggest change comes to the Django `settings.py` file.

Python exposes environment variables
through the `os.environ` dictionary.
Using a twelve-factor Django app means
wiring the environment variables to the Django settings.

For instance,
the `SECRET_KEY` setting should not be checked into source control.
The `SECRET_KEY` can be set like:

```python
import os

SECRET_KEY = os.environ['SECRET_KEY']
```

This is boring code
*at its finest*.
The cool part about this code
is how it declares its intent.
By not providing a default value,
the app will fail to start
unless the `SECRET_KEY` environment variable is defined.
This is an oddly good quality.
Since the variable is required,
it forces the deployment environment
to be complete.
When all the dynamic configuration is set this way,
you can have high confidence
that you have all the necessary configuration.

Twelve-factor apps are not without downsides.
Because everything must be declared in environment variables,
the standard `./manage.py runserver` will not work immediately.
In fact,
any `./manage.py` command will fail to function
without some configuation.
To fix this,
I use {{< extlink "https://honcho.readthedocs.io/en/latest/" "Honcho" >}},
a Python port of {{< extlink "http://ddollar.github.com/foreman" "Foreman" >}}.
Honcho provides tools for working
on twelve-factor apps.
With Honcho,
users define a `Procfile`
to determine which commands to run
to start an environment.
Here's an example:

```text
web: python manage.py runserver
```

When this file is defined,
you can run `honcho start`
to launch the commands.
Even though this seems as likely to break as before,
Honcho takes an extra step of looking
for environment variables
set in a `.env` file.
The `.env` file uses a format like:

```ini
SECRET_KEY='itsasecrettoeverybody'
```

For any variable set
in the file,
that variable is loaded
as an environment variable.

Honcho also includes a `run` command
for one-off commands.
This command does the same loading of `.env`
as the `start` command.

```bash
$ honcho run python manage.py migrate
```

Even though twelve-factor apps require extra work,
I believe that the benefits
that come from using them are very valuable.
With the `os` module
and an extra tool,
you can quickly produce a working twelve-factor Django app
for your environment.
If you do,
I hope you see the same benefits
that I've seen.
