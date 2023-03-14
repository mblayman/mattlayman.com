---
title: "Time Travel with django-simple-history"
description: >-
    Are you tired of manually tracking changes to your Django models? Say hello to django-simple-history! This powerful package allows you to easily keep track of modifications made to your models over time. With django-simple-history, you can retrieve historical records for a model, track changes made by different users, and display historical data in the Django admin interface.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - django-simple-history

---

If you're interested in Django development, you might have come across the `django-simple-history` package. It's a great tool that can help you keep track of changes made to your models over time. In this article, we'll take a closer look at `django-simple-history` and how it can benefit your projects.

## What is `django-simple-history`?

{{< extlink "https://django-simple-history.readthedocs.io/en/latest/index.html" "django-simple-history" >}} is a third-party Django package that provides version control for your models. It allows you to keep track of changes made to your models, including who made the change, when it was made, and what the change was.

This package creates a new table in your database to store the history of your models. Every time a model is saved or deleted, a new record is added to the history table. This record contains all of the fields from the original model, as well as additional metadata about the change.

The django-simple-history package provides a number of features to help you use version control with your models. These include:

 * A simple interface for accessing the history of a model
 * A manager for retrieving historical records of a model
 * Integration with Django's admin interface to display historical records
 * Customizable settings to control the behavior of the history tracking

## Getting started with `django-simple-history`

To get started with `django-simple-history`, you'll need to install it using pip:

```bash
pip install django-simple-history
```

Once you've installed the package, you'll need to add it to your Django project's `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    # ...
    'simple_history',
    # ...
]
```

Next, you'll need to add the `HistoricalRecords` manager to the models that you want to track:

```python
from django.db import models
from simple_history.models import HistoricalRecords

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()

    history = HistoricalRecords()
```

With this setup, `django-simple-history` will automatically track changes made to the `Book` model. You can access the history of a book instance using the `history` attribute:

```python
book = Book.objects.create(
  title='The Catcher in the Rye',
  author='J.D. Salinger',
  published_date=datetime.date.fromisoformat('1951-07-16')
)

book.title = 'The Catcher in the Rye (Revised Edition)'
book.save()

history = book.history.all()
```

In this example, we've created a new `Book` instance and made a change to its title field. After saving the change, we can access the book's history using the `history` attribute. This will return a queryset containing all of the historical records for the book.

## Using `django-simple-history` with Django's admin interface

One of the great features of `django-simple-history` is its integration with Django's admin interface. With just a few extra lines of code, you can display the history of your models directly in the admin interface.

To do this, you'll need to create a subclass of `SimpleHistoryAdmin` for each model that you want to track. Here's an example for the `Book` model:

```python
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Book

@admin.register(Book)
class BookAdmin(SimpleHistoryAdmin):
    pass
```

With this setup, you'll be able to view the history of a book instance directly in the admin interface.

## Customizing django-simple-history

`django-simple-history` provides a number of settings
that you can use to customize its behavior. Here are a few examples:

* `SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD` - Allows users to specify a reason for the change when making modifications to a model. The reason is stored in a text field in the historical record.
* `SIMPLE_HISTORY_HISTORY_ID_USE_UUID` - Uses a UUID for the `history_id` field.
* `SIMPLE_HISTORY_REVERSE_ATTR_NAME` - Changes the name of the related field used to access the historical records of a model.

## Conclusion

`django-simple-history` is a powerful tool that can help you keep track of changes made to your models over time. By using this package, you can easily retrieve historical records for a model, track changes made by different users, and display historical data in the Django admin interface.

In this article, we've covered the basics of `django-simple-history`, including how to install it, add it to your models, and customize its behavior. We've also shown how you can use `django-simple-history` with Django's admin interface to display historical data for your models.

If you're looking for a way to add version control to your Django projects, `django-simple-history` is definitely worth checking out. With its powerful features and easy-to-use interface, it can help you track changes to your models and maintain a complete history of your data.
