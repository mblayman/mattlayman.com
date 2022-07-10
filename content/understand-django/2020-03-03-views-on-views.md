---
title: "Views On Views"
description: >-
    Django URLs expect to send a response
    back to a user.
    Where does that response come from?
    A Django view!
    This article looks
    into the fundamentals
    of views
    and how to use them
    in your project.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - views

---

{{< web >}}
In the previous
[Understand Django]({{< ref "/understand-django/_index.md" >}})
article,
I covered URLs
and the variety
of tools
that Django gives us
to describe the outside interface
to the internet
for your project.
In this article,
{{< /web >}}
{{< book >}}
Now that we have a grasp
on URLs in Django,
{{< /book >}}
we'll examine the core building block
that makes those URLs work:
the Django view.

{{< understand-django-series "views" >}}

## What Is A View?

A view is a chunk of code
that receives an HTTP request
and returns an HTTP response.
Views describe Django's entire purpose:
to respond to requests
made to an application
on the internet.

You might notice
that I'm a bit vague
about "chunk of code."
That was deliberate.
The reason is because views come
in multiple forms.
To call views *functions*
would only be part
of the story.
To call them *classes*
would be a different chapter
in the story.

Even if I attempted
to call views *callables,*
I still would not portray them accurately
because of the ways
that certain types of views
get plugged into a Django app.

Let's start with functions
since I think they are the gentlest introduction
to views.

## Function Views

A function view is exactly that, a function.
The function takes an instance
of `HttpRequest`
as input
and returns an `HttpResponse`
(or one of its many subclasses)
as output.

The classic "Hello World" example
would look like what is listed below.

```python
# application/views.py
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse('Hello World')
```

If you added that view
to a URL configuration
which we learned about
{{< web >}}
in the last article,
{{< /web >}}
{{< book >}}
in the last chapter,
{{< /book >}}
then you could visit a browser
at the URL
and find the text "Hello World"
on your browser page.

Maybe you don't find that very exciting,
but I do,
and I think you should!
The framework did so much work for us,
and *our* job is to write a mere couple of lines
of Python.
When plugged into a web server
on the internet,
your greeting can reach anyone
with access to the net.
That's staggering
and is worth reflecting on.

Django does most of the heavy lifting
for us.
The raw HTTP request fits neatly
into the `HttpRequest` class.
Our example view doesn't make any use
of that information,
but it's accessible
if we need it.
Likewise,
we're not using much
of `HttpResponse`,
but it's doing all the work
to make sure it can appear
on a user's browser
and deliver our message.

To see what we can do with views,
let's look closely
at `HttpRequest` and `HttpResponse`
to get a glimpse
and what's going on.

## HttpRequest

`HttpRequest` is a Python class.
Instances of this class represent an HTTP request.
HTTP is the transfer protocol
that the internet uses to exchange information.
A request can be in a variety of formats,
but a standard request might look like:

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

This example is from a side project
that uses school data.
I have trimmed some lines out
of the request so it will fit better
on the screen,
and I did some slight reformatting
to make the content a bit clearer.

When Django receives a request like this,
it will parse the data
and store the data in an `HttpRequest` instance.
The request provides convenient access
to all parts
of the raw data
with helpful attributes
for the most commonly used parameters.
Considering the example,
the request would have:

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

Other attributes are available
to `HttpRequest`,
but that list will get you far to get started.

I should also note
that `HttpRequest` instances are a common place
to attach extra data.
Django requests pass through many pieces
in the framework.
This makes the objects great candidates
for extra features that you may require.
For instance,
if you need user management
{{< web >}}
(which we will explore in a future article),
{{< /web >}}
{{< book >}}
(which we will explore in a future chapter),
{{< /book >}}
then there is code
that can attach a `request.user` attribute
to represent a user
in your system.
It's *very* handy.

I like to think of `HttpRequest` objects
as the common interface
for most of the inputs
that my code uses.

## HttpResponse

The other major interface
that your views will use
either directly or indirectly
is the `HttpResponse` interface.

Your job as a Django user
is to make your views return
some kind of `HttpResponse`.
A response instance will include all the necessary information
to create a valid HTTP response
for a user's browser.

Some of the common `HttpResponse` attributes include:

* `status_code` - This is the HTTP status code.
    Status codes are a set of numbers
    that HTTP defines
    to tell a client (e.g., a browser)
    about the success or failure
    of a request.
    `200` is the usual success code.
    Any number from `400` and up will indicate some error,
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
`HttpResponse` has a variety
of subclasses
for common uses.
Let's look at some:

{{< web >}}
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
    so you might not use this subclass directly,
    but it's good to know it's available.
* `HttpResponseForbidden` - This type of response can be used
    when you don't want a user
    to access a part
    of your website.
* `JsonResponse` - I haven't focused on JSON yet
    in this series,
    but it's a data format which matches closely
    to Python native data types
    and can be used
    to communicate with JavaScript.
{{< /web >}}
{{< book >}}
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
    in this book,
    but it's a data format which matches closely
    to Python native data types
    and can be used
    to communicate with JavaScript.
{{< /book >}}

```python
>>> from django.http import JsonResponse
>>> response = JsonResponse({'hello': 'world'})
>>> response.content
b'{"hello": "world"}'
```

Aside from the subclasses,
Django has other techniques
to return `HttpResponse` instances
without creating one yourself.
The most common function is `render`.

`render` is a tool
for working with templates.
Templates are the topic
{{< web >}}
of the next article,
{{< /web >}}
{{< book >}}
of the next chapter,
{{< /book >}}
but here is a sneak peek.

You could write a view
for a webpage
and include a lot of HTML
in your Python.
HTML is the markup language
of internet pages
that we use
to describe the format
of a page.

This view might look like:

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
    That doesn't matter much for this small example,
    but it would be a huge problem
    when you try to make many views
    that use a lot of markup
    and need to share a common look.
2. The mixing of Python and HTML is going to get messy.
    Need proof?
    Go look at computing history
    and learn about {{< extlink "https://en.wikipedia.org/wiki/Common_Gateway_Interface" "CGI" >}}.
    It wasn't pretty.
3. How can you join pieces of HTML together?
    Not easily.

With templates,
we can separate the layout
from the logic.

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

{{< web >}}
The important part for this article is not about templates themselves.
{{< /web >}}
{{< book >}}
The important part for this chapter is not about templates themselves.
{{< /book >}}
What's worth noting is that `render` returns an `HttpResponse` instance
that will contain the rendered template
as the content.

That wraps up `HttpRequest` and `HttpResponse`.
With those building blocks,
we can now look at other ways
that you can make Django views
for your project.

## View Classes

By now we've seen this relationship with views:

```text
HttpRequest -> view -> HttpResponse
```

Views do not need to be functions exclusively.
Django also provides tools
to make views out of classes.
These types of views derive
from Django's `View` class.

When you write a class-based view
(often abbreviated to CBVs),
you add instance methods
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
corresponds to a `GET` HTTP request.
Similarly,
you would write a `post` method
to respond to a `POST` HTTP request
and so on.
With that view defined,
we can connect it to a URLconf:

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

At this point,
I would be suitably unimpressed
if I were in your shoes.
Why would we add all
of this boilerplate code
when you can make a function
and be done?
If this were the full story,
I would absolutely agree with you.
This doesn't add much
beyond the function-based version.
If anything,
it has more to remember
so it's probably more confusing.

Where class-based views begin
to shine
is when using some other classes
beyond the initial `View` class.

Django includes a host
of class-based views
to use for a variety
of purposes.
We can explore a few
of them
with our limited exposure
to the full framework so far.

## Out Of The Box Views

I won't exhaustively cover all the class-based views
because there are a lot of them.
Also,
{{< web >}}
if you're joining this article series
from the beginning
and have never done Django before,
{{< /web >}}
{{< book >}}
if you have never done Django before,
{{< /book >}}
then there will still be holes
in your knowledge
(which we will plug together!),
and some of the views will not make much sense.

### RedirectView

This is a view to use
when you want to send users
of your site
to a different place.
You *could* make a view
that returns an `HttpResponseRedirect` instance,
but this class-based view can handle that for you.

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
    path("old-view-path/",
         RedirectView.as_view(url="https://www.somewhereelse.com")),
    path("other-old-path/", RedirectView.as_view(pattern_name='new-view')),
    path("new-path/", NewView.as_view(), name='new-view'),
]
```

`RedirectView` can use `url`
for a full URL
or it can use `pattern_name`
if you need to route
to a view
that moved somewhere else
in your project.

`as_view` is what lets us avoid subclassing `RedirectView`.
The arguments passed to `as_view` override any class attributes.
The following two `RedirectView` uses are equivalent:

```python
# project/urls.py
from django.urls import path
from django.views.generic.base import RedirectView

from application.views import NewView

class SubclassedRedirectView(RedirectView):
    pattern_name = 'new-view'

urlpatterns = [
    path("old-path/", SubclassedRedirectView.as_view()),
    # The RedirectView below acts like SubclassedRedirectView.
    path("old-path/", RedirectView.as_view(pattern_name='new-view')),
    path("new-path/", NewView.as_view(), name='new-view'),
]
```

### TemplateView

{{< web >}}
Earlier in the article,
{{< /web >}}
{{< book >}}
Earlier in the chapter,
{{< /book >}}
we saw briefly how we can separate web page layout
from the logic needed
to build a page
with templates.

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

We will look at template views
in greater detail
{{< web >}}
in the next article
{{< /web >}}
{{< book >}}
in the next chapter
{{< /book >}}
when we dive into templates.

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
* Show data from specific time ranges
    like days, weeks, and months.

As we continue to explore Django,
I will discuss these views
when their related topic (like forms) is the primary subject
{{< web >}}
of an article.
{{< /web >}}
{{< book >}}
of a chapter.
{{< /book >}}
For now,
when you're developing your own views,
try to remember that Django probably has a class-based view
to aid your work.

## Useful View Decorators And Mixins

Before we finish the tour
of views,
let's discuss some useful decorators and mixin classes.

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

Mixin classes serve a very similar purpose
as decorators,
but use Python's multiple inheritance feature
of classes
to "mix in" the new behavior
with an existing class-based view.

### Decorators To Know

When you work
with function-based views,
there is a challenge
when handling different HTTP methods.
Some views will handle multiple methods like:

```python
# application/views.py
from django.http import HttpResponse

def multi_method_view(request):
    if request.method == 'GET':
        return HttpResponse('Method was a GET.')
    elif request.method == 'POST':
        return HttpResponse('Method was a POST.')
```

This view uses the `request` instance `method` attribute
to check the request's HTTP method.
What if you only want your view
to respond to one HTTP method?
Let's say you only want to respond to a POST.
We could write:

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

Both of these techniques work,
but the code is a little messier
because of the extra indentation.
Instead, we can use the `require_POST` decorator
and let Django check the method
for us.

```python
# application/views.py
from django.http import HttpResponse
from django.view.decorators.http import require_POST

@require_POST
def the_view(request):
    return HttpResponse('Method was a POST.')
```

This version states the expectation up front
with the decorator
and declares the contract
that the view will work with.

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
that lets us control *which* users should be allowed
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

The decorator takes a callable
that will accept a single argument
of a user object.
The view will only be accessible
if the return value of the test callable evaluates to `True`.

What I'm trying to show
with these examples
is how single decorators can quickly augment your views
with new features.
And, because of how decorators work to wrap functions,
you can "stack" these together.

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

You can see that these views are similar
to their decorator counterparts
with a slightly different usage pattern.

One thing worth noting
with mixins
is their placement.
Because of the way
that Python handles multiple inheritance,
you should be sure to include mixin classes
to the left
in the list of inherited base classes.
This will ensure that Python will behave appropriately
with these classes.
The exact reason for this placement is
because of Python's method resolution order (MRO) rules
when using multiple inheritance.
MRO is outside of our scope,
but that's what you can search for
if you want to learn more.

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

{{< web >}}
In the next article,
we'll see how views can mix static layout
with the dynamic data we provide
by using templates.
Templates are the workhorse
for your Django-based user interfaces.
We're going to see:

* How to set up templates for your site
* Ways to call templates from views
* How to use data
* How to handle logic
* Built-in functions available to templates
* Customizing templates with your own code extensions

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
