---
title: "Episode 7 - Models and Managers and Querysets, Oh My!"
aliases:
 - /django-riffs/7
 - /djangoriffs/7
description: >-
    On this episode,
    we will explore more about models
    and how to interact with data
    in your database.
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
we will explore more about models
and how to interact with data
in your database.

Listen at {{< extlink "https://djangoriffs.com/episodes/models-managers-querysets" "djangoriffs.com" >}}.

## Last Episode

On the last episode,
we discussed the basics
of setting up a database
and creating a model
to store data.

## Working With Models

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

What does an SQL query look like?
If we save our model example from the last episode,
it would look something like:

```sql
INSERT INTO "application_employee" ("first_name", "last_name", "job_title")
    VALUES ('Tom', 'Bombadil', 'Old Forest keeper')
```

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
SELECT "application_employee"."id",
    "application_employee"."first_name",
    "application_employee"."last_name",
    "application_employee"."job_title"
    FROM "application_employee"
    WHERE "application_employee"."first_name" = Bob
```

What if you want to delete an employee record?

```python
>>> from application.models import Employee
>>> # The price is wrong, Bob!
>>> Employee.objects.filter(first_name='Bob', last_name='Barker').delete()
(1, {'application.Employee': 1})
```

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

employees = Employee.objects.all()  # employees is a QuerySet of all rows!

if should_find_the_bobs:
    employees = employees.filter(first_name='Bob')  # New queryset!
```

Here's are some other `QuerySet` methods
that I use constantly:

* `create` - As an alternative to creating a record instance
    and calling `save`,
    the manager can create a record directly.

```python
Employee.objects.create(first_name='Bobby', last_name='Tables')
```

* `get` - Use this method when you want one
    *and exactly one* record.
    If your query doesn't match
    or will return multiple records,
    you'll get an exception.

```python
the_bob = Employee.objects.get(first_name='Bob', last_name='Marley')

Employee.objects.get(first_name='Bob')
# Raises application.models.Employee.MultipleObjectsReturned

Employee.objects.get(first_name='Bob', last_name='Sagat')
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
Employee.objects.filter(first_name='Bob').update('Robert')
```

* `exists` - Use this method if you want to check
    if rows exist in the database
    that match the condition you want to check.

```python
has_bobs = Employee.objects.filter(first_name='Bob').exists()
```

* `count` - Check how many rows match a condition.
    Because of how SQL works,
    note that this is more efficient
    than trying to use `len` on a queryset.

```python
how_many_bobs = Employee.objects.filter(first_name='Bob').count()
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
>>> a_bob = Employee.objects.filter(first_name='Bob').order_by(
...     'last_name').last()
>>> print(a_bob.last_name)
Ross
```

## Types Of Model Data

When we discussed forms,
we saw
that Django's form system
includes a wide variety
of form fields.
If you look at the
{{< extlink "https://docs.djangoproject.com/en/3.0/ref/forms/fields/" "Form fields" >}} reference
and compare the list
of types
to those in the
{{< extlink "https://docs.djangoproject.com/en/3.0/ref/models/fields/" "Model field reference" >}},
you can observe a lot of overlap.

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

class DungeonsAndDragonsCharacter(models.Model):
    name = models.CharField(max_length=100, default='Conan')
    # Important to note: Pass the function, do not *call* the function!
    strength = models.IntegerField(default=strength_generator)
```

* `unique` - When a field value must be unique
    for all the rows in the database table,
    use `unique`.
    This is a good attribute
    for identifiers
    where you don't expect duplicates.

```python
class ImprobableHero(models.Model):
    name = models.CharField(max_length=100, unique=True)

# There can be only one.
ImprobableHero.objects.create(name='Connor MacLeod')
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
    weight = models.IntegerField(null=True)
```

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

```python
class Pet(models.Model):
    # Not all pets have tails so we want auto-generated forms
    # to allow no value.
    length_of_tail = models.IntegerField(null=True, blank=True)
```

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

```python
class Car(models.Model):
    COLOR_CHOICES = [
        (1, 'Black'),
        (2, 'Red'),
        (3, 'Blue'),
        (4, 'Green'),
        (5, 'White'),
    ]
    color = models.IntegerField(choices=COLOR_CHOICES, default=1)
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
            'For policies that only apply on leap days'
            ' in accordance with Section 987.123'
            ' of the Silly Draconian Order'
        )
    )
```

## What Makes A Database "Relational?"

An overly simplified model
for an employee
with multiple phone numbers might look like:

```python
# application/models.py
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=200)
    phone_number_1 = models.CharField(max_length=32)
    phone_number_2 = models.CharField(max_length=32)
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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=200)

class PhoneNumber(models.Model):
    number = models.CharField(max_length=32)
    PHONE_TYPES = (
        (1, 'Mobile'),
        (2, 'Home'),
        (3, 'Pager'),
        (4, 'Fax'),
    )
    phone_type = models.IntegerField(choices=PHONE_TYPES, default=1)
```

```python
...

class PhoneNumber(models.Model):
    number = models.CharField(max_length=32)
    PHONE_TYPES = (
        (1, 'Mobile'),
        (2, 'Home'),
        (3, 'Pager'),
        (4, 'Fax'),
    )
    phone_type = models.IntegerField(choices=PHONE_TYPES, default=1)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
```

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
tom = Employee.objects.get(first_name='Tom', last_name='Bombadil')
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

There is another relational field type
that we should spend time on.
That field is the `ManyToManyField`.
As you might guess,
this field is used when two types
of data relate to each other
in a many to many fashion.

What if we tried to model this with `ForeignKey` fields?

```python
# application/models.py
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

class House(models.Model):
    address = models.CharField(max_length=256)
    resident = models.ForeignKey(Person, on_delete=models.CASCADE)
```

```python
# application/models.py
from django.db import models

class House(models.Model):
    address = model.CharField(max_length=256)

class Person(models.Model):
    name = models.CharField(max_length=128)
    house = models.ForeignKey(House, on_delete_models.CASCADE)
```

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
    name = models.CharField(max_length=128)

class House(models.Model):
    address = models.CharField(max_length=256)
    residents = models.ManyToManyField(Person)
```

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

We can access the many side
of each model using a queryset.
`residents` will be a `ManyRelatedManager`
and, like other managers,
can provide querysets
by using certain manager methods.

```python
house = House.objects.get(address='123 Main St.')
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

This is how we can use Django models
to interact with data.
We saw:

* Saving new information into the database.
* Asking the database for information that we stored.
* Complex field types to model real world problems.

## Next Time

In the next episode,
we are going to explore Django's built-in
administrative tools
and look at the Django admin site.

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
