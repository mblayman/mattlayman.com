---
title: "Episode 6 - Where Does the Data Go?"
aliases:
 - /django-riffs/6
 - /djangoriffs/6
 - /django-riffs/6.
 - /djangoriffs/6.
description: >-
    On this episode,
    we will learn about storing data
    and how Django manages data
    using models.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - models

---

On this episode,
we will learn about storing data
and how Django manages data
using models.

Listen at {{< extlink "https://open.spotify.com/episode/1zFFGYGhMwDEgquMeUU2vn" "Spotify" >}}.

## Last Episode

On the last episode,
we saw Django forms
and how to interact with users
to collect data.

## Setting Up

A relational database is like a collection
of spreadsheets.
Each spreadsheet is actually called a table.
A table has a set of columns
to track different pieces
of data.
Each row in the table would represent a related group.
For instance,
imagine we have an employee table
for a company.
The columns for an employee table might include a first name, last name,
and job title.
Each row would represent an individual employee.

```text
First name | Last name | Job title
-----------|-----------|----------
John       | Smith     | Software Engineer
-----------|-----------|----------
Peggy      | Jones     | Software Engineer
```

Django uses a relational database
so the framework must have some ability
to set up that database.
The database configuration is in the `DATABASES` setting
in your `settings.py` file.
After running `startproject`,
you'll find:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

## Modeling Your Data

Now that you have an idea
of where Django will store your data,
let's focus on *how* Django will store data.

Django represents data
for a database
in Python classes
called **models**.
Django models are similar
to the form classes
that we saw
in the last article.
A Django model declares the data
that you want to store
in the database
as class level attributes,
just like a form class.
In fact,
the types of fields are extremely similar
to their form counterparts,
and for good reason!
We often want to save form data
and store it
so it makes sense for models
to be similar to forms
in structure.
Let's look at an example.

```python
# application/models.py
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=200)
```

```python
>>> from application.models import Employee
>>> employee = Employee(
...     first_name='Tom',
...     last_name='Bombadil',
...     job_title='Old Forest keeper')
>>> employee.first_name
'Tom'
```

Since the database is a tool
that is external to Django,
the database needs a bit of preparation
before it can receive data
from Django.

## Preparing A Database With Migrations

We now know that Django models are Python classes
that map to database tables.
Database tables don't magically appear.
We need the ability to set up tables
so that they will match the structure
defined in the Python class.
The tool Django provides
to make Django models
and a database sync up
is called the migrations system.

Migrations are Python files
that describe the sequence
of database operations
that are needed
to make a database match any model definitions
that you have in your project.

At the core level,
you need to learn a couple
of Django commands:
`makemigrations`
and `migrate`.

### `makemigrations`

The `makemigrations` command will create any migration files
if there are any pending model changes.
To create our migration file
for the `Employee` model,
we can run:

```bash
(venv) $ ./manage.py makemigrations
Migrations for 'application':
  application/migrations/0001_initial.py
    - Create model Employee
```

The important thing to note is that we require a new migration
when we make model changes
that update any model fields.
This includes:

* Adding new models or new fields
* Modifying existing fields
* Deleting existing fields
* Changing some model metadata and a few other edge cases

### `migrate`

The other command, `migrate`,
takes migration files
and applies them
to a database.
For example:

```bash
(venv) $ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, application, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying application.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying sessions.0001_initial... OK
```

The migration system is also used
by built-in Django applications.
In my sample project,
I used `startproject`
which includes a set
of included applications
in the `INSTALLED_APPS` list.
We can observe that our sample `application` applied its migration,
and the migrations
from the other Django applications
that we included are also applied.

Those are the fundamentals
of migrations.
You can also use migrations
to apply more complex operations
like actions
that are specific
to your selected database.
You can learn more
about what Django migrations can do
in the {{< extlink "https://docs.djangoproject.com/en/3.0/topics/migrations/" "Migrations documentation" >}}.

## Summary

This is how Django stores data
for later use.
We've examined:

* What is a relational database?
* What is a model?
* How does Django synchronize models with a database?

## Next Time

In the next episode,
we will go deeper into models.
We'll cover how to work with models
to save and fetch data
for your application.

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
