---
title: "Modelos de Marcação para as Interfaces de Utilizador"
description: >-
    Quando a tua aplicação de Django devolve uma resposta com a tua interface de utilizador, os modelos de marcação são a ferramenta que usarás para produzir esta interface de utilizador. Este artigo olha considera o que os modelos de marcação são e como usá-los.
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
No artigo anterior da [Entendendo a Django]({{< ref "/understand-django/_index.pt.md" >}}), vimos os fundamentos de usar visões na Django. Este artigo focar-se-á em modelos de marcação.
{{< /web >}}
Os modelos de marcação são a tua principal ferramenta num projeto de Django para gerar uma interface de utilizador. Com os modelos de marcação, seremos capazes de construir as páginas que os utilizadores verão quando visitarem a tua aplicação de Web. Vamos ver como os modelos de marcação ligam-se as visões e quais funcionalidades a Django fornece com o seu sistema de modelo de marcação.

{{< understand-django-series-pt "templates" >}}

## Configure os Modelos de Marcação

Nós precisamos dum lugar para os modelos de marcação morarem. Os modelos de marcação são ficheiros estáticos que a Django preencherá com dados. Para usar estes ficheiros, devemos instruir a Django sobre onde encontrá-los.

Tal como a maioria das partes da Django, esta configuração está no ficheiro de definições do teu projeto. Depois de usares `startproject`, podes encontrar uma seção no teu ficheiro de definições que será chamada de `TEMPLATES`. A seção deve parecer-se com algo como:

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

O sistema de modelo de marcação da Django pode usar vários backend de modelo de marcação. Estes ditam como os teus modelos de marcação funcionarão. Eu recomendaria aguentar com a linguagem de modelo de marcação da Django padrão. Esta linguagem tem a mais firme integração com a abstração e o mais forte suporte.

A próxima coisa a notar é `APP_DIRS` com o seu valor de `True`. Para a linguagem de modelo de marcação da Django, definir este valor para `True` causará a Django à procurar pelos ficheiros de modelo de marcação dentro dum diretório `templates` em cada aplicação de Django no teu projeto. Nota que isto também inclui quaisquer aplicações de terceiros então deverias provavelmente deixar esta definida para `True`.

Então, onde deveriam os *teus* modelos de marcação ir? Existem diferentes escolas de pensamento na comunidade da Django. Alguns programadores acreditam que todos os modelos de marcação deveriam estar dentro das aplicações. Outros imputam para que todos os modelos de marcação do teu projeto deveriam estar num único diretório. Eu estou nesta segunda categoria de programadores. Eu considero valioso manter todos os modelos de marcação para o meu projeto inteiro dentro dum único diretório.

Da minha perspetiva, manter os modelos de marcação num único diretório torna mais claro onde toda disposição e interface de utilizador no teu sistema morarão. Para usar este padrão, devemos definir a variável `DIRS` com o diretório que queremos que a Django inclua. Eu recomendo manter um diretório `templates` na raiz do teu projeto. Se fizeres isto, o valor do tua `DIRS` mudará para algo como:

```python
# project/settings.py

TEMPLATES = [
...
    "DIRS": [BASE_DIR / "templates"],
...
]
```

Finalmente, existe `OPTIONS`. Cada backend pode aceitar uma variedade de opções. `startproject` define um número de processadores de contexto. Voltaremos para os processadores de contexto depois
{{< web >}}
neste artigo.
{{< /web >}}
{{< book >}}
neste capítulo.
{{< /book >}}

Com os teus modelos de marcação definidos, estás pronto para avançares!

## Usando os Modelos de Marcação com a `render`

A Django construi a tua interface de utilizador *interpretando* um modelo de marcação. A ideia por trás da interpretação é que os dados dinâmicos são combinados com um ficheiro de modelo de marcação estático para produzir uma saída final.

Para produzir um `HttpResponse` que contém a saída interpretada, usamos a função `render`. Vamos ver um exemplo na forma duma visão baseada em função (FBV):

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

Neste exemplo, a visão usaria um modelo de marcação localizado em `templates/hello.txt` que poderia conter:

```txt
Hello {{ name }}
```

Quando esta visão responde à uma requisição, um utilizador veria "Hello Johnny" no seu navegador. Existem algumas coisas interessantes à notar sobre este exemplo.

1. O modelo de marcação pode ser qualquer tipo de ficheiro de texto. Mais frequentemente usaremos HTML para fazer uma interface de utilizador então frequentemente veremos `some_template.html`, mas o sistema de modelo de marcação da Django pode interpretar qualquer tipo.
2. No processo de interpretação, a Django pegou o dicionário de dados do contexto e usou suas chaves como nomes de variáveis no modelo de marcação. Por causa da sintaxe especial de chavetas duplas, o backend do modelo de marcação trocou `{{ name }}` pelo valor literal "Johnny" que estava no contexto.

Esta ideia de misturar contexto e disposição estática é o conceito fundamental do trabalho com modelos de marcação.
{{< web >}}
O resto deste artigo baseasse
{{< /web >}}
{{< book >}}
O resto deste capítulo baseasse
{{< /book >}}
neste conceito de origem e mostra o que mais é possível na linguagem do modelo de marcação da Django.

Como um aparte, HTML é um tópico que não iremos explorar diretamente. HTML, **Hypertext Markup Language**, Linguagem de Marcação de Hipertexto, é a linguagem usada na Web para descrever a estrutura duma página. HTML é composta de marcadores e muitos destes marcadores trabalham em pares. Por exemplo, para fazer um *parágrafo*, podes usar o marcador `p`, que é representado envolvendo `p` com os sinais maior do que e menor do que para formar o marcador de "abertura". O marcador de "encerramento" é semelhante, mas este inclui uma barra oblíqua:

```html
<p>This is a paragraph example.</p>
```

{{< web >}}
Do último artigo,
{{< /web >}}
{{< book >}}
Do último capítulo,
{{< /book >}}
podes lembrar-te de ver a `TemplateView`. Naqueles exemplos, fornecemos um nome de modelo de marcação, e declarei que a Django cuidaria do resto. Agora podes começar a entender que a Django recebe o nome do modelo de marcação e chama um código semelhante ao `render` para fornecer um `HttpResponse`. Aqueles modelos de marcação estavam com o dado de contexto em falta para combinar com o modelo de marcação. Um exemplo mais completo replicando a visão baseada em função `hello_view` como uma visão baseada em classe parecer-se-ia com:

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

Este exemplo usa `get_context_data` para que possamos inserir os nossos dados "dinâmicos" no sistema de interpretação para dar-nos a resposta que queremos.

Numa aplicação real, muito do código que precisamos de escrever concentra-se em construir um contexto verdadeiramente dinâmico. Eu estou a usar dados estáticos nestes exemplos para manter as mecânicas do sistema de modelo de marcação claras. Quando veres-me a usar `context`, tente imaginar a construção de dados mais complexos para criar uma interface de utilizador.

Estes são os fundamentos da interpretação. Agora voltaremos a nossa atenção para o que a linguagem de modelo de marcação é capaz de fazer.

## Modelos de Marcação em Ação

Quando usamos os modelos de marcação, recebemos o dado de contexto e o inserimos em espaços reservados dentro do modelo de marcação.

As variáveis do modelo de marcação são a forma mais básica de preencher os espaços reservados com contexto. A seção anterior mostrava um exemplo usando a variável `name`. O dicionário de contexto contém um chave, cujo valor aparece em qualquer parte no modelo de marcação onde esta chave é envolvida por duplas chavetas.

Nós podemos também usar um ponto de acesso quando o dado de contexto for mais complexo. Vamos dizer que o teu modelo de marcação recebe um contexto como:

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

O teu modelo de marcação da Django *não funcionará* se tentares acessar este dado de contexto como um dicionário normal (por exemplo, `{{ address['street'] }}`). Ao invés disto, usarias a notação de ponto para teres acesso aos dados no dicionário:

```txt
The address is:
    {{ address.street }}
    {{ address.city }}, {{ address.state }} {{ address.zip_code}}
```

Isto interpretaria como:

```txt
The address is:
    123 Main St.
    Beverly Hills, CA 90210
```

Os modelos de marcação da Django também tentam ser flexíveis com os tipos de dados de contexto. Tu poderias também passar uma instância de classe da Python como uma classe `Address` com atributos que são iguais as chaves nos dicionário anterior. O modelo de marcação funcionaria da mesma maneira.

A linguagem de modelo de marcação fundamental também inclui algumas palavras-chave de lógica de programação padrão usando *marcadores*. Os marcadores do modelo de marcação parecem-se com `{% some_tag %}` ao passo que as variáveis do modelo de marcação parecem-se com `{{ some_variable }}`. As variáveis estão destinadas a serem espaço reservados à preencher, mas os marcadores oferecem mais poder.

Nós podemos começar com dois marcadores fundamentais, `if` e `for`.

O marcador `if` é para lidar com lógica condicional que o teu modelo de marcação pudesse precisar:

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

Este exemplo apenas incluirá este marcador de cabeçalho de texto de HTML da mensagem de boas-vindas quando o utilizador estiver com a sua sessão iniciada nesta aplicação. Nós começamos o exemplo com um marcador `if`. Observe que o marcador `if` exige um marcador `endif` de encerramento. Os modelos de marcação devem respeitar o espaço em branco visto que a tua disposição pode depender deste espaço em branco. A linguagem de modelo de marcação não pode usar espaço em branco para indicar âmbito como pode com a Python então ao invés disto usa marcadores de encerramento. Como podes supor, também existem os marcadores `else` e `elif` que são aceites dentro um par `if`/`endif`:

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

Neste caso, apenas um dos marcadores de cabeçalho de texto interpretará dependendo de se o utilizador estiver autenticado ou não.

O outro marcador fundamental a considerar é o marcador de laço de repetição `for`. Um lado de repetição `for` nos modelos de marcação da Django comportam-se como podes esperar:

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

A Django iterará sobre os iteráveis como listas e deixarão os utilizadores produzirem respostas de modelo de marcação para cada entrada num iterável. Se o exemplo acima tivesse uma lista de `items` no contexto como:

```python
items = [
    {'name': 'Pizza', 'price': '$12.99'},
    {'name': 'Soda', 'price': '$3.99'},
]
```

Então a saída parecer-se-ia aproximadamente com:

```html
<p>Prices:</p>
<ul>
    <li>Pizza costs $12.99.</li>
    <li>Soda costs $3.99.</li>
</ul>
```

Ocasionalmente, podes querer tomar alguma específica sobre um elemento particular no laço de repetição `for`. A função `enumerate` embutida da Python não está disponível diretamente nos modelos de marcação, mas uma variável especial chamada `forloop` está disponível dentro dum marcador `for`. Esta variável `forloop` tem alguns atributos como `first` e `last` que podes usar para fazer os modelos de marcação comportarem-se de maneira diferente em certas iterações do laço de repetição:

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

Este exemplo produziria:

```txt
Counting:
    1
    2
    3 is last!
```

Equipado com variáveis, marcadores `if`, e marcadores `for`, agora deverias ter a habilidade de criar alguns modelos de marcação razoavelmente poderosos, mas existem mais! 

### Mais Contexto sobre Contexto

Na configuração das definições de modelos de marcação, não falámos dos processadores de contexto. Os processadores de contexto são uma maneira valiosa de estender o contexto que está disponível para os teus modelos de marcação quando forem interpretados.

Neste exemplo temos um conjunto de processadores de contexto que o comando `startproject` da Django trás por padrão:

```python
'context_processors': [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
],
```

Os processadores de contexto são (tecnicamente, chamáveis, mas vamos nos concentrar nas funções) que recebem um `HttpRequest` e deve retornar um dicionário. O dicionário retornado funde-se com qualquer outro contexto que será passado para o modelo de marcação.

Concetualmente, quando preparas para interpretar e dado um dicionário de `context` que era passado para `render`, o sistema de modelo de marcação farão algo como:

```python
for processor in context_processors:
    context.update(processor(request))

# Continue na interpretação de modelo de marcação
```

O verdadeiro código no sistema de modelo de marcação é mais complexo do que este esboço de código de conceito, mas não muito.

Nós podemos olhar na verdadeira definição do processador de contexto `request` incluído naquela lista padrão:

```python
# django/template/context_processors.py

def request(request):
    return {'request': request}
```

Já está! Por causa deste processador de contexto, o objeto `request` estará disponível como variável em qualquer modelo de marcação no teu projeto. Isto é superpoderoso.

<div class='sidebar'>

<h4>Barra lateral</h4>

<p>
Não tenhas medo de olhar o código-fonte dos projetos sobre os quais dependes. Lembra-te de que pessoas normais escreveram as tuas abstrações favoritas! Tu podes aprender lições valiosas a partir daquilo que fizeram. O código pode ser um pouco intimidante a princípio, mas não existe magia por trás dele!
</p>

</div>

O "lado escuro" dos processadores de texto é que executam para todas as requisições. Se escreveres um processador de contexto que é lento e que faz muito cálculo, *cada requisição* sofrerá este impacto de desempenho. Então use os processadores de contexto cuidadosamente.

### Pedaços Reutilizáveis de Modelos de Marcação

Agora falaremos sobre uma das funcionalidades do núcleo de atividade do sistema de modelo de marcação: pedaços reutilizáveis.

Pense sobre um local da Web. A maioria das páginas têm uma aparência semelhante. Elas fazem isto repetindo muito do mesmo HTML, que é a Linguagem de Marcação de Hipertexto que define a estrutura duma página. Estas páginas também usam a mesma CSS, Folhas de Estilo em Cascata, que define os estilos que moldam a aparência dos elementos da página.

Imagine que és convidado para gerir uma aplicação e precisas de criar duas páginas separadas. A página principal parece-se com:

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

E cá está uma página para conhecer a empresa por trás do local da Web:

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

Estes exemplos são quantidades minúsculas de HTML, mas e se fores pedido para mudar a folha de estilo de `styles.css` para uma nova folha de estilo feita por um desenhista chamada `better_styles.css`? Tu terias de atualizar ambos lugares. Agora pense se existissem 2.000 páginas ao invés de 2 páginas. Fazer grandes mudanças rapidamente através duma aplicação seria virtualmente impossível!

A Django ajuda-te a evitar este cenário inteiramente com alguns marcadores. Vamos criar um novo modelo de marcação chamado `base.html`:

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

Criamos um modelo de marcação reutilizável com o marcador `block`! Nós podemos reformar a nossa página principal para usar este novo modelo de marcação:

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

Esta nova versão da página principal *estende* o modelo de marcação de base. Tudo o que modelo de marcação tinha de fazer era definir sua própria versão do bloco `main` para preencher o conteúdo. Nós poderíamos fazer exatamente a mesma coisa com a página sobre.

Se revisitarmos a tarefa de substituir `styles.css` por `better_styles.css`, poderemos fazer a atualização no `base.html` e ter esta mudança aplicada à quaisquer modelos de marcação que o estende. Mesmo se existissem 2.000 páginas que se estendessem todas a partir de `base.html`, mudar a folha de estilo continuaria ser uma linha de código à mudar para uma aplicação inteira.

Este é o poder do sistema de extensão de modelo de marcação da Django. Use `extend` quando precisares de conteúdo que é na maior parte das vezes o mesmo. Adicione uma seção de `block` sempre que precisares de personalizar uma página estendida. Tu podes estender uma página incluindo vários tipos de blocos. O modelo de marcação apenas exibe um bloco de `main`, mas podes ter páginas que personalizam um `sidebar`, `header`, `footer`, ou qualquer coisa que possa variar.

Uma outra ferramenta poderosa para reutilização é o marcador `include`. O marcador `include` é útil quando queres extrair algum pedaço do modelo de marcação que queres usar em várias localizações. Tu podes querer usar `include` para:

1. Manter os modelos de marcação organizados. Tu podes quebrar um grande modelo de marcação em pequenos pedaços que são mais manejáveis.
2. Usar um fragmento de modelo de marcação em diferentes partes da tua aplicação. Talvez tenhas um pedaço de modelo de marcação que deveria apenas aparecer em algumas páginas.

Voltando ao nosso exemplo de aplicação de Web, imagine que `base.html` cresceu até estar com mais de 20.000 linhas. Navegar para a parte correta do modelo de marcação para fazer mudanças agora é mais difícil. Nós podemos decompor o modelo de marcação em pedaços mais pequenos:

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

O marcador `include` pode mover estes pedaços adicionais. Ao fornecer um bom nome para os teus modelos de marcação, se precisasses de mudar a estrutura de alguma seção como navegação, poderias ir ao modelo de marcação com o nome apropriado. Este ficheiro de modelo de marcação focar-se-ia apenas no elemento que precisas mudar.

`block`, `extends`, e `include` são marcadores fundamentais para proteger o teu código da interface de utilizador de crescer desordenadamente por toda a parte com muitas duplicações.

A seguir, falaremos de mais marcadores de modelo de marcação embutidos da Django que podem sobrecarregar a tua interface de utilizador.

## A Caixa de Ferramentas dos Modelos de Marcação

A documentação da Django inclui um {{< extlink "https://docs.djangoproject.com/en/4.1/ref/templates/builtins/" "vasto conjunto de marcadores embutidos" >}} que podes usar nos teus projetos. Nós não iremos cobrir todos, mas nos focaremos em alguns marcadores para dar-te um gosto do que está disponível.

Um dos mais usados marcadores embutidos à parte daqueles que já cobrimos é o marcador `url`.
{{< web >}}
Lembra-te do artigo
{{< /web >}}
{{< book >}}
Lembra-te do capítulo
{{< /book >}}
sobre URLs de que podes receber a URL para uma visão nomeada usando a função `reverse`. E se quisesses usar a URL no teu modelo de marcação? Tu poderias fazer isto:

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

Embora isto funcione, é tedioso ter de enviar todas as URLs através do contexto. Ao invés disto, o nosso modelo de marcação pode criar diretamente a URL apropriada. No exemplo abaixo mostramos como `a_template.html` se pareceria:

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

O marcador `url` é o equivalente do modelo de marcação da função `reverse`. Tal como sua homóloga `reverse`, `url` pode aceitar argumentos ou argumentos de chaves e valores para rotas que esperam outras variáveis. `url` é uma ferramenta incrivelmente útil e aquela que provavelmente usarás com frequência a medida que constróis a tua interface de utilizador.

Um outro marcador útil é o marcador `now`. `now` é um método conveniente para exibir informação sobre a hora atual. Usando o que a Django chama de *especificadores de formato*, podes dizer ao teu modelo de marcação como exibir a hora atual. Queres adicionar o ano atual dos direitos de autor à tua aplicação? Sem problemas!:

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

Um último marcador embutido a considerar é o marcador `spaceless`. A HTML é *particularmente* sensível ao espaço em branco. Existem algumas circunstâncias frustrantes onde esta sensibilidade ao espaço em branco pode arruinar o teu dia quando constróis uma interface de utilizador. Podes fazer um menu de navegação de pixeis perfeito para a tua aplicação com uma lista não ordenada? Talvez. Considere isto:

```html
<ul class="navigation">
    <li><a href="/home/">Home</a></li>
    <li><a href="/about/">About</a></li>
</ul>
```

O espaço em branco indentado nestes itens de lista (ou os caracteres de nova linha que os seguem) podem causar-te problema quando trabalhas com a CSS. Sabendo que o espaço em branco pode afetar a disposição da página, podemos usar `spaceless` assim:

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

Este pequeno fantástico marcador de modelo de marcação removerá todos os espaços entre os marcadores de HTML assim a tua saída parece-se com:

```html
<ul class="navigation"><li><a href="/home/">Home</a></li>...</ul>
```

Com a remoção do espaço adicional, podes ter uma experiência mais consistente com a tua estilização de CSS e poupares-te de alguma frustração.
{{< web >}}
(Eu tive de aparar a saída para ajustar-se melhor no ecrã.)
{{< /web >}}

Existe um outro tipo de embutido que ainda não olhamos. Estas funções embutidas alternativas são chamadas de **filtros**. Os filtros mudam a saída das variáveis nos teus modelos de marcação. A sintaxe do filtro é um pouco interessante. Parece-se com:

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

O elemento importante é o carácter de conduta imediatamente depois duma variável. Este carácter faz sinal ao sistema de modelo de marcação que queremos modificar a variável com algum tipo de transformação. Também observe que os filtros são usados entre chavetas duplas no lugar da sintaxe `{%` que vimos com os marcadores.

Um filtro muito comum é o filtro `date`. Quando passas um instância de `datetime` da Python no contexto, podes usar o filtro `date` para controlar o formato da data e hora. A {{< extlink "https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#date" "documentação" >}} do `date` mostra quais opções podes usar para modificar o formato:

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

Se `a_datetime` for uma instância do Dia das Mentiras, então poderia retornar uma sequência de caracteres como `2020-04-01`. O filtro `date` tem muitos especificadores que possibilitam-te produzir a maioria das saídas de formatação de data que poderias imaginar.

`default` é um filtro útil para quando o valor do teu modelo de marcação avalia para `False`. Isto é perfeito quando temos uma variável com uma sequência de caracteres vazia. O exemplo abaixo resulta em "Nothing to see here" se a variável for falsa:

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

Falso é um conceito na Python que descreve qualquer coisa que a Python avaliará como falso numa expressão booleana. As sequências de caracteres vazias, listas vazias, dicionários vazios, conjuntos vazios, `False`, e `None` são todos valores Falsos. 

`length` é um filtro simples para listas. `{{ a_list_variable|length }}` produzirá um número. É o equivalente do modelo de marcação da Django para a função `len`.

Eu gosto muito do filtro `linebreaks`. Se criares um formulário
{{< web >}}
(o que exploraremos no próximo artigo)
{{< /web >}}
{{< book >}}
(o que exploraremos no próximo capítulo)
{{< /book >}}
e aceitares um campo de área de texto onde o utilizador está autorizado a fornecer novas linhas, então o filtro `linebreaks` permite-te exibir estas novas linhas mais tarde quando interpretares os dados do utilizador. Por padrão, a HTML não mostrará os caracteres de nova linha como pretendido. O filtro `linebreaks` converterá `\n` para um marcador de HTML `<br>`. Prático!

Antes de seguires em frente, vamos considerar mais dois.

`pluralize` é um filtro conveniente para os momentos quando teu texto considera a contagens de coisas. Considera uma contagem de itens:

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

O filtro `pluralize` fará a coisa certa se existirem zero, um, ou mais itens na lista.

```txt
0 items
1 item
2 items
3 items
(and so on)
```

Tenha atenção que `pluralize` não pode lidar com plurais irregulares como "mice" ou "mouse."

O filtro final no nosso passeio é o filtro `yesno`. `yesno` é bom para conversão `True|False|None` em uma mensagem de texto significativo. Imagina que estamos a criar uma aplicação para rastreamento de eventos e a presença duma pessoa é um destes três valores. O nosso modelo de marcação parecer-se-á com:

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

Dependendo do valor da `user_accepted`, o modelo de marcação exibirá algo significativo para um leitor.

Existem muitos filtros embutidos que é realmente difícil delimitar os meus favoritos. Consulte a lista completa para veres o que pode ser útil para ti.

E se os filtros embutidos não cobrirem o que precisas? Não tenhas medo, a Django permite-te criar marcadores e filtros personalizados para os teus próprios fins. Veremos como a seguir.

### Construa o Teu Próprio Sabre de Luz Nos Modelos de Marcação

Quando precisares de construir os teus próprios marcadores ou filtros personalizados, a Django dá-te as ferramentas para fazeres o que precisas.

Existem três elementos principais para trabalhar com marcadores personalizados:

1. Definir os teus marcadores num lugar que a Django espera.
2. Registar os teus marcadores com o motor de modelo de marcação.
3. Carregar os teus marcadores num modelo de marcação para que possam ser usados.

O primeiro passo é colocar os marcadores na localização correta. Para fazer isto, precisamos dum pacote de Python `templatetags` dentro duma aplicação de Django. Nós também precisamos dum módulo neste diretório. Escolha o nome do módulo cuidadosamente porque é o que carregaremos no modelo de marcação mais tarde: 

```txt
application
├── templatetags
│   ├── __init__.py
│   └── custom_tags.py
├── __init__.py
├── ...
├── models.py
└── views.py
```

A seguir, precisamos de criar o nosso marcador ou filtro e registá-lo. Vamos começar com um exemplo de filtro:

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

Agora, se tivermos uma variável `message`, podemos dá-la algum entusiasmo. Para usar o filtro personalizado, devemos carregar o nosso módulo de marcadores no modelo de marcação com o marcador `load`:

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

Se a nossa mensagem foi "You got a perfect score!", então o nosso modelo de marcação mostraria a mensagem e uma das três escolhas pseudo-aleatórias como "You got a perfect score! Wowza!"

Escrever marcadores personalizado básicos é muito semelhante aos filtros personalizados. O código fala melhor do que as palavras:

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

Nós podemos carregar marcadores personalizados e usar o nosso marcador como qualquer outro marcador embutido:

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

Este marcador de boas-vindas responderá à várias variáveis de entrada e varia dependendo do nível fornecido. O exemplo de uso deveria exibir "Hello great champion He-Man!"

Estamos apenas olhando para os tipos mais comuns de marcadores personalizados nos nossos exemplos. Existem funcionalidades de marcação personalizada avançadas que podes explorar na {{< extlink "https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/" "documentação de marcadores de modelos de marcação personalizados da Django" >}}.

A Django também usa `load` para fornecer algumas ferramentas adicionais aos autores de modelo de marcação. Por exemplo, veremos como carregar alguns marcadores personalizados fornecidos pela abstração quando estudarmos sobre como trabalhar com imagens e JavaScript mais tarde.

## Sumário

Agora vimos os modelos de marcação em ação! Vimos: 

* Como configurar os modelos de marcação para a tua aplicação
* Maneiras de chamar os modelos de marcação a partir das visões
* Como usar os dados
* Como manipular a lógica
* Marcadores e filtros embutidos disponíveis para os modelos de marcação
* Personalização de modelos de marcação com as tuas próprias extensões de código

{{< web >}}
No próximo artigo,
{{< /web >}}
{{< book >}}
No próximo capítulo,
{{< /book >}}
examinaremos como os utilizadores podem enviar os dados à uma aplicação de Django com os formulários de HTML. A Django tem ferramentas para tornar a construção de formulário rápido e efetivo. Veremos:

* A classe `Form` que a Django usa para manipular os dados do formulário na Python
* Controlo de quais campos estão nos formulários
* Como os formulários são desenhados para os utilizadores pela Django
* Como fazer a validação de formulário

{{< web >}}
Se gostarias de seguir com a série, sinta-se livre para inscrever-se no meu boletim informativo onde anúncio todos os meus novos conteúdos. Se tiveres outras questões, podes contactar-me na X onde sou {{< extlink "https://x.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;

A tradução deste artigo para o português é cortesia de Nazaré Da Piedade.
