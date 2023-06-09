---
title: "URLs Guiam o Caminho"
description: >-
    Como uma aplicação de Django sabe onde enviar as requisições? Tu tens de dizê-la! Neste próximo artigo na série Entendendo a Django, olhamos as URLs e como ajudar os teus utilizadores a irem ao local correto.
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
No artigo anterior na série [Entendendo a Django]({{< ref "/understand-django/_index.pt.md" >}}), nós vimos como uma requisição de navegador do utilizador sai do navegador para a "porta da frente" da Django.
{{< /web >}}
Agora é hora de olhar
{{< web >}}
em como a Django processa estas requisições.
{{< /web >}}
{{< book >}}
em como a Django processa uma requisição de navegador do utilizador.
{{< /book >}}

Uma requisição de HTTP proveniente de um navegador inclui uma URL descrevendo qual recurso a Django deveria produzir. Já que as URLs podem chegar de várias formas, devemos instruir a Django sobre os tipos de URLs que a nossa aplicação de web pode manipular. É para isto que a *configuração da URL* serve. Na documentação da Django, a configuração da URL é chamada de URLconf, para abreviar.

Onde está a URLconf? A URLconf está no caminho do módulo definido pela definição `ROOT_URLCONF` no ficheiro de definições do teu projeto. Se executaste o comando `startproject`, então esta definição será nomeada como `project.urls` onde "project" é o nome dado como um argumento para o comando. Em outras palavras, a URLconf é colocada em `project/urls.py`, exatamente próximo do ficheiro `settings.py`.

Este explica onde o ficheiro reside, mas não diz-nos muito sobre como funciona. Vamos entrincheirar-nos mais.

{{< understand-django-series-pt "urls" >}}

## URLconf Em Ação

Tente pensar da configuração da URL como uma lista de caminhos de URL que a Django tentará corresponder de alto a baixo. Quando a Django encontra um caminho correspondente, a requisição de HTTP enviará para um pedaço de código de Python que está associado com aquele caminho. Este "pedaço de código de Python" é chamado de uma *visão* que exploraremos mais um pouco. Para o momento, confia que as visões sabem como lidar com as requisições de HTTP.

Nós podemos usar um exemplo de URLconf para trazer isto a vida:

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

O que está aqui corresponde bem com o que descrevi acima: uma lista de caminhos de URL que a Django tentará corresponder de alto a baixo. O conceito chave desta lista é o nome `urlpatterns` ou padrões de URLs. A Django tratará a lista numa variável `urlpatterns` como URLconf.

A ordem desta lista também é importante porque a Django parará de examinar a lista assim que encontrar uma correspondência. O exemplo não mostra qualquer conflito entre os caminhos, mas é possível criar duas entradas de `path` diferentes que podem corresponder a mesma URL que o utilizador submete. Mostrarei um exemplo de como isto acontece depois de vermos um outro aspeto dos caminhos.

Nós podemos trabalhar através de um exemplo para vermos como isto funcionaria para `www.example.com`. Onde consideramos que uma URL numa URLconf, a Django ignora o esquema (`https://`), o domínio (`www.example.com`), e o barra principal para correspondência. Todo o resto é aquilo que a URLConf comparará. 

* Uma requisição para `https://www.example.com/about/` estará como `"about/"` para o processo de correspondência de padrão e corresponderá o segundo `path`. Esta requisição enviaria para visão `views.about`.
* Uma requisição para `https://www.example.com/` estará como `""` para o processo de correspondência de padrão e corresponderá o primeiro `path`. Esta requisição enviaria para visão `views.home`.

> À parte: Tu podes notar que as URLs da Django terminam com um carácter de barra. Este comportamento é por causa de uma escolha da {{< extlink "https://docs.djangoproject.com/en/4.1/misc/design-philosophies/#definitive-urls" "filosofia de desenho" >}} da Django. De fato, se tentares alcançar uma URL como `https://www.example.com/about`, a Django redirecionará a requisição para a mesma URL com a barra anexada por causa da {{< extlink "https://docs.djangoproject.com/en/4.1/ref/settings/#append-slash" "definição padrão" >}} de `APPEND_SLASH`.

## O `path` Diante de Nós

A parte da sequência de caracteres do `path` (por exemplo, `"about/"`) é chamada de *rota*. Uma rota pode ser uma sequência de caracteres simples como tens visto, mas pode incluir outras estruturas especiais com uma funcionalidade chamada de *conversores*. Quando usares um conversor, podes extrair informação de uma URL que uma visão pode usar depois. Considere um caminho como este:

```python
    path(
        "blog/<int:year>/<slug:slug>/",
        views.blog_post
    ),
```

Os dois conversores neste caminho são:

* `<int:year>`
* `<slug:slug>`

O uso de parêntesis angulares e alguns {{< extlink "https://docs.djangoproject.com/en/4.1/topics/http/urls/#path-converters" "nomes reservados" >}} fazem a Django realizar analise adicional numa URL. Cada conversor tem algumas regras esperadas a seguir.

* O conversor de `int` deve corresponder um inteiro.
* O conversor de `slug` deve corresponder uma lesma. Lesma é um pouco do linguajar de jornal que aparece na Django porque a Django começou como um projeto devido a um jornal no Kansas. Uma lesma é uma sequência de caracteres que podem incluir caracteres, números, travessões, e sublinhados.

Dado estas definições de conversor, vamos comparar contra algumas URLs!

* `https://www.example.com/blog/2020/urls-lead-way/` - CORRESPONDE!
* `https://www.example.com/blog/twenty-twenty/urls-lead-way/` - NÃO.
* `https://www.example.com/blog/0/life-in-rome/` - CORRESPONDE! Uh, embora talvez não o que queríamos. Veremos isto em breve.

Agora podemos revisar o nosso problema de ordenação de mais de mais cedo. Considere estes dois caminhos em ordens diferentes:

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

Na primeira ordem, o conversor corresponderá qualquer inteiro seguindo `blog/`, incluindo `https://www.example.com/blog/2020/`. O que significa que a primeira ordem nunca chamará a visão `blog_for_twenty_twenty` porque a Django corresponde as entradas de `path` na ordem. Inversamente, na segunda ordem, `blog/2020/` enviará para `blog_for_twenty_twenty` corretamente porque é correspondida primeiro. Isto significa que existe um lição a lembrar aqui:

{{< web >}}
> Quando incluíres entradas de `path` para corresponder sobre gamas de valores com conversores (como o exemplo de anos acima), certifica-te de colocá-los **depois** das entradas mais específicas.
{{< /web >}}
{{< book >}}
Quando incluíres entradas de `path` para corresponder sobre gamas de valores com conversores (como o exemplo de anos acima), certifica-te de colocá-los **depois** das entradas mais específicas.
{{< /book >}}

## Uma Visão Abreviada de Visões

O que os conversores fazem com esta dado adicional? É difícil de explicar sem tocar nas visões.
{{< web >}}
No próximo artigo cobriremos as visões
{{< /web >}}
{{< book >}}
No próximo capitulo cobriremos as visões
{{< /book >}}
em mais profundidade, mas cá está um compêndio.

Uma visão é o código que recebe uma requisição e retorna uma resposta. Usando a sugestão de tipo opcional da Python cá está um exemplo que enviará uma resposta `Hello World`:

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

O `HttpRequest` é o formato traduzido da Django de uma requisição de HTTP envolvida numa classe contentora conveniente. Do mesmo modo, `HttpResponse` é o que podemos usar para que a Django traduzir os dados da nossa resposta numa resposta de HTTP formatada corretamente que será enviada de volta para o navegador do utilizador.

Agora podemos novamente ver um dos conversores:

```python
    path(
        "blog/<int:year>/",
        views.blog_by_year
    ),
```

Com este conversor no lugar na rota, com o que `blog_by_year` se pareceria?

```python
# application/views.py
from django.http import HttpResponse

def blog_by_year(request, year):
    # ... algum código para manipular o ano
    data = 'Some data set by code above'
    return HttpResponse(data)
```

A Django começa a revelar algumas qualidades refinadas aqui! O conversor fez uma quantidade de trabalho tedioso por nós. O argumento `year` definido pela Django já será um inteiro porque a Django fez a analise e a conversão da sequência de caracteres.

Se alguém submeter `/blog/not_a_number/`, a Django retornará uma resposta "Não Encontrada" porque `not_a_number` não pode ser um inteiro. O benefício disto é que não temos de colocar lógica de verificação adicional no `blog_by_year` para lidar com o caso estranho onde `year` não parece ser um número. Este tipo de funcionalidade é um verdadeiro economizador de tempo! Ele mantém o teu código mais limpo *e* torna a manipulação mais precisa.

E aquele outro exemplo estranho que vimos mais cedo de `/blog/0/life-in-rome/`? Aquele corresponderia ao nosso padrão da seção anterior, mas vamos presumir que queremos corresponder um ano de quatro dígitos. Como podemos fazer isto? Nós podemos usar expressões regulares.

## Caminhos de Expressão Regular

As expressões regulares são uma característica da programação frequentemente ligadas à uma motosserra: *elas são incrivelmente poderosas, mas podes cortar o teu pé se não fores cuidadoso.*

As expressões regulares podem expressar padrões complexos de caracteres duma maneira concisa. Esta concisão muitas vezes dá as expressões regulares uma má reputação de ser difícil de entender. Quando usadas cuidadosamente, podem ser altamente efetivas.

Uma expressão regular (que é frequentemente abreviada para "regex") corresponde padrões complexos em sequências de caracteres. Isto soa exatamente como o nosso problema do ano do blogue! No nosso problema, queremos corresponder apenas um inteiro de quatro dígitos. Vamos olhar uma solução que a Django pode manipular e decompor o que importa.

Como um resto, esta solução corresponderá algum caminho de URL como `blog/2020/urls-lead-way/`.

Nota que, usamos a função `re_path()` para a correspondência de expressão regular, ao invés de `path()`:

```python
re_path(
    r"^blog/(?P<year>[0-9]{4})/(?P<slug>[\w-]+)/$",
    views.blog_post
),
```

Esta sequência de caracteres doida comporta-se exatamente como o nosso exemplo anterior **exceto** que é mais precisa sobre apenas permitir anos de quatro dígitos. A sequência de caracteres doida também tem um nome. É chamada de *padrão de expressão regular*. Quando o código da Django executa, testará os caminhos de URL contra as regras que são definidas neste padrão.

Para vermos como isto funciona, temos de saber o que as partes do padrão significam. Nós podemos explicar este padrão um pedaço de cada vez:

* A própria sequência de caracteres começa com `r"` porque é uma sequência de caracteres crua em Python. Esta é usada porque as expressões regulares usam `\` extensivamente. Sem uma sequência de caracteres crua, um programador teria de escapar a barra obliqua invertida usando `\\`.
* O circunflexo, `^`, significa que "o padrão deve *começar* aqui". Por causa do circunflexo, um caminho que começa como `myblog/...` não funcionará.
* `blog/` é uma interpretação literal. Estes caracteres devem corresponder exatamente.
* A porção dentro dos parênteses `(?P<year>[0-9]{4})` é um *grupo de captura*. A `?P<year>` é o nome associado com o grupo de captura e é parecido com o lado direito dos dois pontos num conversor como `<int:year>`. O nome permite a Django passar o conteúdo num argumento chamado `year` para a visão. A outra parte do grupo de captura, `[0-9]{4}`, é o que o padrão está de fato a corresponder. `[0-9]` é uma *classe de carácter* que significa "corresponde qualquer número de 0 à 9". O `{4}` significa que deve corresponder **exatamente** quatro vezes. Isto é a especificidade que `re_path` dá que o conversor de `int` não poderia!
* A barra, `/`, entre os grupos de captura é um outro carácter literal a corresponder.
* O segundo grupo de captura, `(?P<slug>[\w-]+)`, colocará tudo aquilo que corresponder num argumento nomeado `slug`. A classe de carácter de `[\w-]` contém dois tipos de caracteres. `\w` significa que qualquer carácter que podes ter numa linguagem natural e dígitos e sublinhados. O outro tipo de carácter é um carácter de travessão literal, `-`. Finalmente, o carácter mais, `+`, significa que a classe de carácter deve corresponder 1 ou mais vezes.
* A última barra também é uma correspondência de carácter literal.
* Para completar o padrão, o sinal de dólar, `$`, age como o oposto do circunflexo e significa que "o padrão deve *terminar* aqui". Assim, `blog/2020/some-slug/another-slug/` não corresponderá.

Nota que não podes misturar as sequências de caracteres de estilo de `path` e `re_path`. O exemplo acima tinha que descrever a lesma como uma expressão regular ao invés de usar o conversor de lesma (por exemplo, `<slug:slug>`).

Parabéns! Esta é definitivamente a seção mais difícil
{{< web >}}
deste artigo.
{{< /web >}}
{{< book >}}
deste capítulo.
{{< /book >}}
Se entendeste o que fizemos com a `re_path`, o resto disto deveria ser mais confortável. Se não, *não te preocupes com isto!* Se quiseres saber mais sobre as expressões regulares, saiba que tudo que descrevi no padrão *não* é específico da Django. Ao invés disto, isto é o comportamento embutido da Python. Tu podes aprender mais sobre as expressões regularas a partir da {{< extlink "https://docs.python.org/3/howto/regex.html" "HOWTO de Expressão Regular" >}}.

Saber que este poder com `re_path` existe pode ajudar-te depois na tua jornada da Django, mesmo se não precisares dele agora.

## Agrupando URLs Relacionadas

Até este momento, olhávamos em rotas individuais que podes mapear numa configuração de URL ou `URLconf`. O que podes fazer quando um grupo relacionado de visões deveriam partilhar um caminho comum? Porquê quereríamos fazer isto?

Imaginemos que estás a construir um projeto educacional. No teu projeto, tens escolas, estudantes, e outros conceitos relacionados a educação. Tu *poderias* fazer algo como:

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

Esta abordagem funcionaria bem, mas força a configuração de URL raiz conhecer todas as visões definidas em cada aplicação, `schools` e `students`. Ao invés disto, podemos usar `include` para manipular isto melhor:

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

Então, em cada aplicação, poderíamos ter algo como:

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

O uso da `include` dá a cada aplicação da Django autonomia em quais visões precisa definir. O projeto pode ser completamente "ignorante" do que a aplicação está a fazer.

Além disso, a repetição de `schools/` ou `students/` é removida do primeiro exemplo. Já que a Django processa uma rota, corresponderá a primeira porção da rota e passará o *resto* para a configuração de URL que for definida na aplicação individual. Deste modo, as configurações de URL podem manipular a árvore onde a configuração de URL raiz está onde todas as requisições começam, mas as aplicações individuais podem manipular os detalhes visto que uma requisição é enviada para a aplicação apropriada. 

## Nomeando URLs

Vimos as principais maneiras que as URLs são definidas com `path`, `re_path`, e `include`. Existe um outro aspeto a considerar. Como podemos fazer referência as URLs em outros lugares no código? Considere esta (um pouco disparatada) visão:

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

Um redirecionamento é quando um utilizador tenta visitar uma página e é enviado para outro lugar pelo navegador. Existem maneiras muito melhores de manipular redirecionamentos do que este exemplo mostra, mas esta visão ilustra um ponto diferente. O que aconteceria se quiseres reestruturar o projeto para que as categorias do blogue sejam movidas de `/blog/categories/` para `/marketing/blog/categories/`? Na forma atual, teríamos de concertar esta visão e qualquer outra visão que fazia referência a rota diretamente. Mas que perda de tempo! A Django dá-nos ferramentas para dar nomes de caminhos que são independentes da rota explícita. Nós fizemos isto com o argumento de palavra-chave `name` para `path`:

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

Isto dá-nos `blog_categories` como um nome independente da rota de `/marketing/blog/categories/`. Para usarmos este nome, precisamos de `reverse` como sua contraparte. A nossa visão modificada parece-se com:

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

O trabalho da `reverse` é procurar qualquer nome de caminho e retornar a sua rota equivalente. Isto significa isto:

```python
reverse("blog_categories") == "/marketing/blog/categories/"
```

Pelo menos até quiseres mudá-la novamente. 😁

## Quando Nomes Colidem

O que acontece se tiveres várias URLs que queres dar o mesmo `name`? Por exemplo, `index` ou `detail` são nomes comuns que podes querer aplicar. Nós podemos recorrer ao {{< extlink "https://www.python.org/dev/peps/pep-0020/" "O Zen da Python" >}} por conselho.

> O Zen da Python, por Tim Peters
>
> Belo é melhor do que feio.
>
> ...
>
> **Os espaços de nome são uma ótima ideia -- façamos mais destes!**

Os espaços de nome podem ser novos para ti se não tens estado a programar por muito tempo. Eles são um *espaço partilhado para nomes*. Talvez seja claro, mas eu lembro de ter dificuldades com o conceito quando comecei a escrever software.

Para fazer uma analogia à algo no mundo real, usamos baldes de confiança. Imagine que tens duas bolas vermelhas e duas bolas azuis. Coloque uma bola de cada cor dentro de cada um dos dois baldes rotulados de "A" e "B". Se eu queria uma bola azul específica, não podia dizer "por favor dê-me a bola azul" porque isto seria ambíguo. Ao invés disto, para receber uma bola específica, precisaria de dizer "por favor dê-me a bola azul no balde B". Neste cenário, o balde é o espaço de nome.

O exemplo que usamos para as escolas e estudantes pode ajudar a ilustrar esta ideia no código. Ambas aplicações tinham uma visão `index` para representar a raiz das respetivas porções do projeto (por exemplo, `schools` e `students`). Se queríamos fazer referência aquelas visões, tentaríamos escolher a opção mais fácil de `index`. Infelizmente, se escolheres a`index`, então a Django não pode dizer qual delas é a visão correta para `index`. O nome é ambíguo.

Uma solução é criar o teu próprio espaço de nome prefixando o `name` com algo comum como `schools_`. O problema com esta abordagem é que a configuração de URL repete-se a si mesma:

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

A Django fornece uma alternativa que permitir-te-á manter um nome mais curto:

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

Ao adicionar `app_name`, assinalamos para a Django que estas visões estão num espaço de nome. Agora quando quisermos receber uma URL, usamos o espaço de nome e o nome da URL e os combinamos com um sinal de ponto e vírgula:

```python
reverse("schools:index") == "/schools/"
```

Esta é uma outra conveniência que a Django dá para tornar a nossa experiência de desenvolvimento de aplicação mais fácil.

Isto traz-nos para o fim do assunto de URLs. Por agora, vimos como:

* Fazer uma configuração de URL criando um módulo com uma lista de `urlpatterns`.
* Criar as URLs com `path` e `re_path`.
* Usar conversores para extrair informação para as visões.
* Usar expressões regulares para expressar dados de URL mais complexos.
* Agrupar URLs relacionadas em conjunto com `include`.
* Fazer referência à uma URL pelo seu `name`.
* Colocar nomes relacionados juntos num espaço de nome.

{{< web >}}
No próximo artigo, escavaremos as visões. Este artigo apenas deu a definição mais breve
{{< /web >}}
{{< book >}}
No próximo capítulo, escavaremos as visões. Este capítulo apenas deu a definição mais breve
{{< /book >}}
para o que uma visão é. A Django dá-nos opções muito ricas quando trabalhamos com visões. Exploraremos:

* Funções de visão
* Classes de visão
* Algumas visões de suporte embutidas
* Decoradores que sobrealimentam as visões.

{{< web >}}
Se gostarias de seguir com a série, sinta-se livre para inscrever-se no meu boletim informativo onde anúncio todos os meus novos conteúdos. Se tiveres outras questões, podes contactar-me na Twitter onde sou {{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;
