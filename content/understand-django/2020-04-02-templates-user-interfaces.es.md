---
title: "Plantillas para Interfaces de Usuario"
slug: "plantillas-interfaces-usuario"
description: >-
    Cuando tu aplicación Django
    devuelve una respuesta
    junto a tu interfaz de usuario,
    las plantillas son la herramienta que usarás
    para producir esa interfaz de usuario.
    Este artículo explora
    qué son las plantillas
    y cómo usarlas.
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

Cuando usamos plantillas, tomamos datos de contexto y los insertamos en los marcadores de posición dentro de la plantilla.

Las variables de plantilla son la forma más básica de llenar marcadores de posición con contexto. La sección anterior mostró un ejemplo usando la variable de nombre. El diccionario de contexto contiene una clave de nombre, cuyo valor aparece en cualquier parte de la plantilla donde esa clave está rodeada por llaves dobles.

También podemos usar un punto de acceso cuando los datos de contexto son más complejos. Digamos que su plantilla obtiene contexto como:

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

Tu plantilla de Django no funcionará si intentas acceder a estos datos de contexto como un diccionario normal (por ejemplo, `{{ address[street] }}`). En su lugar, debes usar la notación de puntos para llegar a los datos en el diccionario:

```txt
The address is:
    {{ address.street }}
    {{ address.city }}, {{ address.state }} {{ address.zip_code}}
```

Esto se traduciría como:

```txt
The address is:
    123 Main St.
    Beverly Hills, CA 90210
```

Las plantillas de Django además intentan ser flexibles con los tipos de datos de contexto. También podrías pasar una instancia de clase de Python como una clase `Address` con atributos que son los mismos que las claves en nuestro diccionario anterior. La plantilla funcionará igual.

El lenguaje de plantilla central también incluye algunas palabras clave de lógica de programación estándar mediante el uso de etiquetas. Las etiquetas de plantilla se ven como `{% alguna_etiqueta %}` mientras que las variables de plantilla se ven como `{{ alguna_variable }}`. Las variables están destinadas a ser marcadores de posición para completar, pero las etiquetas ofrecen más poder.

Podemos comenzar con dos etiquetas principales, `if` y `for`.

La etiqueta `if` es para manejar la lógica condicional que tu plantilla podría necesitar:

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

Este ejemplo solo incluirá esta etiqueta de encabezado HTML de mensaje de bienvenida cuando el usuario haya iniciado sesión en la aplicación. Comenzamos el ejemplo con una etiqueta `if`. Observe que la etiqueta `if` requiere una etiqueta `endif` de cierre. Las plantillas deben respetar los espacios en blanco ya que su diseño puede depender de ese espacio en blanco. El lenguaje de la plantilla no puede usar espacios en blanco para indicar el alcance como lo hace con Python, por lo que usa etiquetas de cierre en su lugar. Como puedes suponer, también hay etiquetas `else` y `elif` que se aceptan dentro de un par `if`/`endif`:

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

En este caso, solo se representará una de las etiquetas de encabezado dependiendo de si el usuario está autenticado o no.

La otra etiqueta central a considerar es la etiqueta de bucle `for`. Un bucle `for` en las plantillas de Django se comporta como cabría esperar:

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

Django recorrerá iterables como listas y permitirá a los usuarios generar respuestas de plantilla para cada entrada en un iterable. Si el ejemplo anterior tuviera una lista de elementos en el contexto como:


```python
items = [
    {'name': 'Pizza', 'price': '$12.99'},
    {'name': 'Soda', 'price': '$3.99'},
]
```

Entonces la salida se vería más o menos así:

```html
<p>Prices:</p>
<ul>
    <li>Pizza costs $12.99.</li>
    <li>Soda costs $3.99.</li>
</ul>
```

Ocasionalmente, es posible que desees realizar alguna acción específica en un elemento particular en el bucle `for`. La función de enumeración integrada de Python no está disponible directamente en las plantillas, pero una variable especial llamada `forloop` está disponible dentro de una etiqueta `for`. Esta variable `forloop` tiene algunos atributos como primero (`first`) y último (`last`) que puede usar para hacer que las plantillas se comporten de manera diferente en ciertas iteraciones de bucle:

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

Este ejemplo producirá:

```txt
Counting:
    1
    2
    3 is last!
```

Equipado con variables, etiquetas `if` y etiquetas `for`, ahora deberías tener la capacidad de crear algunas plantillas bastante poderosas, ¡pero hay más!

### Más contexto en contexto

Al establecer la configuración de las plantillas, pasamos por alto los procesadores de contexto. Los procesadores de contexto son una forma valiosa de ampliar el contexto que está disponible para sus plantillas cuando se procesan.

Aquí está el conjunto de procesadores de contexto que el comando `startproject` de Django trae por defecto.

```python
'context_processors': [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
],
```

Los procesadores de contexto son funciones (técnicamente, invocables, pero centrémonos en las funciones) que reciben una `HttpRequest` y deben devolver un diccionario. El diccionario devuelto se fusiona con cualquier otro contexto que se pasará a su plantilla.

Conceptualmente, cuando se prepara para renderizar y se le da un diccionario de contexto que se pasó para renderizar, el sistema de plantillas hará algo como:

```python
for processor in context_processors:
    context.update(processor(request))

# Continue on to template rendering
```

El código real en el sistema de plantilla es más complejo que este boceto de código conceptual, ¡pero no mucho!

Podemos ver la definición real del procesador de contexto de solicitud incluido en esa lista predeterminada:

```python
# django/template/context_processors.py

def request(request):
    return {'request': request}
```

¡Eso es todo! Debido a este procesador de contexto, el objeto de solicitud estará disponible como una variable para cualquier plantilla de su proyecto. Eso es súper poderoso.

<div class='sidebar'>

<h4>Comentario Aparte:</h4>

<p>
No tengas miedo de mirar el código fuente de los proyectos de los que dependes. ¡Recuerda que la gente normal escribió tus frameworks favoritos! Puedes aprender lecciones valiosas de lo que hicieron. El código puede ser un poco intimidante al principio, ¡pero no hay magia en ello!
</p>

</div>

El “lado oscuro” de los procesadores de contexto es que se ejecutan para todas las solicitudes. Si escribe un procesador de contexto que es lento y realiza muchos cálculos, cada solicitud sufrirá ese impacto en el rendimiento. Así que use los procesadores de contexto con cuidado.

### Trozos de plantillas reutilizables

Ahora hablemos de una de las características más poderosas del sistema de plantillas: las piezas reutilizables.

Piensa en un sitio web. La mayoría de las páginas tienen una apariencia similar. Lo hacen repitiendo mucho del mismo HTML, que es el lenguaje de marcado de hipertexto que define la estructura de una página. Estas páginas también usan el mismo CSS, hojas de estilo en cascada, que definen los estilos que dan forma al aspecto de los elementos de la página.

Imagina que te piden que administres un sitio y necesitas crear dos páginas separadas. La página de inicio se parece a lo siguiente:

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

Y aquí hay una página para obtener información sobre la empresa detrás del sitio web:

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

Estos ejemplos son pequeñas cantidades de HTML, pero ¿qué sucede si se le pide que cambie la hoja de estilos de `styles.css` a una nueva hoja de estilos creada por un diseñador llamado `better_styles.css`? Tendrías que actualizar ambos lugares. Ahora piensa si hubiera 2000 páginas en lugar de 2 páginas. ¡Hacer grandes cambios rápidamente en un sitio sería prácticamente imposible!

Django te ayuda a evitar este escenario por completo con algunas etiquetas. Hagamos una nueva plantilla llamada `base.html`:

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

¡Hemos creado una plantilla reutilizable con la etiqueta `block`! Podemos arreglar nuestra página de inicio para usar esta nueva plantilla:

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

Esta nueva versión de la página de inicio amplía la plantilla base. Todo lo que la plantilla tenía que hacer era definir su propia versión del bloque principal (`main`) para completar el contenido. Podríamos hacer exactamente lo mismo con la página “Acerca de “.

Si revisamos la tarea de reemplazar `styles.css` con `better_styles.css`, podemos hacer la actualización en `base.html` y hacer que ese cambio se aplique a cualquier plantilla que lo amplíe. Incluso si hubiera 2,000 páginas que se extendieran desde `base.html`, cambiar la hoja de estilo aún sería una línea de código para cambiar para todo el sitio.

Ese es el poder del sistema de extensión de plantillas de Django. Usa `extend` cuando necesites contenido que sea mayormente el mismo. Agrega una sección `block` cada vez que necesites personalizar una página extendida. Puedes ampliar una página incluyendo varios tipos de secciones block. El ejemplo solo muestra un bloque principal, pero es posible que tenga páginas que personalicen una barra lateral, encabezado, pie de página o lo que sea que pueda variar.

Otra poderosa herramienta para la reutilización es la etiqueta `include`. La etiqueta `include` es útil cuando deseas extraer una parte de la plantilla que deseas usar en varias ubicaciones. Es posible que desees utilizar `include` para:

1. Mantener las plantillas ordenadas. Puedes dividir una plantilla grande en partes pequeñas que sean más manejables.
2. Usar un fragmento de plantilla en diferentes partes de su sitio. Tal vez tengas una pieza de plantilla que solo debería aparecer en unas pocas páginas.

Volviendo al ejemplo de nuestro sitio web, imagina que `base.html` creció hasta tener 20,000 líneas de largo. Navegar a la parte derecha de la plantilla para hacer cambios ahora es más difícil. Podemos descomponer la plantilla en piezas más pequeñas:

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

La etiqueta de `include` puede mover esas piezas adicionales. Al proporcionar un buen nombre para sus plantillas, si necesitas cambiar la estructura de alguna sección como la barra de navegación, puedes ir a la plantilla con el nombre apropiado. Ese archivo de plantilla se centraría solo en el elemento que necesita cambiar.

`block`, `extends` e `include` son etiquetas principales para evitar que el código de la interfaz de usuario se extienda por todas partes con muchas duplicaciones.

A continuación, hablaremos de más etiquetas de plantilla integradas de Django que pueden potenciar tu interfaz de usuario.

## La caja de herramientas de plantillas

La documentación de Django incluye un
{{< extlink "https://docs.djangoproject.com/en/4.1/ref/templates/builtins/" "gran conjunto de etiquetas integradas" >}}
que puedes usar en tus proyectos. No los cubriremos todos, pero me concentraré en algunas etiquetas para darte una idea de lo que está disponible.

Una de las etiquetas integradas más utilizadas, aparte de lo que ya hemos cubierto, es la etiqueta de URL (`url`). Recuerde del artículo sobre direcciones URL que puede llevar la dirección URL a una vista con nombre utilizando la función inversa (`reverse`). ¿Qué pasaría si quisieras usar la URL en tu plantilla? Podrías hacer esto:

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

Si bien esto funciona, es tedioso tener que enrutar todas las URL a través del contexto. En cambio, nuestra plantilla puede crear directamente la URL adecuada. Así es como se vería `a_template.html` en su lugar:

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

La etiqueta `url` es el equivalente de las plantillas a la función inversa. Al igual que su contraparte inversa, `url` puede aceptar args o kwargs para rutas que esperan otras variables. `url` es una herramienta increíblemente útil y probablemente la usarás muchas veces mientras construyes su interfaz de usuario.

Otra etiqueta útil es la etiqueta `now`. `now` es un método conveniente para mostrar información sobre la hora actual. Usando lo que Django llama especificadores de formato, puedes decirle a tu plantilla cómo mostrar la hora actual. ¿Quieres agregar un año de copyright actual a tu sitio web? ¡No hay problema!:

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

Una última etiqueta incorporada a considerar es la etiqueta `spaceless`. HTML es parcialmente sensible a los espacios en blanco. Hay algunas circunstancias frustrantes en las que esta sensibilidad a los espacios en blanco puede arruinar tu día al crear una interfaz de usuario. ¿Puedes hacer un menú de navegación de píxeles perfectos para tu sitio con una lista desordenada? Tal vez. Considera esto:


```html
<ul class="navigation">
    <li><a href="/home/">Home</a></li>
    <li><a href="/about/">About</a></li>
</ul>
```

Los espacios en blanco sangrados en esos elementos de la lista (o los caracteres de nueva línea que los siguen) pueden causar problemas al trabajar con CSS. Sabiendo que el espacio en blanco puede afectar el diseño, podemos usar `spaceless` así:

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

Esta pequeña y ordenada etiqueta de plantilla eliminará todos los espacios entre las etiquetas HTML para que su resultado se vea así:

```html
<ul class="navigation"><li><a href="/home/">Home</a></li>...</ul>
```

Al eliminar el espacio extra, puedes obtener una experiencia más consistente con su estilo CSS y ahorrarte algo de frustración. (Tuve que recortar la salida para que encajara mejor en la pantalla).

Hay otro tipo de incorporado que aún no hemos visto. Estas funciones integradas alternativas se denominan **filtros**. Los filtros cambian la salida de las variables en tus plantillas. La sintaxis del filtro es un poco interesante. Luce así:

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

El elemento importante es el carácter de pleca o barra vertical directamente después de una variable. Este carácter le indica al sistema de plantillas que queremos modificar la variable con algún tipo de transformación. También observe que los filtros se usan entre llaves dobles en lugar de la sintaxis `{%` que hemos visto con las etiquetas.

Un filtro muy común es el filtro de fecha. Cuando pasa una instancia de fecha y hora de Python en el contexto, puede usar el filtro de fecha para controlar el formato de la fecha y hora. La
{{< extlink "https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#date" "documentación" >}}
de la fecha muestra qué opciones puede usar para modificar el formato.

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

Si `a_datetime` fuera una instancia del Día de los Inocentes, entonces podría devolver una cadena como `2020-04-01`. El filtro de fecha tiene muchos especificadores que le permitirán producir la mayoría de las salidas de formato de fecha que pueda imaginar.

`default` es un filtro útil para cuando el valor de su plantilla se evalúa como `False`. Esto es perfecto cuando tienes una variable con una cadena vacía. El siguiente ejemplo muestra "Nada que ver aquí" si la variable es Falsy.

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

Falsy es un concepto en Python que describe cualquier cosa que Python evalúa como falsa en una expresión booleana. Cadenas vacías, listas vacías, dictados vacíos, conjuntos vacíos, `False` y `None` son todos valores falsos comunes.

`length` es un filtro simple para listas. `{{ a_list_variable|length }}` producirá un número. Es la plantilla de Django equivalente a la función `len`.

Me gusta mucho el filtro `linebreaks`. Si crea un formulario (que explicaremos en el próximo artículo) y acepta un campo de área de texto en el que el usuario puede proporcionar nuevas líneas, entonces el filtro de saltos de línea te permite mostrar esas nuevas líneas más adelante cuando representes los datos del usuario. De forma predeterminada, HTML no mostrará caracteres de nueva línea según lo previsto. El filtro de saltos de línea convertirá `\n` en una etiqueta HTML `<br>`. ¡Práctico!

Antes de continuar, consideremos dos filtros más.

`pluralize` es un filtro conveniente para los momentos en que tu texto considera recuentos de cosas. Consideremos un conteo de elementos:

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

El filtro de `pluralize` hará lo correcto si hay cero, uno o más elementos en la lista.

```txt
0 items
1 item
2 items
3 items
(and so on)
```

Ten en cuenta que `pluralize` no puede manejar plurales irregulares como "mice" para "mouse".

El filtro final en nuestro recorrido es el filtro `yesno`. `yesno` es bueno para convertir `True|False|None` en un mensaje de texto significativo. Imagina que estamos haciendo una aplicación para rastrear eventos y la asistencia de una persona es uno de esos tres valores. Nuestra plantilla podría verse así:

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

Según el valor de `user_accepted`, la plantilla mostrará algo significativo para el lector.

Hay tantos filtros integrados que es realmente difícil seleccionar mis favoritos. Consulta la lista completa para ver lo que podría ser útil para tí.

¿Qué sucede si los elementos integrados no cubren lo que necesitas? No temas, Django te permite crear etiquetas y filtros personalizados para tus propios fines. Veremos cómo a continuación.

## Construye tu propio sable de luz en plantillas

Cuando necesites crear tus propias etiquetas o filtros de plantilla, Django te brindará las herramientas para hacer lo que necesites.

Hay tres elementos principales para trabajar con etiquetas personalizadas:

1. Definiendo tus etiquetas en un lugar que espera Django.
1. Registrando tus etiquetas con el motor de plantillas.
1. Cargando tus etiquetas en una plantilla para que puedan ser utilizadas.

El primer paso es colocar las etiquetas en la ubicación correcta. Para hacer eso, necesitamos un paquete Python `templatetags` dentro de una aplicación Django. También necesitamos un módulo en ese directorio. Elige el nombre del módulo con cuidado porque es lo que cargaremos en la plantilla más adelante:

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

A continuación, debemos crear nuestra etiqueta o filtro y registrarlo. Comencemos con un ejemplo de filtro:

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

Ahora, si tenemos una variable `message`, podemos darle un poco de dinamismo. Para usar el filtro personalizado, debemos cargar nuestro módulo de etiquetas en la plantilla con la etiqueta `load`:

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

Si nuestro mensaje fue "¡Obtuviste un puntaje perfecto!", entonces nuestra plantilla debería mostrar el mensaje y una de las tres opciones aleatorias como "¡Obtuviste un puntaje perfecto! ¡Guau!

Escribir etiquetas personalizadas básicas es muy similar a los filtros personalizados. El código hablará mejor que las palabras aquí:

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

Podemos cargar las etiquetas personalizadas y usar nuestra etiqueta como cualquier otra etiqueta integrada:

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

Esta tonta etiqueta de bienvenida responderá a múltiples variables de entrada y variará según el nivel proporcionado. El ejemplo de uso debería mostrar "¡Hola, gran campeón He-Man!"

Solo estamos viendo los tipos más comunes de etiquetas personalizadas en nuestros ejemplos. Hay algunas funciones de etiquetado personalizadas más avanzadas que puede explorar en la
{{< extlink "https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/" "documentación de etiquetas de plantillas personalizadas de Django" >}}.

Django también usa `load` para proporcionar a los autores de plantillas algunas herramientas adicionales. Por ejemplo, veremos cómo cargar algunas etiquetas personalizadas proporcionadas por el framework cuando aprendamos a trabajar con imágenes y JavaScript más adelante.

## Resumen

¡Ahora hemos visto plantillas en acción! Hemos mirado:

* Cómo configurar plantillas para su sitio
* Maneras de llamar plantillas desde vistas
* Cómo usar los datos
* Cómo manejar la lógica
* Etiquetas y filtros incorporados disponibles para las plantillas
* Personalización de plantillas con sus propias extensiones de código

En el próximo artículo, examinaremos cómo los usuarios pueden enviar datos a una aplicación Django con formularios HTML. Django tiene herramientas para hacer que la creación de formularios sea rápida y efectiva. vamos a ver:

* La clase `Form` que usa Django para manejar datos de formularios en Python
* Controlar qué campos hay en los formularios
* Cómo Django presenta los formularios a los usuarios
* Cómo hacer la validación de formularios

Traduccion libre al español cortesía de Saul F.Rojas G.
