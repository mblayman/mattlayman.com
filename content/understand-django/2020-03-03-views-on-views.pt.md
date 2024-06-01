---
title: "Visões Sobre Visões"
description: >-
    As URLs da Django esperam enviar uma resposta de volta para um utilizador. De onde vem esta resposta? Uma visão de Django! Este artigo investiga os fundamentos das visões e como usá-las no teu projeto.
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

{{< web >}}
No artigo anterior do [Entendendo a Django]({{< ref "/understand-django/_index.pt.md" >}}), eu cobri as URLs e a variedade de ferramentas que a Django nos dá para descrever a interface no exterior para a internet para o teu projeto. Neste artigo,
{{< /web >}}
{{< book >}}
Agora que temos uma compreensão sobre as URLs na Django,
{{< /book >}}
examinaremos o bloco de construção principal que faz aquelas URLs funcionarem: a visão da Django.

{{< understand-django-series-pt "views" >}}

## O Que É Uma Visão?

Uma visão é um pedaço de código que recebe uma requisição de HTTP e retorna uma resposta de HTTP. As visões são onde usas a funcionalidade principal da Django: responder às requisições feitas para uma aplicação na internet.

Tu podes notar que sou um pouco vago sobre o "pedaço de código." Isto foi deliberado. A razão é que as visões entram de várias formas. Para dizer que visões são *funções* que seriam parte da história. Os capítulos posteriores desta história cobre como também podem ser implementadas em *classes*.

Mesmo se tentasse chamar visões *chamáveis,* continuaria a não retratá-las com precisão por causa das maneiras que certos tipos de visões são ligados à uma aplicação de Django. Por exemplo, uma visão baseada numa classe *produzirá* uma chamável como veremos numa seção posterior.

Vamos começar com funções uma vez que penso serem a maneira mais gentil de introdução as visões.

## Visões de Função

Uma visão de função é precisamente isto, uma função. A função recebe uma instância de `HttpRequest` como entrada e retorna um `HttpResponse` (ou uma de suas muitas subclasses) como saída.

O clássico exemplo "Olá Mundo" se pareceria com o que está listado abaixo:

```python
# application/views.py
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse('Hello World')
```

Adicionando a visão `hello_word` à configuração de URL que aprendemos
{{< web >}}
no último artigo,
{{< /web >}}
{{< book >}}
no último capítulo,
{{< /book >}}
poderias visitar um navegador na URL e encontrar o texto "Hello World" na página do teu navegador.

Talvez não aches isto muito entusiasmante, mas eu acho, e penso que deverias! A abstração fez tanto por nós, e o *nosso* trabalho é escrever algumas meras linhas de Python. Quando ligada à um servidor de Web na internet, a tua saudação pode alcançar alguém com acesso à internet. É espantoso e é digno de reflexão.

A Django faz a maioria do trabalho pesado por nós. A requisição de HTTP pura encaixa-se perfeitamente à classe `HttpRequest`. A nossa visão de exemplo não usa esta informação, mas está acessível se precisarmos dela. Da mesma maneira, não estamos a usar muito do `HttpResponse`. Mesmo assim, está a fazer todo o trabalho de garantir que aparece no navegador de um utilizador e entregar a nossa mensagem.

Para ver o que podemos fazer com as visões, olharemos com atenção no `HttpRequest` para obtermos um vislumbre do que está a acontecer.

## HttpRequest

`HttpRequest` é uma classe de Python. As instâncias desta classe representam uma requisição de HTTP. HTTP é o protocolo de transferência que a internet usa para trocar informação. Uma requisição pode estar numa variedade de formatos, mas uma requisição padrão pode parecer-se com:

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

{{< web >}}
Este exemplo é dum projeto paralelo que usa dados escolares. Eu recortei algumas linhas da requisição assim enquadrar-se-á melhor no ecrã, e fiz alguma ligeira reformatação para tornar o conteúdo um pouco mais claro.
{{< /web >}}
&nbsp;

Quando a Django recebe uma requisição como esta, analisará os dados e o armazenará numa instância de `HttpRequest`. A requisição fornece acesso conveniente à todas as partes dos dados crus com atributos úteis para os parâmetros mais comummente usados. Quando consideras o exemplo, a requisição teria:

* `method` - Isto corresponde o método HTTP de `POST` e pode ser usado para agir sobre o *tipo* de requisição que o utilizador enviou.
* `content_type` - Este atributo instrui a Django a como lidar com os dados na requisição. O valor de exemplo seria `application/x-www-form-urlencoded` para indicar que isto é um dado de formulário submetido pelo utilizador.
* `POST` - Para requisição de publicação, a Django processa os dados de formulário e armazena os dados numa estrutura parecida com um dicionário. `request.POST['name']` seria `Science` no nosso exemplo.
* `GET` - Tudo adicionado à sequência de caracteres de consulta (por exemplo, o conteúdo depois dum carácter `?` tal como `student=Matt` em `/courses/?student=Matt`) também é armazenado num atributo parecido com um dicionário.
* `headers` - Isto é onde todos os cabeçalhos de HTTP como `Host`, `Accept-Language`, e outros são armazenados. `headers` também é parecido com dicionário e pode ser acessado como `request.headers['Host']`.

Os outros atributos estão disponíveis para o `HttpRequest`, ams aquela lista levar-te-á longe o suficiente para começares. Consulte {{< extlink "https://docs.djangoproject.com/en/4.1/ref/request-response/" "Objetos de requisição e resposta" >}} por outros atributos.

Eu deveria também salientar que as instâncias de `HttpRequest` são um lugar comum para anexar dados adicionais. As requisição da Django passam por vários pedaços na abstração. Isto torna os objetos excelentes candidatos para funcionalidades adicionais que podes precisar. Por exemplo, se precisares de gestão de utilizador
{{< web >}}
(o que exploraremos num artigo do futuro),
{{< /web >}}
{{< book >}}
(o que exploraremos num capítulo do futuro),
{{< /book >}}
existe código que pode anexar um atributo `request.user` para representar um utilizador no teu sistema. É *muito* prático.

Tu podes pensar dos objetos de `HttpRequest` como a interface comum para a maioria das entradas que o meu código usa.

## HttpResponse

A outra interface principal que as tuas visões usarão ou diretamente ou indiretamente é a interface `HttpResponse`.

O teu trabalho como um utilizador da Django é fazer as tuas visões retornarem algum tipo de `HttpResponse`. Uma instância de resposta incluirá todos as informações necessárias para criar uma resposta de HTTP válida para um navegador do utilizador.

Alguns dos atributos de `HttpResponse` comuns incluem:

* `status_code` - Isto é o código do estado do HTTP. Os códigos de estado são um conjunto de números que a HTTP define para dizer ao cliente (por exemplo, um navegador) sobre o sucesso ou fracasso duma requisição. `200` é o código de sucesso habitual. Qualquer número de `400` para cima indica algum erro, como `404` quando um recurso requisitado não foi encontrado.
* `content` - Isto é conteúdo que forneces ao utilizador, A resposta armazena este dado como bytes. Se forneceres dado de sequências de caracteres de Python, a Django o codificará para bytes por ti.

```python
>>> from django.http import HttpResponse
>>> response = HttpResponse('Hello World')
>>> response.content
b'Hello World'
```

Quando trabalhas com as visões da Django, não usarás sempre `HttpResponse`. `HttpResponse` tem uma variedade de subclasses para usos comuns. Vamos olhar alguns:

* `HttpResponseRedirect` - tu podes querer enviar um utilizador para uma página diferente. Talvez o utilizador comprou algo na tua página, e gostarias de enviá-lo para ver uma página de recibo da usa encomenda. Esta subclasse é perfeita para este cenário.
* `HttpResponseNotFound` - Esta é a subclasse usada para criar uma resposta `404 Not Found`. A Django fornece algumas funções auxiliares para retornar isto assim podes não usar esta subclasse diretamente, mas é bom saber que está disponível.
* `HttpResponseForbidden` - Este tipo de resposta pode ser usado quando não queres que o utilizador acesse uma parte da tua aplicação (por exemplo, estado de HTTP `403 Forbidden`).

À parte das subclasses, a Django tem outras técnicas para retornar instâncias de `HttpResponse` sem criar um por ti mesmo. A função mais comum é `render`.

`render` é uma ferramenta para trabalhar com modelos de marcação. Os modelos de marcação são o tópico
{{< web >}}
do próximo artigo,
{{< /web >}}
{{< book >}}
do próximo capítulo,
{{< /book >}}
mas cá está um exemplar.

Tu poderias escrever uma visão para uma página e incluir muito código de HTML no teu programa de Python. A HTML é a linguagem de marcação das páginas da internet que usamos para descrever o formato ou estrutura duma página.

Esta visão pode parecer-se com isto:

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

Embora isto funcione, tem muitos defeitos:

1. O pedaço de HTML não é reutilizável por outras visões. Isto não importa muito para este exemplo pequeno, mas seria um enorme problema quando tentares fazer mais visões que usam muita marcação e precisam partilhar um aspeto comum.
2. A mistura de Python e HTML colocará as coisas em desordem. Precisa de prova? Olhe para história da computação e aprenda sobre a {{< extlink "https://en.wikipedia.org/wiki/Common_Gateway_Interface" "CGI" >}}. Ela não era bonita.
3. Como podes juntar pedaços de HTML em grupo? Não claramente.

Com modelos de marcação, podemos separar a disposição da lógica:

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

E teríamos um outro ficheiro nomeado `template.html` contendo:

```html
<html>
<head><title>Hello World!</title>
<body>
    <h1>This is a demo.</h1>
</body>
</html>
```

{{< web >}}
A parte importante para este artigo não é sobre os próprios modelos de marcação.
{{< /web >}}
{{< book >}}
A parte importante para este capítulo não é sobre os próprios modelos de marcação.
{{< /book >}}
O que é digno de menção é que `render` carrega o conteúdo de `template.html`, recebe a saída, e adiciona esta saída à uma instância de `HttpResponse`.

Isto envolve `HttpRequest` e `HttpResponse`. Com estes blocos de construção, podemos olhar em outras maneiras de puderes criar visões de Django para o teu projeto.

## Classes de Visão

Por agora vimos esta relação com as visões:

```text
HttpRequest -> view -> HttpResponse
```

As visões não precisam de ser exclusivamente funções. A Django também fornece ferramentas para criar visões com classes. Estes tipos de visões derivam da classe `View` da Django.

Quando escreves uma visão baseada em classe (frequentemente abreviada para CBVs), adicionas métodos de instância que correspondem com os métodos de HTTP. Vamos ver um exemplo:

```python
# application/views.py
from django.http import HttpResponse
from django.views.generic.base import View

class SampleView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello from a CBV!")
```

O método `get` na classe corresponde à uma requisição de HTTP `GET`. Os `*args` e `**kwargs` são uma convenção comum na Python para fazer um método ou função que aceite qualquer número de argumentos posicionais ou baseados em palavra-chave. Nós precisamos destes para corresponder a assinatura de método esperada que Django exige para visões baseadas em classe. De maneira semelhante, escreverias um método `post` para responder à uma requisição de HTTP `POST` e assim por diante. Com esta visão definida, podemos conectá-la à uma configuração de URL:

```python
# project/urls.py
from django.urls import path

from application.views import SampleView

urlpatterns = [
    path("", SampleView.as_view()),
]
```

Nota que não passamos `SampleView` para `path` como é. `path` espera um objeto chamável, assim devemos chamar `as_view`, um método de classe que retorna uma função que chamará o código da nossa classe.

Até este ponto, estaria como era de esperar pouco impressionado se estivesse no teu lugar. Porquê adicionaríamos todo este código cozinhado quando podes criar uma função e está feito? Se isto fosse a história completa, concordaria absolutamente contigo. Uma visão baseada em classe não adiciona muito além da versão baseada em função. Se nada, visões baseadas em classe têm mais para lembrar, assim são provavelmente mais confusas.

Onde as visões baseadas em classe começam a brilhar é quando usas algumas outras classes além da classe `View` inicial.

A Django inclui um hospedeiro de visões baseada em classe à usar para uma variedade de fins. Nós podemos explorar algumas delas com a nossa exposição limitada à abstração completa até aqui.

## Visões Fora da Caixa

Eu não cobrirei exaustivamente todas as visões baseadas em classe porque existem muitas. Além disto,
{{< web >}}
Se estiveres a juntar-se a esta séria de artigo desde o princípio e nunca criaste nada com a Django antes,
{{< /web >}}
{{< book >}}
Se nunca criaste nada com a Django antes,
{{< /book >}}
então ainda existirá lacunas no teu conhecimento (que preencheremos juntos!), e algumas das visões não farão muito sentido.

### RedirectView

Use `RedirectView` para enviar os utilizadores da tua página para um lugar diferente. Tu *poderias* criar uma visão que retorna uma instância de `HttpResponseRedirect`, mas esta visão baseada em classe pode lidar com isto por ti:

De fato, podes usar `RedirectView` sem criar uma subclasse dela. Observe:

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

`RedirectView` pode usar `url` para uma URL completa, ou pode usar `pattern_name` se precisares de enviar para uma visão que foi movida noutro lugar no teu projeto.

`as_view` é o que permite-nos evitar criar um subclasse de `RedirectView`. Os argumentos passados para `as_view` sobrepõe quaisquer atributos da classe. Os dois usos de `RedirectView` seguintes são equivalentes: 

```python
# project/urls.py
from django.urls import path
from django.views.generic.base import RedirectView

from application.views import NewView

class SubclassedRedirectView(RedirectView):
    pattern_name = 'new-view'

urlpatterns = [
    path("old-path/", SubclassedRedirectView.as_view()),
    # O RedirectView abaixo comporta-se como SubclassedRedirectView.
    path("old-path/", RedirectView.as_view(pattern_name='new-view')),
    path("new-path/", NewView.as_view(), name='new-view'),
]
```

### TemplateView

{{< web >}}
Anteriormente neste artigo,
{{< /web >}}
{{< book >}}
Anteriormente neste capitulo,
{{< /book >}}
vimos brevemente como separar a disposição da página web da lógica precisou-se de construir uma página com modelos de marcação.

Os modelos de marcação são tão comummente usados que a Django fornece uma classe que sabe como produzir uma resposta com nada mais do que um nome de modelo de marcação.

Um exemplo parece-se com:

```python
# application/views.py
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
```

Nós olharemos as visões de modelo de marcação em muitos mais detalhe
{{< web >}}
no próximo artigo
{{< /web >}}
{{< book >}}
no próximo capítulo
{{< /book >}}
quando mergulharmos em modelos de marcação.

### Outras Classes de Visão

As outras visões baseadas em classe da Django servem a uma variedade de fins. A Django tem visões que:

* Exibirão e manipularão formulários de HTML assim os utilizadores podem introduzir dados e enviar os dados para a aplicação.
* Puxarão dados duma base de dados e mostrarão um registo particular ao utilizador (por exemplo, uma página para ver fatos sobre um filme específico).
* Puxarão dados duma base de dados e mostrarão informação duma coleção de registos ao utilizador (por exemplo, mostrar o elenco de atores dum filme).
* Mostrarão dados a partir limites de tempo específicos como dias, semanas, e meses.

Conforme continuamos a explorar a Django, discutiremos estas visões quando o seu tópico relacionado (como formulários) forem o assunto primário
{{< web >}}
dum artigo.
{{< /web >}}
{{< book >}}
dum capítulo.
{{< /book >}}
Por agora, quando estiveres a desenvolver as tuas próprias visões, tente lembrar que a Django provavelmente tem uma visão baseada em classe para apoiar o teu trabalho.

## Misturas E Decoradores de Visão Úteis

Antes de terminarmos a excursão das visões, vamos discutir algumas classes de mistura e decoradores úteis.

Os decoradores são uma funcionalidade da Python (e muitas outras linguagens) que permitem-te estender uma função com capacidades adicionais. Um decorador pode envolver uma função de visão para fornecer um novo comportamento para uma visão. Os decoradores são úteis quando tens funcionalidade comum que queres adicionar para várias visões sem copiar e colar muito código.

As classes de mistura sem a um fim muito semelhante aos decoradores, mas usam a várias funcionalidades de herança de classes da Python para "misturar" o novo comportamento com uma visão baseada em classe existente. 

### Decoradores À Conhecer

Quando trabalhas com visões baseadas em função, existe um desafio quando lidas com diferentes métodos de HTTP. Por padrão, uma visão baseada em função pode receber requisições de *qualquer* método de HTTP. Algumas visões manipularão vários métodos como:

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

Esta visão usa o atributo `method` da instância de `request` para verificar o método de HTTP da requisição. E se apenas quiseres que a tua visão responda a um método de HTTP? Vamos dizer que apenas queres responder à um `POST`. Nós poderíamos escrever:

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

# OU

def if_clause_view(request):
    if request.method == 'POST':
        return HttpResponse('Method was a POST.')
    else:
        return HttpResponseNotAllowed()
```

Ambas técnicas funcionam, mas o código está um pouco mais sujo por causa da indentação adicional. Ao invés disto, podes usar o decorador `require_POST` e deixar a Django verificar o método por nós:

```python
# application/views.py
from django.http import HttpResponse
from django.view.decorators.http import require_POST

@require_POST
def the_view(request):
    return HttpResponse('Method was a POST.')
```

Esta versão estabelece a expetativa antecipadamente com o decorador e declara o contrato com o qual a visão trabalhará. Se um utilizador tentar um método diferente (como um `GET`), então a Django responderá com o código de estado de HTTP `405`, que é um código de erro para "method not allowed". 

Um outro decorador com que podes encontrar é o decorador `login_required`. Quando chegarmos ao assunto de gestão de utilizador, verás que podemos criar uma visão protegida para uma aplicação incluindo este decorador:

```python
# application/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def the_view(request):
    return HttpResponse('This view is only viewable to authenticated users.')
```

Qualquer utilizador não autorizado será redirecionado automaticamente para página de início de sessão para tua aplicação de Web.

Um exemplo final dum decorador embutido útil é `user_passes_test`. Este é um outro decorador usado com o sistema de gestão de utilizador que permite-nos controlar *quais* utilizadores deveriam ser permitidos acessar uma visão. Por exemplo, poderíamos criar uma visão que apenas utilizadores a nível do pessoal poderiam acessar:

```python
# application/views.py
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

@user_passes_test(lambda user: user.is_staff)
def the_view(request):
    return HttpResponse('Only visible to staff users.')
```

O decorador recebe um chamável que aceitará um único argumento dum objeto do utilizador. A visão apenas é acessível se o valor de retorno do chamável de teste avalia para `True`.

O que estou a tentar mostrar com estes exemplos é como decoradores únicos podem rapidamente aumentar as tuas visões com novas funcionalidades. E, devido como os decoradores funcionam para envolver funções, podes "empilhar" estes um ao outro:

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

### Misturas À Conhecer

As classes de mistura são para visões baseadas em classe como os decoradores são para as visões baseadas em função. Isto não é *completamente* verdadeiro visto que as visões baseadas em classe também podem usar decoradores, mas isto deveria dar-te uma ideia de onde as misturas encaixam-se.

Tais como os decoradores `login_required` e `user_passes_test`, temos equivalentes de mistura de `LoginRequiredMixin` e `UserPassesTestMixin`. Talvez tenhas algumas visões de modelo de marcação que apenas deveriam ser acessíveis aos utilizadores autenticados ou utilizadores a nível do pessoal. Estas visões poderiam parecer-se com:

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

Tu podes ver que estas visões são semelhantes aos equivalente de decorador com um padrão de uso ligeiramente diferente.

Uma coisa digna de atenção com as misturas são as suas colocações. Por causa da maneira que a Python manipula várias heranças, deves estar certo de incluir classes de mistura à esquerda na lista de classes de base herdadas. Isto garantirá que a Python comportar-se-á apropriadamente com estas classes. A razão exata para esta colocação é por causa das regras de ordem de resolução de método da Python quando usas várias heranças. A ordem de resolução de método está fora do âmbito, mas é isto que podes procurar se quiseres saber mais.

Existem muitas outras classes de mistura. A maioria das visões baseadas em classe embutida da Django são construídas compondo várias classes de mistura juntas. Se gostarias de ver como são construídas, consulte {{< extlink "https://ccbv.co.uk/" "Visões Baseadas em Classe Requintadas" >}}, um local mostrando as visões baseadas em classe embutidas e misturas e atributos disponíveis para estas classes.

## Sumário

Isto resume os fundamentos da visão. Nós vimos:

* Funções de visão
* `HttpRequest` e `HttpResponse`
* Classes de visão
* Algumas visões de suporte embutidas
* Decoradores e misturas que sobrecarregam as visões.

{{< web >}}
No próximo artigo,
{{< /web >}}
{{< book >}}
No próximo capítulo,
{{< /book >}}
veremos como as visões podem misturar disposição estática com os dados dinâmicos que fornecemos usando modelos de marcação. Os modelos de marcação são os animais de carga para as tuas interfaces de utilizador baseadas na Django. Nós veremos:

* Como configurar os modelos de marcação para a tua aplicação
* Maneiras de chamar os modelos de marcação a partir das visões
* Como usar dados
* Como manipular a lógica
* Funções embutidas disponíveis para os modelos de marcação
* Personalização de modelos de marcação com as tuas próprias extensões de código

{{< web >}}
Se gostarias de seguir com a série, sinta-se livre para inscrever-se no meu boletim informativo onde anúncio todos os meus novos conteúdos. Se tiveres outras questões, podes contactar-me na X onde sou {{< extlink "https://x.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;

A tradução deste artigo para o português é cortesia de Nazaré Da Piedade.
