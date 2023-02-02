---
title: "Un Vistazo A Las Vistas"
slug: "vistazo-a-las-vistas"
description: >-
    Se espera que las URL de Django devuelvan respuesta al usuario. ¿De dónde viene esa respuesta? ¡De una vista de Django! Este artículo examina los fundamentos de las vistas y como usarlas en tu proyecto.
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

En el artículo anterior de
[Comprendiendo Django]({{< ref "/understand-django/_index.es.md" >}}),
cubrí las URL y la variedad de herramientas que Django nos brinda para describir la interfaz externa a Internet para tu proyecto. En este artículo, examinaremos el bloque de construcción central que hace que esas URL funcionen: las vistas de Django.

{{< understand-django-series-es "views" >}}

## ¿Qué es una vista?

Una vista es un fragmento de código que recibe una solicitud HTTP y devuelve una respuesta HTTP. Las vistas son el lugar donde reside la funcionalidad central de Django: responder a las solicitudes realizadas a una aplicación en Internet.

Se puede notar que soy un poco vago al hablar de un  "fragmento de código". Eso fue deliberado. La razón es que las vistas vienen en múltiples formas. Decir que las vistas son funciones sería parte de la historia. Los capítulos posteriores de esa historia cubren cómo también se pueden implementar en las *clases*.

Incluso si intentara llamar a las vistas “invocables” ( *callables* en inglés), todavía no las representaría con precisión debido a las formas en que ciertos tipos de vistas se conectan a una aplicación de Django. Por ejemplo, una vista basada en una clase *producirá* un invocable como veremos en una sección posterior.

Comencemos con las funciones, ya que creo que son la introducción más suave a las vistas.

## Vistas basadas en funciones

Una vista de función es precisamente eso, una función. La función toma una instancia de `HttpRequest` como entrada y devuelve una `HttpResponse` (o una de sus muchas subclases) como salida.

El ejemplo clásico de "Hello World" se vería como lo que se muestra a continuación:

```python
# application/views.py
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse('Hello World')
```

Al agregar la vista `hello_world` a una configuración de URL como aprendimos en el último artículo, podemos visitar un navegador en la URL y encontrar el texto "Hello World" en la página de nuestro navegador.

Tal vez no lo encuentres muy emocionante, pero yo sí, ¡y pienso que tu también! El framework hizo mucho trabajo para nosotros, y *nuestro* trabajo es escribir un par de líneas de Python. Cuando se conecta a un servidor web en Internet, nuestro saludo puede llegar a cualquier persona con acceso a la red. Eso es asombroso y vale la pena reflexionar sobre ello.

Django hace la mayor parte del trabajo pesado pPor nosotros. La solicitud HTTP sin procesar encaja perfectamente en la clase `HttpRequest`. Nuestra vista de ejemplo no usa esa información, pero es accesible si la necesitamos. Del mismo modo, no usamos mucho `HttpResponse`. Aún así, está haciendo todo el trabajo para garantizar que aparezca en el navegador de un usuario y entregue nuestro mensaje.

Para ver lo que podemos hacer con las vistas, echemos un vistazo de cerca a `HttpRequest` y `HttpResponse` para echar un vistazo a lo que está pasando

## HttpRequest

`HttpRequest` es una clase de Python. Las instancias de esta clase representan una solicitud HTTP. HTTP es el protocolo de transferencia que utiliza Internet para intercambiar información. Una solicitud puede estar en una variedad de formatos, pero una solicitud estándar podría verse así:

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

Este ejemplo es de un proyecto personal que usa datos escolares. Recorté algunas líneas de la solicitud para que se ajuste mejor a la pantalla, e hice un pequeño cambio de formato para que el contenido sea un poco más claro.

Cuando Django recibe una solicitud como esta, analizará los datos y los almacenará en una instancia de `HttpRequest`. La solicitud brinda acceso conveniente a todas las partes de los datos sin procesar con atributos útiles para los parámetros más utilizados. Al considerar el ejemplo, la solicitud tendría:

* `method` - coincide con el método HTTP de `POST` y se puede usar para actuar según el *tipo* de solicitud que envió el usuario.
* `content_type` - este atributo le indica a Django cómo manejar los datos en la solicitud. El valor de ejemplo sería `application/x-www-form-urlencoded` para indicar que se trata de datos de formulario enviados por el usuario.
* `POST` - para las solicitudes POST, Django procesa los datos del formulario y los almacena en una estructura similar a un diccionario. `request.POST['name']` sería `Science` en nuestro ejemplo.
* `GET` - todo lo que se agregue a la cadena de consulta (es decir, el contenido después de un carácter `?` como `student=Matt` en `/courses/?student=Matt`). Esta información también se almacena en un atributo similar a un diccionario.
* `headers` - aquí es donde se almacenan todos los encabezados HTTP como `Host`, `Accept-Language` y los demás. `headers` también es como un diccionario y se puede acceder a ellos como `request.headers['Host']`.

Hay otros atributos disponibles para `HttpRequest`, pero esa lista te llevará lo suficientemente lejos como para comenzar. Echa un vistazo a los
{{< extlink "https://docs.djangoproject.com/en/4.1/ref/request-response/" "objetos de solicitud y respuesta" >}}
para ver los otros atributos.

También debo señalar que las instancias de `HttpRequest` son un lugar común para adjuntar datos adicionales. Las solicitudes de Django pasan por muchas piezas en el framework. Esto hace que los objetos sean excelentes candidatos para funciones adicionales que pueda necesitar. Por ejemplo, si se necesita administración de usuarios (lo cual  exploraremos en un artículo futuro), existe un código que puede adjuntar un atributo `request.user` para representar a un usuario en su sistema. Esto es *muy* útil.

Se podría pensar en los objetos `HttpRequest` como la interfaz común para la mayoría de las entradas que usa nuestro código.

## HttpResponse

La otra interfaz principal que usarán nuestras vistas, ya sea directa o indirectamente, es la interfaz `HttpResponse`.

Tu trabajo como usuario de Django es hacer que tus vistas devuelvan algún tipo de `HttpResponse`. Una instancia de respuesta incluirá toda la información necesaria para crear una respuesta HTTP válida para el navegador de un usuario.

Algunos de los atributos comunes de `HttpResponse` incluyen:

* `status_code` - este es el código de estado HTTP. Los códigos de estado son un conjunto de números que HTTP define para informar a un cliente (por ejemplo, un navegador) sobre el éxito o fracaso de una solicitud. `200` es el código de éxito habitual. Cualquier número de `400` en adelante indicará algún error, como `404` cuando no se encuentra un recurso solicitado.
* `content` - este es el contenido que se proporciona al usuario. La respuesta almacena estos datos como bytes. Si proporciona datos de cadenas de Python, Django los codificará en bytes por usted.

```python
>>> from django.http import HttpResponse
>>> response = HttpResponse('Hello World')
>>> response.content
b'Hello World'
```

Cuando trabaje con vistas de Django, no siempre usará `HttpResponse` directamente. `HttpResponse` tiene una variedad de subclases para usos comunes. Veamos algunos:

* `HttpResponseRedirect` - es posible que desee enviar a un usuario a una página diferente. Quizás el usuario compró algo en su sitio y le gustaría que viera una página de recibo de su pedido. Esta subclase es perfecta para ese escenario.
* `HttpResponseNotFound` - esta es la subclase utilizada para crear una respuesta `404 Not Found`. Django proporciona algunas funciones de ayuda para devolver esto, por lo que es posible que no use esta subclase directamente, pero es bueno saber que está disponible.
* `HttpResponseForbidden` - este tipo de respuesta se puede usar cuando no desea que un usuario acceda a una parte de su sitio web (es decir, estado HTTP `403 Forbidden`).

Además de las subclases, Django tiene otras técnicas para devolver instancias de `HttpResponse` sin crear una tú mismo. La función más común es renderizar (`render`).

`render` es una herramienta para trabajar con plantillas. Las plantillas son el tema del próximo artículo, pero aquí hay un adelanto.

Podría escribir una vista para una página web e incluir mucho HTML en su Python. HTML es el lenguaje de marcado de las páginas de Internet que usamos para describir el formato de una página.

Esta vista podría parecerse a:

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

Si bien esto funciona, tiene muchas deficiencias:

1. El fragmento HTML no es reutilizable por otras vistas. Eso no importa mucho para este pequeño ejemplo, pero sería un gran problema cuando intentas hacer muchas vistas que usan mucho marcado y necesitan compartir una apariencia común.
1. La mezcla de Python y HTML se volverá complicada. ¿Necesitas pruebas? Mire la historia de la computación y aprenda sobre
    {{< extlink "https://en.wikipedia.org/wiki/Common_Gateway_Interface" "CGI" >}}.
    No fue bonito.
1. ¿Cómo se pueden unir piezas de HTML? No es fáci.

Con las plantillas, podemos separar el diseño de la lógica.

```python
# application/views.py
from django.shortcuts import render

def my_html_view(request):
    return render(
        request,
        "template.html",
        {}
    )
```

Y tendríamos otro archivo llamado `template.html` que contiene:

```html
<html>
<head><title>Hello World!</title>
<body>
    <h1>This is a demo.</h1>
</body>
</html>
```

La parte importante de este artículo no se trata de las plantillas en sí. Lo que vale la pena señalar es que `render` carga el contenido de `template.html`, obtiene el resultado y agrega ese resultado a una instancia de `HttpResponse`.

Con eso concluye `HttpRequest` y `HttpResponse`. Con esos componentes básicos, ahora podemos ver otras formas en las que se  pueden crear vistas de Django para nuestro proyecto.

## Vistas basadas en clases

Hasta ahora hemos visto esta relación con las vistas:

```text
HttpRequest -> view -> HttpResponse
```

Las vistas no necesitan ser funciones exclusivamente. Django también proporciona herramientas para crear vistas a partir de clases. Estos tipos de vistas se derivan de la clase `View` de Django.

Cuando se escribe una vista basada en clases (a menudo abreviada como CBV), se agregan métodos de instancia que coinciden con los métodos HTTP. Veamos un ejemplo:

```python
# application/views.py
from django.http import HttpResponse
from django.views.generic.base import View

class SampleView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello from a CBV!")
```

El método `get` de la clase corresponde a una solicitud `GET` HTTP. `*args` y `**kwargs` son una convención común en Python para hacer un método o función que acepte cualquier número de argumentos posicionales o basados en palabras clave. Los necesitamos para que coincidan con la firma del método esperado que requiere Django para los CBV. De manera similar, escribiría un método de publicación (`post`) para responder a una solicitud `POST` HTTP y así sucesivamente. Con esa vista definida, podemos conectarla a una URLconf:

```python
# project/urls.py
from django.urls import path

from application.views import SampleView

urlpatterns = [
    path("", SampleView.as_view()),
]
```

Ten en cuenta que no pasamos `SampleView` a la ruta como está. `path` espera un objeto invocable, por lo que debemos llamar a `as_view`, un método de clase que devuelve una función que llamará al código de nuestra clase.

En este punto, tendria una impresión inadecuada si estuviera en tu lugar. ¿Por qué agregarías todo este código repetitivo cuando puedes hacer una función y terminar? Si esta fuera la historia completa, estaría absolutamente de acuerdo contigo. Una vista basada en clases no agrega mucho más allá de la versión basada en funciones. En todo caso, las CBV tienen más cosas que recordar, por lo que probablemente sean más confusas.

Donde las vistas basadas en clases comienzan a brillar es cuando se usan otras clases más allá de la clase `View` inicial.

Django incluye una gran cantidad de vistas basadas en clases para ser usadas con variados propósitos. Podemos explorar algunos de ellos con nuestra exposición limitada al framework completo hasta ahora

## Vistas listas para usar

No cubriré exhaustivamente todas las vistas basadas en clases porque hay muchas. Además, si te estás uniendo a esta serie de artículos desde el principio y nunca has hecho Django antes, todavía habrá lagunas en tu conocimiento (¡que vamos a llenar!), y algunas de las vistas no tendrán mucho sentido.

### RedirectView

Usa `RedirectView` para enviar a los usuarios de tu sitio a un lugar diferente. *Podrías* crear una vista que devuelva una instancia de `HttpResponseRedirect`, pero esta vista basada en clases puede manejar eso por tí.

De hecho, puedes usar `RedirectView` sin implementar herencia de clases . Mira esto:

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

`RedirectView` puede usar `url` para una URL completa, o puede usar `pattern_name` si necesita enrutar a una vista que se movió a otra parte de su proyecto.

`as_view` es lo que nos permite evitar heredar de `RedirectView`. Los argumentos pasados a `as_view` anulan cualquier atributo de clase. Los siguientes dos usos de `RedirectView` son equivalentes:

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

Anteriormente en este artículo, vimos brevemente cómo separar el diseño de la página web de la lógica necesaria para crear una página con plantillas.

Las plantillas se usan con tanta frecuencia que Django proporciona una clase que sabe cómo producir una respuesta con nada más que un nombre de plantilla.

Un ejemplo sería algo como esto:

```python
# application/views.py
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
```

Veremos las vistas de plantilla con mayor detalle en el próximo artículo cuando nos sumerjamos en las plantillas.

### Otras vistas basadas en clases

Las otras vistas basadas en clases de Django sirven para una variedad de propósitos. Django tiene vistas que:

* Muestran y manejan formularios HTML para que los usuarios puedan ingresar datos y enviarlos a la aplicación.
* Extraen datos de una base de datos y muestran un registro individual al usuario (por ejemplo, una página web para ver datos sobre una película en particular).
* Extraen datos de una base de datos y muestran información de una colección de registros al usuario (por ejemplo, mostrando el elenco de actores de una película).
* Muestran datos de rangos de tiempo específicos como días, semanas y meses.

A medida que continuemos explorando Django, discutiremos estas vistas cuando su tema relacionado (como formularios) sea el tema principal de un artículo. Por ahora, cuando estés desarrollando tus propias vistas, trata de recordar que Django probablemente tiene una vista basada en clases para ayudarte en tu trabajo.

## Útiles decoradores de vista y Mixins

Antes de terminar el recorrido por las vistas, analicemos algunos decoradores útiles y clases llamadas **mixins**.

Los decoradores son una característica de Python (y muchos otros lenguajes) que le permiten extender una función con capacidades adicionales. Un decorador puede ajustar una función de vista para proporcionar un nuevo comportamiento a una vista. Los decoradores son útiles cuando tiene una funcionalidad común que desea agregar a muchas vistas sin copiar y pegar una gran cantidad de código.

Los mixins tienen un propósito muy similar como decoradores, pero utilizan la característica de herencia múltiple de clases en Python para "mezclar" el nuevo comportamiento con una vista basada en clases existente.

### Decoradores a saber

Cuando se trabaja con vistas basadas en funciones, existe un desafío al manejar diferentes métodos HTTP. De forma predeterminada, una vista basada en funciones puede recibir solicitudes de *cualquier* método HTTP. Algunas vistas manejan múltiples métodos como:

```python
# application/views.py
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
)

def multi_method_view(request):
    if request.method == 'GET':
        return HttpResponse('Method was a GET.')
    elif request.method == 'POST':
        return HttpResponse('Method was a POST.')
    return HttpResponseNotAllowed()
```

Esta vista utiliza el atributo de método (`method`) de instancia de solicitud (`request`) para verificar el método HTTP de la solicitud. ¿Qué sucede si solo desea que su vista responda a un método HTTP? Digamos que solo desea responder a un POST. Podríamos escribir:

```python
# application/views.py
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
)

def guard_clause_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()

    return HttpResponse('Method was a POST.')

# OR

def if_clause_view(request):
    if request.method == 'POST':
        return HttpResponse('Method was a POST.')
    else:
        return HttpResponseNotAllowed()
```

Ambas técnicas funcionan, pero el código es un poco más complicado debido a la sangría extra. En su lugar, podemos usar el decorador `require_POST` y dejar que Django verifique el método por nosotros.

```python
# application/views.py
from django.http import HttpResponse
from django.view.decorators.http import require_POST

@require_POST
def the_view(request):
    return HttpResponse('Method was a POST.')
```

Esta versión establece la expectativa por adelantado con el decorador y declara el contrato con el que funcionará la vista. Si un usuario prueba un método diferente (como un `GET`), Django responderá con el código de estado HTTP `405`, que es un código de error para "método no permitido".

Otro decorador común que se puede encontrar es el decorador `login_required`. Cuando lleguemos al tema de la administración de usuarios, verá que podemos crear una vista protegida para una aplicación al incluir este decorador.

```python
# application/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def the_view(request):
    return HttpResponse('This view is only viewable to authenticated users.')
```

Cualquier usuario no autenticado será redirigido automáticamente a la página de inicio de sesión de tu aplicación web.

Un ejemplo final de un útil decorador integrado es `user_passes_test`. Este es otro decorador utilizado con el sistema de administración de usuarios que nos permite controlar *qué* usuarios deben tener acceso a una vista. Por ejemplo, podríamos hacer una vista a la que solo pudieran acceder los usuarios a nivel de personal:

```python
# application/views.py
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

@user_passes_test(lambda user: user.is_staff)
def the_view(request):
    return HttpResponse('Only visible to staff users.')
```

El decorador toma un invocable que aceptará un solo argumento de un objeto user. Solo se podrá acceder a la vista si el valor de retorno del invocable que realiza la prueba se evalúa como `True`.

Lo que estoy tratando de mostrar con estos ejemplos es cómo los decoradores individuales pueden aumentar rápidamente sus vistas con nuevas funciones. Y, debido a la forma en que los decoradores trabajan para envolver funciones, puede "apilarlas" juntas.

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

### Mixins a saber

Los mixins son para las vistas basadas en clases lo que los decoradores son para las vistas basadas en funciones. Esto no es del todo cierto, ya que las vistas basadas en clases también pueden usar decoradores, pero debería darle una idea de dónde encajan los mixins.

Al igual que los decoradores `login_required` y `user_passes_test`, tenemos mixins equivalentes de `LoginRequiredMixin` y `UserPassesTestMixin`. Tal vez tenga algunas vistas de plantilla que solo deberían ser accesibles para usuarios autenticados o usuarios de nivel de personal. Esas vistas podrían verse como:

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

Puedes ver que estas vistas son similares a sus contrapartes de decorador con un patrón de uso ligeramente diferente.

Una cosa que vale la pena señalar con los mixins es su ubicación. Debido a la forma en que Python maneja la herencia múltiple, debes asegurarte de incluir mxins a la izquierda en la lista de clases base heredadas. Esto asegurará que Python se comporte apropiadamente con estas clases. El motivo exacto de esta ubicación se debe a las reglas de orden de resolución de métodos (MRO) de Python cuando se utiliza la herencia múltiple. MRO está fuera de nuestro alcance, pero eso es lo que puede buscar si desea obtener más información.

Hay muchas otras clases de mixin. La mayoría de las vistas integradas basadas en clases de Django se construyen al componer varias clases mixin juntas. Si deseas ver cómo se construyen, consulta
{{< extlink "https://ccbv.co.uk/" "Classy Class-Based Views" >}},
un sitio que muestra los CBV integrados y los complementos y atributos disponibles para esas clases.

## Resumen

Eso es un resumen de los fundamentos de la vistas. Hemos visto:

* Vistas basadas en funciones
* `HttpRequest` y `HttpResponse`
* Vistas basadas en clases
* Algunas vistas de apoyo incorporadas
* Decoradores y mixins que potencian las vistas.

En el próximo artículo, veremos cómo las vistas pueden combinar el diseño estático con los datos dinámicos que proporcionamos mediante el uso de plantillas. Las plantillas son el caballo de batalla para sus interfaces de usuario basadas en Django. vamos a ver:

* Cómo configurar plantillas para su sitio
* Maneras de llamar plantillas desde vistas
* Cómo usar los datos
* Cómo manejar la lógica
* Funciones integradas disponibles para las plantillas
* Personalización de plantillas con sus propias extensiones de código

Traduccion libre al español cortesía de Saul F.Rojas G.
