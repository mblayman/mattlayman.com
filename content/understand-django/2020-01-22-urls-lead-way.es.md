---
title: "Las URL Marcan El Camino"
slug: "url-marcan-camino"
description: >-
    ¿Cómo sabe un sitio de Django dónde enviar solicitudes? ¡Tienes que decírselo!
    En este artículo que continúa la serie Comprendiendo Django, examinaremos las URL y cómo permitir que tus usuarios lleguen al lugar correcto.
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

## Rutas de expresiones regulares

Las expresiones regulares son una función de programación que a menudo se compara con una motosierra: *son increíblemente poderosas, pero puedes cortarte el pie si no tienes cuidado.*

Las expresiones regulares pueden expresar patrones complejos de caracteres de forma concisa. Esta concisión a menudo da a las expresiones regulares la mala reputación de ser difíciles de entender. Sin embargo, cuando se usan con cuidado, pueden ser muy efectivas.

Una expresión regular (que a menudo se abrevia como "regex") coincide con patrones complejos en cadenas. ¡Esto suena exactamente como nuestro problema del año del blog! En nuestro problema, queremos hacer coincidir sólo un número entero de cuatro dígitos. Veamos una solución que Django pueda manejar y luego analicemos lo que significa.

Como recordatorio, esta solución coincidirá con alguna ruta de URL como `blog/2020/urls-lead-way/`. Tenga en cuenta que aquí usamos la función `re_path()` para la coincidencia de expresiones regulares, en lugar de `path()`.

```python
re_path(
    r"^blog/(?P<year>[0-9]{4})/(?P<slug>[\w-]+)/$",
    views.blog_post
),
```

Esta cadena rara se comporta exactamente como nuestro ejemplo anterior, **excepto** que es más precisa y solo permite años de cuatro dígitos. La cadena rara también tiene nombre. Se llama *patrón regex*. Cuando se ejecuta el código Django, probará las rutas de URL con las reglas definidas en este patrón.

Para ver cómo funciona, tenemos que saber qué significan las partes del patrón. Podemos explicar este patrón un fragmento a la vez.

* La cadena en sí comienza con  `r"` porque es una cadena sin procesar en Python. Esto se usa porque las expresiones regulares usan `\`  extensamente. Sin una cadena sin procesar, un desarrollador tendría que escapar de la barra invertida repetidamente usando `\\`.
* El signo de intercalación, `^`, significa "el patrón debe *comenzar* aquí". Debido al signo de intercalación, una ruta que comience como `myblog/...` no funcionará.
* `blog/` es una interpretación literal. Esos caracteres deben coincidir exactamente.
* La parte entre paréntesis `(?P<year>[0-9]{4})` es un *grupo de captura*. `?P<year>` es el nombre que se asocia con el grupo de captura y es similar al lado derecho de los dos puntos en un convertidor como `<int:year>`. El nombre le permite a Django pasar el contenido en un argumento llamado `year` a la vista. La otra parte del grupo de captura, `[0-9]{4}`, es lo que realmente coincide con el patrón. `[0-9]` es una *clase de caracteres* que significa "coincidir con cualquier número del 0 al 9". El `{4}` significa que debe coincidir **exactamente** cuatro veces. ¡Esta es la especificidad que da `re_path` que el convertidor `int` no podría!
* La barra inclinada, `/`, entre los grupos de captura es otro carácter literal que debe coincidir.
* El segundo grupo de captura, `(?P<slug>[\w-]+)`, pondrá lo que coincida en un argumento llamado `slug`. La clase de caracteres de `[\w-]` contiene dos tipos de caracteres. `\w` significa cualquier carácter de palabra que pueda tener en un lenguaje natural y dígitos y guiones bajos. El otro tipo de carácter es un guión literal, `-`, carácter. Finalmente, el carácter más, `+`, significa que la clase de carácter debe coincidir 1 o más veces.
* La última barra también es una coincidencia de carácter literal.
* Para completar el patrón, el signo de dólar, `$`, actúa como el opuesto del signo de intercalación y significa que “el patrón debe *terminar* aquí”. Por lo tanto, `blog/2020/some-slug/another-slug/` no coincidirá.

Tenga en cuenta que no puede mezclar las cadenas de estilo `path` y `re_path`. El ejemplo anterior tenía que describir el slug como una expresión regular en lugar de usar el convertidor de slug (es decir, `<slug:slug>`).

¡Felicidades! Esta es definitivamente la sección más difícil de este artículo. Si entendiste lo que hicimos con `re_path`, el resto de esto debería sentirse muy cómodo. Si no, *¡no te preocupes por eso!* Si quieres saber más sobre las expresiones regulares, debes saber que todo lo que describí en el patrón *no* es específico de Django. En cambio, este es el comportamiento integrado de Python. Puede obtener más información sobre las expresiones regulares en el
{{< extlink "https://docs.python.org/3/howto/regex.html" "Regular Expression HOWTO" >}}
de Python.

Saber que este poder con `re_path` está ahí puede ayudarte más adelante en tu camino con Django, incluso si no lo necesitas ahora.

## Agrupación de URL relacionadas

Hasta este punto, hemos analizado rutas individuales que puede mapear en una URLconf. ¿Qué podemos hacer cuando un grupo relacionado de puntos de vista debe compartir un camino común? ¿Por qué querríamos hacer esto?

Imaginemos que estás construyendo un proyecto educativo. En su proyecto, tiene escuelas, estudiantes y otros conceptos relacionados con la educación. Podrías hacer algo como:

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

Este enfoque funciona bien, pero obliga a la raíz URLconf a conocer todas las vistas definidas en cada aplicación, `schools` y `students`. En cambio, podemos usar `include` para manejar esto mejor.

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

Entonces, en cada aplicación, tendríamos algo como:

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

El uso de `include` le da a cada aplicación de Django autonomía en qué vistas necesita definir. El proyecto puede ser felizmente "ignorante" de lo que está haciendo la aplicación.

Adicionalmente, se elimina la repetición de `schools/` o `students/` del primer ejemplo. A medida que Django procesa una ruta, coincidirá con la primera parte de la ruta y pasará el *resto* a la URLconf que se define en la aplicación individual. De esta forma, las configuraciones de URL pueden formar un árbol donde la raíz URLconf es donde comienzan todas las solicitudes, pero las aplicaciones individuales pueden manejar los detalles a medida que una solicitud se enruta a la aplicación adecuada.

## Nombrar URLs

Hemos analizado las principales formas en que las URL se definen con `path`, `re_path`, e `include`. Hay otro aspecto a considerar. ¿Cómo podemos referirnos a las URL en otros lugares del código? Considere esta vista (bastante tonta):

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

Una redirección es cuando un usuario intenta visitar una página y el navegador lo envía a otro lugar. Hay formas mucho mejores de manejar los redireccionamientos que las que muestra este ejemplo, pero esta vista ilustra un punto diferente. ¿Qué pasaría si desea reestructurar el proyecto para que las categorías del blog se muevan de `/blog/categories/` a `/marketing/blog/categories/`? En la forma actual, tendríamos que arreglar esta vista y cualquier otra vista que hiciera referencia a la ruta directamente.

¡Qué pérdida de tiempo! Django nos brinda herramientas para dar nombres de rutas que son independientes de la ruta explícita. Hacemos esto con el argumento de la palabra clave `name` de la ruta.

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

Esto nos da `blog_categories` como un nombre independiente de la ruta de `/marketing/blog/categories/`. Para usar ese nombre, necesitamos revertir (`reverse`) como su contraparte. Nuestra vista modificada se parece a:

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

El trabajo de `reverse` es buscar cualquier nombre de ruta y devolver su ruta equivalente. Eso significa que:

```python
reverse("blog_categories") == "/marketing/blog/categories/"
```

Al menos hasta que quieras cambiarlo de nuevo. 😁

## Cuando los nombres chocan

¿Qué sucede si tienes varias URL a las que deseas dar el mismo nombre (`name`)? Por ejemplo, índice (`index`) o detalle (`detail`) son nombres comunes que quizás desee aplicar. Podemos recurrir a
{{< extlink "https://www.python.org/dev/peps/pep-0020/" "The Zen of Python" >}}
para obtener asesoramiento.

> El Zen de Python, de Tim Peters
>
> Hermoso es mejor que feo.
>
> ...
>
> **Los espacios de nombres son una gran idea -- ¡hagamos más de eso!**

Los espacios de nombres pueden ser nuevos para tí si no has estado programando por mucho tiempo. Son un *espacio compartido para los nombres*. Tal vez eso esté claro, pero recuerdo haber luchado con el concepto cuando comencé a escribir software.

Para hacer una analogía con algo en el mundo real, usemos contenedores. Imagina que tienes dos bolas rojas y dos bolas azules. Ponga una bola de cada color en cada uno de los dos contenedores etiquetados "A" y "B". Si quisiera una bola azul específica, no puedo decir "por favor, dame la bola azul" porque sería ambiguo. En cambio, para obtener una bola específica, tendría que decir "por favor, dame la bola azul en el contenedor B". En este escenario, el depósito es el espacio de nombres.

El ejemplo que usamos para escuelas y estudiantes puede ayudar a ilustrar esta idea en código. Ambas aplicaciones tenían una vista de `index` para representar la raíz de las partes respectivas del proyecto (es decir, `schools/` y `students/`). Si quisiéramos referirnos a esas vistas, intentaríamos elegir la opción de índice más fácil. Desafortunadamente, si elige `index`, Django no puede decir cuál es la vista correcta para `index`. El nombre es ambiguo.

Una solución es crear su propio espacio de nombres anteponiendo el nombre (`name`) con algo común como `schools_`. El problema con ese enfoque es que la URLconf se repite.

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

Django proporciona una alternativa que te permitirá mantener un nombre más corto.

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

Al añadir `app_name`, señalamos a Django que esas vistas están en un espacio de nombres. Ahora cuando queramos obtener una URL, usaremos el nombre del espacio de nombres y la url unidos con dos puntos.

```python
reverse("schools:index") == "/schools/"
```

Esta es otra conveniencia que brinda Django para facilitar nuestra experiencia de desarrollo de aplicaciones.

Con esto concluimos el tema de las URL. Por ahora, hemos visto cómo:

* Realizar una configuración de URL creando un módulo con una lista de patrones de URL (`urlpatterns`).
* Crear URL con `path` y `re_path`.
* Usar convertidores para extraer información para las vistas.
* Utilizar expresiones regulares para expresar datos de URL más complejos.
* Agrupar las URL relacionadas con `include`.
* Hacer referencia a una URL por su nombre (`name`).
* Poner los nombres relacionados juntos en un espacio de nombres.

En el próximo artículo, profundizaremos en las vistas. Este artículo solo dió la definición más breve de lo que es una vista. Django nos da opciones muy ricas cuando trabajamos con vistas. Vamos a explorar:

* Vistas funcionales
* Vistas basadas en clases
* Algunas vistas de apoyo incorporadas
* Decoradores que potencian las vistas.

Traduccion libre al español cortesía de Saul F.Rojas G.
