---
title: "Episode 8 - Administering Your App"
aliases:
 - /django-riffs/8
 - /djangoriffs/8
 - /django-riffs/8.
 - /djangoriffs/8.
description: >-
    On this episode,
    we will focus
    on the built-in Django administrator's site.
    We'll see what it is,
    how you can configure it,
    and how you can customize it
    to serve your needs.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - admin

---

On this episode,
we will focus
on the built-in Django administrator's site.
We'll see what it is,
how you can configure it,
and how you can customize it
to serve your needs.

Listen at {{< extlink "https://djangoriffs.com/episodes/administering-your-app" "djangoriffs.com" >}}.

## Last Episode

On the last episode,
we explored more about models
and how to interact with data
in your database.

## What Is The Django Admin?

Django includes a web administrative interface
that can help programmers and non-programmers alike.
This administrative interface is usually called the Django admin,
for short.

Like so many other extensions
in the Django ecosystem,
the admin site is a Django application.
The site is so commonly used
that it is pre-configured
when you run the `startproject` command.

The admin site provides tools
for doing create, read, update, or delete operations.
There are a few main pages
that you can navigate
when working in a Django admin site
that direct where the CRUD operations happen.

1. Admin index page -
    This page will show all the models,
    grouped by the Django application they originate from,
    that are registered with the admin.
2. Model list page -
    The list page shows rows of data
    from a model (i.e., a database table).
    From this page,
    an administrator can perform actions
    on multiple database records
    like deleting a set of records
    in a single operation.
3. Add model page -
    The admin provides a page
    where new model instances can be created
    using automatically generated forms
    based on the model's fields.
4. Model change page -
    The change page lets you update an existing model instance
    (i.e., a database table row).
    From this page,
    you can also delete a model instance.

Now that we understand what is in the admin site,
let's focus on how to add your models to the admin.

## Register A Model With The Admin

To make the admin site show your model data,
we need to update `admin.py`.
On a new application created
with `startapp`,
you'll find
that the `admin.py` file is largely empty.
We need to provide a bit
of glue
so that the admin knows
about a model.

The admin site expects a `ModelAdmin` class
for every model
that you want to see displayed
within the site.

```python
# application/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
```

```python
# application/admin.py
from django.contrib import admin

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass
```

There are a couple of important items
to observe
with this `admin.py` file.

1. The `BookAdmin` is a subclass
    of `admin.ModelAdmin`.
2. The `BookAdmin` is registered
    with the admin site
    by using the `admin.register` decorator.

```bash
$ ./manage.py createsuperuser
Username: matt
Email address: matt@somewhere.com
Password:
Password (again):
Superuser created successfully.
```

With a superuser account available,
you're ready to log in
to the admin site.
Because you'll be using a superuser account,
you will have permission
to see every model
that is registered
with the admin site.

## Customizing Your Admin

Making effective admin pages is primarily about
using these attributes
so that the `ModelAdmin` class will do what you want.
As such,
mastering the Django admin site
is all about mastering the `ModelAdmin` options
that are listed
{{< extlink "https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#modeladmin-options" "in the documentation" >}}.
That list is long,
but don't be discouraged!
I think that you can get about 80%
of the value out of the Django admin
by knowing only a handful
of the options.

Let's start with `list_display`.
This `ModelAdmin` attribute controls
which fields will appear
on the list page.
With our book model example,
we could add the title to the page.

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
```

```python
# application/models.py

class Book(models.Model):
    class Category(models.IntegerChoices):
        SCI_FI = 1
        FANTASY = 2
        MYSTERY = 3
        NON_FICTION = 4

    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    category = models.IntegerField(
        choices=Category.choices, default=Category.SCI_FI)
```

By using the `list_filter` attribute,
we can give the admin list page the ability
to filter to the category
that we want.

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('category',)
```

This isn't the only kind
of filtering that the admin can do.
We can also filter in time
with the `date_hierarchy` field.
Next,
let's give the model a `published_date`.

```python
# application/models.py

class Book(models.Model):
    class Category(models.IntegerChoices):
        SCI_FI = 1
        FANTASY = 2
        MYSTERY = 3
        NON_FICTION = 4

    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    category = models.IntegerField(
        choices=Category.choices, default=Category.SCI_FI)
    published_date = models.DateField(default=datetime.date.today)
```

We can can also change the `ModelAdmin`
to use the new field.

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
```

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
```

With this setting,
all of the books
on the page
will be ordered by the title.
The `ordering` attribute will add an appropriate
`ORDER BY` clause to the database query
via the admin-generated ORM `QuerySet`.

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
    search_fields = ("author",)
```

With this option,
this list page will add a search bar
to the top of the page.
In the example,
I added the ability to search based
on the author
of the book.

The results wouldn't compete well
compared to a dedicated search engine,
but getting a decent search feature
for a single line of code is awesome!

The `ModelAdmin` also includes some useful settings
to modify the behavior
of the detail page
of particular database records.

```python
# application/models.py
from django.contrib.auth.models import User

class Book(models.Model):
    class Category(models.IntegerChoices):
        SCI_FI = 1
        FANTASY = 2
        MYSTERY = 3
        NON_FICTION = 4

    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    category = models.IntegerField(
        choices=Category.choices, default=Category.SCI_FI)
    published_date = models.DateField(default=datetime.date.today)
    editor = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
```

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
    raw_id_fields = ("editor",)
    search_fields = ("author",)
```

By using `raw_id_fields`,
the admin changes from using a dropdown
to using a basic text input
which will display the foreign key
of the user record.
Seeing a foreign key number is visually less useful
than seeing the actual name selected
in a dropdown,
but the `raw_id_fields` option adds two features
to alleviate this.

1. A search icon is present.
    If users click on the icon,
    a popup window appears
    to let the user search
    for a record
    in a dedicated selection interface.
2. If the record already has a foreign key
    for the field,
    then the string representation
    of the record
    will display next to the icon.

```python
# application/models.py

class Book(models.Model):
    class Category(models.IntegerChoices):
        SCI_FI = 1
        FANTASY = 2
        MYSTERY = 3
        NON_FICTION = 4

    title = models.CharField(max_length=256)
    slug = models.SlugField()
    author = models.CharField(max_length=256)
    category = models.IntegerField(
        choices=Category.choices, default=Category.SCI_FI)
    published_date = models.DateField(default=datetime.date.today)
    editor = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
```

What is the benefit
of `prepopulated_fields`?
By using this option,
we can instruct the admin site
to populate the `slug` field
based on the `title`
of the book.
Here's the update to the `ModelAdmin`.

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("editor",)
    search_fields = ("author",)
```

Now when we want to add a new book
in the admin,
Django will use some JavaScript
to update the slug field dynamically
as we type the title!

All of the options
that we've examined
have an equivalent method you can override
that is prefixed
with `get_`.
For instance,
if we want to control
what fields users see
on the list page
based on who they are,
we would implement `get_list_display`.
In that method,
we would return a tuple
based on the user's access level.

```python
# application/models.py

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
```

To show other models
on a detail page,
we need to create an inline class
and include it
with the `ModelAdmin`.
The result looks like:

```python
# application/admin.py
from django.contrib import admin

from .models import Book, Review

class ReviewInline(admin.TabularInline):
    model = Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    inlines = [ReviewInline]
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
    raw_id_fields = ("editor",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("author",)
```

We've covered many options
of the `ModelAdmin` class
that you can use
to customize your admin experience
with common functions
that many admin tools require.
**What about the *uncommon* functions?**
For extra customization,
we can use admin actions.

## Taking Action In The Admin

When you want to do work
related to specific records
in your database,
Django provides some techniques
to customize your site
and provide those capabilities.
These customizations are called *actions*
and they appear
on the list page
above the list
of records.

An action method must follow this interface:

```python
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    actions = ['do_some_action']

    def do_some_action(
            self,
            request: HttpRequest,
            queryset: QuerySet
        ) -> Optional[HttpResponse]:
        # Do the work here.
        ...
```

```python
# application/admin.py

def update_premiere(book):
    """Pretend to update the book to be a premiere.

    This function is to make the demo clear.
    In a real application, this could be a manager method instead
    which would update the book and trigger the email notifications
    (e.g., `Book.objects.update_premiere(book)`).
    """
    print(f"Update {book.title} state to change premiere books.")
    print("Call some background task to notify interested users via email.")

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    actions = ["set_premiere"]
    date_hierarchy = "published_date"
    inlines = [ReviewInline]
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
    raw_id_fields = ("editor",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("author",)

    def set_premiere(self, request, queryset):
        if len(queryset) == 1:
            book = queryset[0]
            update_premiere(book)
```

We were able to extend the admin
and hook into the page's user interface
by defining a method
and declaring it as an action.
This is a powerful system
to give administrators control
and allow them
to operate
in custom ways
on the data
in their applications.

## Summary

In this episode,
we looked
at the built-in Django administrator's site.
This powerful extension gives us the ability
to create, view, edit, and delete rows
from database tables associated
with your application's models.

We've covered:

* What the Django admin site is
    and how to set it up
* How to make your models appear in the admin
* How to customize your admin pages quickly
    with options
    provided by the `ModelAdmin` class
* How to create extra actions
    that enable you to do work
    on your model records

## Next Time

In the next episode,
we will cover
the anatomy
of a Django application.
A Django project is composed
of many applications
and we will dig into what an application looks like.

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
