---
title: "Autenticação do Utilizador"
description: >-
    O nosso foco neste artigo Entendendo a Django é como gerir os utilizadores na nossa aplicação de Django. Estudaremos o sistema de autenticação de utilizadores embutido da Django.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - authentication
 - authorization
 - autenticação
 - autorização
series: "Understand Django"

---

{{< web >}}
No artigo anterior da [Entenda a Django]({{< ref "/understand-django/2020-09-29-anatomy-of-an-application.pt.md" >}}), nós aprendemos sobre a estrutura duma *aplicação* da Django e como as aplicações são os componentes centrais de um projeto de Django. Neste artigo,
{{< /web >}}
{{< book >}}
Neste capítulo,
{{< /book >}}
nos aprofundaremos no sistema de autenticação do utilizador embutido na Django. Veremos como a Django facilita a nossa vida, dando-nos ferramentas para ajudar a nossa aplicação da Web a interagir com os utilizadores da nossa aplicação da Web.

{{< understand-django-series-pt "auth" >}}

## Autenticação e Autorização

Nós precisamos de começar com alguns termos antes de iniciarmos o nosso estudo. Quando o nosso projeto interage com os utilizadores, existem dois aspetos primordiais, fortemente ligados aos utilizadores, que devemos ter em conta.

*Autenticação*: Quando um utilizador tenta provar que é quem diz ser, isto é autenticação. Normalmente, um utilizador autenticar-se-á no na nossa aplicação da Web através de um formulário de início de sessão ou utilizando um fornecedor social como Google para verificar a sua identidade.

> A autenticação só pode provar que {{< extlink "https://en.wikipedia.org/wiki/The_Important_Book" "somos nós" >}}.

*Autorização*: O que é que um utilizador pode fazer? A autorização responde a essa pergunta. Nós usamos a autorização para determinar as permissões ou grupos a que um utilizador pertence, de modo a podermos definir o que um utilizador pode fazer na aplicação da Web.

> A autorização determina o que podemos fazer.

O sistema de autenticação da Django cobre ambos os tópicos. Por vezes, a indústria de software encurtará a autenticação como "authn" e autorização como "authz", mas penso que esses rótulos são bastante disparatados e confusos. Eu chamarei os tópicos pelo seu nome completo e me referirei a todo o sistema da Django como "auth".

## Configuração

Se utilizámos o comando `startproject` para iniciar o nosso projeto, então, parabéns, já terminámos e podemos seguir!

As funcionalidades de autenticação na Django exigem um par de aplicações de Django embutidas e um par de classes de intermediários.

As aplicações de Django são:

* `django.contrib.auth` e
* `django.contrib.contenttypes` (da qual a aplicação `auth` depende)

As classes de intermediários são:

* `SessionMiddleware` para armazenar dados sobre um utilizador numa sessão
* `AuthenticationMiddleware` para associar utilizadores com as requisições

Os intermediários e as sessões são tópicos futuros, pelo que temos de considerá-los detalhes internos que podemos ignorar por agora.

A documentação da Django fornece contexto adicional sobre estes pré-requisitos, então precisamos consultar a {{< extlink "https://docs.djangoproject.com/en/4.1/topics/auth/#installation" "secção de instalação do tópico de autenticação" >}} por mais detalhes.

## Quem Autentica?

Se a nossa aplicação da Web terá algum nível de personalização para quem a usa, então precisamos de alguma maneira de rastrear a identidade.

No sistema de autenticação da Django, a identidade é rastreada com um modelo de base de dados `User`. Este modelo de base de dados armazena informações que nós provavelmente queremos associar com qualquer um que use a nossa aplicação da Web. O modelo inclui:

* campos de nome,
* endereço de correio eletrónico,
* campos de data e hora para quando um utilizador se junta ou inicia sessão na nossa aplicação,
* compos booleanos para algumas permissões gerais que são muito comummente necessárias,
* e dados da palavra-passe.

O modelo de base de dados `User` é um modelo extremamente importante em muitos sistemas. A não ser que estejamos criando uma aplicação da Web que seja inteiramente de dados públicos e que não tenha necessidade de ter em conta a identidade, então provavelmente utilizaremos fortemente o modelo `User`.

Mesmo que *não* esperemos que os visitantes da nossa aplicação se identifiquem de alguma maneira, provavelmente ainda nos beneficiaremos do modelo `User` porque este está integrado com a aplicação de administração da Django. Eu mencionei
{{< web >}}
no [Administrar Tudo]({{< ref "/understand-django/2020-08-26-administer-all-the-things.pt.md" >}})
{{< /web >}}
{{< book >}}
no capítulo Administrar Tudo
{{< /book >}}
que precisávamos dum utilizador com determinadas permissões para acessar ao administrador, mas não nos apercebemos dos detalhes do que isso significava.

O administrador só permitirá utilizadores com o atributo `is_staff` definido como `True`. `is_staff` é um dos campos booleanos que listei como incluídos na implementação padrão do modelo de base de dados `User`.

Agora entendemos que o modelo de base de dados `User` é um modelo muito importante numa aplicação de Django. No mínimo, o modelo é importante porque usamos o administrador da Django, mas também pode ser muito importante para as pessoas que chegam a nossa aplicação.

A seguir, analisaremos um pouco mais a autenticação e como esta funciona em conjunto com o modelo de base de dados `User`.

## Autenticação Com Palavras-Passe

Como muitas outras aplicações da Web que usamos, o sistema de autenticação embutido da Django autentica os utilizadores com as palavras-passe.

Quando um utilizador quer autenticar-se, o utilizador deve iniciar a sessão na aplicação. A Django inclui uma visão baseada em classe `LoginView` que pode manipular os passos apropriados. A `LoginView` é um visão de formulário que: 

* Recolhe o `username` e a `password` do utilizador
* Chama a função `django.contrib.auth.authenticate` com o `username` e a `password` para confirmar que o utilizador é quem diz ser
* Redireciona para um caminho definido como valor do parâmetro `next` na sequência de caracteres de consulta do localizador uniforme de recurso ou para `settings.LOGIN_REDIRECT_URL` se o parâmetro `next` não estiver definido
* Ou, se a autenticação falhar, apresenta novamente a página do formulário com as mensagens de erro apropriadas.

Como a função `authenticate` funciona? A função `authenticate` delega a responsabilidade de decidir se as credenciais do utilizador são válidas a um *backend de autenticação*.

Tal como vimos com os modelos de marcação e com as bases de dados, o sistema de autenticação tem backends substituíveis. Com diferentes opções de backend, podemos ter várias maneiras de autenticar. A função `authenticate` percorrerá todos os backends de autenticação definidos na definição da lista `AUTHENTICATION_BACKENDS`. Cada backend pode fazer uma de três coisas:

* Autenticar corretamente com o utilizador e retornar uma instância de `User`.
* Não autenticar e retornar `None`. Neste caso, o backend seguinte é tentado.
* Não autenticar e levantar uma exceção `PermissionDenied`. Neste caso, nenhum outro backend é tentado.

Poderíamos adicionar um backend a esta definição que permite que as pessoas se autentiquem com suas contas de media social ({{< extlink "https://django-allauth.readthedocs.io/en/latest/" "django-allauth" >}} é uma opção para fazer exatamente isto). Podemos estar num ambiente corporativo e precisar dum único início de sessão para nossa empresa. Existem opções de backend que também permitem isto.

Embora existam muitas opções, iremos concentrar-nos no backend embutido incluído com o sistema de autenticação. O backend padrão é chamado de `ModelBackend` e é está no módulo `django.contrib.auth.backends`.

O `ModelBackend` tem este nome porque usa o modelo de base de dados `User` para autenticar. Dado um `username` e `password` do utilizador, o backend compara os dados fornecidos com quaisquer registos de `User` existentes.

A função `authenticate` chama o *método* `authenticate` que existe no `ModelBackend`. O backend pesquisa por um registo de `User` baseado no `username` passado ao método pela função `authenticate`. Se o registo do utilizador existir, o backend chama `user.check_password(password)` onde `password` é a palavra-passe real fornecida pela pessoa que submeteu o pedido a `LoginView`.

A Django não armazena palavras-passe reais. Fazer isto seria uma grande fraqueza na abstração porque qualquer violação da base de dados faria com que todas as palavras-passe dos utilizadores fossem divulgadas. E isto não é nada bom. Neste caso, o campo `password` no modelo de base de dados `User` armazena um *baralho* da palavra-passe.

Talvez nunca tenhamos encontrado o baralhamento antes. Um baralho é um valor calculado que é gerado pela execução de dados de entrada através duma função especial. Os detalhes do cálculo são um tópico muito profundo, especialmente quando considera-se a segurança, mas o que é importante saber sobre baralhos é que não podemos reverter o cálculo.

Por outras palavras, se gerássemos um baralho a partir de `mysekretpassword`, não poderíamos pegar no valor do baralho e descobrir que a entrada original era `mysekretpassword`.

Por que isto é útil? Ao calcular os baralhos, a Django pode armazenar com segurança este valor calculado sem comprometer a palavra-passe dum utilizador. Quando um utilizador deseja autenticar-se numa aplicação, o utilizador submete uma palavra-passe, a Django calcula o baralho desse valor submetido e *compara-o com o baralho armazenado na base de dados*. Se os baralhos corresponderem-se, então a aplicação pode concluir que o utilizador enviou uma palavra-passe correta. Somente o baralho da palavra-passe corresponderia ao baralho armazenado no modelo de base de dados `User`.

O baralhamento é um assunto fascinante. Se quisermos estudar mais sobre os fundamentos de como a Django gere os baralhos, sugeriria a leitura da {{< extlink "https://docs.djangoproject.com/en/4.1/topics/auth/passwords/" "gestão de palavra-passe na documentação da Django" >}} para conhecermos os detalhes.

## Visões de Autenticação

É muita coisa a fazer por autenticação!

Será que a Django esperará que chamemos a função `authenticate` e conectemos todas as visões nós mesmos? Não!

Eu mencionei a `LoginView` anteriormente, mas esta não é a única visão que Django fornece para tornar a autenticação manipulável. Nós podemos adicionar o conjunto de visões com um único `include`:

```python
# project/urls.py

from django.urls import include, path

urlpatterns = [
    ...
    path(
        "accounts/",
        include("django.contrib.auth.urls")
    ),
]
```

Este conjunto inclui uma variedade de funcionalidades.

* Uma visão de início de sessão
* Uma visão de termino de sessão
* Visões para alterar uma palavra-passe
* Visões para redefinir uma palavra-passe

Se optarmos por adicionar este conjunto, o nosso trabalho é sobrepor os modelos de marcação embutidos para corresponderem ao estilo da nossa aplicação. Por exemplo, para personalizar a visão de termino de sessão, criaríamos um ficheiro chamado `registration/logged_out.html` no nosso diretório de modelos de marcação. A documentação de {{< extlink "https://docs.djangoproject.com/en/4.1/topics/auth/default/#all-authentication-views" "todas visões de autenticação" >}} fornece informações sobre cada visão e o nome de cada modelo de marcação a sobrepor. Notemos que devemos fornecer um modelo para a visão de início de sessão, uma vez que a abstração não fornece um modelo predefinido para esta visão.

Se tivermos necessidades mais complexas para a nossa aplicação da Web, podemos querer considerar algumas aplicações de Django externas que existem no ecossistema. Pessoalmente, gosto da {{< extlink "https://django-allauth.readthedocs.io/en/latest/" "django-allauth" >}}. O projeto é muito personalizável e fornece um caminho para adicionar autenticação social para se registar com a nossa plataforma de rede social de escolha. Eu também gosto da `django-allauth` porque esta inclui fluxos de registo que não temos que construir nós mesmos. A aplicação definitivamente vale a pena ser conferida.

Já vimos como a Django autentica os utilizadores duma aplicação da Web com o modelo de base de dados `User`, a função `authenticate`, e o backend de autenticação embutido, e o `ModelBackend`. Também vimos como a Django fornece visões para auxiliar com o início de sessão, termino de sessão, e gestão de palavras-passe.

Uma vez que um utilizador estiver autenticado, o que é que este utilizador pode fazer? Nós veremos isto a seguir quando explorarmos autorização na Django.

## O Que é Permitido?

### Autorização a partir dos Atributos do Utilizador

A Django tem várias maneiras de nos permitir controlar o que um utilizador pode fazer na nossa aplicação.

A maneira mais simples de verificar um utilizador é verificar se a aplicação identificou ou não o utilizador. Antes de um utilizador ser autenticado através do início de sessão, este utilizador é anónimo. De fato, o sistema de autenticação da Django tem uma classe especial para representar este tipo de utilizador anónimo. Seguindo o princípio da menor surpresa, a classe chama-se `AnonymousUser`.

O modelo de base de dados `User` inclui um atributo `is_authenticated`. Previsivelmente, os utilizadores que se autenticaram retornarão `True` para `is_authenticated` enquanto as instâncias de `AnonymousUser` retornarão `False` para o mesmo atributo.

A Django fornece um decorador `login_required` que pode usar esta informação de `is_authenticated`. O decorador bloqueará qualquer visão que precise que um utilizador esteja autenticado.

Este pode ser o nível apropriado de verificação de autorização se tivermos uma aplicação que restrinja quem tem permissão para iniciar sessão. Por exemplo, se estivermos executando uma aplicação “Software as a Service (SaaS)” que exige que os utilizadores paguem uma subscrição para usarem o produto, então podemos ter uma verificação de autorização suficiente ao verificar `is_authenticated`. Neste cenário, se a nossa aplicação apenas permitir que os utilizadores com uma subscrição ativa (ou uma subscrição de avaliação) iniciem sessão, `login_required` impedirá que qualquer utilizador não pagante use o nosso produto.

Existem outros valores booleanos no modelo de base de dados `User` que podemos usar para verificação de autorização:

* `is_staff` é um booleano para decidir se um utilizador é ou não um membro da equipa. Por padrão, este booleano é `False`. Só os utilizadores ao nível do pessoal estão autorizados a usarem a aplicação de administração da Django embutida. Também podemos usar o decorador `staff_member_required` se tivermos visões que só devem ser usadas por membros da nossa equipa com esta permissão.
* `is_superuser` é um indicador especial para indicar um utilizador que deve ter acesso a tudo. Este conceito de “superuser” é muito semelhante ao super utilizador que está presente nos sistemas de permissão de Linux. Não existe um decorador especial para este booleano, mas poderíamos usar o decorador `user_passes_test` se tivéssemos visões muito privadas que precisássemos proteger:

```python
from django.contrib.admin.views.decorators import (
    staff_member_required
)
from django.contrib.auth.decorators import (
    user_passes_test
)
from django.http import HttpResponse

@staff_member_required
def a_staff_view(request):
    return HttpResponse(
        "You are a user with staff level permission."
    )

def check_superuser(user):
    return user.is_superuser

@user_passes_test(check_superuser)
def special_view(request):
    return HttpResponse(
        "Super special response"
    )
```

O decorador `user_passes_test` comporta-se de maneira muito parecida com `login_required`, mas aceita um invocável que recebe um objeto de utilizador e retorna um booleano. Se o valor booleano for `True`, a requisição é permitida e o utilizador recebe a resposta. Se o valor booleano for `False`, o utilizador será redirecionado à página de início de sessão.

### Autorização de Permissões e Grupos

O primeiro conjunto de verificações que analisámos são os dados armazenados com um registo do modelo de base de dados `User`.  Embora isto funcione bem para alguns casos que se aplicam a muitas aplicações, o que dizer da autorização que depende do que a nossa aplicação faz?

A Django vem com um sistema de permissões flexível que permite à nossa aplicação controlar quem pode ver o quê. O sistema de permissões inclui algumas permissões convenientes criadas automaticamente, bem como a capacidade de criar permissões personalizadas para qualquer finalidade. Estes registos de permissões são instâncias do modelo de base de dados `Permission` de `django.contrib.auth.models`.

Sempre que criarmos um modelo de base de dados, a Django criará um conjunto adicional de permissões. Estas permissões auto-criadas mapeiam as operações Criar (Create), Ler (Read), Atualizar (Update), e Eliminar (Delete) (CRUD) que podemos esperar usar na administração da Django. Por exemplo, se tivermos uma aplicação `pizzas` e criarmos um modelo de base de dados `Topping`, a Django criaria as seguintes permissões:

* `pizzas.add_topping` para Criar (Create)
* `pizzas.view_topping` para Ler (Read)
* `pizzas.change_topping` para Atualizar (Update)
* `pizzas.delete_topping` para Eliminar (Delete)

Uma grande razão para criar estas permissões é para auxiliar o nosso desenvolvimento *e* adicionar controlo ao administrador da Django. Os utilizadores de nível de pessoal (isto é, `user.is_staff == True`) na nossa aplicação, não têm permissões para começar. Isto é um padrão seguro para que qualquer novo membro do pessoal não possa acessar a todos os dados do nosso sistema, e menos que lhes concedamos mais permissões à medida que ganhamos confiança neles.

Quando utilizadores do pessoal iniciarem a sessão no administrador da Django, inicialmente verão muito pouco. À medida que as permissões são concedidas à conta do utilizador, o administrador da Django revelará informação adicional correspondente às permissões selecionadas. Embora as permissões sejam frequentemente concedidas através da página de administração de `User`, podemos adicionar permissões a um utilizador por código. O modelo de base de dados `User` possui um campo `ManyToManyField` chamado `user_permissions` que associa instâncias de utilizadores a permissões particulares.

Continuando com o exemplo da aplicação de pizas, talvez trabalhemos com um chefe para a nossa aplicação de pizas. O nosso chefe pode precisar de controlar quaisquer novas coberturas que devam estar disponíveis aos clientes, mas provavelmente não queremos que o chefe possa eliminar encomendas do histórico da aplicação.

Para o chefe, concederíamos as permissões `pizzas.add_topping`, `pizzas.view_topping` e `pizzas.change_topping`, mas deixaríamos de fora `orders.delete_order`:

```python
from django.contrib.auth.models import (
    Permission, User
)
from django.contrib.contenttypes.models import (
    ContentType
)
from pizzas.models import Topping

content_type = ContentType.objects.get_for_model(
    Topping
)
permission = Permission.objects.get(
    content_type=content_type,
    codename="add_topping"
)
chef_id = 42
chef = User.objects.get(id=42)
chef.user_permissions.add(permission)
```

Nós não cobrimos a aplicação `contenttypes`, então este código pode parecer incomum para nós, mas o sistema de autenticação usa tipos de conteúdo como uma maneira de referenciar modelos de base de dados genericamente ao lidar com permissões. Podemos saber mais sobre os tipos de conteúdo e os seus usos na documentação da {{< extlink "https://docs.djangoproject.com/en/4.1/ref/contrib/contenttypes/" "abstração contenttypes" >}}. O ponto importante a ser observado a partir do exemplo é que as permissões se comportam como qualquer outro modelo de base de dados da Django.

Adicionar permissões a utilizadores individuais é uma boa funcionalidade para um equipa pequena, mas se a nossa equipa crescer, pode tornar-se num pesadelo.

Suponhamos que a nossa aplicação tem enorme sucesso e que precisamos de controlar uma grande equipa de apoio para ajudar a resolver os problemas dos clientes. Se a nossa equipa de apoio necessitar de visualizar determinados modelos de base de dados no nosso sistema, seria uma grande chatice se tivéssemos de gerir isto por membro do pessoal.

A Django consegue criar grupos para aliviar este problema. O modelo de base de dados `Group` é a intersecção entre um conjunto de permissões e um conjunto de utilizadores. Assim, podemos criar um grupo como "Support Team,", atribuir todas as permissões que esta equipa deve ter e incluir todo o nosso pessoal de apoio nesta equipa. Agora, sempre que os membros da equipa de apoio necessitarem duma nova permissão, esta pode ser adicionada imediatamente ao grupo.

Os grupos de um utilizador são controlados com um outro campo `ManyToManyField` chamado `groups`:

```python
from django.contrib.auth.models import (
    Group, User
)

support_team = Group.objects.get(
    name="Support Team"
)
support_sally = User.objects.get(
    username="sally"
)
support_sally.groups.add(support_team)
```

Para além das permissões embutidas que a Django cria e do sistema de gestão de grupos, podemos criar permissões adicionais para os nossos próprios fins.

Daremos permissão ao nosso chefe para cozer pizas na nossa aplicação imaginária:

```python
from django.contrib.auth.models import (
    Permission, User
)
from django.contrib.contenttypes.models import (
    ContentType
)
from pizzas.models import Pizza

content_type = ContentType.objects.get_for_model(
    Pizza
)
permission = Permission.objects.create(
    codename="can_bake",
    name="Can Bake Pizza",
    content_type=content_type,
)
chef_id = 42
chef = User.objects.get(id=42)
chef.user_permissions.add(permission)
```

Para verificar a permissão no nosso código, podemos usar o método `has_perm` no modelo de base de dados `User`. `has_perm` espera um rótulo de aplicação e o nome de código da permissão unidos por um ponto:

```python
>>> chef = User.objects.get(id=42)
>>> chef.has_perm('pizzas.can_bake')
True
```

Podemos também usar um decorador numa visão para verificar uma permissão também. O decorador verificará a `request.user` para a permissão correta:

```python
# pizzas/views.py

from django.contrib.auth.decorators import permission_required

@permission_required('pizzas.can_bake')
def bake_pizza(request):
    # Hora de cozer a piza
    # se lhe for permitido.
    ...
```

## Trabalhar com Utilizadores Nas Visões e Modelos de Marcação

Já falámos sobre como autenticar utilizadores e como verificar a sua autorização. Como *interagimos* com os utilizadores no nosso código de aplicação?

A primeira maneira é dentro das visões. Parte da configuração do sistema de autenticação é incluir o `AuthenticationMiddleware` em `django.contrib.auth.middleware`.

Este intermediário tem uma função no processamento de requisições: adicionar um atributo `user` ao `request` que a visão receberá. Este intermediário dá-nos um acesso muito limpo e conveniente ao registo do utilizador:

```python
# application/views.py

from django.http import HttpResponse

def my_view(request):
    if request.user.is_authenticated:
        return HttpResponse(
            'You are logged in.'
        )
    else:
        return HttpResponse(
            'Hello guest!'
        )
```

O `AuthenticationMiddleware` é o que possibilita os decoradores
{{< web >}}
que descrevi neste artigo
{{< /web >}}
{{< book >}}
que descrevi neste capítulo
{{< /book >}}
(isto é, `login_required`, `user_passes_test`, e `permission_required`) funcionarem. Cada um dos decoradores encontra o registo `user` como um atributo anexado ao `request`.

E quanto aos modelos de marcação? Se tivéssemos de adicionar um utilizador ao contexto duma visão para cada visão, isto seria aborrecido.

Felizmente, existe um processador de contexto chamado `auth` que nos permite evitar esta dor (o processador está em `django.contrib.auth.context_processors`). O processador de contexto adicionará um `user` ao contexto de cada visão ao processar uma requisição.

É necessário relembrar que um processador de contexto é uma função que recebe um objeto `request` e retorna um dicionário que será combinado no contexto. Sabendo isto, podemos adivinhar como funciona este processador de contexto?

Se nossa resposta for `AuthenticationMiddleware`, recebemos um biscoito (cookie)! 🍪 Uma vez que o intermediário adiciona o `user` ao `request`, o processador de contexto tem a tarefa muito simples de criar um dicionário como `{'user': request.user}`. Há um pouco mais sobre a implementação real, e podemos consultar o {{< extlink "https://github.com/django/django/blob/4.1/django/contrib/auth/context_processors.py#L49" "código-fonte da Django" >}} se quisermos ver estes detalhes.

O que isto parece na prática? Na verdade, já vimos isto! Um dos exemplos da explicação dos modelos de marcação utilizou a variável de contexto `user`. Eis o exemplo novamente para não termos de retroceder:

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

Se decidirmos usar as permissões da Django, também podemos aproveitar a variável de contexto `perms` nos nossos modelos de marcação. Esta variável é também fornecida pelo processador de contexto `auth` e dá ao nosso modelo de marcação acesso às permissões do `user` concisamente. A {{< extlink "https://docs.djangoproject.com/en/4.1/topics/auth/default/#permissions" "documentação da Django" >}} inclui alguns bons exemplos de como a variável `perms` pode ser usada.

Já vimos como a Django influencia o intermediário de autenticação para tornar os utilizadores facilmente acessíveis às nossas visões e modelos de marcação.

## Sumário

{{< web >}}
Neste artigo,
{{< /web >}}
{{< book >}}
Neste capítulo,
{{< /book >}}
entramos no sistema de autenticação de utilizador embutido da Django.

Estudamos sobre:

* Como a autenticação é configurada
* Como a autenticação funciona
* O que o modelo de base de dados `User` é
* Visões embutidas da Django para criação de um sistema de início de sessão
* Quais níveis de autorização estão disponíveis
* Como acessar os utilizadores nas visões e modelos de marcação

{{< web >}}
Da próxima vez, estudaremos o intermediário
{{< /web >}}
{{< book >}}
No próximo capítulo, estudaremos o intermediário
{{< /book >}}
na Django. Conforme o nome implica, intermediário é algum código que existe no "meio" do processo da requisição e da resposta. Estudaremos sobre:

* O modelo mental para consideração do intermediário
* Como escrever o nosso próprio intermediário
* Algumas das classes de intermediário que vêm com a Django.

{{< web >}}
Se gostarias de seguir juntamente com a série, sinta-se a vontade para inscrever-se no meu boletim informativo onde anuncio todos os meus novos conteúdos. Se tiveres outras questões, podes contactar-me na X onde sou o {{< extlink "https://x.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;

A tradução deste artigo para o português é cortesia de Nazaré Da Piedade.
