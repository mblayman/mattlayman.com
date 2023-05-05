---
title: "Templates For User Interfaces"
description: >-
    When your Django application sends back a response with your user interface, templates are the tool you'll use to produce that user interface. This article looks at what templates are and how to use them.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - templates

---

{{< web >}}
In the previous [Understand Django]({{< ref "/understand-django/_index.md" >}}) article, we looked at the fundamentals of using views in Django. This article will focus on templates.
{{< /web >}}
Templates are your primary tool in a Django project for generating a user interface. With templates, you'll be able to build the pages that users will see when they visit your web app. Let's see how templates hook into views and what features Django provides with its template system.

{{< understand-django-series "templates" >}}

## Set Up Templates

We need a place for templates to live. Templates are static files that Django will fill in with data. In order to use those files, we must instruct Django on where to find them.

Like most parts of Django, this configuration is in your project's settings file. After you use `startproject`, you can find a section in your settings file that will be called `TEMPLATES`. The section should look something like:

```python
# project/settings.py

TEMPLATES = [{
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
}]
```

Django's template system can use multiple template backends. The backends dictate how your templates will work. I would recommend sticking with the default Django template language. This language has the tightest integration with the framework and the strongest support.

The next thing to notice is `APP_DIRS` with its value of `True`. For the Django template language, setting this value to `True` will cause Django to look for template files within a `templates` directory in each Django application in your project. Note that this also includes any third party applications so you should probably leave this set to `True`.

So, where should *your* templates go? There are different schools of thought in the Django community. Some developers believe in having all templates within applications. Others ascribe to having all your project's templates in a single directory. I'm in this second category of developers. I find it valuable to keep all of the templates for my entire project within a single directory.

From my perspective, keeping templates in a single directory makes it very clear where all the layout and UI in your system will live. To use that pattern, we must set the `DIRS` variable with the directory that we want Django to include. I recommend keeping a `templates` directory at the root of your project. If you do that, your `DIRS` value will change to something like:

```python
# project/settings.py

TEMPLATES = [
...
    "DIRS": [BASE_DIR / "templates"],
...
]
```

Finally, there is `OPTIONS`. Each backend can accept a variety of options. `startproject` sets a number of context processors. We'll come back to context processors later
{{< web >}}
in this article.
{{< /web >}}
{{< book >}}
in this chapter.
{{< /book >}}

With your templates set up, you're ready to go!

## Using Templates With Render

Django builds your user interface by *rendering* a template. The idea behind rendering is that dynamic data is combined with a static template file to produce a final output.

To produce an `HttpResponse` that contains rendered output, we use the `render` function. Let's see an example in the form of a function-based view (FBV):

```python
# application/views.py

from django.shortcuts import render

def hello_view(request):
    context = {'name': 'Johnny'}
    return render(
        request,
        'hello.txt',
        context
    )
```

In this example, the view would use a template located in `templates/hello.txt` which could contain:

```txt
Hello {{ name }}
```

When this view responds to a request, a user would see "Hello Johnny" in their browser. There are some interesting things to note about this example.

1. The template can be any plain text file type. Most often we will use HTML to make a user interface so you will often see `some_template.html`, but the Django template system can render on any type.
2. In the process of rendering, Django took the context data dictionary and used its keys as variable names in the template. Because of special double curly brace syntax, the template backend swapped out `{{ name }}` for the literal value of "Johnny" that was in the context.

This idea of mixing context and static layout is the core concept of working with templates.
{{< web >}}
The rest of this article builds
{{< /web >}}
{{< book >}}
The rest of this chapter builds
{{< /book >}}
on this root concept and shows what else is possible in the Django template language.

As an aside, HTML is a topic that we are not going to explore directly. HTML, the Hypertext Markup Language, is the language used on the web to describe the structure of a page. HTML is composed of tags and many of these tags work in pairs. For example, to make a *paragraph*, you can use a `p` tag, which is represented by wrapping `p` with greater than and less than symbols to form the "opening" tag. The "closing" tag is similar, but it includes a forward slash.

```html
<p>This is a paragraph example.</p>
```

{{< web >}}
From the last article,
{{< /web >}}
{{< book >}}
From the last chapter,
{{< /book >}}
you may recall seeing the `TemplateView`. In those examples, we provided a template name, and I declared that Django would take care of the rest. Now you can start to understand that Django takes the template name and calls code similar to `render` to provide an `HttpResponse`. Those examples were missing context data to combine with the template. A fuller example replicating the `hello_view` function-based view as a class-based-view would look like:

```python
# application/views.py

from django.views.generic.base import TemplateView

class HelloView(TemplateView):
    template_name = 'hello.txt'

    def get_context_data(
        self,
        *args,
        **kwargs
    ):
        context = super().get_context_data(
            *args, **kwargs)
        context['name'] = 'Johnny'
        return context
```

This example uses `get_context_data` so that we can insert our "dynamic" data into the rendering system to give us the response we want.

In a real application, a lot of the code that we need to write focuses on building up a truly dynamic context. I'm using static data in these examples to keep the mechanics of the template system clear. When you see me use `context`, try to imagine more complex data building to create a user interface.

Those are the fundamentals of rendering. We'll now turn our attention to what the Django template language is capable of.

## Templates In Action

When using templates, we take context data and insert it into the placeholders within the template.

Template variables are the most basic form of filling placeholders with context. The previous section showed an example by using the `name` variable. The context dictionary contains a `name` key, whose value appears anywhere in the template where that key is surrounded by double curly braces.

We can also use a dot access when the context data is more complex. Let's say your template gets context like:

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

Your Django template *won't* work if you try to access this context data like a regular dictionary (e.g., `{{ address['street'] }}`). Instead, you would use dot notation to get to the data in the dictionary:

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

Django templates also try to be flexible with the types of context data. You could also pass in a Python class instance like an `Address` class with attributes that are the same as the keys in our previous dictionary. The template would work the same.

The core template language also includes some standard programming logic keywords by using *tags*. Template tags look like `{% some_tag %}` whereas template variables look like `{{ some_variable }}`. Variables are meant to be placeholders to fill in, but tags offer more power.

We can start with two core tags, `if` and `for`. The `if` tag is for handling conditional logic that your template might need:

{{< web >}}
```django
{% if user.is_authenticated %}
    <h1>Welcome, {{ user.username }}</h1>
{% endif %}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{% if user.is_authenticated %}
    <h1>Welcome, {{ user.username }}</h1>
{% endif %}
```
{{< /book >}}

This example will only include this welcome message HTML header tag when the user is logged in to the application. We started the example with an `if` tag. Observe that the `if` tag requires a closing `endif` tag. Templates must respect whitespace since your layout might depend on that whitespace. The template language can't use whitespace to indicate scope like it can with Python so it uses closing tags instead. As you might guess, there are also `else` and `elif` tags that are accepted inside of an `if`/`endif` pair:

{{< web >}}
```django
{% if user.is_authenticated %}
    <h1>Welcome, {{ user.username }}</h1>
{% else %}
    <h1>Welcome, guest</h1>
{% endif %}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{% if user.is_authenticated %}
    <h1>Welcome, {{ user.username }}</h1>
{% else %}
    <h1>Welcome, guest</h1>
{% endif %}
```
{{< /book >}}

In this case, only one of the header tags will render depending on whether the user is authenticated or not.

The other core tag to consider is the `for` loop tag. A `for` loop in Django templates behaves as you might expect:

{{< web >}}
```django
<p>Prices:</p>
<ul>
{% for item in items %}
    <li>{{ item.name }} costs {{ item.price }}.</li>
{% endfor %}
</ul>
```
{{< /web >}}
{{< book >}}
```djangotemplate
<p>Prices:</p>
<ul>
{% for item in items %}
    <li>{{ item.name }} costs {{ item.price }}.</li>
{% endfor %}
</ul>
```
{{< /book >}}

Django will loop over iterables like lists and let users output template responses for each entry in an iterable. If the example above had a list of `items` in the context like:

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

Occasionally, you may want to take some specific action on a particular element in the `for` loop. Python's built in `enumerate` function isn't available directly in templates, but a special variable called `forloop` is available inside of a `for` tag. This `forloop` variable has some attributes like `first` and `last` that you can use to make templates behave differently on certain loop iterations:

{{< web >}}
```django
Counting:
{% for number in first_three_numbers %}
    {{ number }}{% if forloop.last %} is last!{% endif %}
{% endfor %}
```
{{< /web >}}
{{< book >}}
```djangotemplate
Counting:
{% for number in first_three_numbers %}
    {{ number }}{% if forloop.last %} is last!{% endif %}
{% endfor %}
```
{{< /book >}}

This example would produce:

```txt
Counting:
    1
    2
    3 is last!
```

Equipped with variables, `if` tags, and `for` tags, you should now have the ability to make some fairly powerful templates, but there's more!

### More Context On Context

In the setup of the templates settings, we glossed over context processors. Context processors are a valuable way to extend the context that is available to your templates when they are rendered.

Here's the set of context processors that Django's `startproject` command brings in by default:

```python
'context_processors': [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
],
```

Context processors are functions (technically, callables, but let's focus on functions) that receive an `HttpRequest` and must return a dictionary. The returned dictionary merges with any other context that will be passed to your template.

Conceptually, when preparing to render and given a `context` dictionary that was passed to `render`, the template system will do something like:

```python
for processor in context_processors:
    context.update(processor(request))

# Continue on to template rendering
```

The actual code in the template system is more complex than this concept code sketch, but not by much!

We can look at the actual definition of the `request` context processor included in that default list:

```python
# django/template/context_processors.py

def request(request):
    return {'request': request}
```

That's it! Because of this context processor, the `request` object will be available as a variable to any template in your project. That's super powerful.

<div class='sidebar'>

<h4>Sidebar</h4>

<p>
Don't be afraid to look at the source code of the projects that you depend on. Remember that regular people wrote your favorite frameworks! You can learn valuable lessons from what they did. The code might be a little intimidating at first, but there is no magic going on!
</p>

</div>

The "dark side" of context processors is that they run for all requests. If you write a context processor that is slow and does a lot of computation, *every request* will suffer that performance impact. So use context processors carefully.

### Reusable Chunks Of Templates

Now let's talk about one of the powerhouse features of the template system: reusable pieces.

Think about a website. Most pages have a similar look and feel. They do this by repeating a lot of the same HTML, which is Hypertext Markup Language that defines the structure of a page. These pages also use the same CSS, Cascading Style Sheets, which define the styles that shape the look of the page elements.

Imagine you're asked to manage a site and you need to create two separate pages. The homepage looks like:

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

And here is a page to learn about the company behind the website:

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

These examples are tiny amounts of HTML, but what if you're asked to change the stylesheet from `styles.css` to a new stylesheet made by a designer called `better_styles.css`? You would have to update both places. Now think if there were 2,000 pages instead of 2 pages. Making big changes quickly across a site would be virtually impossible!

Django helps you avoid this scenario entirely with a few tags. Let's make a new template called `base.html`:

{{< web >}}
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
{{< /web >}}
{{< book >}}
```djangotemplate
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet"
            type="text/css"
            href="styles.css">
    </head>
    <body>
        {% block main %}{% endblock %}
    </body>
</html>
```
{{< /book >}}

We've created a reusable template with the `block` tag! We can fix up our homepage to use this new template:

{{< web >}}
```django
{% extends "base.html" %}

{% block main %}
    <h1>Hello from the Home page</h1>
{% endblock %}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{% extends "base.html" %}

{% block main %}
    <h1>Hello from the Home page</h1>
{% endblock %}
```
{{< /book >}}

This new version of the homepage *extends* the base template. All the template had to do was define its own version of the `main` block to fill in the content. We could do the exact same thing with the about page.

If we revisit the task of replacing `styles.css` with `better_styles.css`, we can make the update in `base.html` and have that change apply to any templates that extend it. Even if there were 2,000 pages that all extended from `base.html`, changing the stylesheet would still be one line of code to change for an entire site.

That's the power of Django's template extension system. Use `extend` when you need content that is mostly the same. Add a `block` section whenever you need to customize an extended page. You can extend a page by including multiple types of blocks. The example only shows a `main` block, but you might have pages that customize a `sidebar`, `header`, `footer`, or whatever might vary.

Another powerful tool for reuse is the `include` tag. The `include` tag is useful when you want to extract some chunk of template that you want to use in multiple locations. You may want to use `include` to:

1. Keep templates tidy. You can break a large template up into small pieces that are more manageable.
2. Use a template fragment in different parts of your site. Maybe you have a piece of template that should only appear on a few pages.

Coming back to our website example, imagine that `base.html` grew to be 20,000 lines long. Navigating to the right part of the template to make changes is now harder. We can decompose the template into smaller pieces:

{{< web >}}
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
{{< /web >}}
{{< book >}}
```djangotemplate
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
{{< /book >}}

The `include` tag can move those extra pieces around. By providing a good name for your templates, if you needed to change the structure of some section like navigation, you could go to the template with the appropriate name. That template file would focus on only the element that you need to change.

`block`, `extends`, and `include` are core tags for keeping your user interface code from sprawling all over the place with lots of duplication.

Next, let's talk about more of Django's built-in template tags that can supercharge your UI.

## The Templates Toolbox

The Django documentation includes a {{< extlink "https://docs.djangoproject.com/en/4.1/ref/templates/builtins/" "large set of built-in tags" >}} that you can use in your projects. We aren't going to cover all of them, but I'll focus on a few tags to give you a flavor of what is available.

One of the most used built-in tags aside from what we've already covered is the `url` tag.
{{< web >}}
Recall from the article
{{< /web >}}
{{< book >}}
Recall from the chapter
{{< /book >}}
on URLs that you can get the URL to a named view by using the `reverse` function. What if you wanted to use the URL in your template? You could do this:

```python
# application/views.py

from django.shortcuts import render
from django.urls import reverse

def the_view(request):
    context = {
        'the_url': reverse('a_named_view')
    }
    return render(
        request,
        'a_template.html',
        context
    )
```

While this works, it's tedious to have to route all URLs through the context. Instead, our template can directly create the proper URL. Here's what `a_template.html` might look like instead:

{{< web >}}
```django
<a href="{% url "a_named_view" %}">Go to a named view</a>
```
{{< /web >}}
{{< book >}}
```djangotemplate
<a href="{% url "a_named_view" %}">Go to a named view</a>
```
{{< /book >}}

The `url` tag is the template equivalent of the `reverse` function. Like its `reverse` counterpart, `url` can accept args or kwargs for routes that expect other variables. `url` is an incredibly useful tool and one that you will probably reach for many times as you build your user interface.

Another useful tag is the `now` tag. `now` is a convenient method to display information about the current time. Using what Django calls *format specifiers*, you can tell your template how to display the current time. Want to add a current copyright year to your website? No problem!:

{{< web >}}
```django
&copy; {% now "Y" %} Your Company LLC.
```
{{< /web >}}
{{< book >}}
```djangotemplate
&copy; {% now "Y" %} Your Company LLC.
```
{{< /book >}}

One final built-in tag to consider is the `spaceless` tag. HTML is *partially* sensitive to whitespace. There are some frustrating circumstances where this whitespace sensitivity can ruin your day when building a user interface. Can you make a pixel perfect navigation menu for your site with an unordered list? Maybe. Consider this:

```html
<ul class="navigation">
    <li><a href="/home/">Home</a></li>
    <li><a href="/about/">About</a></li>
</ul>
```

The indented whitespace on those list items (or the new line characters that follow them) might cause you trouble when working with CSS. Knowing that the whitespace can affect layout, we can use `spaceless` like so:

{{< web >}}
```django
{% spaceless %}
<ul class="navigation">
    <li><a href="/home/">Home</a></li>
    <li><a href="/about/">About</a></li>
</ul>
{% endspaceless %}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{% spaceless %}
<ul class="navigation">
    <li><a href="/home/">Home</a></li>
    <li><a href="/about/">About</a></li>
</ul>
{% endspaceless %}
```
{{< /book >}}

This neat little template tag will remove all the spaces between HTML tags so your output looks like:

```html
<ul class="navigation"><li><a href="/home/">Home</a></li>...</ul>
```

By removing the extra space, you may get a more consistent experience with your CSS styling and save yourself some frustration.
{{< web >}}
(I had to trim the output to fit better on the screen.)
{{< /web >}}

There is another kind of built-in that we have not looked at yet. These alternative built-in functions are called **filters**. Filters change the output of variables in your templates. The filter syntax is a bit interesting. It looks like:

{{< web >}}
```django
Here's a filter example: {{ a_variable|some_filter:"filter arguments" }}
```
{{< /web >}}
{{< book >}}
```djangotemplate
Here's a filter example:
{{ a_variable|some_filter:"filter arguments" }}
```
{{< /book >}}

The important element is the pipe character directly after a variable. This character signals to the template system that we want to modify the variable with some kind of transformation. Also observe that filters are used between double curly braces instead of the `{%` syntax that we've seen with tags.

A very common filter is the `date` filter. When you pass a Python `datetime` instance in the context, you can use the `date` filter to control the format of the datetime. The `date` {{< extlink "https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#date" "documentation" >}} shows what options you can use to modify the format:

{{< web >}}
```django
{{ a_datetime|date:"Y-m-d" }}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{{ a_datetime|date:"Y-m-d" }}
```
{{< /book >}}

If `a_datetime` was an instance of April Fools' Day, then it could return a string like `2020-04-01`. The `date` filter has many specifiers that will enable you to produce most of the date formatting outputs you could think of.

`default` is a useful filter for when your template value evaluates to `False`. This is perfect when you've got a variable with an empty string. The example below outputs "Nothing to see here" if the variable was Falsy:

{{< web >}}
```django
{{ a_variable|default:"Nothing to see here." }}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{{ a_variable|default:"Nothing to see here." }}
```
{{< /book >}}

Falsy is a concept in Python that describes anything that Python will evaluate as false in a boolean expression. Empty strings, empty lists, empty dicts, empty sets, `False`, and `None` are all common Falsy values.

`length` is a simple filter for lists. `{{ a_list_variable|length }}` will produce a number. It is the Django template equivalent to the `len` function.

I like the `linebreaks` filter a lot. If you create a form
{{< web >}}
(which we'll explore in the next article)
{{< /web >}}
{{< book >}}
(which we'll explore in the next chapter)
{{< /book >}}
and accept a text area field where the user is allowed to provide newlines, then the `linebreaks` filter allows you to display those newlines later when rendering the user's data. By default, HTML will not show new line characters as intended. The `linebreaks` filter will convert `\n` to a `<br>` HTML tag. Handy!

Before moving on, let's consider two more.

`pluralize` is a convenient filter for the times when your text considers counts of things. Consider a count of items.

{{< web >}}
```django
{{ count_items }} item{{ count_items|pluralize }}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{{ count_items }} item{{ count_items|pluralize }}
```
{{< /book >}}

The `pluralize` filter will do the right thing if there are zero, one, or more items in the list.

```txt
0 items
1 item
2 items
3 items
(and so on)
```

Be aware that `pluralize` can't handle irregular plurals like "mice" for "mouse."

The final filter in our tour is the `yesno` filter. `yesno` is good for converting `True|False|None` into a meaningful text message. Imagine we're making an application for tracking events and a person's attendance is one of those three values. Our template might look like:

{{< web >}}
```django
{{ user.name }} has {{ user_accepted|yesno:"accepted,declined,not RSVPed" }}.
```
{{< /web >}}
{{< book >}}
```djangotemplate
{{ user.name }} has {{ user_accepted|yesno:"accepted,declined,not RSVPed" }}.
```
{{< /book >}}

Depending on the value of `user_accepted`, the template will display something meaningful to a reader.

There are so many built-ins that it's really hard to narrow down my favorites. Check out the full list to see what might be useful for you.

What if the built-ins don't cover what you need? Have no fear, Django lets you make custom tags and filters for your own purposes. We'll see how next.

## Build Your Own Lightsaber In Templates

When you need to build your own template tags or filters, Django gives you the tools to make what you need.

There are three major elements to working with custom tags:

1. Defining your tags in a place that Django expects.
2. Registering your tags with the template engine.
3. Loading your tags in a template so they can be used.

The first step is to put the tags in the correct location. To do that, we need a `templatetags` Python package inside of a Django application. We also need a module in that directory. Choose the module name carefully because it is what we will load in the template later on:

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

Next, we need to make our tag or filter and register it. Let's start with a filter example:

```python
# application/templatetags/custom_tags.py

import random
from django import template

register = template.Library()

@register.filter
def add_pizzazz(value):
    pieces_of_flair = [
        ' Amazing!',
        ' Wowza!',
        ' Unbelievable!'
    ]
    return value + random.choice(pieces_of_flair)
```

Now, if we have a `message` variable, we can give it some pizzazz. To use the custom filter, we must load our tags module into the template with the `load` tag:

{{< web >}}
```django
{% load custom_tags %}

{{ message|add_pizzazz }}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{% load custom_tags %}

{{ message|add_pizzazz }}
```
{{< /book >}}

If our message was "You got a perfect score!", then our template should show the message and one of the three random choices like "You got a perfect score! Wowza!"

Writing basic custom tags is very similar to custom filters. Code will speak better than words here:

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

We can load the custom tags and use our tag like any other built-in tag:

{{< web >}}
```django
{% load custom_tags %}

{% champion_welcome "He-Man" 50 %}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{% load custom_tags %}

{% champion_welcome "He-Man" 50 %}
```
{{< /book >}}

This silly welcome tag will respond to multiple input variables and vary depending on the provided level. The example usage should display "Hello great champion He-Man!"

We're only looking at the most common kinds of custom tags in our examples. There are some more advanced custom tagging features which you can explore in the {{< extlink "https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/" "Django custom template tags documentation" >}}.

Django also uses `load` to provide template authors with some additional tools. For instance, we will see how to load some custom tags provided by the framework when we learn about working with images and JavaScript later on.

## Summary

Now we've seen templates in action! We've looked at:

* How to set up templates for your site
* Ways to call templates from views
* How to use data
* How to handle logic
* Built-in tags and filters available to templates
* Customizing templates with your own code extensions

{{< web >}}
In the next article,
{{< /web >}}
{{< book >}}
In the next chapter,
{{< /book >}}
we are going to examine how users can send data to a Django application with HTML forms. Django has tools to make form building quick and effective. We're going to see:

* The `Form` class that Django uses to handle form data in Python
* Controlling what fields are in forms
* How forms are rendered to users by Django
* How to do form validation

{{< web >}}
If you'd like to follow along with the series, please feel free to sign up for my newsletter where I announce all of my new content. If you have other questions, you can reach me online on Twitter where I am {{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;
