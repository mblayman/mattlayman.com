---
title: "Store Data With Models"
description: >-
    In this article,
    we will see how to store data
    into a database
    with Django models.
    The article covers how models act
    as an interface
    to let your application
    store and fetch data.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - models

---

{{< web >}}
In the previous
[Understand Django]({{< ref "/understand-django/_index.md" >}})
article,
we encountered forms
and how forms allow your application
to receive data
from users
who use your site.
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
you'll see how to take
that data
and store it
into a database
so that your application can use that data
or display it later.

{{< understand-django-series "models" >}}

## Setting Up

Let's figure out where your data goes
before getting deep
into how to work with it.
Django uses databases
to store data.
More specifically,
Django uses *relational* databases.
Covering relational databases would be a gigantic topic
so you'll have to settle
for a **very** abridged version.

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

The "relational" part of a relational database comes into play
because multiple tables can *relate*
to each other.
In our company example,
the database could have a table of phone numbers
that it uses to store the phone number
of each employee.

Why not put the phone number in the same employee table?
Well,
what would happen if a company needed a cell phone number
and home phone number?
By having separate tables,
we could support tracking multiple phone number types.
There is a lot of power that comes
from being able to separate these different kinds
of data.
We'll see the power of relational databases
as we explore how Django exposes
that power.

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

Like we saw with the templates system,
Django supports multiple databases.
Unlike the template system,
the database settings refer to each supported backend as an "engine"
instead of "backend."
The default database engine
from `startproject`
is set to use
{{< extlink "https://www.sqlite.org/index.html" "SQLite" >}}.
SQLite is a great starting choice
because it fits an entire relational database
into a single file
which the settings name `db.sqlite3`.
This choice of engine really lowers the barrier
to starting
with Django
since new Django developers don't have to go download additional tools
to try Django out.

SQLite is an amazing little database
and probably the mostly widely used database
in the world.
The database exists in every smartphone you could think of.
Even though SQLite is amazing,
it's not a good fit for many scenarios
where you'd want to use Django.
For starters,
the database only permits one user
to write to it
at a time.
That's a huge problem if you're planning
to make a site that serves many people simultaneously.

Because SQLite is not the best fit
for an application on the web,
you'll likely need to switch
to a different relational database.
I'd recommend {{< extlink "https://www.postgresql.org/" "PostgreSQL" >}}.
Postgres (as it is often "abbreviated" to) is a wildly popular,
open source database
that is very well supported.
Combined with {{< extlink "https://www.psycopg.org/docs/" "psycopg2" >}}
as the Django engine,
you'll find that many places
that can host your Django app will work well
with Postgres.

We can explore more database configuration
{{< web >}}
in a future article
{{< /web >}}
{{< book >}}
in a future chapter
{{< /book >}}
on deployment.
For now,
while you're learning,
SQLite is perfectly well suited
for the task.

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
{{< web >}}
in the last article.
{{< /web >}}
{{< book >}}
in the last chapter.
{{< /book >}}
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
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    job_title = models.CharField(
        max_length=200
    )
```

This model class describes the pieces
that we want to include
in a database table.
Each model class represents one database table.
If we wanted the phone numbers
that I mentioned earlier,
we'd create a separate `PhoneNumber` class.
Conventionally,
we use a singular name
instead of a plural
when naming the class.
We do that because each *row*
in the table
is represented
as an object instance.

```python
>>> from application.models import Employee
>>> employee = Employee(
...     first_name='Tom',
...     last_name='Bombadil',
...     job_title='Old Forest keeper')
>>> employee.first_name
'Tom'
```

This example appears
to create a new employee,
but it's missing a key element.
We haven't saved the `employee` instance
to the database.
We can do that with `employee.save()`,
but,
if you are following along
and try to call that right now,
it will fail
with an error that says
that the employee table doesn't exist.

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

Because Django works
with many databases,
these database operations are defined
in Python files
so that the operations can be abstract.
By using abstract operations,
the Django migration system can plug in the specific database commands
for whatever database you're using.
If you're starting out with SQLite,
then moving to PostgreSQL
when you're ready
to put your application
on the internet,
then the migration system will do its best
to smooth over the differences
to minimize the amount
of work you would need
while making the transition.

Initially,
you can get pretty far
without understanding the internals
of how migration files work.
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

If you do not make a migration,
you will likely encounter errors
when fetching data
from the database.
This is because Django only builds queries
based on what is defined
in the Python code.
The system assumes
that the database is in the proper state.
Django will try to query
on database tables
even if those tables don't exist yet!

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

This is the output that happens
when applying our new migration.
What is all this stuff!?

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

If you run the `migrate` command again,
you won't see the same output.
That's because Django keeps tracks
of which migrations were applied.
The migration system will only execute any *unapplied* migrations.

Those are the fundamentals
of migrations.
You can also use migrations
to apply more complex operations
like actions
that are specific
to your selected database.
You can learn more
about what Django migrations can do
in the {{< extlink "https://docs.djangoproject.com/en/4.0/topics/migrations/" "Migrations documentation" >}}.

## Working With Models

After running migrations,
your database will be prepared
to communicate properly
with Django.

To create new rows
in our new database tables,
we can use a model's `save` method.
When you save a model instance,
Django will send a message
to the database
that effectively says
"add this new data
to this database table."
These database "messages"
are actually called **queries**.

As I mentioned
in the settings section,
Django communicates
with the database
via a database engine.
The database engine uses Structured Query Language (SQL)
to communicate
with the actual database.
SQL is the common standard
that Django's supported databases all "speak."
Since Django uses SQL,
that's why messages are named "query."

What does an SQL query look like?
If we save our model example from earlier,
it would look something like:

```sql
INSERT INTO "application_employee"
    ("first_name", "last_name", "job_title")
VALUES
    ('Tom', 'Bombadil', 'Old Forest keeper')
```

Note that this example is an `INSERT` query
when using the SQLite engine.
Like natural languages,
SQL has a variety of dialects
depending on the database
that you select.
The databases do their best to adhere
to some standards,
but each database has its quirks,
and the job
of the database engine is
to even out those differences
where possible.

This is another area where Django does a ton
of hard work
on your behalf.
The database engine translates your `save` call
into the proper SQL query.
SQL is a deep topic
that we can't possibly cover fully
{{< web >}}
in this article.
{{< /web >}}
{{< book >}}
in this chapter.
{{< /book >}}
Thankfully,
we don't have to
because of Django's ORM!

ORM stands for Object Relational Mapper.
The job of an ORM
is to map (or translate)
from Python *objects*
to a *relational* database.
This means that we spend our time working
in Python code,
and we let Django figure out how
to get and put data
into the database.

Using `save` on a model record is such a small example
of the Django ORM.
What else can we do?
We can do things like:

* Get all rows from the database.
* Get a filtered set of rows based on some filtering criteria.
* Update a set of rows at the same time.
* Delete rows from the database.

Most of these operations
with the Django ORM work
through a `Manager` class.
Where our previous example showed how
to manipulate a single row,
a model manager has methods designed
for interacting with multiple rows.

We can analyze our fictitious employee table.
The manager for a model is attached to the model class
as an attribute named `objects`.
Let's see some code:

```python
>>> from application.models import Employee
>>> bobs = Employee.objects.filter(first_name='Bob')
>>> for bob in bobs:
...     print(f"{bob.first_name} {bob.last_name}")
...
Bob Ross
Bob Barker
Bob Marley
Bob Dylan
>>> print(bobs.query)
SELECT
    "application_employee"."id",
    "application_employee"."first_name",
    "application_employee"."last_name",
    "application_employee"."job_title"
FROM "application_employee"
WHERE "application_employee"."first_name" = Bob
```

In this example,
we're using the manager
to filter to a subset
of employees
within the table.
The `bobs` variable returned
by the `filter` method
is a `QuerySet`.
As you might guess,
it represents a set of rows
that an SQL query will return.
Whenever you have a queryset,
you can print the query
to see the exact SQL statement
that Django will run
on your behalf.

What if you want to delete an employee record?

```python
>>> from application.models import Employee
>>> # The price is wrong, Bob!
>>> Employee.objects.filter(
... first_name='Bob',
... last_name='Barker').delete()
(1, {'application.Employee': 1})
```

A queryset can apply operations in bulk.
In this case,
the filter is sufficiently narrow
that only one record was deleted,
but it could have included more
if the SQL query matched more database table rows.

The `QuerySet` class has a variety
of methods
that are useful
when working with tables.
Some of the methods also have the interesting property
of returning a new queryset.
This is a beneficial capability
when you need to apply additional logic
for your query.

```python
from application.models import Employee

# employees is a QuerySet of all rows!
employees = Employee.objects.all()

if should_find_the_bobs:
    # New queryset!
    employees = employees.filter(
        first_name='Bob'
    )
```

Here's are some other `QuerySet` methods
that I use constantly:

* `create` - As an alternative to creating a record instance
    and calling `save`,
    the manager can create a record directly.

```python
Employee.objects.create(
    first_name='Bobby',
    last_name='Tables'
)
```

* `get` - Use this method when you want one
    *and exactly one* record.
    If your query doesn't match
    or will return multiple records,
    you'll get an exception.

```python
the_bob = Employee.objects.get(
    first_name='Bob',
    last_name='Marley'
)

Employee.objects.get(first_name='Bob')
# Raises application.models.Employee.MultipleObjectsReturned

Employee.objects.get(
    first_name='Bob',
    last_name='Sagat'
)
# Raises application.models.Employee.DoesNotExist
```

* `exclude` - This method lets you exclude rows
    that may be part of your existing queryset.

```python
the_other_bobs = (
    Employee.objects.filter(first_name='Bob')
    .exclude(last_name='Ross')
)
```

* `update` - With this method,
    you can update a group of rows
    in a single operation.

```python
Employee.objects.filter(
    first_name='Bob'
).update('Robert')
```

* `exists` - Use this method if you want to check
    if rows exist in the database
    that match the condition you want to check.

```python
has_bobs = Employee.objects.filter(
    first_name='Bob').exists()
```

* `count` - Check how many rows match a condition.
    Because of how SQL works,
    note that this is more efficient
    than trying to use `len` on a queryset.

```python
how_many_bobs = Employee.objects.filter(
    first_name='Bob').count()
```

* `none` - This returns an empty queryset for the model.
    How could this be useful?
    I use this when I need to protect certain data access.

```python
employees = Employee.objects.all()

if not is_hr:
    employees = Employee.objects.none()
```

* `first` / `last` - These methods will return an individual model instance
    if one matches.
    The methods use ordering on the models
    to get the desired result.
    We use `order_by` to tell how we want the results arranged.

```python
>>> a_bob = Employee.objects.filter(
...     first_name='Bob').order_by(
...     'last_name').last()
>>> print(a_bob.last_name)
Ross
```

With the knowledge
of how you can interact
with models,
we can focus more closely
on what data can be stored
in models
(and, thus, in your database).

## Types Of Model Data

The `Employee` table that I've used
as the example
{{< web >}}
for this article
{{< /web >}}
{{< book >}}
for this chapter
{{< /book >}}
only has three `CharField` fields
on the model.
The choice was deliberate
because I wanted you
to have a chance
to absorb a bit about the Django ORM
and working with querysets
before seeing other data types.

{{< web >}}
We saw in the forms article
{{< /web >}}
{{< book >}}
We saw in the forms chapter
{{< /book >}}
that Django's form system
includes a wide variety
of form fields.
If you look at the
{{< extlink "https://docs.djangoproject.com/en/4.0/ref/forms/fields/" "Form fields" >}} reference
and compare the list
of types
to those in the
{{< extlink "https://docs.djangoproject.com/en/4.0/ref/models/fields/" "Model field reference" >}},
you can observe a lot of overlap.

Like their form counterparts,
models have `CharField`,
`BooleanField`,
`DateField`,
`DateTimeField`,
and many other similar types.
The field types share many common attributes.
Most commonly,
I think you will use or encounter the following attributes.

* `default` - If you want to be able to create a model record
    without specifying certain values,
    then you can use `default`.
    The value can either be a literal value
    or callable function that produces a value.

```python
# application/models.py
import random

from django.db import models

def strength_generator():
    return random.randint(1, 20)

class DungeonsAndDragonsCharacter(
    models.Model
):
    name = models.CharField(
        max_length=100,
        default='Conan'
    )
    # Important: Pass the function,
    # do not *call* the function!
    strength = models.IntegerField(
        default=strength_generator
    )
```

* `unique` - When a field value must be unique
    for all the rows in the database table,
    use `unique`.
    This is a good attribute
    for identifiers
    where you don't expect duplicates.

```python
class ImprobableHero(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

# There can be only one.
ImprobableHero.objects.create(
    name='Connor MacLeod'
)
```

* `null` - A relational database has the ability
    to store the absence of data.
    In the database,
    this value is thought of as `NULL`.
    Sometimes this is an important distinction
    versus a value that is empty.
    For instance,
    on a `Person` model,
    an integer field like `number_of_children` would mean very different things
    for a value of 0
    versus a value of `NULL`.
    The former indicates that a person has no children
    while the latter indicates
    that the number of children is unknown.
    The presence of null conditions requires more checking
    in your code
    so Django defaults to making `null` be `False`.
    This means that a field does not allow `NULL`.
    Null values can be useful if needed,
    but I think its better to avoid them
    if you can
    and try to keep actual data about a field.

```python
class Person(models.Model):
    # This field would always have a value since it can't be null.
    # Zero counts as a value and is not NULL.
    age = models.IntegerField()
    # This field could be unknown and contain NULL.
    # In Python, a NULL db value will appear as None.
    weight = models.IntegerField(
        null=True
    )
```

{{< web >}}
* `blank` - The `blank` attribute is often used
    in conjunction with the `null` attribute.
    While the `null` attribute allows a database
    to store `NULL`
    for a field,
    `blank` allows *form validation*
    to permit an empty field.
    This is used by forms
    which are automatically generated
    by Django
    like in the Django administrator site
    which we'll talk about in the next article.
{{< /web >}}
{{< book >}}
* `blank` - The `blank` attribute is often used
    in conjunction with the `null` attribute.
    While the `null` attribute allows a database
    to store `NULL`
    for a field,
    `blank` allows *form validation*
    to permit an empty field.
    This is used by forms
    which are automatically generated
    by Django
    like in the Django administrator site
    which we'll talk about in the next chapter.
{{< /book >}}

```python
class Pet(models.Model):
    # Not all pets have tails,
    # so we want auto-generated forms
    # to allow no value.
    length_of_tail = models.IntegerField(
        null=True,
        blank=True
    )
```

{{< web >}}
* `choices` - We saw `choices`
    in the forms article
    as a technique
    for helping users pick the right value
    from a constrained set.
    `choices` can be set on the model.
    Django can do validation
    on the model
    that will ensure
    that only particular values are stored
    in a database field.
{{< /web >}}
{{< book >}}
* `choices` - We saw `choices`
    in the forms chapter
    as a technique
    for helping users pick the right value
    from a constrained set.
    `choices` can be set on the model.
    Django can do validation
    on the model
    that will ensure
    that only particular values are stored
    in a database field.
{{< /book >}}

```python
class Car(models.Model):
    COLOR_CHOICES = [
        (1, 'Black'),
        (2, 'Red'),
        (3, 'Blue'),
        (4, 'Green'),
        (5, 'White'),
    ]
    color = models.IntegerField(
        choices=COLOR_CHOICES,
        default=1
    )
```

* `help_text` - As applications get bigger
    or if you work on a large team
    with many people creating Django models,
    the need for documentation grows.
    Django permits help text
    that can be displayed
    with a field value
    in the Django administrator site.
    This help text is useful
    to remind your future self
    or educate a coworker.

```python
class Policy(models.Model):
    is_section_987_123_compliant = models.BooleanField(
        default=False,
        help_text=(
        'For policies that only apply'
        ' on leap days in accordance'
        ' with Section 987.123'
        ' of the Silly Draconian Order'
        )
    )
```

Those are the attributes
that I believe users are most likely
to encounter.
There are also a couple of important field types
that require special attention:
relational fields.

## What Makes A Database "Relational?"

Relational databases have the ability
to link different types
of data together.
We got a brief example
of this earlier
{{< web >}}
in this article
{{< /web >}}
{{< book >}}
in this chapter
{{< /book >}}
when we considered
an employee
with multiple phone numbers.

An overly simplified model
for an employee
with multiple phone numbers might look like:

```python
# application/models.py
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    job_title = models.CharField(
        max_length=200
    )
    phone_number_1 = models.CharField(
        max_length=32
    )
    phone_number_2 = models.CharField(
        max_length=32
    )
```

This single table could hold a couple
of numbers,
but this solution has some deficiencies.

* What if an employee has more than two phone numbers?
    It's possible for a person to have multiple cell phones,
    a land line at their residence,
    a pager number,
    a fax number,
    and so on.
* How can we know what type of phone number is
    in `phone_number_1` and `phone_number_2`?
    If you pull the employee record
    to try to call the individual
    and dial a fax number instead,
    you'd have a hard time talking to them.

Instead,
what if we had two separate models?

```python
# application/models.py
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    job_title = models.CharField(
        max_length=200
    )

class PhoneNumber(models.Model):
    number = models.CharField(
        max_length=32
    )
    PHONE_TYPES = (
        (1, 'Mobile'),
        (2, 'Home'),
        (3, 'Pager'),
        (4, 'Fax'),
    )
    phone_type = models.IntegerField(
        choices=PHONE_TYPES,
        default=1
    )
```

We've got two separate tables.
How can we link the tables
so that an employee can have one, two, or two hundred phone numbers?
For that,
we can use the `ForeignKey` relational field type.
Here is a slightly updated version of `PhoneNumber`.

```python
...

class PhoneNumber(models.Model):
    number = models.CharField(
        max_length=32
    )
    PHONE_TYPES = (
        (1, 'Mobile'),
        (2, 'Home'),
        (3, 'Pager'),
        (4, 'Fax'),
    )
    phone_type = models.IntegerField(
        choices=PHONE_TYPES,
        default=1
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )
```

This update says that every phone number must now be associated
with an employee record.
`on_delete` is a required attribute
that determines what will happen
when an employee record gets deleted.
In this case, `CASCADE` means
that deleting an employee row will cascade
and delete any of the employee's related phone numbers too.

The key to how this works is by understanding *keys*.
When you make a Django model,
you get an extra field added
to your model
by the framework.
This field is called an `AutoField`.

```python
# This is what Django adds to your model.
id = models.AutoField(primary_key=True)
```

An `AutoField` adds a column
to a database table
that will assign each row
in the table
a unique integer.
Each new row increments
from the previous row
and numbering starts
at one.
This number is the identifier
for the row
and is called the *primary key*.

If Tom Bombadil is the first employee
in the table,
then the row `id` value would be `1`.

Knowing about primary keys,
we're equipped to understand foreign key fields.
In the case
of the `PhoneNumber.employee` foreign key field,
any phone number row will store the value
of some employee row's primary key.
This is usually called a one to many relationship.

A `ForeignKey` is a one to many relationship
because multiple rows from a table
(in this case, `PhoneNumber`)
can reference a single row
in another table, namely, `Employee`.
In other words,
an employee can have multiple phone numbers.
If we wanted to get Tom's phone numbers,
then one possible way would be:

```python
tom = Employee.objects.get(
    first_name='Tom',
    last_name='Bombadil'
)
phone_numbers = PhoneNumber.objects.filter(employee=tom)
```

The query for `phone_numbers` would be:

```sql
SELECT
    "application_phonenumber"."id",
    "application_phonenumber"."number",
    "application_phonenumber"."phone_type",
    "application_phonenumber"."employee_id"
FROM "application_phonenumber"
WHERE "application_phonenumber"."employee_id" = 1
```

In the database,
Django will store the table column
for the foreign key
as `employee_id`.
The query is asking for all phone number rows
that match when the employee ID is 1.
Since primary keys have to be unique,
that value of 1 can only match Tom Bombadil
so the resulting rows will be phone numbers
that are associated
with that employee.

There is another relational field type
that we should spend time on.
That field is the `ManyToManyField`.
As you might guess,
this field is used when two types
of data relate to each other
in a many to many fashion.

Let's think about neighborhoods.
Neighborhoods can have a variety
of mixed residence types
like houses, apartments, condominiums
and so on,
but to keep the example simpler,
we'll assume that neighborhoods are composed
of houses.
Each house in a neighborhood is the home
of one or more people.

What if we tried to model this with `ForeignKey` fields?

```python
# application/models.py
from django.db import models

class Person(models.Model):
    name = models.CharField(
        max_length=128
    )

class House(models.Model):
    address = models.CharField(
        max_length=256
    )
    resident = models.ForeignKey(
        Person,
        on_delete=models.CASCADE
    )
```

This version shows a scenario
where a house can only have a single resident.
A person could be the resident
of multiple houses,
but those houses would be pretty lonely.
What if we put the foreign key
on the other side
of the modeling relationship?

```python
# application/models.py
from django.db import models

class House(models.Model):
    address = model.CharField(
        max_length=256
    )

class Person(models.Model):
    name = models.CharField(
        max_length=128
    )
    house = models.ForeignKey(
        House,
        on_delete_models.CASCADE
    )
```

In this version,
a house can have multiple residents,
but a person can only belong to a single house.

Neither of these scenarios model the real world well.
In the real world,
houses can and do often hold multiple people.
Simultaneously,
many people in the world have a second house
like a beach house
or a summer cottage in the woods.
Both sides of the model relationship can have many
of the other side.

With a `ManyToManyField`,
you can add the field to either side.
Here's the new modeling.

```python
# application/models.py
from django.db import models

class Person(models.Model):
    name = models.CharField(
        max_length=128
    )

class House(models.Model):
    address = models.CharField(
        max_length=256
    )
    residents = models.ManyToManyField(
        Person
    )
```

How does this work at the database level?
We saw with foreign keys
that one table can hold the primary key
of another table's row
in its own data.
Unfortunately,
a single database column cannot hold multiple foreign keys.
That means that the modeling above does *not* add `residents`
to the `House` table.
Instead,
the relationship is handled
by adding a *new* database table.
This new table contains the mapping
between people and houses
and stores rows
that contain primary keys from each model.

Let's think of an example
to see what this looks like.
Suppose there are three people records
with primary keys of 1, 2, and 3.
Let's also suppose that there are three houses
with primary keys of 97, 98, and 99.
To prove that the many-to-many relationship works
in both directions,
we'll assume these conditions are true:

* People with primary keys of 1 and 2 reside in house 97.
* The person with primary key 3 owns house 98 and 99.

The data in the new mapping table between `Person` and `House`
would contain data like:

```text
Person | House
-------|------
1      | 97
2      | 97
3      | 98
3      | 99
```

Because of the joining table,
Django is able to query either side of the table
to get related houses or residents.

We can access the "many" side
of each model using a queryset.
`residents` will be a `ManyRelatedManager`
and, like other managers,
can provide querysets
by using certain manager methods.

Getting the reverse direction is a little less obvious.
Django will add another `ManyRelatedManager`
to the `Person` model automatically.
The name of that manager is the model name joined with `_set`.
In this circumstance,
that name is `house_set`.
You can also provide a `related_name` attribute
to the `ManyToManyField` if you want a different name
like if you wanted to call it `houses` instead.

```python
house = House.objects.get(
    address='123 Main St.'
)
# Note the use of `all()`!
for resident in house.residents.all():
    print(resident.name)

person = Person.objects.get(name='Joe')
for house in person.house_set.all():
    print(house.address)
```

Understanding `ForeignKey` and `ManyToManyField` is an important step
to modeling your problem domain well.
By having these tools available to you,
you can begin to create many
of the complex data relationships that exist
with real world problems.

## Summary

{{< web >}}
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
we've explored:

* How to set up a database for your project.
* How Django uses special classes called models to keep data.
* Running the commands that will prepare a database
    for the models you want to use.
* Saving new information into the database.
* Asking the database for information that we stored.
* Complex field types to model real world problems.

With this ability to store data
into a database,
**you have all the core tools
for building an interactive website
for your users!**
{{< web >}}
In this series,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
we have examined:

* URL handling
* views to run your code and business logic
* templates to display your user interface
* forms to let users input and interact with your site
* models to store data into a database for long term storage

This is the core set of features
that most websites have.
Since we've seen the core topics
that make Django sites work,
we're ready to focus our attention
on some of the other amazing tools
that set Django apart
from the pack.

First on the list is the built-in
Django administrators site
that let's you explore the data
that you store
in your database.
We'll cover:

* What the Django admin site is
* How to make your models appear in the admin
* How to create extra actions that your admin users can do

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
