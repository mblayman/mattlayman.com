---
title: "Announcing django-denied"
description: >-
    Django has a new authorization option
    with django-denied.
    This new package makes authorization checks required
    for all of your views
    in your Django app.
image: /staticimg/2022/lock.jpg
categories:
  - Python
  - Django
tags:
  - Python
  - Django
  - authorization
slug: announcing-django-denied
date: 2022-08-01
---

I have paranoia
when it comes to my Django app.

I run a homeschool scheduling service called
[School Desk](https://www.theschooldesk.app/).
My Software as a Service (SaaS) lets families plan their homeschool activities.
Since the app deals with data about students
(including *my* kids!),
it's important to me
that every user's data is protected,
so that users can only view their own information.

When I designed the system,
I picked a shared Postgres schema
(i.e., all courses, regardless of user, are in a single database table).
With this design,
I need authorization checks to guarantee
that one user can't access another user's data.

My paranoia made me worry
that I would forget an authorization check
and allow access to everyone,
or, *worse*,
forget `login_required` and expose data
to the public internet.

I wanted the peace of mind
that my views were safe by default.

I created a new Django package to help me achieve this peace of mind.

## django-denied

[django-denied](https://pypi.org/project/django-denied/)
is an authorization package
that *denies **all** views by default.*

With django-denied,
as a baseline,
all views require authentication unless exempted
with an `allow` decorator.
But that's still not enough to access a view.
As a developer,
I *must* add an authorization check
to permit access to the view.
If I forget the authorization check,
django-denied will intercept a request
and return a `403 Forbidden` response.

Using this allow list style,
it's impossible for me
to make a working view
without including authorization.

> Authorization is a requirement
for all views to work.

If this approach sounds useful
to your app
or future project,
check out the package and let me know what you think!

## Example

This is the example
that I've included in the documentation
in case you don't want to click over
to the package's page.

<hr>

This section shows a more complete example
of an authorizer
to give you a sense
of how django-denied works in practice.

For our example,
we'll consider a project tracking application.
This is little more than a TODO list
that groups the tasks into projects.

Here are the models.

```python
# application/models.py
from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    completed = models.BooleanField(default=False)
```

For this simple system,
only project owners can do anything
with a task.
Let's create the authorizer for that.

```python
# application/authorizers.py


def task_authorized(request, **view_kwargs):
    return Task.objects.filter(
        project__owner=request.user,
        pk=view_kwargs["pk"],
    ).exists()
```

These are the URLs we want to support
with this authorizer.

```python
# application/urls.py

from django.urls import path

from .views import task_detail, task_edit

urlpatterns = [
    path("tasks/<int:pk>/", task_detail, name="task_detail"),
    path("tasks/<int:pk>/edit/", task_detail, name="task_edit"),
]
```

Now we can set our views
and set their authorization.

```python
# application/views.py
from denied.decorators import authorize
from django.shortcuts import render

from .authorizers import task_authorized
from .models import Task


@authorize(task_authorized)
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, "task_detail.html", {"task": task})


@authorize(task_authorized)
def task_edit(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, "task_edit.html", {"task": task})
```

Since the authorizer handles the access control,
we can be confident that the task is safe to fetch
by its key alone.
Access control is pushed to the boundary of the view
so that the view's internal logic is about as simple
as you can make it.