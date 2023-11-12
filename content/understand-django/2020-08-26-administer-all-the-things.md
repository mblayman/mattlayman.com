---
title: "Administer All The Things"
description: >-
    This article will look
    at how maintainers
    of an application
    can manage their data
    through Django's built-in administrative tools.
    We will see how to build admin pages
    and customize the admin tools
    to help teams navigate their apps.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - admin
series: "Understand Django"

---

{{< web >}}
In the previous
[Understand Django]({{< ref "/understand-django/_index.md" >}})
article,
we used models
to see how Django stores data
in a relational database.
{{< /web >}}
We covered all the tools
to bring your data to life
in your application.
{{< web >}}
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
we will focus
on the built-in tools
that Django provides
to help us manage that data.

{{< understand-django-series "admin" >}}

## What Is The Django Admin?

When you run an application,
you'll find data
that needs special attention.
Maybe you're creating a blog
and need to create and edit tags or categories.
Perhaps you have an online shop
and need to manage your inventory.
Whatever you're building,
you'll probably have to manage *something*.

How can you manage that data?

* If you're a programmer,
    you can probably log into your server,
    fire up a Django management shell,
    and work with data directly
    using Python.
* If you're not a programmer,
    well,
    I guess you're out of luck!
    **Nope, that's not true!**

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

Before proceeding,
I'd first like to make note of a security issue.
When using `startproject`,
Django will put the admin site
at `/admin/`
by default.
**Change this**.
The starter template conveniently sets up the admin site
for you,
but this default URL makes it easy
for {{< extlink "https://en.wikipedia.org/wiki/Script_kiddie" "script kiddies" >}}
to try to attack your admin site
to gain access.
Putting your admin site on a different URL *won't* fully protect your site
(because you should never rely
on "security through obscurity"),
but it will help avoid a large amount
of automated attacks.

The Django admin gives you a quick ability
to interact
with your models.
As you will see shortly,
you can register a model
with the admin site.
Once the model is registered,
you can use the site interface
to perform CRUD operations
on the data.

CRUD is an acronym
that describes the primary functions
of many websites.
The acronym stands for:

* **Create** - A website can create data (i.e., insert data into the database)
* **Read** - Users can see the data
* **Update** - Data can be updated by users
* **Delete** - A user can delete data from the system

If you think about the actions
that you take on a website,
most actions will fall
into one of those four categories.

The admin site provides tools
for doing all of those operations.
There are a few main pages
that you can navigate
when working in a Django admin site
that direct where the CRUD operations happen.
These pages are available to you
with very little effort
on your part
aside from the registration process
that you'll see
in the next section.

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

If you inspect this small set of pages,
you'll notice
that every part of the CRUD acronym can occur
in this admin site.
{{< web >}}
The power to create and destroy is in your hands. 😈
{{< /web >}}
{{< book >}}
The power to create and destroy is in your hands.
{{< /book >}}

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

Let's consider a crude modeling
of a book.

```python
# application/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(
        max_length=256
    )
    author = models.CharField(
        max_length=256
    )
```

Now we can create a `ModelAdmin` class
for the `Book` model.

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

You can also register an admin class
by calling `register`
after the class
if you don't want to use a decorator.

```python
# application/admin.py
from django.contrib import admin

from .models import Book

class BookAdmin(admin.ModelAdmin):
    pass

admin.site.register(Book, BookAdmin)
```

Now that we have a model registered
with the admin site,
how do we view it?
Fire up your trusty development server
with `runserver`
and visit the URL
that used to be `/admin/`
(because you did change
to something different from `/admin/`, right? Right!?).

On this page,
you'll encounter a login screen.
We haven't worked through the authentication system yet,
but, for now,
we can understand that only user accounts
that have a staff level permission
can log in.

Django provides a command
that will let us create a user account
with staff level permission
and all other permissions.
Like Linux operating systems,
the user account
with all permissions
is called a superuser.
You can create a superuser account
with the `createsuperuser` command.

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

Once you've logged in,
you can view the `Book` model's admin page.
Poke around!
Create a book with the "Add Book" button.
View the list page.
Edit the book.
Delete the book.
You can see that with a tiny amount
of work
on your part,
Django gives you a full CRUD interface
for interacting with your model.

We added the most simple `ModelAdmin` possible.
The body of the class was a `pass`
instead of any attributes.
Django gives us a ton
of options
to let us control how our admin pages
for `Book` will behave.
Let's go on a tour
of some commonly used admin attributes.

## Customizing Your Admin

Like many other parts of Django,
the framework uses class level attributes
to define the behavior
of a class.
Unlike forms and models
where class level attributes are mostly fields
that you're defining
for yourself,
`ModelAdmin` classes provide values
for attributes
that are well defined
in the documentation.
These attributes act as hooks
that let you customize the behavior
of your admin pages.

Making effective admin pages is primarily about
using these attributes
so that the `ModelAdmin` class will do what you want.
As such,
mastering the Django admin site
is all about mastering the `ModelAdmin` options
that are listed
{{< extlink "https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#modeladmin-options" "in the documentation" >}}.
That list is long,
but don't be discouraged!
I think that you can get about 80%
of the value out of the Django admin
by knowing only a handful
of the options.

When you poked around
on the `Book` pages,
you probably noticed
that the listing of books is quite bland.
The default list looks something
like a list of links
that show `Book object (#)`.
We can change the look and utility
of this page
with a few different settings.

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

Django will make whatever is listed first
into the link
that a user can click
to view the admin detail page
for a model record.
In this example,
I'm using the `id` field
as the link,
but I could have used a single element tuple
of `('title',)` to make the page show
only the titles
with the titles
being the links.

Sometimes you will have a type of model
where you only want to see a subset
of the records.
Suppose that the `Book` model has a category field.

```python
# application/models.py

class Book(models.Model):
    class Category(
        models.IntegerChoices
    ):
        SCI_FI = 1
        FANTASY = 2
        MYSTERY = 3
        NON_FICTION = 4

    # ... title and author from before

    category = models.IntegerField(
        choices=Category.choices,
        default=Category.SCI_FI
    )
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

The option will put a sidebar
on the right side
of the admin page.
In that sidebar,
you would see the categories
that I included
in the `Category` choices class.
If I click on the "Fantasy" link,
then my browser will navigate
to `/admin/application/book/?category__exact=2`
and will only display database rows
that have a matching category.

This isn't the only kind
of filtering that the admin can do.
We can also filter in time
with the `date_hierarchy` field.
Next,
let's give the model a `published_date`.

```python
# application/models.py

class Book(models.Model):
    # ... title, author, category

    published_date = models.DateField(
        default=datetime.date.today
    )
```

We can also change the `ModelAdmin`
to use the new field.

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
```

By including the `date_hierarchy` attribute,
the list page will contain some new user interface elements.
Across the top of the page will be selectors
to help filter down to the right time range.
This is a very useful way to look through your database table.

We can still go further.
Perhaps we want all of the books to be sorted
by their titles.
Even if the `ordering` attribute is not set
on the model's meta options,
the `ModelAdmin` has its own `ordering` attribute.

*What's "meta?"*
Aside from fields,
a Django model can set extra information
about how to handle data.
These extra options are the "meta" attributes
of the model.
A Django model adds meta info
by including a nested `Meta` class
on the model.
Check out the
{{< extlink "https://docs.djangoproject.com/en/4.1/ref/models/options/" "Model Meta options" >}}
to see what other features are available
to customize model behavior.

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

The final convenient list page option
that I want to highlight
is the `search_fields` option.

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

When you search,
your resulting URL could look
{{< web >}}
like `/admin/application/book/?q=tolkien`.
{{< /web >}}
{{< book >}}
like `/admin/application/book/? q=tolkien`.
{{< /book >}}
Django will do a case insensitive search
on the field.
The `QuerySet` would be something like:

```python
search_results = Book.objects.filter(
    author__icontains="tolkien"
)
```

The results wouldn't compete well
compared to a dedicated search engine,
but getting a decent search feature
for a single line of code is awesome!

The `ModelAdmin` also includes some useful settings
to modify the behavior
of the detail page
of particular database records.

For instance,
let's assume
that the `Book` model
has a `ForeignKey`
to track an editor.

```python
# application/models.py
from django.contrib.auth.models import User

class Book(models.Model):
    # ... title, author, category
    # published_date from before

    editor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
```

On the admin page
for an individual book,
the `editor` field will be a dropdown
by default.
This field will include every `User` record
in your application.
If you have a popular site
with thousands or millions of users,
the page would be crushed
under the weight
of loading all those user records
into that dropdown.

Instead of having a useless page
that you can't load,
you can use `raw_id_fields`.

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

Another option that can be useful
is the `prepopulated_fields` option.
Back in our discussion
of URLs,
we talked about slug fields.
Slugs are often used
to make pleasant URLs
for detail pages
showing an individual model instance.
Let's add a `SlugField`
to the `Book` model.

```python
# application/models.py

class Book(models.Model):
    # ... title, author, category
    # published_date, editor from before

    slug = models.SlugField()
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

To this point,
every attribute that we've added
to the admin
is static configuration.
What do you do if you want to vary
how the admin pages behave
based on something dynamic?

Thankfully,
the Django team thought of that too.
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
# application/admin.py
from django.contrib import admin

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    ...

    def get_list_display(self, request):
        if request.user.is_superuser:
            return (
                'id',
                'title',
                'author',
                'category',
            )

        return ('id', 'title')
```

One final attribute to consider
is called `inlines`.
I don't reach for this option often,
but it's a convenient way
to see *other* models
that are related to a particular model.

Suppose our sample application has reviews
for books.
We could add a model like:

```python
# application/models.py

class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
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

By adding the inline class
to the list of `inlines`,
the detail page will show any reviews
that are associated
with a book.
Additionally,
you could create new reviews
from the detail page
since the admin will include a few blank forms
by default.

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

In the default admin site,
there is an action
that lets administrators delete records.
If you select some rows
with the checkboxes
on the left hand side,
select "Delete selected \<object type\>",
then click "Go",
you will be presented
with a page
that asks for confirmation
about deleting the rows you picked.

The same kind of flow could be applied
for any actions
that you want
to perform
on database records.
We can do this
by adding a method
on our `ModelAdmin`.

The method must follow this interface:

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

The queryset will represent the set
of model records
that the user selected.
If the method returns `None`,
then the user will be returned
to the same admin page.
If the method returns an `HttpResponse`,
then the user will see that response
(which is what happens
with the delete confirmation page
of the delete action).
Whatever you do between the method being called
and the method returning
is up to you.

Maybe our sample book application
could set a book
to premiere
on the site
as an important new available title.
In this hypothetical scenario,
we might have code
that unsets any older premiere book
or sends out emails
to people who have expressed interest
when new premieres are announced.

For this scenario,
we could add an action
that would do these things.

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

    def set_premiere(
        self,
        request,
        queryset
    ):
        if len(queryset) == 1:
            book = queryset[0]
            update_premiere(book)
```

Django will use the name
of the method
to set the label
for the dropdown
on the list page.
In this case,
the action label will be "Set premiere".

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

{{< web >}}
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
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

{{< web >}}
Next time we will cover
{{< /web >}}
{{< book >}}
In the next chapter we will cover
{{< /book >}}
the anatomy
of a Django application.
A Django project is composed
of many applications.
We will explore:

* The conventional structure of a Django app
* How Django identifies and loads applications
* Why applications are crucial for the Django ecosystem

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
