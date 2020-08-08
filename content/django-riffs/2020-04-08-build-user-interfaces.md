---
title: "Episode 4 - Building User Interfaces"
aliases:
 - /django-riffs/4
 - /djangoriffs/4
 - /django-riffs/4.
 - /djangoriffs/4.
description: >-
    On this episode,
    we look at templates,
    the primary tool
    that Django provides
    to build user interfaces
    in your Django app.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - templates

---

On this episode,
we look at templates,
the primary tool
that Django provides
to build user interfaces
in your Django app.

Listen at {{< extlink "https://djangoriffs.com/episodes/building-user-interfaces" "djangoriffs.com" >}}.

## Last Episode

On the previous episode,
we talked about views
and how views handle requests
to create HTTP responses
for users.

## Set Up

Templates are static files
that Django will fill in
with data.
In order to use those files,
we must instruct Django
on where to find them.

```python
# project/settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

From my perspective,
keeping templates in a single directory
makes it very clear
where all the layout and UI
in your system will live.
To use that pattern,
we must set the `DIRS` variable
with the directory
that we want Django to include.
I recommend keeping a `templates` directory
at the root of your project.
If you do that,
your `DIRS` value will change
to something like:

```python
# project/settings.py

TEMPLATES = [
    ...
        "DIRS": [os.path.join(BASE_DIR, "templates")],
    ...
]
```

## Using Render

Django builds your user interface
by *rendering* a template.
The idea behind rendering is
that dynamic data is combined
with a static template file
to produce a final output.

```python
# application/views.py

from django.shortcuts import render

def a_template_view(request):
    context = {'first_name': 'Johnny'}
    return render(request, 'hello.html', context)
```

```html
<h1>Hello {{ first_name }}</h1>
```

There are some interesting things to note
about this example.

1. The template can be any plain text file type.
2. In the process of rendering,
    Django took the context data dictionary
    and used its keys as variable names
    in the template.

> This idea of mixing context and static layout is the core concept
of working with templates.

Reconsider `TemplateView` from the last episode.

```python
# application/views.py

from django.views.generic.base import TemplateView

class HelloView(TemplateView):
    template_name = 'hello.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['first_name'] = 'Johnny'
        return context
```

## Template Core Elements

When using templates,
we take context data
and insert it
into the placeholders
within the template.

This most basic form
of filling placeholders
with context
are template variables.
The previous section showed an example
by using the `name` variable.
The context dictionary contained a `name` key
and double curly braces
like `{{ name }}` are
where the `name` value is used.

```python
context = {
    'address': {
        'street': '123 Main St.',
        'city': 'Beverly Hills',
        'state': 'CA',
        'zip_code': '90210',
    }
}
```

```txt
The address is:
    {{ address.street }}
    {{ address.city }}, {{ address.state }} {{ address.zip_code}}
```

This would render as:

```txt
The address is:
    123 Main St.
    Beverly Hills, CA 90210
```

The core template language also includes some standard programming logic keywords
by using *tags*.
Template tags look like `{% some_tag %}`
whereas template variables look like `{{ some_variable }}`.
Variables are meant to be placeholders
to fill in,
but tags offer more power.

The `if` tag is for handling conditional logic
that your template might need.

```django
{% if user.is_authenticated %}
    <h1>Welcome, {{ user.username }}</h1>
{% endif %}
```

This example will only include this welcome message HTML header tag
when the user is logged in
to the application.
We started the example
with an `if` tag.

```django
{% if user.is_authenticated %}
    <h1>Welcome, {{ user.username }}</h1>
{% else %}
    <h1>Welcome, guest</h1>
{% endif %}
```

In this case, only one of the header tags will render
depending on whether the user is authenticated or not.

The other core tag
to consider
is the `for` loop tag.

```django
<p>Prices:</p>
<ul>
{% for item in items %}
    <li>{{ item.name }} costs {{ item.price }}.</li>
{% endfor %}
</ul>
```

```python
items = [
    {'name': 'Pizza', 'price': '$12.99'},
    {'name': 'Soda', 'price': '$3.99'},
]
```

Then the output would look roughly like:

```html
<p>Prices:</p>
<ul>
    <li>Pizza costs $12.99.</li>
    <li>Soda costs $3.99.</li>
</ul>
```

The `forloop` variable has some attributes
like `first` and `last`
that you can use to make templates behave differently
on certain loop iterations.

```django
Counting:
{% for number in first_three_numbers %}
    {{ number }}{% if forloop.last %} is last!{% endif %}
{% endfor %}
```

### Context Processors

Here's the set of context processors
that Django's `startproject` command brings in
by default.

```python
'context_processors': [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
],
```

We can look
at the actual definition of the `request` context processor included
in that default list.

```python
# django/template/context_processors.py

def request(request):
    return {'request': request}
```

That's it!
Because of this context processor,
the `request` object will be available
as a variable
to any template
in your project.
That's super powerful.

### Reusable Templates

Now let's talk about one of the powerhouse features
of the template system: reusable pieces.

```html
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="styles.css">
    </head>
    <body>
        <h1>Hello from the Home page</h1>
    </body>
</html>
```

Here is a page to learn about the company
behind the website.

```html
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="styles.css">
    </head>
    <body>
        <h1>Learn about our company</h1>
    </body>
</html>
```

Imagine there were 2,000 pages
instead of 2 pages.
Making big changes quickly across a site would be virtually impossible!

Django helps you avoid this scenario entirely
with a few tags.
Let's make a new template called `base.html`.

```django
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="styles.css">
    </head>
    <body>
        {% block main %}{% endblock %}
    </body>
</html>
```

```django
{% extends "base.html" %}

{% block main %}
    <h1>Hello from the Home page</h1>
{% endblock %}
```

That's the power of Django's template extension system.

Another powerful tool for reuse is the `include` tag.
What happens when a template file is super long?

You may want to use `include` to:

1. Keep templates tidy.
    You can break a large template up into small pieces
    that are more manageable.
2. Use a template fragment
    in different parts of your site.
    Maybe you have a piece of template
    that should only appear on a few pages.

```django
<!DOCTYPE html>
<html>
    {% include "head.html" %}
    <body>
        {% include "navigation.html" %}
        {% block main %}{% endblock %}
    </body>
    {% include "footer.html" %}
</html>
```

`block`, `extends`, and `include` are core tags
for keeping your user interface code
from sprawling all over the place
with lots of duplication.

## Built-in Features

The Django documentation includes
a {{< extlink "https://docs.djangoproject.com/en/3.0/ref/templates/builtins/" "large set of built-in tags" >}}
that you can use
in your projects.

One of the most used built-in tags
aside from what we've already covered
is the `url` tag.

You could do this:

```python
# application/views.py

from django.shortcuts import render
from django.urls import reverse

def the_view(request):
    context = {'the_url': reverse('a_named_view')}
    return render(request, 'a_template.html', context)
```

Instead,
our template can directly create the proper URL.
Here's what `a_template.html` might look like instead:

```django
<a href="{% url "a_named_view" %}">Go to a named view</a>
```

The `url` tag is the template equivalent
of the `reverse` function.

There is another kind of built-in
that we have not looked at yet.
These alternative built-in functions are called **filters**.
Filters change the output of variables
in your templates.

```django
Here's a filter example: {{ a_variable|some_filter:"filter arguments" }}
```

A very common filter is the `date` filter.
When you pass a Python `datetime` instance
in the context,
you can use the `date` filter
to control the format
of the datetime.
The `date` {{< extlink "https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#date" "documentation" >}} shows
what options you can use
to modify the format.

```django
{{ a_datetime|date:"Y-m-d" }}
```

If `a_datetime` was an instance of April Fools' Day,
then it could return a string like `2020-04-01`.
The `date` filter has many specifiers
that will enable you to produce most date formatting outputs
that you could think of.

`default` is a useful filter
for when your template value evaluates to `False`.

```django
{{ a_variable|default:"Nothing to see here." }}
```

If you create a form
(which we'll explore in the next episode)
and accept a text area field where the user is allowed
to provide newlines,
then the `linebreaks` filter is great
if you want to display those newlines later
when rendering the user's data.
By default,
HTML will not show new line characters as intended.
The `linebreaks` filter will convert `\n`
to a `<br>` HTML tag.
Handy!

`pluralize` is a convenient tag
for the times when your text considers counts
of things. Consider a count of items.

```django
{{ count_items }} item{{ count_items|pluralize }}
```

The `pluralize` tag will do the right thing
if there are zero, one, or more items
in the list.

```txt
0 items
1 item
2 items
3 items
(and so on)
```

`yesno` is good for converting `True|False|None`
into a meaningful text message.

```django
{{ user.name }} has {{ user_accepted|yesno:"accepted,declined,not RSVPed" }}.
```

Depending on the value of `user_accepted`,
the template will display something meaningful
to a reader.

## Custom Tags

When you need to build your own template tags or filters,
Django gives you the tools to make what you need.

There are three major elements to working with custom tags:

1. Defining your tags in a place that Django expects.
2. Registering your tags with the template engine.
3. Loading your tags in a template so they can be used.

The first step is to put the tags
in the correct location.
To do that,
we need a `templatetags` Python package
inside of a Django application.
We also need a module
in that directory.
Choose the module name carefully
because it is what we will load
in the template later on.

```txt
application
├── templatetags
│   ├── __init__.py
│   └── custom_tags.py
├── __init__.py
├── ...
├── models.py
└── views.py
```

```python
# application/templatetags/custom_tags.py

import random
from django import template

register = template.Library()

@register.filter
def add_pizzazz(value):
    pieces_of_flair = [' Amazing!', ' Wowza!', ' Unbelievable!']
    return value + random.choice(pieces_of_flair)
```

Now,
if we have a `message` variable,
we can give it some pizzazz.
To use the custom filter,
we must load our tags module
into the template
with the `load` tag.

```django
{% load custom_tags %}

{{ message|add_pizzazz }}
```

Writing basic custom tags is very similar
to custom filters.
Code will speak better than words here.

```python
# application/templatetags/custom_tags.py

import random
from django import template

register = template.Library()

@register.simple_tag
def champion_welcome(name, level):
    if level > 42:
        welcome = f"Hello great champion {name}!"
    elif level > 20:
        welcome = f"Greetings noble warrior {name}!"
    elif level > 5:
        welcome = f"Hello {name}."
    else:
        welcome = "Oh, it's you."
    return welcome
```

We can load the custom tags and use our tag like any other built-in tag.

```django
{% load custom_tags %}

{% champion_welcome "He-Man" 50 %}
```

There are some more advanced custom tagging features
which you can explore
in the {{< extlink "https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/" "Django custom template tags documentation" >}}.

## Summary

Now we've seen templates in action!
We've looked at:

* How to set up templates for your site
* Ways to call templates from views
* How to use data
* How to handle logic
* Built-in tags and filters available to templates
* Customizing templates with your own code extensions

## Next Time

In the next episode,
our focus will turn to forms.
Forms are the primary tool
that web pages use to accept data from users.
We'll see how Django helps us make forms quickly
so our sites can interact
with users.

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
