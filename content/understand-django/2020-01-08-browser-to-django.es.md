---
title: "Del Navegador A Django"
slug: "navegador-a-django"
description: >-
    Django te ayuda a construir sitios web en Python.
    ¿Cómo funciona?
    En esta serie,
    exploramos Django de arriba a abajo
    para mostrarte cómo crear el sitio web que deseas.
    Comenzaremos desde el principio con el navegador.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django

---

Quizás hayas oído hablar de
{{< extlink "https://www.djangoproject.com/" "Django" >}}
y cómo puede ayudarte a construir sitios web. Podrías ser un novato en Python, en desarrollo web o en programación.

Esta serie
"[Comprendiendo Django]({{< ref "/understand-django/_index.es.md" >}})",
te enseñará todo acerca de Django, A lo largo de esta serie, revelaré cómo Django es una herramienta poderosa que puede desbloquear el potencial de cualquier persona interesada en crear aplicaciones en Internet. Django es utilizado por compañías como Instagram, Eventbrite, Disqus y Udemy, y también es una gran herramienta para personas como tú.

Vamos a adoptar un enfoque de alto nivel para aprender Django. En lugar de comenzar desde abajo con todas las piezas del framework, te daré un panorama general, luego explicaré cada capa con más detalle para revelar cuánto hace Django por los desarrolladores y el poder que Django tiene bajo el capó.

Comencemos desde la parte superior de la experiencia de Internet de un usuario: el navegador web.

{{< understand-django-series-es "browser" >}}

## Hacer una solicitud desde el navegador

Django es un framework de desarrollo web, pero ¿qué diablos significa eso? ¿Cómo funcionan los sitios web? No voy a poder analizar todos los detalles, pero este post aportará algunos conceptos para desarrollar su comprensión. Veremos la forma en que su navegador web solicita datos de Internet y la "plomería" necesaria para que eso funcione. Equipado con las palabras clave y los acrónimos que se encuentran en este capítulo, deberías poder comenzar tu propia investigación sobre estos temas.

Internet funciona satisfaciendo el deseo de un usuario de enviar y recibir información. Esa “información” toma muchas formas diferentes,  tales como:

* Vídeos de gatos en YouTube
* Discusiones políticas en las redes sociales
* Perfiles de otras personas en sitios de citas.

Independientemente de lo que busque la gente, la información se transfiere a través de los mismos mecanismos. En la jerga de Internet, todos los tipos de información y datos se encuentran bajo el nombre de *recurso*.

La forma en que obtenemos recursos es con localizadores uniformes de recursos o URL
({{< extlink "https://en.wikipedia.org/wiki/URL" "Uniform Resource Locators" >}}),
para abreviar. Tú  ya sabes lo que son las URL, incluso si no las conoces por su nombre.

* {{< extlink "https://en.wikipedia.org/" "https://en.wikipedia.org/" >}}
* {{< extlink "https://www.djangoproject.com/" "https://www.djangoproject.com/" >}}
* {{< extlink "https://www.mattlayman.com/img/django.png" "https://www.mattlayman.com/img/django.png" >}}

Todos estos son ejemplos de URL. A menudo las llamamos direcciones web porque son muy similares a las direcciones postales. Una URL es la dirección de algún recurso en Internet. Cuando presionas Enter en la barra de direcciones de tu navegador, estás diciendo "Por favor, navegador, tráeme esto". En otras palabras, hacemos una solicitud (*request*) desde el navegador. Esta solicitud inicia una gran cadena de eventos desde su navegador hasta el sitio web en esa URL para que el recurso del sitio pueda aparecer ante tus ojos.

¿Qué hay en esta cadena de eventos? ¡Hay un montón de cosas! Pasaremos por alto muchas de las capas en esta discusión porque supongo que no planeas llegar al nivel de cómo funcionan las señales eléctricas en los cables de red. En cambio, centrémonos en dos partes principales de la cadena por ahora: **DNS** y **HTTP**

### Nombres, nombres, nombres

Una URL representa un recurso que se desea de Internet. ¿Cómo sabe Internet de dónde viene? Ahí es donde entra el DNS. DNS significa Sistema de Nombres de Dominio
({{< extlink "https://en.wikipedia.org/wiki/Domain_Name_System" "Domain Name System" >}}).
La palabra más importante  allí es "Nombre". Volvamos a la analogía de la dirección.

En una dirección postal (al menos desde la perspectiva de los EE. UU.), está la calle, la ciudad y el estado. Podríamos escribirlo así:

```text
123 Main St., Springfield, IL
```

Esta dirección va de lo más específico a lo más general. 123 Main St. se encuentra en la ciudad de Springfield en el estado de Illinois (IL).

Del mismo modo, una URL se ajusta a un formato similar:

```text
www.example.com
```

La terminología es diferente, pero el concepto de específico a general es el mismo. Cada pieza entre períodos es un tipo de *dominio*. Veamoslas en orden inverso:

* `com` se considera un dominio de nivel superior,
  {{< extlink "https://en.wikipedia.org/wiki/Top-level_domain" "TLD" >}}.
  Los TLD son cuidadosamente administrados por un grupo especial llamado
  {{< extlink "https://www.icann.org/" "ICANN" >}}.
* `example` es el nombre de dominio. Esta es la identidad principal de un servicio en Internet, ya que es el identificador específico que un usuario probablemente reconocería.
* `www` se considera el *subdominio* de un dominio. Un dominio puede tener muchos de estos como `www`, `m`, `mail`, `wiki` o cualquier nombre que el propietario del dominio quiera nombrar. Los subdominios también pueden tener más de un nivel de profundidad, por lo que `a.b.example.com` es válido, y `a` es un subdominio de `b.example.com` y `b` es un subdominio de `example.com`.

Los nombres de dominio no son la forma en que se comunican las computadoras. El nombre de dominio es algo “amigable” para un humano. Los sistemas de redes están diseñados para trabajar con números, por lo que esos nombres de dominio deben traducirse a algo que el sistema de redes pueda usar. Para ello, Internet utiliza un sistema de servidores DNS que actúan como la capa de traducción entre los nombres de dominio y los números que utilizan las redes informáticas. Un servidor es una computadora de propósito especial diseñada para proporcionar servicios a otros dispositivos llamados clientes.

Tal vez hayas visto estos números de redes. Los números se denominan direcciones IP, abreviatura de direcciones de Protocolo de Internet
({{< extlink "https://en.wikipedia.org/wiki/Internet_Protocol" "Internet Protocol" >}}).
Los ejemplos comunes incluyen:

* `127.0.0.1` como la dirección que tiene su computadora en su red interna.
* `192.168.0.1` como dirección predeterminada que podría usar un router doméstico.

Los ejemplos de direcciones IP anteriores son especiales porque esas direcciones están en
{{< extlink "https://en.wikipedia.org/wiki/Subnetwork" "subredes" >}}
especialmente designadas, pero dejaremos esa tangente a un lado. Puede profundizar en ese tema por su cuenta si lo dese.

Las redes privadas tienen direcciones IP como los dos ejemplos que mencioné anteriormente. Las máquinas en redes públicas también tienen direcciones IP. Por ejemplo, `172.253.115.105` es una dirección IP para `www.google.com` al momento de escribir este artículo.

Si desea averiguar la dirección IP de un nombre de dominio, puede instalar una herramienta popular llamada dig. Encontré la dirección IP de Google ejecutando este comando:

```bash
dig www.google.com
```

El sistema toma nombres de dominio y mantiene una tabla de enrutamiento distribuida de nombres a direcciones IP en toda la colección de servidores DNS. **¿Espera, qué?**

Los servidores DNS se acumulan en una jerarquía gigantesca. Cuando su navegador realiza una solicitud, solicita al servidor DNS más cercano a su máquina la dirección IP del nombre de dominio que solicitó. El servidor DNS mantiene una tabla de búsqueda de nombres de dominio a direcciones IP durante un período de tiempo. Si el nombre de dominio no está en la tabla, puede preguntar a otro servidor DNS en una cadena que seguirá buscando la dirección IP del dominio. Esto conduce a un par de resultados:

* Si ninguno de los servidores puede encontrar el dominio, el navegador se da por vencido y le muestra un mensaje como “Hmm. Estamos teniendo problemas para encontrar ese sitio”. (de la página Servidor no encontrado de Firefox).
* Si el navegador obtiene la dirección IP del servidor DNS, puede continuar con la solicitud.

La jerarquía es gigantesca, pero es amplia, no profunda. En otras palabras, hay muchas máquinas que participan en el DNS (como el router de su hogar), pero la cantidad de eslabones en la cadena para realizar una solicitud desde su computadora hasta los servidores raíz del sistema es relativamente pequeña.

Esto se simplifica para excluir algunos de los rincones verrugosos del DNS. La página de Wikipedia que vinculé al comienzo de esta sección cubre el DNS con mucho más detalle si está interesado en obtener más información.

### ¿Qué estamos enviando?

La otra pieza vital que necesitamos explorar es HTTP, o el Protocolo de Transferencia de Hipertexto
({{< extlink "https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol" "Hypertext Transfer Protocol" >}}).
Esta parte de la comunicación por Internet describe cómo se transfiere el contenido entre los navegadores y los servidores o, de manera más general, entre cualquier computadora que use el protocolo.

El protocolo utiliza un formato estándar y un conjunto de comandos para comunicarse. Algunos de los comandos comunes son:

* `GET` - Obtener un recurso existente
* `POST` - Crear o actualizar un recurso
* `DELETE` - Eliminar un recurso
* `PUT` - Actualizar un recurso

Una solicitud HTTP es como enviar un archivo de texto a través de la red. Si visita mi sitio web en `https://www.mattlayman.com/about/`, su navegador enviará una solicitud como:

```http
GET /about/ HTTP/1.1
Host: www.mattlayman.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
```

Hay otras partes que he omitido, pero esto nos ayuda a comenzar. La línea superior proporciona el comando, la ruta a un recurso en particular en el sitio (es decir, `/about/`) y una versión del protocolo a usar.

Después de la primera línea hay una lista de encabezados (headers). Los encabezados son datos adicionales que le dicen al servidor más sobre la solicitud. El encabezado `Host` es obligatorio porque nombra el sitio web que se va a recuperar (puede existir más de un sitio web en la misma dirección IP), pero cualquier otro encabezado es opcional.

En el ejemplo, también mostré el encabezado `Accept`. Este encabezado le dice al servidor qué tipo de contenido puede recibir el navegador como respuesta. Hay otros encabezados que pueden decirle a un servidor qué más debe "saber". Estos encabezados pueden:

* Indicar qué tipo de navegador está realizando la solicitud (este es el encabezado `User-Agent`).
* Decir cuándo se solicitó el recurso anteriormente para determinar si se debe devolver una nueva versión (el encabezado `Last-Modified`).
* Declarar que el navegador puede recibir datos comprimidos que puede descomprimir después de recibirlos para ahorrar ancho de banda (el encabezado `Accept-Encoding`).

La mayoría de los encabezados son manejados automáticamente por navegadores y servidores, pero veremos casos en los que queremos usar estos encabezados nosotros mismos, por lo que es bueno saber que existen.

## Entrega de una respuesta

¡Es hora de hablar de Django! Ahora tenemos una idea aproximada de lo que hacen los navegadores. Un navegador envía una solicitud HTTP a una URL que es resuelta por el sistema DNS. Esa solicitud llega a un servidor que está conectado a la dirección IP del nombre de dominio. Django vive en dicho servidor y es responsable de responder a las solicitudes con una respuesta HTTP.

La respuesta es lo que el usuario del navegador quería. Las respuestas pueden ser imágenes, páginas web, videos o cualquier formato que un navegador pueda manejar.

Antes de que Django pueda manejar una solicitud, hay una capa más que recorrer: el servidor web de Python.

### Donde HTTP se encuentra con Python

Un servidor web es el software en una *máquina* diseñada para manejar las solicitudes HTTP entrantes. A veces, esta terminología puede ser confusa porque las personas también pueden aplicar el nombre "servidor web" a una máquina completa que está sirviendo tráfico web. En este caso, me refiero al programa real que escucha y responde a las solicitudes web.

Un framework web de Python como Django se ejecuta con un servidor web. La función del servidor web es traducir la solicitud HTTP sin procesar a un formato que comprenda el framework. En el mundo de Python, se utiliza un formato específico para que cualquier servidor web pueda comunicarse con cualquier framework web de Python. Ese formato es la interfaz de puerta de enlace del servidor web, o WSGI
({{< extlink "https://wsgi.readthedocs.io/en/latest/what.html" "Web Server Gateway Interface" >}}),
que a menudo se pronuncia "wiz-yi".

{{< web >}}
{{< figure src="/img/2020/wsgi.jpg" caption="Web Server Gateway Interface" >}}
{{< /web >}}

WSGI permite que servidores web comunes como
{{< extlink "https://gunicorn.org/" "Gunicorn" >}},
{{< extlink "https://uwsgi-docs.readthedocs.io/en/latest/" "uWSGI" >}},
o {{< extlink "https://modwsgi.readthedocs.io/en/develop/" "mod_wsgi" >}}
se comuniquen con marcos web comunes de Python como Django,
{{< extlink "https://palletsprojects.com/p/flask/" "Flask" >}},
o {{< extlink "https://trypyramid.com/" "Pyramid" >}}.
Si realmente quieres ser un nerd, puedes explorar todos los detalles de ese formato
en {{< extlink "https://www.python.org/dev/peps/pep-3333/" "PEP 3333" >}}.

### El trabajo de Django

Una vez que el servidor web envía una solicitud, Django debe devolver una *respuesta*. Su rol como desarrollador de Django es definir los recursos que estarán disponibles desde el servidor. Eso significa que debes:

* Describir el conjunto de URLS a las que reaccionará Django.
* Escribir el código que activa esas URL y devuelve la respuesta.

Hay mucho que desglosar en esas dos declaraciones, por lo que exploraremos temas individuales en artículos futuros. A estas alturas, espero que tengas una idea de cómo llega una solicitud desde tu navegador a una máquina que ejecuta Django.

{{< web >}}
{{< figure src="/img/2020/request-response.jpg" caption="Life of a browser request" >}}
{{< /web >}}

Este artículo está relativamente libre de ejemplos de código y por una buena razón. Ya hay suficientes conceptos con los que luchar y no quería agregarle complejidad al código. Escribir ese código será el enfoque de esta serie de artículos para que podamos responder preguntas como:

* ¿Cómo construimos páginas web y le damos a todo un aspecto común?
* ¿Cómo pueden los usuarios interactuar con una aplicación y enviar datos a los que la aplicación pueda reaccionar?
* ¿Cómo almacena y recupera datos Django para hacer que los sitios sean dinámicos?
* ¿Quién puede acceder a la aplicación y cómo se controla ese acceso?
* ¿Qué seguridad necesitamos agregar para garantizar que la información de nuestros usuarios sea segura y privada?

Django tiene respuestas para todas estas cosas y mucho más. La filosofía de Django es incluir todas las piezas necesarias para hacer una aplicación web completa para Internet. Esta filosofía de "baterías incluidas" es lo que hace que Django sea tan poderoso. La misma filosofía también puede hacer que Django parezca abrumador. Mi objetivo en esta serie es presentar pieza tras pieza para desarrollar su comprensión de Django para que pueda ser productivo y comenzar su propia aplicación web.

En el próximo artículo, nuestro enfoque estará en aquellas URL a las que responderá nuestra aplicación. Veremos:

* Cómo declarar las URL.
* Cómo agrupar conjuntos de URL relacionadas
* Cómo extraer información de las URL que puede usar
* El código que devuelve las respuestas

Si desea seguir la serie, no dude en suscribirse a mi boletín informativo donde anuncio todo mi contenido nuevo. Si tiene otras preguntas, puede comunicarse conmigo en línea en X, donde soy
{{< extlink "https://x.com/mblayman" "@mblayman" >}}.

Finalmente, hay un tema extra más...

## Configuración de Django

En la serie, veremos muchos ejemplos de código, pero no configuraremos Django desde cero cada vez. Las siguientes instrucciones de configuración lo ayudarán a comenzar con cada ejemplo futuro.

Vamos a usar una terminal para ejecutar comandos. Windows, macOS y Linux son todos un poco diferentes. Estoy mostrando macOS aquí porque eso es lo que uso. El signo de dólar (`$`) es el carácter inicial tradicional para una terminal bash, así que cuando enumere los comandos, no escriba ese carácter. Intentaré dar consejos y resaltar las diferencias cuando pueda.

Necesitamos un lugar para poner nuestro trabajo. Dado que esta serie se llama "Understand Django", (en inglés) usaré ese nombre. Puede nombrar su proyecto de manera diferente si lo prefiere.

```bash
$ mkdir understand-django
$ cd understand-django
```

A continuación, instalamos Django en un entorno virtual para mantener las dependencias de nuestro proyecto separadas del resto de los paquetes de Python instalados en nuestra máquina. Tener esta separación de otros paquetes instalados es una buena manera de evitar conflictos con otros proyectos de Python que pueda estar ejecutando en su computadora.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Esto puede cambiar el indicador de tu terminal para que ahora comience con (venv) para indicar que el entorno virtual está en uso. Otros sistemas operativos activan el entorno virtual de forma diferente. Consulta la
{{< extlink "https://docs.python.org/3/library/venv.html" "documentación del módulo venv" >}}
para obtener más información sobre tu sistema operativo.

Ahora se puede instalar Django y el código del framework Django se agregará al entorno virtual.

```bash
(venv) $ pip install Django
```

Django incluye algunas herramientas que podemos usar para iniciar un proyecto rápidamente. Ejecutaremos un solo comando para que funcione.

```bash
(venv) $ django-admin startproject project .
```

Este comando dice "iniciar un proyecto llamado 'proyecto' en el directorio actual (`.`)". La elección de “proyecto” como nombre es intencional. `startproject` creará un directorio llamado `proyecto` que contendrá varios archivos que usará para configurar toda su aplicación web. Puedes nombrar tu proyecto como quieras, pero creo que usar el nombre genérico me hace la vida más fácil cuando cambio entre diferentes aplicaciones web de Django. Siempre sé dónde residen los archivos relacionados con mi proyecto. Después de que finalice este comando, debería tener algunos archivos y un diseño que lucen así:

```bash
(venv) $ ls
manage.py project venv
```

Tenga en cuenta que, además del directorio del `proyecto`, Django creó un archivo `manage.py`. Este archivo es un script que te ayudará a interactuar con Django. Aprenderá mucho más sobre `manage.py` a medida que avancemos. Para verificar si los conceptos básicos funcionan, intente:

```bash
(venv) $ python manage.py runserver
...
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Cuando inicie el servidor web, es probable que vea un mensaje como:

```text
You have ## unapplied migration(s).
Your project may not work properly
until you apply the migrations for app(s):
<a list of names here>
```

Exploraremos el tema de las migraciones más adelante, así que no se preocupe por ese mensaje por ahora.

Si copia y pega esa URL (es decir, `http://127.0.0.1:8000/`) en su navegador, debería ver una página de inicio de bienvenida. Además, si mira hacia atrás en su terminal, encontrará `"GET / HTTP/1.1"`. Este mensaje muestra que Django respondió a una solicitud HTTP. ¡Excelente!

La otra cosa que necesitamos es una "aplicación". Este es (quizás de manera confusa) el nombre de un componente de Django en un proyecto. Lo que debe recordar es que un proyecto de Django contiene una o más aplicaciones. Las aplicaciones contendrán la mayor parte del código que necesita escribir cuando trabaja con Django.

Después de salir del servidor, puede crear una aplicación para trabajar con ella:

```bash
(venv) $ python manage.py startapp application
```

Esto generará otro conjunto de archivos que siguen la estructura estándar de un componente de aplicación Django dentro de un directorio llamado `application`. Este ejemplo usa un nombre aburrido, pero, a diferencia del `proyecto`, debe elegir un nombre que tenga sentido para su aplicación web (por ejemplo, `películas` sería un buen nombre para una aplicación web que se trata de películas). Todos estos archivos se discutirán en detalle en un tema futuro.

Finalmente, debemos conectar esa aplicación a la configuración del proyecto de Django. La configuración del proyecto le permite configurar Django para satisfacer sus necesidades. Abra `project/settings.py`, busque `INSTALLED_APPS` y agregue a la lista para que se vea así:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'application',
]
```

Eso es todo lo que tenemos que hacer para comenzar con nuestros ejemplos de código en el próximo artículo. `application` será nuestra aplicación de referencia. El código de los temas futuros no es un tutorial, pero en ocasiones usaré `application` para orientarlo sobre dónde encontraría archivos en su propia aplicación web de Django. Tenemos un proyecto Django que puede ejecutarse localmente para realizar pruebas y está configurado con su primera aplicación. ¡Nos vemos pronto para hablar sobre la creación de URL y recursos!

Traduccion libre al español cortesía de Saul F.Rojas G.
