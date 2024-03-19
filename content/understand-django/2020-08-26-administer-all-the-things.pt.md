---
title: "Administrador de Todas as Coisas"
description: >-
    Este artigo olhará em como os responsáveis duma aplicação podem gerir os seus dados através das ferramentas administrativas embutidas da Django. Nós veremos como construir páginas de administração e personalizar as ferramentas de administração para ajudar as equipas a navegarem as suas aplicações.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - admin
series: "Understand Django"

---

{{< web >}}
No anterior artigo da [Entendendo a Django]({{< ref "/understand-django/2020-06-25-store-data-with-models.pt.md" >}}), usamos os modelos de base de dados para ver como a Django armazena os dados numa base de dados relacional.
{{< /web >}}
Nós cobrimos todas as ferramentas para trazer os nossos dados à vida na nossa aplicação.
{{< web >}}
Neste artigo,
{{< /web >}}
{{< book >}}
Neste capítulo,
{{< /book >}}
nos concentraremos nas ferramentas embutidas que a Django fornece para ajudar-nos a gerir aqueles dados.

{{< understand-django-series-pt "admin" >}}

## O Que É A Administração da Django?

Quando executamos uma aplicação, encontraremos dados que precisam de atenção especial. Talvez estejamos a criar um blogue e precisamos de criar e editar rótulos ou categorias. Talvez temos uma loja digital e precisamos de administrar o nosso inventário. O que quer que estejamos a construir, provavelmente teremos de gerir *algo*.

Como podemos gerir este dado?:

* Se formos programadores, provavelmente podemos registar no nosso servidor, disparar uma concha de gestão da Django, e trabalhar com o dado diretamente usando a Python.
* Se não formos programadores, bem, eu acho que estamos sem sorte! **Não, isto não é verdade!**

A Django inclui uma interface administrativa que pode ajudar os programadores e não programadores da mesma maneira. Esta interface administrativa é normalmente chamada a administração da Django.

Tal como muitas outras extensões no ecossistema a Django, a página de administração é uma aplicação de Django. A página é tão comummente usada que é pré-configurada quando executamos o comando `startproject`.

Antes de prosseguirmos, gostaria primeiro de salientar um problema de segurança. Quando usamos `startproject`, a Django colocará a página de administração em `/admin/` por padrão. **Mude isto**. O modelo de projeto de ponto de partida configura convenientemente a página de administração por nós, mas esta URL padrão torna fácil para os {{< extlink "https://en.wikipedia.org/wiki/Script_kiddie" "os aspirantes a piratas informáticos" >}} tentarem atacar o nosso local de administração para conseguirem acesso. Colocar a nossa página de administração numa URL diferente *não protegerá* completamente a nossa aplicação (porque nunca devemos depender da "segurança através da obscuridade"), mas ajudará a evitar uma grande quantidade de ataques automatizados.

A administração da Django dá-nos uma habilidade rápida de interagir com os nossos modelos de base de dados. Como veremos brevemente, podemos registar um modelo de base de dados com a página de administração. Assim que o modelo de base de dados estiver registado, podemos usar a interface da aplicação para realizar operações CRUD sobre os dados.

CRUD é um acrónimo que descreve as funções primárias de muitas aplicações da Web. O acrónimo significa:

* **Create (Criar)** - Uma aplicação da Web pode criar dados (isto é, inserir dados numa base de dados)
* **Read (Ler)** - Os utilizadores podem ver os dados
* **Update (Atualizar)** - Os dados podem ser atualizados pelos utilizadores
* **Delete (Eliminar)** - Um utilizador pode eliminar os dados do sistema

Se pensarmos sobre as ações que podemos tomar numa aplicação da Web, a maioria das ações caiem numa destas quatro categorias.

A aplicação de administração fornece ferramentas para realizar todas estas operações. Existem algumas páginas principais que podemos navegar quando trabalhamos numa aplicação de administração da Django que dirigem onde as operações CRUD acontecem. Estas páginas estão disponíveis à nós com muito pouco esforço da nossa parte à parte do processo de registo que veremos na próxima seção:

1. Página do índice da administração - Está página mostra todos os modelos de base de dados, agrupados pela aplicação da Django de onde originaram-se, que estão registadas com a administração.
2. Página da lista - A página de lista mostra as linhas de dados dum modelo de base de dados (isto é, uma tabela da base de dados). A parte desta página, um administrador pode realizar ações sobre vários registos da base de dados como eliminar um conjunto de registos numa única operação.
3. Adicionar página de modelo de base de dados - A administração fornece uma página onde as novas instâncias de modelo de base de dados podem ser criados usando formulários gerados automaticamente baseados nos campos do modelo de base de dados.
4. Página de mudança de modelo de base de dados - A página de mudança permite-nos atualizar uma instância de modelo de base de dados existente (isto é, uma linha da tabele da base de dados). A partir desta página, também podemos eliminar uma instância de modelo de base de dados.

Se inspecionarmos este pequeno conjunto de páginas, notaremos que todas as partes do acrónimo CRUD podem ocorrer nesta aplicação de administração. O poder de criar e destruir está nas nossas mãos. 😈

Agora que entendemos o que está na aplicação de administração, vamos focar-nos em como adicionar os nossos modelos de base de dados à administração.

## Registar Um Modelo de Base de Dados Com A Administração

Para fazer a aplicação de administração mostrar os nossos modelos de base de dados, precisamos de atualizar o `admin.py`. Numa nova aplicação criada com `startapp`, encontraremos este ficheiro `admin.py` que está em grande parte vazio. Nós precisamos fornecer um pouco de cola para que a administração reconhecer um modelo de base de dados.

A aplicação de administração espera uma classe `ModelAdmin` para todos os modelos de base de dados que queremos ver exibido dentro da aplicação.

Vamos considerar uma modelagem rudimentar dum livro:

```python
# application/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(
        max_length=256
    )
    author = models.CharField(
        max_length=256
    )
```

Agora podemos criar uma classe `ModelAdmin` para o modelo de base de dados `Book`:

```python
# application/admin.py
from django.contrib import admin

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass
```

Existem alguns items importantes à observar com este ficheiro `admin.py`:

1. O `BookAdmin` é uma subclasse de `admin.ModelAdmin`.
2. O `BookAdmin` é registado com a aplicação de administração usando o decorador `admin.register`.

Nós também podemos registar uma classe de administração chamando `register` depois da classe se não quisermos usar um decorador:

```python
# application/admin.py
from django.contrib import admin

from .models import Book

class BookAdmin(admin.ModelAdmin):
    pass

admin.site.register(Book, BookAdmin)
```

Agora que temos um modelo de base de dados registado com a aplicação de administração, como o visualizamos? Disparamos o nosso servidor de desenvolvimento de confiança com `runserver` e visitamos a URL que costumava ser `/admin/` (porque mudamos para algo diferente de `/admin/`, certo? Certo!?).

Nesta página, nos depararemos com uma tela de início de sessão. Nós ainda não trabalhamos através do sistema de autenticação, mas, por agora, podemos entender que apenas contas de utilizador que têm um permissão de nível de pessoal pode iniciar a sessão.

A Django fornece um comando que nos permitirá criar uma conta de utilizador com a permissão de nível de pessoal e todas outras permissões. Tal como os sistemas operativos baseados no Linux, a conta de utilizador com todas as permissões é chamada de um super utilizador. Nós podemos criar uma conta de super utilizador com o comando `createsuperuser`:

```bash
$ ./manage.py createsuperuser
Username: matt
Email address: matt@somewhere.com
Password:
Password (again):
Superuser created successfully.
```

Com uma conta de super utilizador disponível, estamos prontos para iniciar a sessão na aplicação de administração. Uma vez que usaremos uma conta de super utilizador, teremos a permissão de ver todos os modelos de base de dados que estão registados com a aplicação de administração.

Assim que tivermos iniciado a sessão, podemos visualizar a página de administração do modelo de base de dados `Book`. Podemos vasculhar! Criar um livro com o botão "Add Book". Visualizar a página de lista. Editar o livro. Eliminar o livro. Nós podemos ver isto com uma quantidade muito pequena de trabalho da nossa parte, a Django dá-nos uma interface de CRUD completa para interagirmos com o nosso modelo de base de dados.

Nós adicionamos o `ModelAdmin` mais simples possível. O corpo da classe era um `pass` ao invés de quaisquer atributos. A Django dá-nos uma tonelada de opções para permitir-nos controlar como as nossas páginas de administração para `Book` comportar-se-ão. Vamos avançar numa digressão de alguns atributos de administração comummente usados.

## Personalizando A Nossa Administração

Tal como muitas das outras partes da Django, a abstração usa atributos de nível de classe para definir o comportamento duma classe. Diferente dos formulários e modelos de base de dados onde os atributos de nível de classe são maioritariamente campos que estamos a definir para nós mesmos, as classes de `ModelAdmin` fornecem valores para os atributos que são bem definidos na documentação. Estes atributos agem como gatilhos que permitem-nos personalizar o comportamento das nossas páginas de administração.

Tornar páginas de administração efetivas é primariamente sobre usar estes atributos para que a classe `ModelAdmin` faça o que queremos. Como tal, dominar a aplicação de administração da Django é todo sobre dominar as opções da `ModelAdmin` que são listadas {{< extlink "https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#modeladmin-options" "na documentação" >}}. Esta lista é longa, mas não precisamos estar desanimados! Eu penso que podemos obter 80% do valor fora da administração da Django conhecendo apenas um punhado de opções.

Quando vasculhamos sobre as páginas do `Book`, provavelmente notamos que a listagem dos livros é muito branda. A lista padrão parece-se com uma lista de ligações que mostra `Book object (#)`. Nós podemos mudar a aparência e utilidade desta página com alguns definições diferentes.

Vamos começar com `list_display`. Este atributo da `ModelAdmin` controla quais campos aparecerão na página de lista. Com o nosso exemplo de modelo de base de dados de livro, poderíamos adicionar o título à página:

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
```

A Django transformará tudo aquilo que estiver listado numa ligação que um utilizador pode clicar para visualizar a página de detalhe da administração para um registo de modelo de base de dados. Neste exemplo, estávamos a usar o campo `id` como ligação, mas poderíamos ter usado uma única tupla de elemento de `('title',)` para fazer a página mostrar apenas os títulos com os títulos sendo as ligações.

Algumas vezes teremos um tipo de modelo de base de dados onde apenas queremos ver um subconjunto de registos. Suponhamos que o modelo de base de dados `Book` tem um campo de categoria:

```python
# application/models.py

class Book(models.Model):
    class Category(
        models.IntegerChoices
    ):
        SCI_FI = 1
        FANTASY = 2
        MYSTERY = 3
        NON_FICTION = 4

    # ... `title` e `author` de antes

    category = models.IntegerField(
        choices=Category.choices,
        default=Category.SCI_FI
    )
```

Com o uso do atributo `list_filter`, podemos dar a página de lista da administração a habilidade de filtrar à categoria que queremos:

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('category',)
```

A opção colocará uma barra lateral no lado direito da página de administração. Nesta barra lateral, veríamos as categorias que incluímos na classe de escolhas da `Category`. Se clicarmos sobre a ligação "Fantasy", então o nosso navegador navegará para `/admin/application/book/?category__exact=2` e apenas exibirá as linhas da base de dados que tiverem uma categoria correspondente.

Este não é o único tipo de filtragem que a administração pode fazer. Nós também podemos filtrar o tempo com o campo `data_hierarchy`. A seguir, vamos dar ao modelo de base de dados um `published_date`:

```python
# application/models.py

class Book(models.Model):
    # ... title, author, category

    published_date = models.DateField(
        default=datetime.date.today
    )
```

Nós também podemos mudar a `ModelAdmin` para usar o novo campo:

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
```

Com a inclusão do atributo `date_hierarchy`, a página de lista conterá alguns novos elementos de interface de utilizador. Sobre o cimo da página estarão seletores para ajudar a filtrar para o limite de tempo correto. Isto é uma maneira muito útil examinar cuidadosamente a nossa base de dados.

Nós podemos continuar a avançar. Talvez queiramos que todos os livros sejam organizados pelo seus títulos. Mesmo se o atributo `ordering` não estiver definido nas opções de meta do modelo de base de dados, a `ModelAdmin` tem seu próprio atributo `ordering`.

*O que é "meta"?* À parte dos campos, um modelo de base de dados da Django pode definir informação adicional sobre como manipular os dados. Estas opções adicionais são os atributos de "meta" do modelo de base de dados. Um modelo de base de dados da Django adiciona informação de meta incluindo uma classe `Meta` encaixada no modelo de base de dados. Consulte as {{< extlink "https://docs.djangoproject.com/en/4.1/ref/models/options/" "opções de Meta do Modelo de Base de Dados" >}} para ver quais outras funcionalidades estão disponíveis para personalizar o comportamento do modelo de base de dados:

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
```

Com esta definição, todos os livros na página serão ordenados pelo título. O atributo `ordering` adicionará uma clausula `ORDER BY` apropriada à consulta de base de dados através da `QuerySet` do mapeador relacional de objeto gerado pela administração.

A opção da página de lista conveniente final que queremos destacar é a opção `search_fields`:

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
    search_fields = ("author",)
```

Com esta opção, esta página de lista adicionará um barra de pesquisa no cimo da página. Neste exemplo, adicionamos a habilidade de pesquisar baseado no autor do livro.

Quando pesquisamos, a nossa URL resultante poderia parecer-se com `/admin/application/book/?q=tolkien`. A Django fará uma pesquisa insensível a caixa sobre o campo. A `QuerySet` seria algo como:

```python
search_results = Book.objects.filter(
    author__icontains="tolkien"
)
```

Os resultados não competiriam bem comparados à um motor de pesquisa dedicado, mas obter uma funcionalidade de pesquisa decente para uma única linha de código é fantástico!

A `ModelAdmin` também inclui algumas definições úteis para modificar o comportamento da página de detalhe dos registos de base de dados em especial.

Por exemplo, vamos assumir que o modelo de base de dados `Book` tem uma `ForeignKey` para rastrear um editor:

```python
# application/models.py
from django.contrib.auth.models import User

class Book(models.Model):
    # ... `title`, `author`, `category`
    # `published_date` de antes

    editor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
```

Na página de administração para um livro particular, o campo `editor` será uma lista pendente por padrão. Este campo incluirá cada registo de `User` na nossa aplicação. Se tivermos um aplicação popular com milhares ou milhões de utilizadores, a página seria esmagada sob o peso de carregar todos estes registos de utilizador nesta lista pendente.

No lugar de ter uma página inútil que não podemos carregar, podemos usar `raw_id_fields`:

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
    raw_id_fields = ("editor",)
    search_fields = ("author",)
```

Com o uso de `raw_id_fields`, a administração muda de usar uma lista pendente para usar uma entrada de texto básica que exibirá a chave estrangeira do registo do utilizador. Ver um número de chave estrangeira é visualmente menos útil do que ver nome exato selecionado numa lista pendente, mas a opção `raw_id_fields` adiciona duas funcionalidades para aliviar isto:

1. Um ícone de pesquisa é apresentado. Se os utilizadores clicarem sobre o ícone, uma janela sobreposta aparece para permitir o utilizador pesquisar por um registo numa interface de seleção dedicado.
2. Se o registo já tem uma chave estrangeira para o campo, então a representação de sequência de caracteres do registo exibir-se-á próximo ao ícone.

Uma outra opção que pode ser útil é a opção `prepopulated_fields`. De volta a nossa discussão de URLs, falamos sobre os campos de lesma. As lesmas são muitas vezes usadas para tornar as URLs agradáveis para as páginas de detalhe exibirem uma instância de modelo de base de dados em especial:

```python
# application/models.py

class Book(models.Model):
    # ... `title`, `author`, `category`
    # `published_date`, `editor` de antes

    slug = models.SlugField()
```

Qual é o benefício do `prepopulated_fields`? Com o uso desta opção, podemos instruir a aplicação de administração à povoar o campo `slug` baseado no `title` do livro. Eis a atualização à `ModelAdmin`:

```python
# application/admin.py

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("editor",)
    search_fields = ("author",)
```

Agora quando queremos adicionar um novo livro na administração, a Django usará algum JavaScript para atualizar o campo de lesma dinamicamente a medida que digitamos o título!

Para este ponto, cada atributo que adicionamos à administração é uma configuração estática. O que nós fazemos se quisermos variar como as páginas de administração comportam-se baseado em algo dinâmico?

Felizmente, a equipa da Django também pensou nisto. Todas as opções que examinamos têm um método equivalente que podemos sobrepor que está prefixado com `get_`. Por exemplo, se quisermos controlar quais campos os utilizadores vêm na página de lista baseado em quem são, implementaríamos `get_list_display`. Neste método, retornaríamos uma tupla baseada no nível de acesso do utilizador:

```python
# application/admin.py
from django.contrib import admin

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    ...

    def get_list_display(self, request):
        if request.user.is_superuser:
            return (
                'id',
                'title',
                'author',
                'category',
            )

        return ('id', 'title')
```

Um atributo final à considerar é chamado de `inlines`. Não lidamos com esta opção muitas vezes, mas é uma maneira conveniente de ver *outros* modelos de base de dados que estão relacionados à um modelo de base de dados em especial.

Suponhamos que a nossa aplicação de amostra tem criticas para os livros. Nós poderíamos adicionar um modelo de base de dados como:

```python
# application/models.py

class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    comment = models.TextField()
```

Para mostrar os outros modelos de base de dados na página de detalhe, precisamos criar uma classe em linha e incluí-la com a `ModelAdmin`. O resultado parece-se com:

```python
# application/admin.py
from django.contrib import admin

from .models import Book, Review

class ReviewInline(admin.TabularInline):
    model = Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    inlines = [ReviewInline]
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
    raw_id_fields = ("editor",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("author",)
```

Com a adição da classe em linha à lista de `inlines`, a página de detalhe mostrará quaisquer criticas que estiverem associadas com um livro. Adicionalmente, poderíamos criar novas criticas a partir da página de detalhe uma vez que a administração incluirá alguns formulários em branco por padrão.

Nós cobrimos muitas opções da classe `ModelAdmin` que podemos usar para personalizar a nossa experiência de administração com funções comuns que muitas ferramentas de administração exigem. **E as funções *incomuns*?** Para personalização adicional, podemos usar as ações de administração.

## Tomando Providências Na Administração

Quando queremos realizar trabalho relacionado à registos específicos na nossa base de dados, a Django fornece algumas técnicas para personalizar a nossa aplicação e fornecer estas capacidades. Estas personalizações são chamadas de *ações* e aparecem na página de lista acima da lista de registos.

Na aplicação de administração padrão, existe uma ação que permite os administradores eliminar registos. Se selecionarmos algumas linhas com as caixas de confirmação à esquerda, selecionamos "Delete selected \<object type\>", depois clicamos em "Go", seremos presenteados com uma página que pedi a confirmação sobre eliminação das linhas que escolhemos.

O mesmo tipo de fluxo poderia ser aplicado para quaisquer ações que quisermos realizar sobre os registos de base de dados. Nós podemos fazer isto adicionando um método na nossa `ModelAdmin`.

O método deve seguir esta interface:

```python
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    actions = ['do_some_action']

    def do_some_action(
            self,
            request: HttpRequest,
            queryset: QuerySet
        ) -> Optional[HttpResponse]:
        # Fazer o trabalho neste bloco.
        ...
```

O conjunto de consulta representará o conjunto de registos de modelo de base de dados que utilizador selecionou. Se o método retornar `None`, então o utilizador será retornado à mesma página de administração. Se o método retornar um `HttpResponse`, então o utilizador verá esta resposta (que é o que acontece com a página de confirmação da eliminação da ação de eliminação). Tudo aquilo que fizermos entre o método sendo chamado e o método retornado é responsabilidade nossa.

Possivelmente a nossa aplicação de livro de amostra poderia definir um livro para estrear na aplicação como um novo importante título disponível. Neste cenário hipotético, podemos ter código que desfaz a definição de qualquer livro de estreia mais antigo ou envia correios-eletrónicos às pessoas que expressaram interesse quando as novas estreias forem anunciada.

Para este cenário, poderíamos adicionar uma ação que faria estas coisas:

```python
# application/admin.py

def update_premiere(book):
    """Pretend to update the book to be a premiere.

    This function is to make the demo clear.
    In a real application, this could be a manager method instead
    which would update the book and trigger the email notifications
    (e.g., `Book.objects.update_premiere(book)`).
    """
    print(f"Update {book.title} state to change premiere books.")
    print("Call some background task to notify interested users via email.")

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    actions = ["set_premiere"]
    date_hierarchy = "published_date"
    inlines = [ReviewInline]
    list_display = ("id", "title")
    list_filter = ("category",)
    ordering = ("title",)
    raw_id_fields = ("editor",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("author",)

    def set_premiere(
        self,
        request,
        queryset
    ):
        if len(queryset) == 1:
            book = queryset[0]
            update_premiere(book)
```

A Django usará o nome do método para definir o rótulo para a lista pendente na página de lista. Neste caso, o rótulo da ação será "Set premiere".

Nós fomos capazes de estender a administração e prender na interface do utilizador da página definindo um método e declarando-o como uma ação. Isto é um sistema poderoso para dar aos administradores controlo e permiti-los operar de maneiras personalizadas sobre os dados nas suas aplicações.

## Sumário

{{< web >}}
Neste artigo,
{{< /web >}}
{{< book >}}
Neste capítulo,
{{< /book >}}
vimos a aplicação do administrador da Django embutida. Esta poderosa extensão dá-nos a habilidade de criar, visualizar, editar, e eliminar as linhas das tabelas da base de dados associada com os modelos de base de dados da nossa aplicação.

Nós cobrimos:


* O que a aplicação de administração da Django é e como a configurar
* Como fazer os nossos modelos de base de dados aparecerem na administração
* Como personalizar as nossas páginas de administração rapidamente com opções fornecidas pela classe `ModelAdmin`
* Como criar ações adicionais que permitem-nos realizar trabalho sobre os nossos registos de modelo de base de dados

{{< web >}}
Para a próxima cobriremos
{{< /web >}}
{{< book >}}
No próximo capítulo cobriremos
{{< /book >}}
a anatomia duma aplicação de Django. Um projeto de Django é composto de várias aplicações. Nós exploraremos:

* A estrutura convencional duma aplicação de Django
* Como a Django identifica e carrega as aplicações
* Porquê as aplicações são cruciais para o ecossistema da Django

{{< web >}}
Se gostarias de seguir juntamente com a série, sinta-se a vontade para inscrever-se no meu boletim informativo onde anuncio todos os meus novos conteúdos. Se tiveres outras questões, podes contactar-me na Twitter onde sou o {{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;

A tradução deste artigo para o português é cortesia de Nazaré Da Piedade.
