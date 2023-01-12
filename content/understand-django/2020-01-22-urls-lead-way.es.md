---
title: "Las URL Marcan El Camino"
slug: "url-marcan-camino"
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

En el último artículo de la serie
[Comprendiendo Django]({{< ref "/understand-django/_index.es.md" >}}),
vimos cómo la solicitud del navegador de un usuario pasa de su navegador a la "puerta principal" de Django. Ahora es el momento de ver cómo Django procesa esas solicitudes.

Una solicitud HTTP proveniente de un navegador incluye una URL que describe qué recurso debe producir Django. Dado que las URL pueden tener muchas formas, debemos instruir a Django sobre los tipos de URL que nuestra aplicación web puede manejar. Para eso está la *configuración de URL*. En la documentación de Django, la configuración de URL se llama URLconf, para abreviar.

¿Dónde está la URLconf? La URLconf está en la ruta del módulo establecida por la configuración `ROOT_URLCONF` en el archivo de configuración de su proyecto. Si ejecutó el comando `startproject`, esa configuración se llamará como `proyecto.urls`, donde "proyecto" es el nombre dado como argumento para el comando. En otras palabras, la URLconf se coloca en `proyecto/urls.py`, justo al lado del archivo `settings.py`.

Eso explica dónde reside el archivo, pero no nos dice mucho sobre cómo funciona. Profundicemos más.

{{< understand-django-series-es "urls" >}}

## URLconf en acción

Trata de pensar en la configuración de URL como una lista de rutas de URL que Django intentará hacer coincidir de arriba a abajo. Cuando Django encuentra una ruta coincidente, la solicitud HTTP se enruta a un fragmento de código de Python asociado con esa ruta. Ese "trozo de código de Python" se llama una *vista* que explicaremos más en un momento. Por el momento, confía en que las vistas saben cómo manejar las solicitudes HTTP.

Podemos usar un URLconf de ejemplo para darle vida a este concepto:

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

Lo que vemos aquí coincide bien con lo que describí anteriormente: una lista de rutas de URL que Django intentará hacer coincidir de arriba a abajo. El aspecto clave de esta lista es el nombre de `urlpatterns`. Django tratará la lista en una variable `urlpatterns` como URLconf.

El orden de esta lista también es importante porque Django dejará de escanear la lista tan pronto como encuentre una coincidencia. El ejemplo no muestra ningún conflicto entre las rutas, pero es posible crear dos entradas de ruta (`path`) diferentes que pueden coincidir con la misma URL que envía un usuario. Mostraré un ejemplo de cómo puede suceder eso después de que veamos otro aspecto de las rutas.

Podemos trabajar con un ejemplo para ver cómo funciona esto para `www.example.com`. Al considerar una URL en una URLconf, Django ignora el esquema (`https://`), el dominio (`www.example.com`) y la barra inclinada inicial para la coincidencia. Todo lo demás es con lo que se comparará la URLconf.

* Una solicitud a `https://www.example.com/about/` se verá como `"about/"` para el proceso de coincidencia de patrones y coincidirá con la segunda ruta. Esa solicitud se enruta a la vista `views.about`.
* Una solicitud a `https://www.example.com/` se verá como `""` (una cadena de texto vacía) en el proceso de coincidencia de patrones y coincidirá con la primera ruta. Esa solicitud se enruta a la vista `views.home`.

> Aparte: puedes notar que las URL de Django terminan con un carácter de barra inclinada. Este comportamiento se debe a una elección de
{{< extlink "https://docs.djangoproject.com/en/4.1/misc/design-philosophies/#definitive-urls" "filosofía de diseño" >}} choice.
de Django. De hecho, si intenta llegar a una URL como `https://www.example.com/about`, Django redirigirá la solicitud a la misma URL con la barra inclinada añadida debido a la
{{< extlink "https://docs.djangoproject.com/en/4.1/ref/settings/#append-slash" "configuración predeterminada" >}}
de `APPEND_SLASH`.

## El camino antes que nosotros

La parte de cadena de texto de una ruta (por ejemplo, `"about/"`) se considera la ruta en si misma. Una ruta puede ser una cadena de texto simple como se ha visto, pero puede incluir otras estructuras especiales con una característica llamada `convertidores`. Cuando usas un convertidor, puedes extraer información de una URL que una vista puede usar más tarde. Considera una ruta como esta:

```python
    path(
        "blog/<int:year>/<slug:slug>/",
        views.blog_post
    ),
```

Los dos convertidores en esta ruta son:

* `<int:year>`
* `<slug:slug>`

El uso de corchetes angulares y algunos
{{< extlink "https://docs.djangoproject.com/en/4.1/topics/http/urls/#path-converters" "nombres reservados" >}}
hacen que Django realice un análisis adicional en una URL. Cada convertidor tiene algunas reglas esperadas a seguir.

* El convertidor `int` debe coincidir con un número entero.
* El convertidor de `slug` debe coincidir con un slug. 
    Slug es un término salido de la jerga de los periódicos que aparece en Django porque Django comenzó como un proyecto de un periódico en Kansas. Un slug es una cadena que puede incluir caracteres, números, guiones y guiones bajos.

Dadas esas definiciones de convertidor, ¡comparemos con algunas URL!

* `https://www.example.com/blog/2020/urls-lead-way/` - ¡COINCIDE!
* `https://www.example.com/blog/twenty-twenty/urls-lead-way/` - NO.
* `https://www.example.com/blog/0/life-in-rome/` - ¡COINCIDE! Uh, quizás no sea lo que queríamos. Veremos eso pronto.

Ahora podemos revisar nuestro problema de ordenamiento de antes. Considere estas dos rutas en diferentes órdenes:

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

En el primer orden, el convertidor coincidirá con cualquier número entero después de `blog/`, incluido `https://www.example.com/blog/2020/`. Eso significa que el primer pedido nunca llamará a la vista `blog_for_twenty_twenty` porque Django hace coincidir las entradas de la ruta en orden.

Por el contrario, en el segundo orden, `blog/2020/` se enrutará correctamente a `blog_for_twenty_twenty` porque coincide primero. Eso significa que hay una lección para recordar aquí:

> Cuando incluyas entradas de ruta que coincidan en rangos de valores con convertidores (como el ejemplo de años anterior), asegúrate de colocarlas **después** de las entradas más específicas.

## Una “vista abreviada” de vistas

¿Qué hacen los convertidores con estos datos adicionales? Eso es difícil de explicar sin tocar las vistas. El próximo artículo cubrirá las vistas con mucha más profundidad, pero aquí hay una introducción.

Una vista es un código que toma una solicitud y devuelve una respuesta. Usando type hint de Python de manera opcional, aquí hay un ejemplo que devolverá la respuesta `Hola mundo`.

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

`HttpRequest` es el formato traducido de Django de una solicitud HTTP envuelta en una clase de contenedor conveniente. Del mismo modo, `HttpResponse` es lo que podemos usar para que Django traduzca nuestros datos de respuesta en una respuesta HTTP con el formato adecuado que se enviará de vuelta al navegador del usuario.

Ahora podemos mirar de nuevo uno de los convertidores.

```python
    path(
        "blog/<int:year>/",
        views.blog_by_year
    ),
```

Con este convertidor en la ruta, ¿cómo sería `blog_by_year`?

```python
# application/views.py
from django.http import HttpResponse

def blog_by_year(request, year):
    # ... some code to handle the year
    data = 'Some data set by code above'
    return HttpResponse(data)
```

¡Django comienza a revelar algunas buenas cualidades aquí! El convertidor hizo un montón de trabajo tedioso para nosotros. El argumento `year` establecido por Django ya será un número entero porque Django realizó el análisis y la conversión de cadenas.

Si alguien envía `/blog/not_a_number/`, Django devolverá una respuesta No encontrado porque `not_a_number` no puede ser un número entero. El beneficio de esto es que no tenemos que poner una lógica de verificación adicional en `blog_by_year` para manejar el caso extraño en el que el año no parece un número. ¡Ese tipo de característica es un ahorro de tiempo real! Mantiene su código más limpio y hace que el manejo sea más preciso.

¿Qué pasa con ese otro ejemplo extraño que vimos antes de `/blog/0/life-in-rome/`? Eso coincidiría con nuestro patrón de la sección anterior, pero supongamos que queremos coincidir con un año de cuatro dígitos. ¿Cómo podemos hacer eso? Podemos usar expresiones regulares.

## Regular Expression Paths

Regular expressions are a programming feature
often likened to a chainsaw:
*they are incredibly powerful,
but you can cut off your foot
if you're not careful.*

Regular expressions can express complex patterns
of characters
in a concise way.
This conciseness often gives regular expressions a bad reputation
of being difficult to understand.
When used carefully, though,
they can be highly effective.

A regular expression
(which is often abbreviated to "regex")
matches complex patterns
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

* The string itself starts with `r"`
    because it is a raw string in Python.
    This is used because regular expressions use `\` extensively.
    Without a raw string,
    a developer would have to escape the backslash repeatedly
    by using `\\`.
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

Note that you cannot mix the `path` style and `re_path` style strings.
The example above had to describe the slug as a regular expression
instead of using the slug converter (i.e., `<slug:slug>`).

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
even if you don't need it now.

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
    return HttpResponseRedirect(
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

from blog import views

urlpatterns = [
    ...
    path(
        "/marketing/blog/categories/",
        views.categories,
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
    return HttpResponseRedirect(
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
Put one ball of each color
in each of the two buckets labeled "A" and "B."
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
{{< /web >}}
{{< book >}}
In the next chapter,
we'll dig into views.
This chapter only gave the briefest definition
{{< /book >}}
to what a view is.
Django gives us very rich options
when working with views.
We're going to explore:

* View functions
* View classes
* Some built-in supporting views
* Decorators that supercharge views.

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
