---
title: "Plantillas para Interfaces de Usuario"
slug: "plantillas-interfaces-usuario"
description: >-
    When your Django application
    sends back a response
    with your user interface,
    templates are the tool you'll use
    to produce that user interface.
    This article looks
    at what templates are
    and how to use them.
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

En el artículo anterior
[Comprender Django]({{< ref "/understand-django/_index.es.md" >}}),
analizamos los fundamentos del uso de vistas en Django. Este artículo se centrará en las plantillas. Las plantillas serán tu herramienta principal en un proyecto Django para generar una interfaz de usuario. Con las plantillas, podrás crear las páginas que los usuarios verán cuando visiten tu aplicación web. Veamos cómo las plantillas se conectan a las vistas y qué funciones proporciona Django con su sistema de plantillas.

{{< understand-django-series-es "templates" >}}

## Configurar plantillas

Necesitamos un lugar en donde colocar las plantillas. Las plantillas son archivos estáticos que Django llenará con datos. Para usar estos archivos, debemos indicar a Django dónde encontrarlos.

Como la mayoría de las partes de Django, esta configuración se encuentra en el archivo de configuración de tu proyecto. Después de usar el comando `startproject`, puedes encontrar una sección en el archivo settings llamada `TEMPLATES`. La sección debería ser algo como:

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

El sistema de plantillas de Django puede usar múltiples backends de plantillas. Los backends dictan cómo funcionarán sus plantillas. Recomendaría seguir con el lenguaje de plantillas predeterminado de Django . Este lenguaje tiene la integración más estrecha con el framework y el soporte más sólido.

Lo siguiente a notar es `APP_DIRS` con su valor de `True`. Para el lenguaje de plantilla de Django, establecer este valor en `True` hará que Django busque archivos de plantilla dentro de un directorio de plantillas en cada aplicación de Django en tu proyecto. Ten en cuenta que esto también incluye aplicaciones de terceros, por lo que probablemente deberías dejar este valor en `True`.

Entonces, ¿dónde deberían ir *tus* plantillas? Hay diferentes escuelas de pensamiento en la comunidad de Django. Algunos desarrolladores creen en tener todas las plantillas dentro de las aplicaciones. Otros recomiendan tener todas las plantillas de su proyecto en un solo directorio. Estoy en esta segunda categoría de desarrolladores. Encuentro valioso mantener todas las plantillas para todo mi proyecto dentro de un solo directorio.

Desde mi perspectiva, mantener las plantillas en un solo directorio deja muy claro dónde vivirá todo el diseño y la interfaz de usuario en su sistema. Para usar ese patrón, debemos configurar la variable `DIRS` con el directorio que queremos que incluya Django. Recomiendo mantener un directorio de plantillas en el directorio raíz de tu proyecto. Si haces eso, tu valor `DIRS` cambiará a algo como:

```python
# project/settings.py

TEMPLATES = [
...
    "DIRS": [BASE_DIR / "templates"],
...
]
```

Finalmente, están las opciones (`OPTIONS`). Cada backend puede aceptar una variedad de opciones. El comando `startproject` establece una serie de procesadores de contexto. Volveremos a los procesadores de contexto más adelante en este artículo.

Con tus plantillas configuradas, ¡estás listo para comenzar!

## Uso de plantillas con renderizado

Django construye su interfaz de usuario mediante la representación de una plantilla. La idea detrás del renderizado es que los datos dinámicos se combinan con un archivo de plantilla estático para producir un resultado final.

Para producir una `HttpResponse` que contenga una salida renderizada, usamos la función `render`. Veamos un ejemplo en forma de vista basada en funciones (FBV):

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

En este ejemplo, la vista usaría una plantilla ubicada en `templates/hello.txt` que podría contener:

```txt
Hello {{ name }}
```

Cuando esta vista responde a una solicitud, un usuario vería "Hello Johnny" en su navegador. Hay algunas cosas interesantes a tener en cuenta sobre este ejemplo.

1. La plantilla puede ser cualquier tipo de archivo de texto sin formato. La mayoría de las veces usaremos HTML para crear una interfaz de usuario, por lo que a menudo verá `alguna_plantilla.html`, pero el sistema de plantillas de Django puede representar cualquier tipo.
1. En el proceso de renderizado, Django tomó el diccionario de datos de contexto y usó sus claves como nombres de variables en la plantilla. Debido a la sintaxis especial de doble llave, el backend de la plantilla cambió `{{ nombre }}` por el valor literal de "Johnny" que estaba en el contexto.

Esta idea de mezclar contexto y diseño estático es el concepto central de trabajar con plantillas. El resto de este artículo se basa en este concepto raíz y muestra qué más es posible en el lenguaje de plantillas de Django.

Por otra parte, HTML es un tema que no vamos a explorar directamente. HTML, el lenguaje de marcado de hipertexto, es el lenguaje utilizado en la web para describir la estructura de una página. HTML se compone de etiquetas y muchas de estas etiquetas funcionan en pares. Por ejemplo, para hacer un *párrafo*, puede usar una etiqueta `p`, que se representa envolviendo `p` con símbolos de mayor que y menor que para formar la etiqueta de "apertura". La etiqueta de "cierre" es similar, pero incluye una barra diagonal:

```html
<p>This is a paragraph example.</p>
```

Del último artículo, puedes recordar haber visto `TemplateView`. En esos ejemplos, proporcionamos un nombre de plantilla y declaramos que Django se encargaría del resto. Ahora se puede comenzar a comprender que Django toma el nombre de la plantilla y llama a un código similar para renderizar para proporcionar una `HttpResponse`. A esos ejemplos les faltaban datos de contexto para combinar con la plantilla. Un ejemplo más completo que replica la vista basada en la función `hello_view` como una vista basada en clases sería el siguiente:

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

Este ejemplo usa `get_context_data` para que podamos insertar nuestros datos "dinámicos" en el sistema de renderizado para darnos la respuesta que queremos.

En una aplicación real, mucho del código que necesitamos escribir se enfoca en construir un contexto verdaderamente dinámico. Estoy usando datos estáticos en estos ejemplos para mantener clara la mecánica del sistema de plantillas. Cuando me veas usar `context`, intenta imaginar una construcción de datos más compleja para crear una interfaz de usuario.

Esos son los fundamentos del renderizado. Ahora centraremos nuestra atención en lo que es capaz de hacer el lenguaje de plantillas Django.

## Plantillas en acción

When using templates,
we take context data
and insert it
into the placeholders
within the template.

Template variables are the most basic form
of filling placeholders with context.
The previous section showed an example
by using the `name` variable.
The context dictionary contains a `name` key,
whose value appears anywhere in the template
where that key is surrounded by double curly braces.

We can also use a dot access
when the context data is more complex.
Let's say your template gets context like:

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

Your Django template *won't* work
if you try to access this context data
like a regular dictionary
(e.g., `{{ address['street'] }}`).
Instead,
you would use dot notation
to get to the data
in the dictionary.

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

Django templates also try
to be flexible
with the types of context data.
You could also pass in a Python class instance
like an `Address` class
with attributes
that are the same as the keys
in our previous dictionary.
The template would work the same.

The core template language also includes some standard programming logic keywords
by using *tags*.
Template tags look like `{% some_tag %}`
whereas template variables look like `{{ some_variable }}`.
Variables are meant to be placeholders
to fill in,
but tags offer more power.

We can start
with two core tags, `if` and `for`.

The `if` tag is for handling conditional logic
that your template might need.

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

This example will only include this welcome message HTML header tag
when the user is logged in
to the application.
We started the example
with an `if` tag.
Observe that the `if` tag requires a closing `endif` tag.
Templates must respect whitespace
since your layout might depend
on that whitespace.
The template language can't use whitespace
to indicate scope
like it can with Python
so it uses closing tags instead.
As you might guess,
there are also `else` and `elif` tags
that are accepted inside
of an `if`/`endif` pair.

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

In this case, only one of the header tags will render
depending on whether the user is authenticated or not.

The other core tag
to consider
is the `for` loop tag.
A `for` loop
in Django templates
behaves as you might expect.

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

Django will loop over iterables
like lists
and let users output template responses
for each entry in an iterable.
If the example above had a list
of `items`
in the context like:

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

Occasionally,
you may want to take some specific action
on a particular element
in the `for` loop.
Python's built in `enumerate` function isn't available directly
in templates,
but a special variable called `forloop` is available
inside of a `for` tag.
This `forloop` variable has some attributes
like `first` and `last`
that you can use to make templates behave differently
on certain loop iterations.

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

Equipped with variables,
`if` tags,
and `for` tags,
you should now have the ability to make some fairly powerful templates,
but there's more!

### More Context On Context

In the setup
of the templates settings,
we glossed over context processors.
Context processors are a valuable way
to extend the context
that is available
to your templates
when they are rendered.

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

Context processors are functions
(technically, callables, but let's focus on functions)
that receive an `HttpRequest`
and must return a dictionary.
The returned dictionary merges
with any other context
that will be passed to your template.

Conceptually,
when preparing to render
and given a `context` dictionary
that was passed to `render`,
the template system will do something like:

```python
for processor in context_processors:
    context.update(processor(request))

# Continue on to template rendering
```

The actual code in the template system is more complex
than this concept code sketch,
but not by much!

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

<div class='sidebar'>

<h4>Sidebar</h4>

<p>
Don't be afraid to look at the source code
of the projects
that you depend on.
Remember that regular people wrote your favorite frameworks!
You can learn valuable lessons
from what they did.
The code might be a little intimidating at first,
but there is no magic going on!
</p>

</div>

The "dark side" of context processors is
that they run for all requests.
If you write a context processor
that is slow and does a lot of computation,
*every request* will suffer
that performance impact.
So use context processors carefully.

### Reusable Chunks Of Templates

Now let's talk about one of the powerhouse features
of the template system: reusable pieces.

Think about a website.
Most pages have a similar look and feel.
They do this by repeating a lot of the same HTML,
which is Hypertext Markup Language
that defines the structure
of a page.
These pages also use the same CSS, Cascading Style Sheets,
which define the styles that shape the look
of the page elements.

Imagine you're asked to manage a site
and you need to create two separate pages.
The homepage looks like:

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

And here is a page to learn about the company
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

These examples are tiny amounts of HTML,
but what if you're asked to change the stylesheet
from `styles.css`
to a new stylesheet made
by a designer called `better_styles.css`?
You would have to update both places.
Now think if there were 2,000 pages
instead of 2 pages.
Making big changes quickly across a site would be virtually impossible!

Django helps you avoid this scenario entirely
with a few tags.
Let's make a new template called `base.html`.

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

We've created a reusable template with the `block` tag!
We can fix up our homepage
to use this new template.

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

This new version of the homepage *extends* the base template.
All the template had to do was define its own version
of the `main` block
to fill in the content.
We could do the exact same thing with the about page.

If we revisit the task of replacing `styles.css`
with `better_styles.css`,
we can make the update in `base.html`
and have that change apply
to any templates
that extend it.
Even if there were 2,000 pages
that all extended from `base.html`,
changing the stylesheet would still be one line
of code
to change
for an entire site.

That's the power of Django's template extension system.
Use `extend` when you need content
that is mostly the same.
Add a `block` section whenever you need to customize an extended page.
You can extend a page by including multiple types of blocks.
The example only shows a `main` block,
but you might have pages that customize a `sidebar`, `header`, `footer`,
or whatever might vary.

Another powerful tool for reuse is the `include` tag.
The `include` tag is useful
when you want to extract some chunk
of template
that you want to use
in multiple locations.
You may want to use `include` to:

1. Keep templates tidy.
    You can break a large template up into small pieces
    that are more manageable.
2. Use a template fragment
    in different parts of your site.
    Maybe you have a piece of template
    that should only appear on a few pages.

Coming back to our website example,
imagine that `base.html` grew to be 20,000 lines long.
Navigating to the right part
of the template
to make changes
is now harder.
We can decompose the template
into smaller pieces.

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

The `include` tag can move those extra pieces around.
By providing a good name for your templates,
if you needed to change the structure of some section
like navigation,
you could go to the template
with the appropriate name.
That template file would focus
on only the element that you need to change.

`block`, `extends`, and `include` are core tags
for keeping your user interface code
from sprawling all over the place
with lots of duplication.

Next, let's talk about more
of Django's built-in template tags
that can supercharge your UI.

## The Templates Toolbox

The Django documentation includes
a {{< extlink "https://docs.djangoproject.com/en/4.1/ref/templates/builtins/" "large set of built-in tags" >}}
that you can use
in your projects.
We aren't going to cover all of them,
but I'll focus
on a few tags
to give you a flavor
of what is available.

One of the most used built-in tags
aside from what we've already covered
is the `url` tag.
{{< web >}}
Recall from the article
{{< /web >}}
{{< book >}}
Recall from the chapter
{{< /book >}}
on URLs
that you can get the URL
to a named view
by using the `reverse` function.
What if you wanted to use the URL
in your template?
You could do this:

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

While this works,
it's tedious to have to route all URLs
through the context.
Instead,
our template can directly create the proper URL.
Here's what `a_template.html` might look like instead:

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

The `url` tag is the template equivalent
of the `reverse` function.
Like its `reverse` counterpart,
`url` can accept args or kwargs
for routes
that expect other variables.
`url` is an incredibly useful tool
and one that you will probably reach for many times
as you build your user interface.

Another useful tag is the `now` tag.
`now` is a convenient method
to display information
about the current time.
Using what Django calls *format specifiers*,
you can tell your template how to display the current time.
Want to add a current copyright year to your website?
No problem!

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

One final built-in tag to consider is the `spaceless` tag.
HTML is *partially* sensitive to whitespace.
There are some frustrating circumstances
where this whitespace sensitivity can ruin your day
when building a user interface.
Can you make a pixel perfect navigation menu
for your site with an unordered list?
Maybe. Consider this:

```html
<ul class="navigation">
    <li><a href="/home/">Home</a></li>
    <li><a href="/about/">About</a></li>
</ul>
```

The indented whitespace on those list items
(or the new line characters that follow them)
might cause you trouble
when working with CSS.
Knowing that the whitespace can affect layout,
we can use `spaceless` like so:

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

This neat little template tag will remove all the spaces
between HTML tags
so your output looks like:

```html
<ul class="navigation"><li><a href="/home/">Home</a></li>...</ul>
```

By removing the extra space,
you may get a more consistent experience
with your CSS styling
and save yourself some frustration.
{{< web >}}
(I had to trim the output to fit better on the screen.)
{{< /web >}}

There is another kind of built-in
that we have not looked at yet.
These alternative built-in functions are called **filters**.
Filters change the output of variables
in your templates.
The filter syntax is a bit interesting.
It looks like:

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

The important element is the pipe character directly
after a variable.
This character signals to the template system
that we want to modify the variable
with some kind of transformation.
Also observe that filters are used
between double curly braces
instead of the `{%` syntax
that we've seen with tags.

A very common filter is the `date` filter.
When you pass a Python `datetime` instance
in the context,
you can use the `date` filter
to control the format
of the datetime.
The `date` {{< extlink "https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#date" "documentation" >}} shows
what options you can use
to modify the format.

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

If `a_datetime` was an instance of April Fools' Day,
then it could return a string like `2020-04-01`.
The `date` filter has many specifiers
that will enable you to produce most
of the date formatting outputs
you could think of.

`default` is a useful filter
for when your template value evaluates to `False`.
This is perfect when you've got a variable
with an empty string.
The example below outputs "Nothing to see here"
if the variable was Falsy.

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

Falsy is a concept in Python
that describes anything
that Python will evaluate as false
in a boolean expression.
Empty strings, empty lists, empty dicts, empty sets, `False`, and `None`
are all common Falsy values.

`length` is a simple filter
for lists.
`{{ a_list_variable|length }}` will produce a number.
It is the Django template equivalent to the `len` function.

I like the `linebreaks` filter a lot.
If you create a form
{{< web >}}
(which we'll explore in the next article)
{{< /web >}}
{{< book >}}
(which we'll explore in the next chapter)
{{< /book >}}
and accept a text area field where the user is allowed
to provide newlines,
then the `linebreaks` filter allows you
to display those newlines later
when rendering the user's data.
By default,
HTML will not show new line characters as intended.
The `linebreaks` filter will convert `\n`
to a `<br>` HTML tag.
Handy!

Before moving on,
let's consider two more.

`pluralize` is a convenient filter
for the times when your text considers counts
of things. Consider a count of items.

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

The `pluralize` filter will do the right thing
if there are zero, one, or more items
in the list.

```txt
0 items
1 item
2 items
3 items
(and so on)
```

Be aware that `pluralize` can't handle irregular plurals
like "mice" for "mouse."

The final filter in our tour is the `yesno` filter.
`yesno` is good for converting `True|False|None`
into a meaningful text message.
Imagine we're making an application
for tracking events
and a person's attendance is one
of those three values.
Our template might look like:

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

Depending on the value of `user_accepted`,
the template will display something meaningful
to a reader.

There are so many built-ins
that it's really hard to narrow down my favorites.
Check out the full list
to see what might be useful for you.

What if the built-ins don't cover what you need?
Have no fear,
Django lets you make custom tags and filters
for your own purposes.
We'll see how next.

## Build Your Own Lightsaber In Templates

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

Next,
we need to make our tag or filter
and register it.
Let's start with a filter example.

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

Now,
if we have a `message` variable,
we can give it some pizzazz.
To use the custom filter,
we must load our tags module
into the template
with the `load` tag.

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

If our message was "You got a perfect score!",
then our template should show the message
and one of the three random choices
like "You got a perfect score! Wowza!"

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

This silly welcome tag will respond
to multiple input variables
and vary depending on the provided level.
The example usage should display "Hello great champion He-Man!"

We're only looking at the most common kinds
of custom tags
in our examples.
There are some more advanced custom tagging features
which you can explore
in the {{< extlink "https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/" "Django custom template tags documentation" >}}.

Django also uses `load`
to provide template authors
with some additional tools.
For instance,
we will see how to load some custom tags provided
by the framework
when we learn about working with images and JavaScript later on.

## Summary

Now we've seen templates in action!
We've looked at:

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
we are going to examine
how users can send data to a Django application
with HTML forms.
Django has tools
to make form building quick and effective.
We're going to see:

* The `Form` class that Django uses to handle form data in Python
* Controlling what fields are in forms
* How forms are rendered to users by Django
* How to do form validation

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




Cuando usamos plantillas, tomamos datos de contexto y los insertamos en los marcadores de posición dentro de la plantilla.

Las variables de plantilla son la forma más básica de llenar marcadores de posición con contexto. La sección anterior mostró un ejemplo usando la variable de nombre. El diccionario de contexto contiene una clave de nombre, cuyo valor aparece en cualquier parte de la plantilla donde esa clave está rodeada por llaves dobles.

También podemos usar un punto de acceso cuando los datos de contexto son más complejos. Digamos que su plantilla obtiene contexto como:



Tu plantilla de Django no funcionará si intentas acceder a estos datos de contexto como un diccionario normal (por ejemplo, {{ address[street] }}). En su lugar, debes usar la notación de puntos para llegar a los datos en el diccionario:



Esto se traduciría como:



Las plantillas de Django además intentan ser flexibles con los tipos de datos de contexto. También podrías pasar una instancia de clase de Python como una clase  “address” con atributos que son los mismos que las claves en nuestro diccionario anterior. La plantilla funcionará igual.

El lenguaje de plantilla central también incluye algunas palabras clave de lógica de programación estándar mediante el uso de etiquetas. Las etiquetas de plantilla se ven como {% alguna_etiqueta %} mientras que las variables de plantilla se ven como {{ alguna_variable }}. Las variables están destinadas a ser marcadores de posición para completar, pero las etiquetas ofrecen más poder.

Podemos comenzar con dos etiquetas principales, if y for.

La etiqueta if es para manejar la lógica condicional que tu plantilla podría necesitar:



Este ejemplo solo incluirá esta etiqueta de encabezado HTML de mensaje de bienvenida cuando el usuario haya iniciado sesión en la aplicación. Comenzamos el ejemplo con una etiqueta if. Observe que la etiqueta if requiere una etiqueta endif de cierre. Las plantillas deben respetar los espacios en blanco ya que su diseño puede depender de ese espacio en blanco. El lenguaje de la plantilla no puede usar espacios en blanco para indicar el alcance como lo hace con Python, por lo que usa etiquetas de cierre en su lugar. Como puedes suponer, también hay etiquetas else y elif que se aceptan dentro de un par if/endif:



En este caso, solo se representará una de las etiquetas de encabezado dependiendo de si el usuario está autenticado o no.

La otra etiqueta central a considerar es la etiqueta de bucle for. Un bucle for en las plantillas de Django se comporta como cabría esperar:



Django recorrerá iterables como listas y permitirá a los usuarios generar respuestas de plantilla para cada entrada en un iterable. Si el ejemplo anterior tuviera una lista de elementos en el contexto como:



Entonces la salida se vería más o menos así:



Ocasionalmente, es posible que desees realizar alguna acción específica en un elemento particular en el bucle for. La función de enumeración integrada de Python no está disponible directamente en las plantillas, pero una variable especial llamada forloop está disponible dentro de una etiqueta for. Esta variable forloop tiene algunos atributos como primero y último que puede usar para hacer que las plantillas se comporten de manera diferente en ciertas iteraciones de bucle:



Este ejemplo producirá:



Equipado con variables, etiquetas if y etiquetas for, ahora deberías tener la capacidad de crear algunas plantillas bastante poderosas, ¡pero hay más!

Más contexto en contexto

Al establecer la configuración de las plantillas, pasamos por alto los procesadores de contexto. Los procesadores de contexto son una forma valiosa de ampliar el contexto que está disponible para sus plantillas cuando se procesan.

Aquí está el conjunto de procesadores de contexto que el comando startproject de Django trae por defecto.



Los procesadores de contexto son funciones (técnicamente, invocables, pero centrémonos en las funciones) que reciben una HttpRequest y deben devolver un diccionario. El diccionario devuelto se fusiona con cualquier otro contexto que se pasará a su plantilla.

Conceptualmente, cuando se prepara para renderizar y se le da un diccionario de contexto que se pasó para renderizar, el sistema de plantillas hará algo como:



El código real en el sistema de plantilla es más complejo que este boceto de código conceptual, ¡pero no mucho!

Podemos ver la definición real del procesador de contexto de solicitud incluido en esa lista predeterminada:



¡Eso es todo! Debido a este procesador de contexto, el objeto de solicitud estará disponible como una variable para cualquier plantilla de su proyecto. Eso es súper poderoso.

Comentario Aparte:

No tengas miedo de mirar el código fuente de los proyectos de los que dependes. ¡Recuerda que la gente normal escribió tus frameworks favoritos! Puedes aprender lecciones valiosas de lo que hicieron. El código puede ser un poco intimidante al principio, ¡pero no hay magia en ello!

El “lado oscuro” de los procesadores de contexto es que se ejecutan para todas las solicitudes. Si escribe un procesador de contexto que es lento y realiza muchos cálculos, cada solicitud sufrirá ese impacto en el rendimiento. Así que use los procesadores de contexto con cuidado.

Trozos de plantillas reutilizables

Ahora hablemos de una de las características más poderosas del sistema de plantillas: las piezas reutilizables.

Piensa en un sitio web. La mayoría de las páginas tienen una apariencia similar. Lo hacen repitiendo mucho del mismo HTML, que es el lenguaje de marcado de hipertexto que define la estructura de una página. Estas páginas también usan el mismo CSS, hojas de estilo en cascada, que definen los estilos que dan forma al aspecto de los elementos de la página.

Imagina que te piden que administres un sitio y necesitas crear dos páginas separadas. La página de inicio se parece a lo siguiente:



Y aquí hay una página para obtener información sobre la empresa detrás del sitio web:



Estos ejemplos son pequeñas cantidades de HTML, pero ¿qué sucede si se le pide que cambie la hoja de estilos de estilos.css a una nueva hoja de estilos creada por un diseñador llamado better_styles.css? Tendrías que actualizar ambos lugares. Ahora piensa si hubiera 2000 páginas en lugar de 2 páginas. ¡Hacer grandes cambios rápidamente en un sitio sería prácticamente imposible!

Django te ayuda a evitar este escenario por completo con algunas etiquetas. Hagamos una nueva plantilla llamada base.html:



¡Hemos creado una plantilla reutilizable con la etiqueta block! Podemos arreglar nuestra página de inicio para usar esta nueva plantilla:



Esta nueva versión de la página de inicio amplía la plantilla base. Todo lo que la plantilla tenía que hacer era definir su propia versión del bloque principal para completar el contenido. Podríamos hacer exactamente lo mismo con la página “Acerca de “.

Si revisamos la tarea de reemplazar styles.css con better_styles.css, podemos hacer la actualización en base.html y hacer que ese cambio se aplique a cualquier plantilla que lo amplíe. Incluso si hubiera 2,000 páginas que se extendieran desde base.html, cambiar la hoja de estilo aún sería una línea de código para cambiar para todo el sitio.

Ese es el poder del sistema de extensión de plantillas de Django. Usa extends cuando necesites contenido que sea mayormente el mismo. Agrega una sección block cada vez que necesites personalizar una página extendida. Puedes ampliar una página incluyendo varios tipos de secciones block. El ejemplo solo muestra un bloque principal, pero es posible que tenga páginas que personalicen una barra lateral, encabezado, pie de página o lo que sea que pueda variar.

Otra poderosa herramienta para la reutilización es la etiqueta include. La etiqueta include es útil cuando deseas extraer una parte de la plantilla que deseas usar en varias ubicaciones. Es posible que desees utilizar include para:

Mantener las plantillas ordenadas. Puedes dividir una plantilla grande en partes pequeñas que sean más manejables.
Usar un fragmento de plantilla en diferentes partes de su sitio. Tal vez tengas una pieza de plantilla que solo debería aparecer en unas pocas páginas.

Volviendo al ejemplo de nuestro sitio web, imagina que base.html creció hasta tener 20,000 líneas de largo. Navegar a la parte derecha de la plantilla para hacer cambios ahora es más difícil. Podemos descomponer la plantilla en piezas más pequeñas:



La etiqueta de include puede mover esas piezas adicionales. Al proporcionar un buen nombre para sus plantillas, si necesitas cambiar la estructura de alguna sección como la barra de navegación, puedes ir a la plantilla con el nombre apropiado. Ese archivo de plantilla se centraría solo en el elemento que necesita cambiar.

Block, extends e include son etiquetas principales para evitar que el código de la interfaz de usuario se extienda por todas partes con muchas duplicaciones.

A continuación, hablaremos de más etiquetas de plantilla integradas de Django que pueden potenciar tu interfaz de usuario.
La caja de herramientas de plantillas
La documentación de Django incluye un gran conjunto de etiquetas integradas que puedes usar en tus proyectos. No los cubriremos todos, pero me concentraré en algunas etiquetas para darte una idea de lo que está disponible.

Una de las etiquetas integradas más utilizadas, aparte de lo que ya hemos cubierto, es la etiqueta de URL. Recuerde del artículo sobre direcciones URL que puede llevar la dirección URL a una vista con nombre utilizando la función inversa. ¿Qué pasaría si quisieras usar la URL en tu plantilla? Podrías hacer esto:



Si bien esto funciona, es tedioso tener que enrutar todas las URL a través del contexto. En cambio, nuestra plantilla puede crear directamente la URL adecuada. Así es como se vería una_plantilla.html en su lugar:



La etiqueta url es el equivalente de las plantillas a la función inversa. Al igual que su contraparte inversa, url puede aceptar args o kwargs para rutas que esperan otras variables. url es una herramienta increíblemente útil y probablemente la usarás muchas veces mientras construyes su interfaz de usuario.

Otra etiqueta útil es la etiqueta now. Now es un método conveniente para mostrar información sobre la hora actual. Usando lo que Django llama especificadores de formato, puedes decirle a tu plantilla cómo mostrar la hora actual. ¿Quieres agregar un año de copyright actual a tu sitio web? ¡No hay problema!:



Una última etiqueta incorporada a considerar es la etiqueta spaceless. HTML es parcialmente sensible a los espacios en blanco. Hay algunas circunstancias frustrantes en las que esta sensibilidad a los espacios en blanco puede arruinar tu día al crear una interfaz de usuario. ¿Puedes hacer un menú de navegación de píxeles perfectos para tu sitio con una lista desordenada? Tal vez. Considera esto:



Los espacios en blanco sangrados en esos elementos de la lista (o los caracteres de nueva línea que los siguen) pueden causar problemas al trabajar con CSS. Sabiendo que el espacio en blanco puede afectar el diseño, podemos usar spaceless así:



Esta pequeña y ordenada etiqueta de plantilla eliminará todos los espacios entre las etiquetas HTML para que su resultado se vea así:



Al eliminar el espacio extra, puedes obtener una experiencia más consistente con su estilo CSS y ahorrarte algo de frustración. (Tuve que recortar la salida para que encajara mejor en la pantalla).

Hay otro tipo de incorporado que aún no hemos visto. Estas funciones integradas alternativas se denominan filtros. Los filtros cambian la salida de las variables en tus plantillas. La sintaxis del filtro es un poco interesante. Luce así:



El elemento importante es el carácter de pleca o barra vertical directamente después de una variable. Este carácter le indica al sistema de plantillas que queremos modificar la variable con algún tipo de transformación. También observe que los filtros se usan entre llaves dobles en lugar de la sintaxis {%%} que hemos visto con las etiquetas.

Un filtro muy común es el filtro de fecha. Cuando pasa una instancia de fecha y hora de Python en el contexto, puede usar el filtro de fecha para controlar el formato de la fecha y hora. La documentación de la fecha muestra qué opciones puede usar para modificar el formato.



Si a_datetime fuera una instancia del Día de los Inocentes, entonces podría devolver una cadena como “2020-04-01”. El filtro de fecha tiene muchos especificadores que le permitirán producir la mayoría de las salidas de formato de fecha que pueda imaginar.

default es un filtro útil para cuando el valor de su plantilla se evalúa como False. Esto es perfecto cuando tienes una variable con una cadena vacía. El siguiente ejemplo muestra "Nada que ver aquí" si la variable es Falsy.



Falsy es un concepto en Python que describe cualquier cosa que Python evalúa como falsa en una expresión booleana. Cadenas vacías, listas vacías, dictados vacíos, conjuntos vacíos, Falso y Ninguno son todos valores falsos comunes.

length es un filtro simple para listas. {{ a_list_variable|length }} producirá un número. Es la plantilla de Django equivalente a la función length.

Me gusta mucho el filtro linebreaks. Si crea un formulario (que explicaremos en el próximo artículo) y acepta un campo de área de texto en el que el usuario puede proporcionar nuevas líneas, entonces el filtro de saltos de línea te permite mostrar esas nuevas líneas más adelante cuando representes los datos del usuario. De forma predeterminada, HTML no mostrará caracteres de nueva línea según lo previsto. El filtro de saltos de línea convertirá \n en una etiqueta HTML <br>. ¡Práctico!

Antes de continuar, consideremos dos filtros más.

pluralize es un filtro conveniente para los momentos en que tu texto considera recuentos de cosas. Consideremos un conteo de elementos:



El filtro de pluralize hará lo correcto si hay cero, uno o más elementos en la lista.



Ten en cuenta que pluralize no puede manejar plurales irregulares como "mice" para "mouse".

El filtro final en nuestro recorrido es el filtro yesno. yesno es bueno para convertir Verdadero|Falso|Ninguno en un mensaje de texto significativo. Imagina que estamos haciendo una aplicación para rastrear eventos y la asistencia de una persona es uno de esos tres valores. Nuestra plantilla podría verse así:



Según el valor de user_accepted, la plantilla mostrará algo significativo para el lector.

Hay tantos filtros integrados que es realmente difícil seleccionar mis favoritos. Consulta la lista completa para ver lo que podría ser útil para tí.

¿Qué sucede si los elementos integrados no cubren lo que necesitas? No temas, Django te permite crear etiquetas y filtros personalizados para tus propios fines. Veremos cómo a continuación.

Construye tu propio sable de luz en plantillas
Cuando necesites crear tus propias etiquetas o filtros de plantilla, Django te brindará las herramientas para hacer lo que necesites.

Hay tres elementos principales para trabajar con etiquetas personalizadas:

Definiendo tus etiquetas en un lugar que espera Django.
Registrando tus etiquetas con el motor de plantillas.
Cargando tus etiquetas en una plantilla para que puedan ser utilizadas.

El primer paso es colocar las etiquetas en la ubicación correcta. Para hacer eso, necesitamos un paquete Python templatetags dentro de una aplicación Django. También necesitamos un módulo en ese directorio. Elige el nombre del módulo con cuidado porque es lo que cargaremos en la plantilla más adelante:



A continuación, debemos crear nuestra etiqueta o filtro y registrarlo. Comencemos con un ejemplo de filtro:



Ahora, si tenemos una variable message, podemos darle un poco de dinamismo. Para usar el filtro personalizado, debemos cargar nuestro módulo de etiquetas en la plantilla con la etiqueta load:


Si nuestro mensaje fue "¡Obtuviste un puntaje perfecto!", entonces nuestra plantilla debería mostrar el mensaje y una de las tres opciones aleatorias como "¡Obtuviste un puntaje perfecto! ¡Guau!

Escribir etiquetas personalizadas básicas es muy similar a los filtros personalizados. El código hablará mejor que las palabras aquí:



Podemos cargar las etiquetas personalizadas y usar nuestra etiqueta como cualquier otra etiqueta integrada:



Esta tonta etiqueta de bienvenida responderá a múltiples variables de entrada y variará según el nivel proporcionado. El ejemplo de uso debería mostrar "¡Hola, gran campeón He-Man!"

Solo estamos viendo los tipos más comunes de etiquetas personalizadas en nuestros ejemplos. Hay algunas funciones de etiquetado personalizadas más avanzadas que puede explorar en la documentación de etiquetas de plantillas personalizadas de Django.

Django también usa load para proporcionar a los autores de plantillas algunas herramientas adicionales. Por ejemplo, veremos cómo cargar algunas etiquetas personalizadas proporcionadas por el framework cuando aprendamos a trabajar con imágenes y JavaScript más adelante.

Resumen
¡Ahora hemos visto plantillas en acción! Hemos mirado:

Cómo configurar plantillas para su sitio
Maneras de llamar plantillas desde vistas
Cómo usar los datos
Cómo manejar la lógica
Etiquetas y filtros incorporados disponibles para las plantillas
Personalización de plantillas con sus propias extensiones de código

En el próximo artículo, examinaremos cómo los usuarios pueden enviar datos a una aplicación Django con formularios HTML. Django tiene herramientas para hacer que la creación de formularios sea rápida y efectiva. vamos a ver:

La clase Form que usa Django para manejar datos de formularios en Python
Controlar qué campos hay en los formularios
Cómo Django presenta los formularios a los usuarios
Cómo hacer la validación de formularios

Si deseas seguir la serie, no dudes en suscribirte a mi boletín informativo donde anuncio todo mi contenido nuevo. Si tienes otras preguntas, puede comunicarse conmigo en línea en Twitter, donde soy @mblayman.

