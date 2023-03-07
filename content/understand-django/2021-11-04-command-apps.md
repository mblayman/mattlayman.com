---
title: "Command Your App"
description: >-
    With this Understand Django article,
    you'll learn about commands.
    Commands are the way to execute scripts
    that interact with your Django app.
    We'll see built-in commands
    and how to build your own commands.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - commands
series: "Understand Django"

---

In the last
{{< web >}}
[Understand Django]({{< ref "/understand-django/_index.md" >}})
article,
{{< /web >}}
{{< book >}}
chapter,
{{< /book >}}
we dug into file management.
We saw how Django handles user uploaded files
and how to deal with them safely.

{{< web >}}
With this article,
{{< /web >}}
{{< book >}}
With this chapter,
{{< /book >}}
you'll learn about commands.
Commands are the way to execute scripts
that interact with your Django app.
We'll see built-in commands
and how to build your own.

{{< understand-django-series "commands" >}}

## Why Commands?

Django makes it possible
to run code from a terminal
with `./manage.py`,
but why is this helpful or needed?
Consider this script:

```python
# product_stat.py

from application.models import Product

print(Product.objects.count())
```

which you could try running with:

```bash
$ python product_stat.py
```

The problem with this script is that Django is not ready to run yet.
If you tried to run this kind of code,
you would get an `ImproperlyConfigured` exception.
There are a couple of modifications
that you could make to get the script to run.

* Call `django.setup()`.
* Specify the `DJANGO_SETTINGS_MODULE`.

```python
# product_stat.py
import django

django.setup()

from application.models import Product

print(Product.objects.count())
```

Note that `django.setup()` must be before your Django related imports
(like the `Product` model in this example).
Now the script can run if you supply where the settings are located too.

```bash
$ DJANGO_SETTING_MODULE=project.settings python product_stat.py
```

This arrangement is less than ideal,
but why else might we want a way to run commands through Django?

Try running `./manage.py -h`.

What you'll likely see is more commands
than what Django provides alone.
This is where we begin to see more value
from the command system.
Because Django provides a standard way
to run scripts,
other Django applications can bundle useful commands
and make them easily accessible
to you.

Now that you've had a chance to see why commands exist
to run scripts
for Django apps,
let's back up and see *what* commands are.

## We Hereby Command

Django gives us a tool to run commands
before we've even started our project.
That tool is the `django-admin` script.
We saw it all the way back
{{< web >}}
in the first article
{{< /web >}}
{{< book >}}
in the first chapter
{{< /book >}}
where I provided a short set
of setup instructions
to get you started
if you've never used Django before.

After you've started a project,
your code will have a `manage.py` file,
{{< web >}}
and the commands you've seen in most articles are in the form of:
{{< /web >}}
{{< book >}}
and the commands you've seen in most chapters are in the form of:
{{< /book >}}

```bash
$ ./manage.py some_command
```

What's the difference
between `django-admin` and `manage.py`?
In truth, **not much!**

`django-admin` comes from Django's Python packaging.
In Python packages,
package developers can create scripts
by defining an entry point
in the {{< extlink "https://github.com/django/django/blob/4.1/setup.cfg" "packaging configuration" >}}.
In Django,
this configuration looks like:

```ini
[options.entry_points]
console_scripts =
    django-admin = django.core.management:execute_from_command_line
```

Meanwhile,
the entire `manage.py`
of a Django project looks like:

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

If you look closely,
you can see that the different scripts are both ways
to invoke the `execute_from_command_line` function
to run a command.
The primary difference is that the latter script will attempt
to set the `DJANGO_SETTINGS_MODULE` environment variable automatically.
Since Django needs to have `DJANGO_SETTINGS_MODULE` defined
for most commands
(note: `startproject` does *not* require that variable),
`manage.py` is a more convenient way
to run commands.

`execute_from_command_line` is able to present
what commands are available to a project,
whether a command comes from Django itself,
an installed app,
or is a custom command that you created yourself.
How are the commands discovered?
*The command system does discovery by following some packaging conventions.*

Let's say your project has an app named `application`.
Django can find the command if you have the following packaging structure.

```text
application
├── __init__.py
├── management
│   ├── __init__.py
│   └── commands
│       ├── __init__.py
│       └── custom_command.py
├── models.py
└── views.py
... Other typical Django app files
```

With this structure, you could run:

```bash
$ ./manage.py custom_command
```

Notes:

* Django will create a command for a module found
    in `<app>/management/commands/<command name>.py`.
* Don't forget the `__init__.py` files!
    Django can only discover the commands
    if `management` and `commands` are proper Python package directories.
* The example uses `custom_command`,
    but you can name your command
    with whatever valid Python module name that you want.

Unfortunately,
we can't slap some Python code
into `custom_command.py`
and assume that Django will know how to run it.
Within the `custom_command.py` module,
Django needs to find a `Command` class
that subclasses a `BaseCommand` class
that is provided by the framework.
Django requires this structure to give command authors a consistent way
to access features
of the command system.

With the `Command` class,
you can add a `help` class attribute.
Adding help can give users a description
of what your command does when running
`./manage.py custom_command -h`.

The `Command` class will also help you with handling arguments.
If your command needs to work with user input,
you'll need to parse that data.
Thankfully,
the class integrates
with Python's built-in `argparse` module.
By including an `add_arguments` method,
a command can parse the data
and pass the results
to the command's handler method in a structured way.
If you've had to write Python scripts before,
then you may understand how much time this kind of parsing can save you
(and for those who haven't, the answer is "a lot of time!").

Other smaller features exist within the `Command` class too.
Perhaps you only want your command to run
if your project has satisfied certain pre-conditions.
Commands can use the `requires_migration_checks`
or `requires_system_checks`
to ensure that the system is in the correct state
before running.

I hope it's clear
that the goal of the `Command` class is
to help you with common actions
that many commands will need to use.
There is a small API to learn,
but the system is a boon to making scripts quickly.

## Command By Example

Let's consider a powerful use case
to see a command in action.
When you initially start a Django app,
all of your app's interaction will probably be through web pages.
After all,
you were trying to use Django to make a web app,
right?
What do you do when you need to do something
that doesn't involve a browser?

This kind of work for your app is often considered *background* work.
Background work is a pretty deep topic
and will often involve special background task software
like
{{< extlink "https://docs.celeryproject.org/en/stable/getting-started/introduction.html" "Celery" >}}.
When your app is at an early stage,
Celery or similar software can be overkill and far more than you need.

A simpler alternative for some background tasks could be a command paired
with a scheduling tool like
{{< extlink "https://en.wikipedia.org/wiki/Cron" "cron" >}}.

On one of my projects,
I offer free trials for accounts.
After 60 days,
the free trial ends
and users either need to pay
for the service
or discontinue using it.
By using a command
and pairing it
with the
{{< extlink "https://devcenter.heroku.com/articles/scheduler" "Heroku Scheduler" >}},
I can move accounts from their trial status
to expired
with a daily check.

The following code is very close
to what my `expire_trials` command looks like
in my app.
I've simplified things a bit,
so that you can ignore the details
that are specific to my service.

```python
# application/management/commands/expire_trials.py

import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from application.models import Account


class Command(BaseCommand):
    help = "Expire any accounts that are TRIALING beyond the trial days limit"

    def handle(self, *args, **options):
        self.stdout.write(
            "Search for old trial accounts..."
        )
        # Give an extra day to be gracious and avoid customer complaints.
        cutoff_days = 61
        trial_cutoff = timezone.now() - datetime.timedelta(days=cutoff_days)
        expired_trials = Account.objects.filter(
            status=Account.TRIALING, created__lt=trial_cutoff
        )
        count = expired_trials.update(
            status=Account.TRIAL_EXPIRED
        )
        self.stdout.write(
            f"Expired {count} trial(s)"
        )
```

I configured the scheduler
to run `python manage.py expire_trials`
every day
in the early morning.
The command checks the current time
and looks for `Account` records
in the trialing state
that were created before the cutoff time.
From that query set,
the affected accounts are set to the expired account state.

How can you test this command?
There are a couple of approaches you can take
when testing a command.

If you need to simulate calling the command
with command line arguments,
then you can use `call_command`
from `django.core.management`.
Since the example command doesn't require arguments,
I didn't take that approach.

Generally, my preference is to create a command object
and invoke the `handle` method directly.
In my example above,
you can see that the command uses `self.stdout`
instead of calling `print`.
Django does this so that you could check your output
if desired.

Here is a test for this command:

```python
# application/tests/test_commands.py

from io import StringIO

from application.management.commands.expire_trials import (
    Command
)
from application.models import Account
from application.tests.factories import AccountFactory

def test_expires_trials():
    """Old trials are marked as expired."""
    stdout = StringIO()
    account = AccountFactory(
        status=Account.TRIALING,
        created=timezone.now() - datetime.timedelta(days=65),
    )
    command = Command(stdout=stdout)

    command.handle()

    account.refresh_from_db()
    assert account.status == Account.TRIAL_EXPIRED
    assert "Expired 1 trial(s)" in stdout.getvalue()
```

In this test,
I constructed a command instance
and checked the account state
after the command invocation.
Also,
observe that the `StringIO` instance is injected
into the `Command` constructor.
By building the command this way,
checking the output becomes a very achievable task
via the `getvalue` method.

Overall,
this scheme of making a command
and running it on a schedule
avoids all the work
of setting up a background worker process.
I've been extremely satisfied
with how this technique has worked
for me,
and I think it's a great pattern
when your app doesn't have to do a lot
of complex background processing.

## Useful Commands

Django is full of
{{< extlink "https://docs.djangoproject.com/en/4.1/ref/django-admin/" "useful commands" >}}
that you can use for all kinds of purposes.
{{< web >}}
Thus far in this series,
{{< /web >}}
{{< book >}}
Thus far in this book,
{{< /book >}}
we've discussed a bunch of them, including:

* `check` - Checks that your project is in good shape.
* `collectstatic` - Collects static files into a single directory.
* `createsuperuser` - Creates a super user record.
* `makemigrations` - Makes new migration files based on model changes.
* `migrate` - Runs any unapplied migrations to your database.
* `runserver` - Runs a development web server to check your app.
* `shell` - Starts a Django shell that allows you to use Django code
    on the command line.
* `startapp` - Makes a new Django app from a template.
* `startproject` - Makes a new Django project from a template.
* `test` - Executes tests that check the validity of your app.

Here is a sampling of other commands
that I find useful
when working with Django projects.

### `dbshell`

The `dbshell` command starts a different kind of shell.
The shell is a database program
that will connect to the same database
that your Django app uses.
This shell will vary based on your choice of database.

For instance,
when using PostgreSQL,
`./manage.py dbshell`
will start `{{< extlink "https://www.postgresql.org/docs/current/app-psql.html" "psql" >}}`.
From this shell,
you can execute SQL statements directly
to inspect the state
of your database.
I don't reach for this command often,
but I find it very useful to connect
to my database without having to remember database credentials.

### `showmigrations`

The `showmigrations` command has a simple job.
The command shows all the migrations
for each Django app
in your project.
Next to each migration is an indicator
of whether the migration is applied
to your database.

Here is an example of the `users` app
from one of my Django projects:

```bash
$ ./manage.py showmigrations users
users
 [X] 0001_initial
 [X] 0002_first_name_to_150_max
 [ ] 0003_profile
```

In my real project,
I've applied all the migrations,
but for this example,
I'm showing the third migration
as it would appear
if the migration wasn't applied yet.

`showmigrations` is a good way to show the state
of your database
from Django's point of view.

### `sqlmigrate`

The `sqlmigrate` command is *very* handy.
The command will show you what SQL statements Django would run
for an individual migration file.

Let's see an example.
In Django 3.1,
the team changed the `AbstractUser` model
so that the `first_name` field could have a maximum length
of 150 characters.
Anyone using the `AbstractUser` model
(which includes me)
had to generate a migration
to apply that change.

From my `showmigrations` output above,
you can see that the second migration
of my `users` app applied this particular framework change.

To see the Postgres SQL statements
that made the change,
I can run:

```bash
$ ./manage.py sqlmigrate users 0002
BEGIN;
--
-- Alter field first_name on user
--
ALTER TABLE "users_user" ALTER COLUMN "first_name" TYPE varchar(150);
COMMIT;
```

From this,
we can tell that Postgres executed an `ALTER COLUMN`
{{< extlink "https://en.wikipedia.org/wiki/Data_definition_language" "DDL" >}}
statement
to modify the length
of the `first_name` field.

### `squashmigrations`

Django migrations are a stack of separate database changes
that produce a final desired schema state
in your database.
Over time,
your Django apps will accumulate migration files,
but those files have a shelf life.
The `squashmigrations` command is designed
to let you tidy up an app's set
of migration files.

By running `squashmigrations`,
you can condense an app's migrations
into a significantly smaller number.
The reduced migrations can accurately represent your database schema,
and make it easier to reason about what changes happened
in the app's history.
As a side benefit,
migration squashing can make Django's migration handling faster
because Django gets to process fewer files.

## Even More Useful Commands

The commands above come with the standard Django install.
Adding in third-party libraries gives you access
to even more cool stuff to help with your project development!

A package that I often reach for
with my Django projects is the
{{< extlink "https://django-extensions.readthedocs.io/en/latest/index.html" "django-extensions" >}}
package.
This package is full of goodies,
including some great optional commands
that you can use!

A couple of my favorites include:

### `shell_plus`

How often do you fire up a Django shell,
import a model,
then do some ORM queries
to see the current state of the database?
This is something I do *quite* often.

The `shell_plus` command is like the regular shell,
but the command will import all your models *automatically*.
For the five extra characters
of `_plus`,
you can save your fingers a lot of typing
to import your models
and get directly to whatever you needed the shell for.

The command will also import some commonly used Django functions
and features
like `reverse`, `settings,` `timezone`, and more.

Also,
if you have installed a separate REPL like
{{< extlink "https://ipython.org/" "IPython" >}},
`shell_plus` will attempt to use the alternate REPL instead
of the default version that comes with Python.

### `graph_models`

When I'm live streaming my side projects
on {{< extlink "https://www.youtube.com/c/MattLayman" "my YouTube channel" >}},
I will often want to show the model relationships
of my Django project.
With the `graph_models` command,
I can create an image of all my models
and how those models relate to each other
(using UML syntax).
This is a great way to:

* Remind myself of the data modeling choices in my apps.
* Orient others to what I'm doing with my project.

This particular command requires some extra setup
to install the right tools
to create images,
but the setup is manageable
and the results are worth it.

Aside from `shell_plus` and `graph_models`,
there are 20 other commands that you can use
that may be very useful to you.
You should definitely check out django-extensions.

## Summary

{{< web >}}
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
you saw Django commands.
We covered:

* Why commands exist in the Django framework
* How commands work
* How to create your own custom command and how to test it
* Useful commands from the core framework and the django-extensions package

{{< web >}}
In the next article,
{{< /web >}}
{{< book >}}
In the next chapter,
{{< /book >}}
we're going to look into performance.
You'll learn about:

* How Django sites get slow
* Ways to optimize your database queries
* How to apply caching to save processing

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
&nbsp;
