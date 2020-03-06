---
title: "Episode 3 - Views On Django"
aliases:
 - /django-riffs/3
 - /djangoriffs/3
description: >-
    On this episode,
    we look at views,
    a major component
    within Django
    and a primary place
    where your code will run.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - views

---

On this episode,
we look at views,
a major component
within Django
and a primary place
where your code will run.

Listen at {{< extlink "https://djangoriffs.com/episodes/views-on-django" "djangoriffs.com" >}}.

## Last Episode

On the previous episode,
we talked about URLs
and how they describe the main interface
that a browser can use
to interact with your application.

## What Is A View?

A view is a chunk of code
that receives an HTTP request
and returns an HTTP response.
Views describe Django's entire purpose:
to respond to requests
made to an application
on the internet.

## Function Views

A function view is exactly that, a function.
The function takes an instance
of `HttpRequest`
as input
and returns an `HttpResponse`
(or one of its many subclasses)
as output.

```python
# application/views.py
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse('Hello World')
```

## HttpRequest

`HttpRequest` is a Python class.
Instances of this class represent an HTTP request.

```http
POST /courses/0371addf-88f7-49e4-ac4d-3d50bb39c33a/edit/ HTTP/1.1
Host: 0.0.0.0:5000
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 155
Origin: http://0.0.0.0:5000
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Pragma: no-cache
Cache-Control: no-cache

name=Science
&monday=on
&tuesday=on
&wednesday=on
&thursday=on
&friday=on
```

When Django receives a request like this,
it will parse the data
and store the data in an `HttpRequest` instance.
Here are some common attributes.

* `method` - This matches the HTTP method of `POST`
    and can be used to act
    on the *kind* of request the user sent.
* `content_type` - This attribute instructs Django
    on how to handle the data
    in the request.
    The example value would be `application/x-www-form-urlencoded `
    to indicate that this is user submitted form data.
* `POST` - For POST requests,
    Django processes the form data
    and stores the data
    into a dictionary-like structure.
    `request.POST['name']` would be `Science`
    in our example.
* `GET` - For a GET request,
    anything added to the query string
    (i.e., the content after a `?` character
    such as `student=Matt`
    in `/courses/?student=Matt` is stored
    in a dictionary-like attribute as well.
* `headers` - This is where all the HTTP headers
    like `Host`, `Accept-Language`,
    and the others are stored.

## HttpResponse

The other major interface
that your views will use
either directly or indirectly
is the `HttpResponse` interface.

Some of the common `HttpResponse` attributes include:

* `status_code` - This is the HTTP status code.
    Status codes are a set of numbers
    that HTTP defines
    to tell a client (i.e., a browser)
    about the success or failure
    of a request.
    `200` is the usual success code.
    Any number from `400` and up will indicate some error
    like `404` when something is not found.
* `content` - This is the content
    that you provide to the user.
    The response stores this data as bytes.
    If you supply Python string data,
    Django will encode to bytes for you.

```python
>>> from django.http import HttpResponse
>>> response = HttpResponse('Hello World')
>>> response.content
b'Hello World'
```

When working with Django views,
you won't always use `HttpResponse` directly.
Some common examples:

* `HttpResponseRedirect` - You may want to send a user
    to a different page.
    Perhaps the user bought something
    on your site,
    and you would like them to see a receipt page
    of their order.
    This subclass is perfect
    for that scenario.
* `HttpResponseNotFound` - This is the subclass used
    to create a `404 Not Found` response.
    Django provides some helper functions to return this
    so you may not use this subclass directly,
    but it's good to know it's available.
* `HttpResponseForbidden` - This type of response happens
    when you don't want a user
    to access a part
    of your website.
* `JsonResponse` - I haven't focused on JSON yet
    in this series,
    but it's a data format which matches closely
    to Python native data types
    and can be used
    to communicate with JavaScript.

Django has other techniques
to return `HttpResponse` instances
without creating one yourself.
The most common function is `render`.

`render` is a tool
for working with templates.
Templates are the topic
of the next article,
but here is a sneak peek.

An undesirable way
to send HTML:

```python
from django.http import HttpResponse

def my_html_view(request):
    response_content = """
    <html>
    <head><title>Hello World!</title>
    <body>
        <h1>This is a demo.</h1>
    </body>
    </html>
    """
    return HttpResponse(response_content)
```

While this works,
it has many shortcomings.

1. The HTML chunk isn't reusable by other views.
2. The mixing of Python and HTML is going to get messy.
3. How can you join pieces of HTML together?

The alternative:

```python
# application/views.py
from django.shortcuts import render

def my_html_view(request):
    return render(request, "template.html", {})
```

And we would have another file named `template.html` containing:

```html
<html>
<head><title>Hello World!</title>
<body>
    <h1>This is a demo.</h1>
</body>
</html>
```

That wraps up `HttpRequest` and `HttpResponse`.

## View Classes

Views do no need to be functions exclusively.
Django also provides tools
to make views out of classes.
These types of views derive
from Django's `View` class.

When you write a class-based view
(often abbreviated to CBVs),
you add class methods
that match up
with HTTP methods.
Let's see an example:

```python
# application/views.py
from django.http import HttpResponse
from django.views.generic.base import View

class SampleView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello from a CBV!")
```

The `get` method
on the class
corresponds to a `GET` HTTP request method.
This relationship holds
for all the HTTP methods.

```python
# project/urls.py
from django.urls import path

from application.views import SampleView

urlpatterns = [
    path("", SampleView.as_view()),
]
```

Note that we don't pass `SampleView`
to `path` as is.
`path` expects a callable object
so we must call `as_view`
which is a class method
that returns a function
that will call the code
in our class.

Django includes a host
of class-based views
to use for a variety
of purposes.
We can explore a few
of them
with our limited exposure
to the full framework so far.

## Out Of The Box Views

### RedirectView

This is a view to use
when you want to send users
of your site
to a different place.
You *could* make a view
that returns an `HttpResponseRedirect` instance,
but this view can handle that for you.

In fact,
you can use `RedirectView`
without subclassing it.
Check this out:

```python
# project/urls.py
from django.urls import path
from django.views.generic.base import RedirectView

from application.views import NewView

urlpatterns = [

    path("new-path/", NewView.as_view(), name='new-view'),
    path("old-path/", RedirectView.as_view(pattern_name='new-view')),
]
```

`as_view` is what let's us avoid subclassing `RedirectView`.
The arguments passed to `as_view` override any class attributes.

### TemplateView

Templates are so commonly used
that Django provides a class
that knows how to produce a proper response
with nothing more than a template name.

An example looks like:

```python
# application/views.py
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
```

### Other View Classes

Django's other class-based views serve a variety
of purposes.
Django has views that will:

* Display and handle HTML forms
    so users can input data
    and send the data
    to the application.
* Pull data from a database
    and show an individual record
    to the user
    (e.g., a webpage to see facts about an individual movie).
* Pull data from a database
    and show information
    from a collection of records
    to the user
    (e.g., showing the cast of actors from a movie).
* Allow a user to create or update data
    that will be saved to a database.
* Show data from specific time ranges
    like days, weeks, and months.

For now,
when you're developing your own views,
try to remember that Django probably has a class-based view
to aid your work.

## Useful View Decorators And Mixins

Decorators are a feature
of Python
(and many other languages)
that let you extend a function
with additional capabilities.
A decorator can wrap a view function
to provide new behavior
to a view.
This is useful
when you have common functionality
that you want to add to many views
without copying and pasting a lot of code around.

Mixin classes serves a very similar purpose
as decorators,
but behave with Python's multiple inheritance feature
of classes
to "mix in" the new behavior
with an existing class-based view.

### Decorators To Know

What if you only want
to handle certain HTTP methods?
Consider:

```python
# application/views.py
from django.http import HttpResponse

def multi_method_view(request):
    if request.method == 'GET':
        return HttpResponse('Method was a GET.')
    elif request.method == 'POST':
        return HttpResponse('Method was a POST.')
```

```python
# application/views.py
from django.http import Http404, HttpResponse

def guard_clause_view(request):
    if request.method != 'POST':
        raise Http404()

    return HttpResponse('Method was a POST.')

# OR

def if_clause_view(request):
    if request.method == 'POST':
        return HttpResponse('Method was a POST.')
    else:
        raise Http404()
```

Instead, we can use the `require_POST` decorator
and let Django check the method
for us.

```python
# application/views.py
from django.http import HttpResponse
from django.views.decorators.http import require_POST

@require_POST
def the_view(request):
    return HttpResponse('Method was a POST.')
```

Another common decorator you may encounter is the `login_required` decorator.
When we get to the subject
of user management,
you'll see that we can make a protected view
for an app
by including this decorator.

```python
# application/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def the_view(request):
    return HttpResponse('This view is only viewable to authenticated users.')
```

A final example
of a useful built-in decorator
is `user_passes_test`.
This is another decorator used
with the user management system
that let's us control *which* users should be allowed
to access a view.
For instance,
we could make a view that only staff-level users could access.

```python
# application/views.py
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

@user_passes_test(lambda user: user.is_staff)
def the_view(request):
    return HttpResponse('Only visible to staff users.')
```

And, they stack!

```python
# application/views.py
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.view.decorators.http import require_POST

@require_POST
@user_passes_test(lambda user: user.is_staff)
def the_view(request):
    return HttpResponse('Only staff users may POST to this view.')
```

### Mixins To Know

Mixin classes are to class-based views
as decorators are to function-based views.
This isn't *completely* true
since class-based views can also use decorators,
but it should give you an idea
of where mixins fit.

Like the `login_required`
and `user_passes_test` decorators,
we have mixin equivalents
of `LoginRequiredMixin`
and `UserPassesTestMixin`.
Maybe you have some template views
that should only be accessible
to authenticated users
or staff-level users.
Those views could look like:

```python
# application/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

class StaffProtectedView(UserPassesTestMixin, TemplateView):
    template_name = 'staff_eyes_only.html'

    def test_func(self):
        return self.request.user.is_staff
```

There are plenty
of other mixin classes.
In fact,
most of Django's built-in class-based views are constructed
by composing various mixin classes together.
If you'd like to see how they are constructed,
check out {{< extlink "https://ccbv.co.uk/" "Classy Class-Based Views" >}}
which is a site showing the built-in CBVs
along with the mixins and attributes available
to those classes.

## Summary

That's a wrap on view fundamentals.
We've looked at:

* View functions
* `HttpRequest` and `HttpResponse`
* View classes
* Some built-in supporting views
* Decorators and mixins that supercharge views.

## Next Time

In the next episode,
we'll examine templates
in more depth.
Templates are a sub-language
within Django
that are your primary tool
for making user interfaces
with Django's built-in features.

You can follow the show
on {{< extlink "https://djangoriffs.com" "djangoriffs.com" >}}.
Or follow me or the show
on Twitter
at
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}
or
{{< extlink "https://twitter.com/djangoriffs" "@djangoriffs" >}}.

Please rate or review
on iTunes, Spotify,
or from wherever you listen to podcasts.
Your rating will help others discover the podcast,
and I would be very grateful.

Django Riffs is supported by listeners like *you*.
If you can contribute financially
to cover hosting and production costs,
please check out my {{< extlink "https://www.patreon.com/mblayman" "Patreon page" >}}
to see how you can help out.
