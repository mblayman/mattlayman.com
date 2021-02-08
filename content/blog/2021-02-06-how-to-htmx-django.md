---
title: "How To Use Htmx In Django"
description: >-
    How do you use htmx (the lightweight JavaScript library
    that uses HTML markup)
    in Django?
    This article shows how and provides an example usage.
image: img/2021/htmx-django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - htmx

---

This article show you
how to use htmx in Django.
What is htmx?
According to the {{< extlink "https://htmx.org/" "htmx website" >}}:

> htmx allows you to access AJAX, CSS Transitions, WebSockets
and Server Sent Events directly in HTML, using attributes,
so you can build modern user interfaces with the simplicity
and power of hypertext.

The example that we'll craft
is an ability to delete a task
from a list of tasks
without reloading the whole page.

## Step 1: Add The Script

Here's a base template
for our example
that I'll store in `base.html`.

```html
<html>
  <head><title>Htmx Demo!</title></head>
  <body>
    {% block main %}{% endblock %}
    <script src="https://unpkg.com/htmx.org@1.1.0"></script>
    <script>
      document.body.addEventListener('htmx:configRequest', (event) => {
        event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
      })
    </script>
  </body>
</html>
```

The critical element to this template
(and the impetus for this entire article!)
is the event listener
after the script that includes htmx.

Because htmx uses HTTP methods other
than GET,
Django will expect a CSRF security token
in the requests.
The small function added
in the script block ensures
that htmx AJAX requests
includes a CSRF token
that allows non-GET requests
to work.

If you don't include this configuration,
Django will respond to requests
with a `403 Forbidden` status code.

## Step 2: Create The Tasks List View

We need a view to display tasks.
Let's assume that we have a `Task` model
that includes a `description` text field.

```python
# application/views.py

from django.shortcuts import render

from .models import Task

def display_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'display_tasks.html', {'tasks': tasks})
```

```python
# project/urls.py

from django.urls import path

from application.views import display_tasks

urlpatterns = [
    path('tasks/', display_tasks, name='display_tasks'),
]
```

That should be enough
for your Django project
to display the tasks at `/tasks/`.
Let's see the `display_tasks.html` template.

```django
{% extends "base.html" %}

{% block main %}
    <h1>Tasks</h1>
    {% include "tasks_list.html" %}
{% endblock %}
```

That template depends on `tasks_lists.html`
which looks like:

```html
<div id="tasks">
  {% for task in tasks %}
    <div>{{ forloop.counter }} {{ task.description }}</div>
  {% endfor %}
</div>
```

This version of the view doesn't use htmx
or have the ability
to delete a task.
The view will display a numbered list
of items.
(Yes,
I recognize that this could have used an `ol` tag,
but use your imagination
that the layout is much more complicated
than this example.)

## Step 3: Add The Delete Task View

I included the for loop to illustrate a point.
What happens if you delete a row
via JavaScript
and remove the div from the DOM?
The numbering is going to be messed up
since a number value will be missing!

Our htmx solution will solve that issue.
Let's see the view.

```python
# application/views.py

from django.views.decorators.http import require_http_methods

...

@require_http_methods(['DELETE'])
def delete_task(request, id):
    Task.objects.filter(id=id).delete()
    tasks = Task.objects.all()
    return render(request, 'tasks_list.html', {'tasks': tasks})
```

Observe that this DELETE view returns an HTML response
of the `tasks_list.html` partial template.
This is crucial for htmx
because the library will use that content.

```python
# project/urls.py

from django.urls import path

from application.views import delete_task, display_tasks

urlpatterns = [
    path('tasks/', display_tasks, name='display_tasks'),
    path('tasks/<int:id>/delete/', delete_task, name='delete_task'),
]
```

Now that we have the delete view,
we can add the new functionality
and use htmx.

```html
<div id="tasks"
  hx-confirm="Are you sure you want to delete this task?"
  hx-target="#tasks"
  hx-swap="outerHTML">
  {% for task in tasks %}
    <div>{{ forloop.counter }} {{ task.description }}
      <a class="block mr-2 hover:text-gray-600"
        hx-delete="{% url 'delete_task' task.id %}">
        Delete?
      </a>
    </div>
  {% endfor %}
</div>
```

Here's how this flows:

* When a user clicks "Delete?," that user will be prompted
    with a standard browser alert box
    with the question from `hx-confirm`.
    This works for each task `div`
    because htmx will inherit attributes
    from its parent content.
    Using attributes from parents can reduce the amount
    of extra markup in your output.
* If the user confirms,
    htmx will send a `DELETE` request
    to a URL like `/tasks/42/delete/`
    because of `hx-delete`.
* The delete view will delete the task
    from the database
    and return a new list (properly numbered!)
    in the response.
* Htmx will take the response
    and set the content
    in `hx-target`.
    The `hx-swap` instructs htmx how to place the new content.
    The default sets the inner HTML,
    but we want to replace the `tasks` ID completely
    since the partial template
    includes a new `tasks` ID.

This example is simplified
on purpose
so you can probably see ways
to do this using POST
and redirects,
but that's not quite the point
I'm trying to make.
Because htmx can swap
in content,
the tool opens all kinds
of options
to modify a page dynamically
and drive that content using views
and server side rendering.

I hope you see the value and simplicity
that htmx provides
from reviewing this example.
I'm excited to use htmx
in my projects
to sprinkle in dynamic functionality
while minimizing the amount of JavaScript
that I have to write.

## Learn More

Do you want to learn how Django works
or what Django is used for?
Then I suggest you check out my
[Understand Django]({{< ref "/understand-django/_index.md" >}})
series of articles next.
In that series,
I explain Django
to new (and old!) web developers.
I think it will help you
on your journey to becoming a Django dev.

Subscribe to my [newsletter]({{< ref "/newsletter.md" >}})
and follow me
{{< extlink "https://twitter.com/mblayman" "on Twitter" >}}
to learn more about Django
as I release new content.
