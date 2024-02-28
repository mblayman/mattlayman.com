---
title: "A Anatomia Duma Aplicação"
description: >-
    Este artigo explora as aplicações. As aplicações são elementos estruturais fundamentais dum projeto de Django. Nós veremos a composição duma aplicação e como usá-las efetivamente.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - applications
series: "Understand Django"

---

{{< web >}}
No artigo anterior da série [Entendendo a Django]({{< ref "/understand-django/2020-08-26-administer-all-the-things.pt.md" >}}), mergulhamos no sítio dos administradores da Django. Nós vimos o que o sítio era e como configurá-lo e personalizá-lo. Neste artigo,
{{< /web >}}
{{< book >}}
Neste capítulo,
{{< /book >}}
examinaremos o que acontece numa aplicação. As aplicações são os elementos fundamentais dum projeto de Django.

{{< understand-django-series-pt "apps" >}}

## O Que é uma Aplicação?

Antes de sabermos o que uma aplicação de Django **é**, provavelmente precisamos começar por o que esta **não é** porque a terminologia é confusa. No mundo do desenvolvimento da Web, os programadores podem chamar uma sítio da Web duma "aplicação da Web".

No linguajar da Django, uma "aplicação da Web" é um *projeto* de Django. Todos os pedaços que reúnem-se para fazer um sítio da Web são um projeto. Os componentes primários dentro do projeto são chamados de *aplicações*. Em outras palavras, um projeto de Django é construído a partir duma ou mais aplicações.

Esta situação é muito semelhante aos pacotes da Python. A industria de software muitas vezes descreve a unidade de software como um "pacote". Nós pensamos de `pip`, `npm`, ou `apt` como gestores de "pacote". Isto conduz a um problema de nomenclatura semelhante porque a Python também chama qualquer diretório com um ficheiro `__init__.py` de "pacote".

Na realidade, o código que descarregamos usando `pip` é tecnicamente chamado de "{{< extlink "https://packaging.python.org/overview/" "distribuição" >}}". Embora que coloquialmente falemos dos descarregamentos da PyPI (Python Package Index ou Índice de Pacote da Python) como pacotes, estamos realmente falando de distribuições, e uma distribuição é uma unidade que contém um ou mais pacotes de Python.

Com sorte, agora entendemos a relação das aplicações na Django.

> A nossa "aplicação da Web" é um **projeto** de Django composto por uma ou mais **aplicações** de Django.

## Estrutura da Aplicação

Olharemos para uma aplicação de Django completamente carregada para vermos a estrutura razoavelmente padronizada que encontraremos nos projetos de Django.

Uma aplicação usualmente tenta capturar um conceito fundamental dentro nosso sistema.
{{< web >}}
Para este artigo,
{{< /web >}}
{{< book >}}
Para este capítulo,
{{< /book >}}
usaremos os filmes como o conceito que queremos modelar.

Vamos ver o que uma estrutura do projeto padrão inclui, depois o desenvolveremos com todos os adicionais:

```bash
(venv) $ ./manage.py startapp movies
(venv) $ tree movies
movies
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

`admin.py`: Este ficheiro é onde todas as nossas classes de `ModelAdmin` vivem para alimentar como a aplicação de filmes aparecerá no administrador da Django.
{{< web >}}
Nós podemos aprender mais sobre o administrador no artigo [Administrar Tudo]({{< ref "/understand-django/2020-08-26-administer-all-the-things.pt.md" >}}).
{{< /web >}}

`apps.py`: Este ficheiro é para a `AppConfig` da aplicação. Nós discutiremos a `AppConfig` e como usá-la
{{< web >}}
mais tarde neste artigo.
{{< /web >}}
{{< book >}}
mais tarde neste capítulo.
{{< /book >}}

`migrations`: Este diretório é onde todas as migrações da base de dados são armazenadas para a aplicação. Quaisquer mudanças do modelo para esta aplicação gerará uma migração e criará um ficheiro de migração numerado neste diretório.
{{< web >}}
Nós podemos encontrar mais informações sobre as migrações no artigo [Armazenar Dados com os Modelos de Base de Dados]({{< ref "/understand-django/2020-06-25-store-data-with-models.pt.md" >}}).
{{< /web >}}

`models.py`: Este ficheiro é o lar para todas as classes de `Model` da Django na aplicação. Os modelos representam todos os dados da nossa base de dados.
{{< web >}}
Nós podemos aprender mais sobre os modelos de base dados no artigo [Armazenar Dados com os Modelos de Base de Dados]({{< ref "/understand-django/2020-06-25-store-data-with-models.pt.md" >}}).
{{< /web >}}

`tests.py`: Este ficheiro é para os testes automatizados. Nós cobriremos testes automatizados na Django
{{< web >}}
num artigo futuro.
{{< /web >}}
{{< book >}}
num capítulo futuro.
{{< /book >}}
Por agora, posso dizer que *sempre* **elimino** este ficheiro e o substituo por um pacote `tests`. Um pacote `tests` é superior porque podemos separar em ficheiros mais focados como `test_models.py` para sabermos onde os testes apropriados estão.

`views.py`: Este ficheiro é onde as funções ou classes de visão da Django vão. As visões são os códigos de colagem que conectam as rotas do nosso localizador de recurso uniforme aos nossos modelos de base de dados.
{{< web >}}
Eu escrevi sobre as visões no artigo [Visões Sobre Visões]({{< ref "/understand-django/2020-03-03-views-on-views.pt.md" >}}).
{{< /web >}}

Isto é tudo que vem com uma aplicação gerada, mas quais são os outros ficheiros em falta que comummente veremos numa aplicação de Django?

`urls.py`: Este ficheiro é muitas vezes usado para criar rotas que agrupam logicamente todas funcionalidades relacionadas ao filme. O ficheiro `urls.py` alimentaria todas as rotas em algo como `www.mysite.com/movies/`.
{{< web >}}
Nós podemos encontrar informação sobre os Localizadores de Recurso Uniforme no artigo [URLs Guiam o Caminho]({{< ref "/understand-django/2020-01-22-urls-lead-way.pt.md" >}}).
{{< /web >}}

`forms.py`; Quando usamos as classes de `Form` da Django para interagirmos com os utilizadores, este é o ficheiro onde os formulários são armazenados.
{{< web >}}
Nós podemos descobrir mais sobre os formulários no artigo [Interação do Utilizador com Formulários]({{< ref "/understand-django/2020-05-05-user-interaction-forms.pt.md" >}}).
{{< /web >}}

`templatetags`: Este diretório é um pacote da Python que incluiria um módulo como `movies_tags.py`, onde definiríamos quaisquer marcadores personalizados do modelo de marcação a usar quando desenharmos os nossos modelos de marcação de hipertexto.
{{< web >}}
Os marcadores personalizados são um tópico no [Modelos de Marcação para as Interfaces do Utilizador]({{< ref "/understand-django/2020-04-02-templates-user-interfaces.pt.md" >}}).
{{< /web >}}

`templates`: Este diretório pode armazenar os modelos de marcação de hipertexto que a aplicação desenhará. Eu pessoalmente prefiro usar um diretório `templates` para o projeto inteiro conforme discutido
{{< web >}}
no artigo [Modelos de Marcação para as Interfaces do Utilizador]({{< ref "/understand-django/2020-04-02-templates-user-interfaces.pt.md" >}}),
{{< /web >}}
{{< book >}}
no capítulo dos modelos de marcação de hipertexto,
{{< /book >}}
mas diretórios de `templates` são comummente encontrados dentro das aplicações individuais da Django, especialmente para aplicações de terceiros que podemos puxar para dentro do nosso projeto.

`static`: Para os ficheiros estáticos que queremos exibir, tais como imagens, podemos usar o diretório `static`. Nós discutiremos mais os ficheiros estáticos
{{< web >}}
num artigo futuro.
{{< /web >}}
{{< book >}}
num capítulo futuro.
{{< /book >}}

`management`: Os utilizadores podem estender a Django com comandos personalizados que podem ser chamados através do `manage.py`. Estes comandos são armazenados neste pacote. Os comandos personalizados são um tópico futuro
{{< web >}}
nesta série.
{{< /web >}}
{{< book >}}
neste livro.
{{< /book >}}

`locale`: Quando fazemos traduções e internacionalização, os ficheiros de tradução devem ter uma casa. Este é o propósito do diretório `locale`.

`managers.py`: Este ficheiro nem sempre é usado, mas se a nossa aplicação tiver muitos administradores personalizados, então podemos querer separá-los dos nossos modelos neste ficheiro.
{{< web >}}
Os administradores são um tópico no artigo [Armazenar Dados com os Modelos de Base de Dados]({{< ref "/understand-django/2020-06-25-store-data-with-models.pt.md" >}}).
{{< /web >}}

A maioria das aplicações *não* terão todos estes pedaços, mas isto deve dar-nos uma ideia do que são quando estivermos explorando as aplicações da Django na natureza por conta própria. Eis como a nossa árvore de amostra se pareceria:

```bash
(venv) $ tree movies
movies
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── locale
│   └── es
│       └── LC_MESSAGES
│           ├── django.mo
│           └── django.po
├── management
│   ├── __init__.py
│   └── commands
│       ├── __init__.py
│       └── do_movie_stuff.py
├── managers.py
├── migrations
│   ├── 0001_initial.py
│   └── __init__.py
├── models.py
├── static
│   └── movies
│       └── moviereel.png
├── templates
│   └── movies
│       ├── index.html
│       └── movie_detail.html
├── templatestags
│   ├── __init__.py
│   └── movies_tags.py
├── tests
│   ├── __init__.py
│   ├── test_models.py
│   └── test_views.py
├── urls.py
└── views.py
```

## Carregando as Aplicações

Já vimos o que está numa aplicação de Django e temos uma ideia da composição duma aplicação. Como é que a Django carrega as aplicações?

A Django *não* faz a descoberta automática das aplicações de Django dentro do nosso projeto. Se quisermos que a Django inclua uma aplicação no nosso projeto, *devemos* adicionar a aplicação à nossa lista de `INSTALLED_APPS` no ficheiro definições.

Este é um bom exemplo da Django seguindo o espírito da Python de favorecer o explícito sobre o implícito. Ao sermos explícitos, o nosso projeto não arrisca-se a incluir aplicações que não esperamos. Isto pode parecer ridículo para aplicações que nós mesmos escrevemos, mas ficaremos gratos se algum pacote de terceiros no nosso ambiente virtual tiver uma aplicação de Django que não queremos no nosso projeto.

Na inicialização, quando uma aplicação estiver na `INSTALLED_APPS`, a Django procurará por uma classe de `AppConfig`. Esta classe é armazenada no `apps.py` a partir do comando `startapp` e contém metadados sobre a aplicação.

Quando a Django inicia, esta inicializará o sistema fazendo o seguinte:

* Carregar as definições
* Configurar o registo (um tópico que exploraremos no futuro)
* Inicializar um registo de aplicação
* Importar cada pacote da `INSTALLED_APPS`
* Importar um módulo de modelos de base de dados para cada aplicação
* Invocar o método `ready` de cada `AppConfig` descoberta

O método `ready` é uma função gatilho útil para tomar ações na inicialização. Já que os modelos de base de dados já estão carregados no momento em que o método é chamado, é um lugar seguro para interagir com a Django.

Se tentarmos executar o código de configuração antes que a Django esteja pronta, e tentarmos fazer algo como usar o mapeamento de objeto-relacional para interagir com os dados da base de dados, provavelmente receberemos uma exceção de `AppRegistryNotReady`. A maioria das aplicações não precisará executar o código de inicialização, mas saber sobre o gatilho `ready` é uma pedaço útil de conhecimento para manter no bolso de trás.

## Aplicações do Ecossistema

Uma aplicação é uma ferramenta importante para agrupar os diferentes componentes lógicos do nosso projeto, mas as aplicações também têm outro objetivo. As aplicações são a base para a maioria das extensões de terceiros no ecossistema da Django.

Uma grande razão para usar a Django é que a abstração tem uma abordagem de "baterias incluídas". A maioria das ferramentas que precisamos para construir um sítio da Web estão diretamente integrada na abstração. Esta é uma abordagem muito diferente em comparação com a {{< extlink "https://flask.palletsprojects.com/en/2.2.x/" "Flask" >}}, que fornece uma interface de programação de aplicação relativamente pequena e depende muito de bibliotecas de terceiros.

Embora a Django inclua a maioria das peças principais para uma aplicação da Web, a abstração não inclui *tudo*. Quando queremos incluir mais funcionalidades, as aplicações da Django preenchem as lacunas.

Antes de irmos para o PyPI, não precisamos ir além do pacote `django.contrib`, uma coleção de aplicações "contribuídas" fornecidas pela propria Django. Quando executamos o comando `startproject`, a Django incluirá uma variedade de aplicações embutidas que executam diferentes funções. Se não precisarmos de alguma funcionalidade, podemos optar por não usá-la, removendo a aplicação da nossa lista em `INSTALLED_APPS`.

Eu penso que está é a grande diferença de filosofia por trás da abstração. Alguns programadores gostam de começar com um núcleo de funcionalidade extremamente mínimo e construí-lo com base nas suas necessidades. A filosofia da Django parece ser que começamos com uma linha de base opinada e reduzimos o que não é necessário. A Django não espera que usaremos todas as funcionalidades em todas as aplicações, mas muitas das funcionalidades que desejaremos estarão prontas quando precisarmos delas.

Do meu ponto de vista, acho que a filosofia da Django é a correta (chocante, não é? 🤪). A vantagem da filosofia da Django é que se aproveita o conhecimento de pessoas que construíram aplicações da Web durante muito tempo. Não só aproveita esse conhecimento, como também beneficia o polimento aplicação pelos programadores da Django para integrar os diferentes sistemas importantes num todo consistente. O que nos resta é uma abstração que parece pertencer ao mesmo ambiente, e penso que isso tem um impacto positivo na nossa produtividade.

Quando construímos a partir dum núcleo mínimo e trabalhamos para cima, dependemos de saber tudo o que é necessário para colocar algo na Web. Isto significa que conhecemos todas as peças e sabemos como aparafusá-las. Mas a maioria das pessoas *não* conhece todas as peças (porque são muitas!).

Se começarmos minimamente e não conhecermos as peças, aprenderemos ao longo do caminho, mas o que acontece quando nos deparamos com um novo conceito que não se enquadra no nosso modelo mental original? Por exemplo, a segurança é uma parte crítica que pode destruir o nosso modelo mental quando tomamos conhecimento duma classe de vulnerabilidades que podem restringir o que é possível fazer com segurança. Quando seguimos esta abordagem de construir a partir do zero, penso que o resultado será naturalmente a nossa própria abstração personalizada. Se este é o caso de alguns, ótimo. Façam-no. Para mim, quero uma abstração que seja um bem de consumo e que seja comummente compreendida por muitas pessoas.

Muito bem, então, o que isto tem a haver com as aplicações da Django? As aplicações são módulos independentes e reutilizáveis. Uma vez que têm uma estrutura razoavelmente padronizada, um projeto pode integrar rapidamente uma nova aplicação. Isto significa que podemos tirar partido do conhecimento e experiência (leia-se: cicatrizes de batalha) de outros programadores da Web. Todas as aplicações obedecem às mesmas regras, pelo que nós, enquanto programadores, passamos menos tempo a integrar a aplicação ao nosso projeto e mais tempo a beneficiar-se do que esta faz.

Eu penso que esta estrutura padrão também facilita a experimentação de novas aplicações. Quando preciso de alguma nova funcionalidade, vou muitas vezes consultar os {{< extlink "https://djangopackages.org/" "Pacotes da Django" >}} para procurar por aplicações que satisfaçam as minhas necessidades. Na minha experiência, adicionar uma nova aplicação é, em muitos casos, pouco mias do que instalar o pacote, adicionar a aplicação à lista `INSTALLED_APPS` e colocar uma `include` no meu ficheiro `urls.py`. Alguns pacotes exigem mais configurações do que isso, mas penso que o custo de integração é suficientemente baixo para que eu possa experimentar rapidamente e desistir da minha decisão se descobrir que uma aplicação não faz o que preciso.

Em suma, as aplicações da Django tornam o trabalho com o ecossistema da Django uma experiência mais agradável.

## Sumário

{{< web >}}
Neste artigo,
{{< /web >}}
{{< book >}}
Neste capítulo,
{{< /book >}}
estudámos
as aplicações da Django.

Nós vimos:

* O que é uma aplicação de Django
* Como uma aplicação da Django é estruturada
* Como o ecossistema da Django beneficia-se dum formato comum que cria componentes reutilizáveis

{{< web >}}
Da próxima vez, estudaremos a autenticação
{{< /web >}}
{{< book >}}
A seguir, estudaremos a autenticação
{{< /book >}}
na Django.

Nós estudaremos:

* Como são criados e geridos os utilizadores
* Como lidar com as permissões dos utilizadores
* Como trabalhar com utilizadores nas nossas visões e modelos de marcação

{{< web >}}
Se gostarias de seguir juntamente com a série, sinta-se a vontade para inscrever-se no meu boletim informativo onde anuncio todos os meus novos conteúdos. Se tiveres outras questões, podes contactar-me na Twitter onde sou o {{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;
