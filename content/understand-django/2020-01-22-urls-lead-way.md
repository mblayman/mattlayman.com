---
title: "URLs Lead The Way"
description: >-
    How does a Django site know
    where to send requests?
    You have to tell it!
    In this next article
    in the Understand Django series,
    we look at URLs
    and how to let your users get
    to the right place.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django

---

{{< web >}}
In the last article
in the
[Understand Django]({{< ref "/understand-django/_index.md" >}})
series,
we saw how a user's browser request goes
from their browser
to Django's "front door."
{{< /web >}}
Now it's time to look
{{< web >}}
at how Django processes those requests.
{{< /web >}}
{{< book >}}
at how Django processes a user's browser requests.
{{< /book >}}

An HTTP request coming
from a browser
includes a URL describing which resource Django should produce.
Since URLs can come
in many forms,
we must instruct Django
on the kinds
of URLs
that our web application can handle.
This is what the *URL configuration* is for.
In the Django documentation,
the URL configuration is called a URLconf,
for short.

Where is the URLconf?
The URLconf is at the module path set
by the `ROOT_URLCONF` setting
in your project's settings file.
If you ran the `startproject` command,
then that setting will be named
like `project.urls`
where "project" is the name given
as an argument
to the command.
In other words,
the URLconf is placed right next to the `settings.py` file
in `project/urls.py`.

That explains where the file resides,
but it doesn't tell us much
about how it works.
Let's dig in more.

{{< understand-django-series "urls" >}}

## URLconf In Action

Try to think
of the URL configuration
as a list
of URL paths
that Django will attempt to match
from top to bottom.
When Django finds a matching path,
the HTTP request will route
to a chunk of Python code
that is associated with that path.
That "chunk of Python code" is called a *view*
which we will explore more
in a bit.
For the moment,
trust that views know how
to handle HTTP requests.

We can use an example URLconf
to bring this to life.

```python
# project/urls.py
from django.urls import path

from application import views

urlpatterns = [
    path("", views.home),
    path("about/", views.about),
    path("contact/", views.contact),
    path("terms/", views.terms),
]
```

What's here matches well
with the description
that I described above:
a list of URL paths
that Django will try to match
from top to bottom.
The key aspect of this list is the name `urlpatterns`.
Django will treat the list
in a `urlpatterns` variable
as the URLconf.

The order of this list is also important.
The example doesn't show any conflict
between paths,
but it's possible to create two different `path` entries
that can match the same URL
that a user submits.
I'll show an example
of how that can happen
after we see another aspect
of paths.

We can work through this example
to see how this would work
for `www.acme.com`.
When considering a URL
in a URLconf,
Django does not use the scheme (`https://`),
the domain (`www.acme.com`),
or the leading slash
for matching.
Everything else is what the URLconf will match against.

* A request to `https://www.acme.com/about/` will look
    like `"about/"`
    to the pattern matching process
    and match the second `path`.
    That request would route
    to the `views.about` view.
* A request to `https://www.acme.com/` will look
    like `""`
    to the pattern matching process
    and match the first `path`.
    That request would route
    to the `views.home` view.

> Aside:
You might notice
that Django URLs end
with a slash character.
In fact,
if you attempt to reach a URL
like `https://www.acme.com/about`,
Django will redirect the request
to the same URL
with the slash appended
because of the `APPEND_SLASH`
{{< extlink "https://docs.djangoproject.com/en/4.0/ref/settings/#append-slash" "default setting" >}}.
This behavior is because
of a Django {{< extlink "https://docs.djangoproject.com/en/4.0/misc/design-philosophies/#definitive-urls" "design philosophy" >}} choice.

## The `path` Before Us

If all I gave you was the example above,
I wouldn't fault you
if you thought "Wow, Django is dumb. Why isn't `urlpatterns` a dictionary like below?"

```python
urlpatterns = {
    "": views.home,
    "about/": views.about,
    "contact/": views.contact,
    "terms/": views.terms,
}
```

The reason is that `path` has more power
than I initially revealed.
Most of that power
is in the first string parameter
passed to the function.
The string part of `path`
(e.g., `"about/"`) is called the *route*.

A route can be a plain string
as you've seen,
but it can include other special structures
with a feature called *converters*.
When you use a converter,
you can extract information out
of a URL
that a view can use later.
Consider a path like this:

```python
    path(
        "blog/<int:year>/<slug:slug>/",
        views.blog_post
    ),
```

The two converters in this path are:

* `<int:year>`
* `<slug:slug>`

The use of angle brackets
and some {{< extlink "https://docs.djangoproject.com/en/4.0/topics/http/urls/#path-converters" "reserved names" >}}
cause Django to attempt extra parsing
on a URL.
Each converter has some expected rules to follow.

* The `int` converter must match an integer.
* The `slug` converter must match a slug.
    Slug is a bit of newspaper lingo
    that appears in Django
    because Django started
    as a project
    out of a newspaper in Kansas.
    A slug is a string that can include characters, numbers, dashes, and underscores.

Given those converter definitions,
let's compare against some URLs!

* `https://www.acme.com/blog/2020/urls-lead-way/` - MATCH!
* `https://www.acme.com/blog/twenty-twenty/urls-lead-way/` - NOPE.
* `https://www.acme.com/blog/0/life-in-rome/` - MATCH!
    Uh, maybe not what we wanted though.
    Let's look at that soon.

Now we can revisit our ordering problem
from earlier.
Consider these two paths
in different orders:

```python
    path(
        "blog/<int:year>/",
        views.blog_by_year
    ),
    path(
        "blog/2020/",
        views.blog_for_twenty_twenty
    ),

# vs.

    path(
        "blog/2020/",
        views.blog_for_twenty_twenty
    ),
    path(
        "blog/<int:year>/",
        views.blog_by_year
    ),
```

In the first ordering,
the converter will match any integer following `blog/`,
including `https://www.acme.com/blog/2020/`.
That means that the first ordering will never call the `blog_for_twenty_twenty` view
because Django matches `path` entries in order.

Conversely,
in the second ordering,
`blog/2020/` will route to `blog_for_twenty_twenty` properly
because it is matched first.
That means there's a lesson
to remember here:

{{< web >}}
> When including `path` entries that match
    on ranges
    with converters,
    be sure to put them **after** the more specific entries.
{{< /web >}}
{{< book >}}
When including `path` entries that match
    on ranges
    with converters,
    be sure to put them **after** the more specific entries.
{{< /book >}}

## An Abbreviated View Of Views

What do converters do with this extra data?
That's hard to explain
without touching on views.
{{< web >}}
The next article will cover views
{{< /web >}}
{{< book >}}
The next chapter will cover views
{{< /book >}}
in far more depth,
but here's a primer.

A view is code
that takes a request
and returns a response.
Using Python's optional type checking,
here's an example
that will send a `Hello World` response.

```python
from django.http import (
    HttpRequest,
    HttpResponse
)

def some_view(
    request: HttpRequest
) -> HttpResponse:
    return HttpResponse('Hello World')
```

The `HttpRequest` is Django's translated format
of an HTTP request
wrapped up in a convenient container class.
Likewise, `HttpResponse` is what we can use
so that Django will translate our response data
into a properly formatted HTTP response
that will be sent back to the user's browser.

Now we can look
at one of the converters again.

```python
    path(
        "blog/<int:year>/",
        views.blog_by_year
    ),
```

With this converter in place
in the route,
what would `blog_by_year` look like?

```python
# application/views.py
from django.http import HttpResponse

def blog_by_year(request, year):
    # ... some code to handle the year
    data = 'Some data set by code above'
    return HttpResponse(data)
```

Django begins to reveal some nice qualities here!
The converter did a bunch
of tedious work
for us.
The `year` argument set
by Django
will already be an integer
because Django did the string parsing
and conversion.

If someone submits `/blog/not_a_number/`,
Django will return a Not Found response
because `not_a_number` can't be an integer.
The benefit of this
is that we don't have to put extra checking logic
in `blog_by_year`
to handle the weird case where `year` doesn't look like a number.
That kind of feature is a real time saver!
It keeps your code cleaner
*and* makes handling more precise.

What about that other strange example
that we saw earlier
of `/blog/0/life-in-rome/`?
That would match our pattern
from the earlier section,
but let's assume we want to match a four digit year.
How can we do that?
We can use regular expressions.

## Regular Expressions Paths

Regular expressions are a programming feature
often likened to a chainsaw:
*they are incredibly powerful,
but you can cut off your foot
if you're not careful.*

Regular expressions can express complex relationships
and match patterns
in a very concise way.
This conciseness often gives regular expressions a bad reputation
of being difficult to understand.
When used carefully though,
they can be a great tool
for a job.

One job that a regular expression
(which is often abbreviated to "regex")
is suited for
is matching complex patterns
in strings.
This sounds exactly like our blog year problem!
In our problem,
we want to match a four digit integer only.
Let's look at a solution
that Django can handle
and then break down what it means.

As a reminder,
this solution will match some URL path
like `blog/2020/urls-lead-way/`.

Note, we use the `re_path()` function for 
regular expression matching here, instead of `path()`.

```python
re_path(
    r"^blog/(?P<year>[0-9]{4})/(?P<slug>[\w-]+)/$",
    views.blog_post
),
```

This crazy string behaves exactly like our earlier example
**except** that it is more precise
about only allowing four digit years.
The crazy string also has a name.
It is called a *regex pattern*.
When the Django code runs,
it will test URL paths against the rules
that are defined in this pattern.

To see how it works,
we have to know what the parts of the pattern mean.
We can explain this pattern one chunk
at a time.

* The caret, `^`, means "the pattern must *start* here."
    Because of the caret,
    a path that starts like `myblog/...` will not work.
* `blog/` is a literal interpretation.
    Those characters must match exactly.
* The portion inside parentheses `(?P<year>[0-9]{4})` is a *capture group*.
    The `?P<year>` is the name to associate
    with the capture group and is similar
    to the right side of the colon
    in a converter like `<int:year>`.
    The name allows Django
    to pass on the content
    in an argument called `year`
    to the view.
    The other part of the capture group, `[0-9]{4}`,
    is what the pattern is actually matching.
    `[0-9]` is a *character class*
    which means "match any number from 0 through 9."
    The `{4}` means that it must match **exactly** four times.
    This is the specificity that `re_path` gives
    that the `int` converter could not!
* The slash, `/`, between capture groups is another literal character to match.
* The second capture group, `(?P<slug>[\w-]+)`, will put whatever it matches
    into an argument named `slug`.
    The character class of `[\w-]` contains two types
    of characters. `\w` means any word character
    that you might have in a natural language
    and digits and underscores.
    The other type of character is a literal dash, `-`, character.
    Finally, the plus, `+`, character means
    that the character class must match 1 or more times.
* The last slash is also a literal character match.
* To complete the pattern,
    the dollar sign, `$`, acts like the opposite
    of the caret and means
    "the pattern must *end* here."
    Thus, `blog/2020/some-slug/another-slug/` will not match.

Congratulations!
This is definitely the hardest section
{{< web >}}
of this article.
{{< /web >}}
{{< book >}}
of this chapter.
{{< /book >}}
If you understood what we did
with `re_path`,
the rest of this should feel very comfortable.
If not,
*please don't fret about it!*
If you want to know more about regular expressions,
know that everything I described
in the pattern
is *not* Django specific.
Instead,
this is Python's built-in behavior.
You can learn more
about regular expressions
from Python's {{< extlink "https://docs.python.org/3/howto/regex.html" "Regular Expression HOWTO" >}}.

Knowing that this power
with `re_path`
is there may help you later
on your Django journey,
even if you don't need it today.

## Grouping Related URLs

Up to this point,
we've looked at individual routes
that you can map
in a URLconf.
What can we do
when a related group
of views
should share a common path?
Why would we want to do this?

Let's imagine you're building an educational project.
In your project,
you have schools, students, and other education related concepts.
You *could* do something like:

```python
# project/urls.py
from django.urls import path

from schools import (
    views as schools_views,
)
from students import (
    views as students_views,
)

urlpatterns = [
    path(
        "schools/", schools_views.index
    ),
    path(
        "schools/<int:school_id>/",
        schools_views.school_detail,
    ),
    path(
        "students/",
        students_views.index,
    ),
    path(
        "students/<int:student_id>/",
        students_views.student_detail,
    ),
]
```

This approach would work fine,
but it forces the root URLconf
to know about all the views defined
in each app, `schools` and `students`.
Instead,
we can use `include`
to handle this better.

```python
# project/urls.py
from django.urls import include, path

urlpatterns = [
    path(
        "schools/",
        include("schools.urls"),
    ),
    path(
        "students/",
        include("students.urls"),
    ),
]
```

Then,
in each application,
we would have something like:

```python
# schools/urls.py
from django.urls import path

from schools import views

urlpatterns = [
    path("", views.index),
    path(
        "<int:school_id>/",
        views.school_detail
    ),
]
```

The use of `include` gives each Django app autonomy
in what views it needs to define.
The project can be blissfully "ignorant"
of what the application is doing.

Additionally,
the repetition of `schools/` or `students/` is removed
from the first example.
As Django processes a route,
it will match
on the first portion
of the route
and pass the *remainder*
onto the URLconf
that is defined in the individual app.
In this way,
URL configurations can form a tree
where the root URLconf is where all requests start,
but individual applications can handle the details
as a request is routed to the proper app.

## Naming URLs

We've looked at the main ways
that URLs get defined
with `path`, `re_path`, and `include`.
There is another aspect to consider.
How can we refer to URLs
in other places in the code?
Consider this (rather silly) view:

```python
# application/views.py
from django.http import (
    HttpResponseRedirect
)

def old_blog_categories(request):
    return HttpRequestRedirect(
        "/blog/categories/"
    )
```

A redirect is when a user tries to visit a page
and is sent somewhere else
by the browser.
There are much better ways to handle redirects
than this example shows,
but this view illustrates a different point.
What would happen if you want to restructure the project
so that blog categories moved
from `/blog/categories/`
to `/marketing/blog/categories/`?
In the current form,
we would have to fix this view
and any other view
that referenced the route directly.

What a waste of time!
Django gives us tools to give paths names
that are independent
from the explicit route.
We do this with the `name` keyword argument to `path`.

```python
# project/urls.py
from django.urls import path

from blog import views as blog_views

urlpatterns = [
    ...
    path(
        "/marketing/blog/categories/",
        blog_views.categories,
        name="blog_categories"
    ),
    ...
]
```

This gives us `blog_categories`
as an independent name
from the route
of `/marketing/blog/categories/`.
To use that name,
we need `reverse`
as its counterpart.
Our modified view looks like:

```python
# application/views.py
from django.http import (
    HttpResponseRedirect
)
from django.urls import reverse

def old_blog_categories(request):
    return HttpRequestRedirect(
        reverse("blog_categories")
    )
```

The job of `reverse`
is to look up any path name
and return its route equivalent.
That means that:

```python
reverse("blog_categories") == "/marketing/blog/categories/"
```

At least until you want to change it again. 😁

## When Names Collide

What happens
if you have multiple URLs
that you want to give the same `name`?
For instance,
`index` or `detail` are common names
that you may want to apply.
We can turn to
{{< extlink "https://www.python.org/dev/peps/pep-0020/" "The Zen of Python" >}}
for advice.

> The Zen of Python, by Tim Peters
>
> Beautiful is better than ugly.
>
> ...
>
> **Namespaces are one honking great idea -- let's do more of those!**

Namespaces might be new to you
if you haven't been programming long.
They are a *shared space for names*.
Maybe that's clear,
but I recall struggling
with the concept
when I first began to write software.

To make an analogy
to something in the real world,
let's use trusty buckets.
Imagine you have two red balls
and two blue balls.
Put one color ball
in one of two buckets labeled "A" and "B."
If I wanted a specific blue ball,
I can't say "please give me the blue ball"
because that would be ambiguous.
Instead,
to get a specific ball,
I would need to say "please give me the blue ball in bucket B."
In this scenario,
the bucket is the namespace.

The example that we used for schools and students
can help illustrate this idea
in code.
Both apps had an `index` view
to represent the root
of the respective portions of the project
(i.e., `schools/` and `students/`).
If we wanted to refer
to those views,
we'd try to pick the easiest choice
of `index`.
Unfortunately,
if you pick `index`,
then Django can't tell which one is the right view
for `index`.
The name is ambiguous.

One solution is to create your own namespace
by prefixing `name`
with something common
like `schools_`.
The trouble with that approach is that the URLconf repeats itself.

```python
# schools/urls.py
from django.urls import path

from schools import views

urlpatterns = [
    path(
        "",
        views.index,
        name="schools_index"
    ),
    path(
        "<int:school_id>/",
        views.school_detail,
        name="schools_detail"
    ),
]
```

Django provides an alternative
that will let you keep a shorter name.

```python
# schools/urls.py
from django.urls import path

from schools import views

app_name = "schools"
urlpatterns = [
    path("", views.index, name="index"),
    path(
        "<int:school_id>/",
        views.school_detail,
        name="detail"
    ),
]
```

By adding `app_name`,
we signal to Django
that these views are in a namespace.
Now when we want to get a URL,
we use the namespace name
and the URL name
and join them
with a colon.

```python
reverse("schools:index") == "/schools/"
```

This is another convenience
that Django gives
to make our application development experience easier.

That brings us to a close
on the subject of URLs.
By now,
we've seen how to:

* Make a URL configuration
    by making a module with a list of `urlpatterns`.
* Create URLs with `path` and `re_path`.
* Use converters to extract information for views.
* Use regular expressions to express more complex URL data.
* Group related URLs together with `include`.
* Refer to a URL by its `name`.
* Put related names together in a namespace.

{{< web >}}
In the next article,
we'll dig into views.
This article only gave the briefest definition
to what a view is.
Django gives us very rich options
when working with views.
We're going to explore:

* View functions
* View classes
* Some built-in supporting views
* Decorators that supercharge views.

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
