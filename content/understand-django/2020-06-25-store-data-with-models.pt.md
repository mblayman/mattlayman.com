---
title: "Armazenar Dados com Modelos de Base de Dados"
description: >-
    Neste artigo, veremos como armazenar dados numa base de dados com os modelos de base de dados da Django. O artigo cobre como os modelos de base de dados atuam como uma interface para permitir a nossa aplicação armazenar e buscar os dados.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - models

---

{{< web >}}
No artigo de [Entender a Django]({{< ref "/understand-django/2020-05-05-user-interaction-forms.pt.md" >}}) anterior, encontrámos os formulários e como os formulários permitem a nossa aplicação receber dados dos utilizadores que usam a nossa aplicação. Neste artigo, veremos como pegar nestes dados
{{< /web >}}
{{< book >}}
Neste capítulo, veremos como pegar nestes dados
{{< /book >}}
e armazená-los numa base de dados para que a nossa aplicação passa estes dados ou exibi-los depois.

{{< understand-django-series-pt "models" >}}

## Configuração

Vamos compreender onde os nossos dados vão antes de mergulhar em como trabalhar com eles. A Django usa as bases de dados para armazenar os dados. Mais especificamente, a Django usa as bases de dados *relacionais*. A cobertura de bases de dados *relacionais* tornaria o tópico gigantesco então termos de nos decidir por uma versão *muito* resumida.

Uma base de dados relacional é como uma coleção de folhas de cálculo. Cada folha de cálculo é na realidade chamada duma tabela. Uma tabela tem um conjunto de colunas para rastrear diferentes pedaços de dados. Cada linha na tabela representaria um grupo relacionado. Por exemplo, suponhamos que temos uma tabela de empregado para uma empresa. As colunas para uma tabela de empregado podem incluir um primeiro nome, último nome e o título profissional. Cada linha representaria um empregado individual:

```text
First name | Last name | Job title
-----------|-----------|----------
John       | Smith     | Software Engineer
-----------|-----------|----------
Peggy      | Jones     | Software Engineer
```

A parte "relacional" duma base de dados relacional entra em ação porque várias tabelas podem *relacionarem-se* umas às outras. No nosso exemplo de empresa, a base de dados poderia ter uma tabela de números de telefones que a usa para armazenar o número de telefone de cada empregado.

Porquê não colocar o número de telefone na mesma tabela? Bem, o que aconteceria se uma empresa precisasse dum número telefone pessoal e número de telefone caseiro? Ter de separar as tabelas, poderíamos suportar rastrear vários tipos de número de telefone. Existe muito poder que vem da capacidade de separar estes diferentes tipos de dados. Veremos o poder das bases de dados relacionais a medida que explorarmos como a Django expõe este poder.

A Django usa uma base de dados relacional então a abstração deve ter alguma habilidade de definir esta base de dados. A configuração da base de dados está na definição `DATABASES` no nosso ficheiro `settings.py`. Depois de executar `startproject`, encontraremos:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

Como vimos com o sistema de modelos de marcação, a Django suporta várias bases de dados. Ao contrário do sistema de modelos de marcação, as definições da base de dados refere-se à cada backend suportado como um "motor" ao invés de "backend". O motor de base de dados padrão desde o `startproject` é definido para usar {{< extlink "https://www.sqlite.org/index.html" "SQLite" >}}. SQLite é uma excelente escolha inicial porque serve uma base de dados relacional inteira num único ficheiro o qual as definições nomeiam de `db.sqlite3`. Esta escolha de motor de fato baixa a barreira para começar com a Django visto que novos programadores de Django não têm de instalar ferramentas adicionais para experimentar a Django.

SQLite é uma pequena base de dados fantástica e provavelmente a base de dados mais usada no mundo. A base de dados existe em todos os telemóveis inteligentes que possamos imaginar. Apesar da SQLite ser fantástica, não é uma boa opção para muitos cenários onde queremos usar a Django. Para começar, a base de dados apenas permitem que um utilizador escreva nela de cada vez. Isto é um grande problema se estivermos a planear criar uma aplicação que sirva muitas pessoas em simultâneo.

Uma vez que a SQLite não é a melhor opção para uma aplicação na Web, provavelmente teremos de mudar para uma base de dados relacional diferente. Eu recomendo {{< extlink "https://www.postgresql.org/" "PostgreSQL" >}}. Postgres (como frequentemente é "abreviada") é a base de dados mais popular de código-aberto que é muito bem suportada. Combinada com o {{< extlink "https://www.psycopg.org/docs/" "psycopg2" >}} como motor da Django, descobriremos que muitos lugares que podem hospedar a nossa aplicação de Django trabalharão bem com a Postgres.

Nós podemos explorar mais configurações de base de dados
{{< web >}}
num futuro artigo
{{< /web >}}
{{< book >}}
num futuro capítulo
{{< /book >}}
sobre implementação em produção. Por agora, enquanto aprendemos, SQLite é perfeitamente adequada para a tarefa.

## Modelando os Nossos Dados

Agora que temos uma ideia de onde a Django armazenará os nossos dados, vamos focar em *como* a Django armazenará os dados.

A Django representa os dados para uma base de dados em classes da Python chamadas de **modelos** de base de dados. Os modelos de base de dados da Django são semelhantes às classes de formulário que vimos
{{< web >}}
no artigo anterior.
{{< /web >}}
{{< book >}}
no capítulo anterior.
{{< /book >}}
Um modelo de base de dados da Django declara os dados que queremos armazenar na base de dados como atributos de nível de classe, tal como uma classe de formulário. De fato, os tipos dos campos são extremamente semelhantes aos seus equivalentes de formulário, e por boa razão! Nós muitas vezes queremos guardar os dados do formulário e armazená-lo então faz sentido os modelos de base de dados serem semelhantes aos formulários em estrutura. Vamos olhar um exemplo:

```python
# application/models.py
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    job_title = models.CharField(
        max_length=200
    )
```

Esta classe de modelo de base de dados descreve os pedaços que queremos incluir numa tabela de base de dados. Cada classe de modelo de base de dados representa uma tabela de base de dados. Se quisermos os número de telefone que mencionamos anteriormente, criaríamos uma classe `PhoneNumber` separada. De maneira convencional, usamos um nome singular ao invés dum plural quando nomeamos a classe. Nós fazemos isto porque cada *linha* na tabela é representada como uma instância de objeto:

```python
>>> from application.models import Employee
>>> employee = Employee(
...     first_name='Tom',
...     last_name='Bombadil',
...     job_title='Old Forest keeper')
>>> employee.first_name
'Tom'
```

Este exemplo parece criar um novo empregado, mas falta-lhe um elemento chave. Nós não guardamos a instância de `employee` na base de dados. Nós podemos fazer isto com `employee.save()`, mas se estivermos a seguir o processo e tentarmos chamar este agora mesmo, falhará com um erro que diz que a tabela de `employee` não existe.

Uma vez que a base de dados é uma ferramenta que é externa à Django, a base de dados precisa dum pouco de preparação antes de poder receber os dados da Django.

## Preparando uma Base de Dados com Migrações

Nós agora sabemos que os modelos de base dados da Django são classes da Python que mapeiam às tabelas da base de dados. As tabelas da base de dados não aparecem magicamente. Nós precisamos da habilidade de configurar as tabelas para que correspondam a estrutura definida na classe de Python. A ferramenta que a Django fornece para sincronizar os modelos de base de dados da Django e uma base de dados é chamada de sistema de migrações.

As migrações são ficheiros de Python que descrevem a sequência de opções de base de dados que são necessárias para fazer uma base de dados corresponder quaisquer definições de modelo de base de dados que tivermos no nosso projeto.

Uma vez que a Django trabalha com muitas bases de dados, estas operações de base de dados são definidas nos ficheiros de Python para que as opções possam ser abstratas. Ao usar opções abstratas, o sistema de migração da Django pode ligar os comandos de base de dados específicos para qualquer base de dados que estivermos a usar. Se começarmos com a SQLite, depois movemos para PostgreSQL quando estivermos prontos para colocar a nossa aplicação na internet, depois o sistema de migração fará o seu melhor para atenuar as diferenças, de mode a minimizar uma quantidade de trabalho desnecessário precisaríamos para efetuar a transição.

Inicialmente, podemos ir muito longe sem compreender os aspetos internos de como os ficheiros de migração funcionam. Ao nível do núcleo, precisamos aprender um pouco de comandos da Django: `makemigrations` e `migrate`.

### `makemigrations`

O comando `makemigrations` criará quaisquer ficheiros de migração se existir quaisquer mudanças de modelo de base de dados pendentes. Para criar o nosso ficheiro de migração para o modelo de base de dados `Employee`, podemos executar:

```bash
(venv) $ ./manage.py makemigrations
Migrations for 'application':
  application/migrations/0001_initial.py
    - Create model Employee
```

O que é importante notar é que necessitamos duma nova migração quando fazemos mudanças ao modelo de base de dados que atualizam quaisquer campos. Isto inclui:

* Adicionar novos modelos e campos de base de dados
* Modificar campos existentes
* Eliminar campos existentes
* Mudar alguns metadados do modelo de base de dados e alguns outros casos extremos

Se não fizermos uma migração, provavelmente encontraremos erros quando buscarmos dados da base de dados. Isto acontece porque a Django apenas constrói consultas baseada no que está definido no código da Python. O sistema assume que a base de dados está no estado apropriado. A Django tentará consultar as tabelas da base de dados mesmo se estas tabelas ainda não existirem!

### `migrate`

O outro comando, `migrate`, pega os ficheiros de migração e aplica-os à base de dados. Por exemplo:

```bash
(venv) $ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, application, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying application.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying sessions.0001_initial... OK
```

Esta é a saída que acontece quando aplicamos a nossa nova migração. O que é tudo isto? 

O sistema de migração também é usado por aplicações da Django embutidas. No nosso projeto de exemplo, usamos `startproject` que inclui um conjunto de aplicações comuns na lista `INSTALLED_APPS`. Nós podemos observar que a nossa `application` de exemplo aplicou a sua migração, e as migrações de outras aplicações da Django que incluímos também são aplicadas.

Se executarmos o comando `migrate` novamente, não veremos a mesma saída. Isto porque a Django rastreia quais migrações foram aplicadas. O sistema de migração apenas executarão quaisquer migrações *não aplicadas*.

Nós também podemos limitar quais migrações à executar fornecendo um nome de aplicação da Django:

```bash
(venv) $ ./manage.py migrate application
```

Estes são os fundamentos de migrações. Nós também podemos usar migrações para aplicar operações mais complexas como ações que são específicas à nossa base de dados selecionada. Nós podemos aprender mais sobre o que as migrações da Django podem fazer na {{< extlink "https://docs.djangoproject.com/en/4.1/topics/migrations/" "documentação das Migrações" >}}.

## Trabalhando com Modelos de Base de Dados

Depois de executar as migrações, a nossa base de dados estará preparada para comunicar-se apropriadamente com a Django.

Para criar novas linhas nas nossas novas tabelas de base de dados, podemos usar um método `save` do modelo de base de dados. Quando guardamos uma instância de modelo de base de dados, a Django enviará uma mensagem à base de dados que efetivamente diz "adicionar este novo dado à esta tabela da base de dados". Estas "mensagens" da base de dados são na realidade chamadas de **consultas**.

Como mencionamos na seção de definições, a Django comunica-se com a base de dados através dum motor da base de dados. O motor da base de dados usa a Linguagem de Consulta Estruturada (SQL) para comunicar com a base de dados de verdade. SQL é o padrão comum que todas as bases de dados suportadas pela Django "falam". Desde a Django usa SQL, é por isto que uma mensagem é nomeada de "consulta".

Qual é o aspeto duma consulta de SQL? Se guardarmos o nosso anterior exemplo de modelo de base de dados, seria algo do género:

```sql
INSERT INTO "application_employee"
    ("first_name", "last_name", "job_title")
VALUES
    ('Tom', 'Bombadil', 'Old Forest keeper')
```

Nota que este exemplo é uma consulta `INSERT` quando usamos o motor da SQLite. Tal como línguas naturais, a SQL tem uma variedade de dialetos dependendo da base de dados que selecionarmos. As bases de dados fazem o seu melhor para aderirem à alguns padrões, mas cada base de dados tem suas peculiaridades, e o trabalho do motor de base de dados é nivelar essas diferenças sempre que possível.

Isto é uma outra área onde a Django faz uma tonelada de trabalho duro em nosso nome. O motor de base e dados traduz a nossa chamada de `save` em uma consulta de SQL apropriada. SQL é um tópico profundo que possivelmente não podemos cobrir completamente
{{< web >}}
neste artigo.
{{< /web >}}
{{< book >}}
neste capítulo.
{{< /book >}}
Felizmente, não precisamos de o fazer por causa do ORM da Django!

ORM significa "Object Relational Mapper" ou Mapeador Relacional de Objeto. O trabalho dum ORM é mapear (ou traduzir) de *objetos* da Python para uma base de dados *relacional*. Isto significa que passaremos o nosso tempo trabalhando no código Python, e deixaremos a Django descobrir como obter e colocar dados na base de dados.

Usar `save` num registo de modelo é tanto um exemplo pequeno do ORM da Django. O que mais podemos fazer? Nós podemos fazer coisas como:

* Receber todas as linhas da base de dados.
* Receber um conjunto filtrado de linhas baseado em algum critério de filtragem.
* Atualizar um conjunto de linhas ao mesmo tempo.
* Eliminar lidas da base de dados.

Muitas destas operações com o ORM da Django funcionam através duma classe `Manager`. Onde o nosso anterior exemplo mostrou como manipular um única linha, um gestor de modelo de base de dados tem métodos desenhados para interagir com várias linhas.

Nós podemos analisar a nossa de empregado fictícia. O gestor para um modelo de base de dados está anexado à classe de modelo de base de dados como um atributo nomeado `objects`. Vamos ver algum código:

```python
>>> from application.models import Employee
>>> bobs = Employee.objects.filter(first_name='Bob')
>>> for bob in bobs:
...     print(f"{bob.first_name} {bob.last_name}")
...
Bob Ross
Bob Barker
Bob Marley
Bob Dylan
>>> print(bobs.query)
SELECT
    "application_employee"."id",
    "application_employee"."first_name",
    "application_employee"."last_name",
    "application_employee"."job_title"
FROM "application_employee"
WHERE "application_employee"."first_name" = Bob
```

Neste exemplo, estamos a usar o gestor para filtrar um subconjunto de empregados dentro da tabela. A variável `bobs` retornado pelo método `filter` é um `QuerySet`. Como podemos supor, este representa um conjunto de linhas que uma consulta de SQL retornará. Sempre que tivermos um conjunto de consulta, podemos imprimir a consulta para ver a declaração de SQL exata que a Django executará em nosso nome.

E se quisermos eliminar um registo de empregado?:

```python
>>> from application.models import Employee
>>> # The price is wrong, Bob!
>>> Employee.objects.filter(
... first_name='Bob',
... last_name='Barker').delete()
(1, {'application.Employee': 1})
```

Um conjunto de consulta pode aplicar operações em massa. Neste caso, o filtro é suficientemente limitado que apenas um registo foi eliminado, mas poderia ter incluído mais se a consulta de SQL correspondesse mais linhas da tabela da base de dados.

A classe `QuerySet` tem uma variedade de métodos que são úteis quando trabalhamos com as tabelas. Alguns dos métodos também tém a propriedade interessante de retornar um novo conjunto de consulta. Isto é uma capacidade benéfica quando precisamos de aplicar lógica adicional para a nossa consulta:

```python
from application.models import Employee

# employees é um conjunto de consulta de todas as linhas!
employees = Employee.objects.all()

if should_find_the_bobs:
    # Novo conjunto de consulta!
    employees = employees.filter(
        first_name='Bob'
    )
```

Cá estão alguns outros métodos de `QuerySet` que usamos constantemente:

* `create` - Como uma alternativa para criar uma instância de registo e chamar `save`, o gestor pode criar um registo diretamente:

```python
Employee.objects.create(
    first_name='Bobby',
    last_name='Tables'
)
```

* `get` - Use este método quando quiseres um *e exatamente um* registo. Se a tua consulta não corresponder ou retornará vários registos, ou terás uma exceção:

```python
the_bob = Employee.objects.get(
    first_name='Bob',
    last_name='Marley'
)

Employee.objects.get(first_name='Bob')
# Levanta
# application.models.Employee.MultipleObjectsReturned

Employee.objects.get(
    first_name='Bob',
    last_name='Sagat'
)
# Levanta application.models.Employee.DoesNotExist
```

* `exclude` - Este método permite-te excluir linhas que podem ser parte do teu conjunto de consulta existente:

```python
the_other_bobs = (
    Employee.objects.filter(first_name='Bob')
    .exclude(last_name='Ross')
)
```

* `update` - Com este método, podes atualizar um grupo de linhas numa única operação:

```python
Employee.objects.filter(
    first_name='Bob'
).update(first_name='Robert')
```

* `exists` - Use este método se quiseres verificar se existem linhas na base de dados que correspondem à condição que queres verificar:

```python
has_bobs = Employee.objects.filter(
    first_name='Bob').exists()
```

* `count` - Verifica quais linhas correspondem uma condição: Por causa de como a SQL funciona, nota que isto é mais eficiente do que tentar usar `len` num conjunto de consultas:

```python
how_many_bobs = Employee.objects.filter(
    first_name='Bob').count()
```

* `none` - Isto retorna um conjunto de consultas vazio para o modelo de base de dados. Como poderia isto ser útil? Nós usamos isto quando precisamos proteger certo acesso de dados:

```python
employees = Employee.objects.all()

if not is_hr:
    employees = Employee.objects.none()
```

* `first` / `last` - Estes métodos retornarão uma instância de modelo de base de dados individual se existir uma correspondência. Os métodos usam a ordenação sobre os modelos de base de dados para obterem o resultado desejado. Nós usamos `order_by` para dizer como queremos que os resultados sejam organizados:

```python
>>> a_bob = Employee.objects.filter(
...     first_name='Bob').order_by(
...     'last_name').last()
>>> print(a_bob.last_name)
Ross
```

Uma operação `order_by` também pode reverter a ordem dos resultados. Para fazer isto, adiciona um traço antes do nome do campo como `order_by('-last_name')`.

Com o conhecimento de como podemos interagir com os modelos de base de dados, podemos concentrar-nos mais nos dados que podem ser armazenados nos modelos de base de dados (e, assim, na nossa base de dados)

## Tipos de Dados do Modelo de Base de Dados

A tabela `Employee` que usávamos como exemplo
{{< web >}}
para este artigo
{{< /web >}}
{{< book >}}
para este capítulo
{{< /book >}}
apenas tem três campos `CharField` no modelo de base de dados. A escolha foi deliberada porque queríamos que tivéssemos uma oportunidade de absorver um pouco sobre a ORM da Django e trabalhar com os conjuntos de consultas antes de ver outros tipos de dados.

{{< web >}}
Nós vimos no artigo de formulários
{{< /web >}}
{{< book >}}
Nós vimos no capítulo de formulários
{{< /book >}}
que o sistema de formulário da Django inclui uma vasta variedade de campos de formulário. Se olharmos na referência dos {{< extlink "https://docs.djangoproject.com/en/4.1/ref/forms/fields/" "campos de Formulário" >}} e compararmos a lista de tipos à aqueles na {{< extlink "https://docs.djangoproject.com/en/4.1/ref/models/fields/" "referência de campo do Modelo de Base de Dados" >}}, podemos observar uma grande sobreposição.

Tal como os seus equivalentes do formulário, os modelos de base de dados têm `CharField`, `BooleanField`, `DateField`, `DateTimeField`, e muitos outros tipos semelhantes. Os tipos de campos partilham muitos atributos comuns. Mais comummente, eu penso que usarás ou encontrarás os seguintes atributos:

* `default` - Se quisermos ser capazes de criar um registo de modelo de base de dados sem especificar certos valores, então podemos usar `default`. O valor pode ou ser um valor literal ou fuma função chamável que produz um valor:

```python
# application/models.py
import random

from django.db import models

def strength_generator():
    return random.randint(1, 20)

class DungeonsAndDragonsCharacter(
    models.Model
):
    name = models.CharField(
        max_length=100,
        default='Conan'
    )
    # Importante: Passar a função,
    # não *chamar* a função!
    strength = models.IntegerField(
        default=strength_generator
    )
```

* `unique` - Quando um valor de campo deve ser único para todas as linhas na tabela da base de dados, usamos `unique`. Isto é um bom atributo para identificadores onde não podemos esperar duplicados:

```python
class ImprobableHero(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

# Só pode existir um.
ImprobableHero.objects.create(
    name='Connor MacLeod'
)
```

* `null` - Uma base de dados relacional tem a habilidade de armazenar a ausência de dados. Na base de dados, este valor é considerado como `NULL`. Algumas vezes isto é uma distinção importante contra o valor que é vazio. Por exemplo, num modelo de base de dados `Person`, um campo de inteiro como `number_of_children` significaria muitas coisas diferentes para um valor de 0 contra um valor de `NULL`. O primeiro indica que um pessoa não tem filhos enquanto o segundo indica que o número de filhos é desconhecido. A presença de condições nulas exige mais verificação no nosso código, então o padrão da Django é fazer `null` ser `False`. Isto significa que um campo não permite `NULL`. Os valores nulos podem ser úteis se necessários, mas penso ser melhor evitá-los se puderes e tentar manter dados verdadeiros sobre um campo:

```python
class Person(models.Model):
    # Este campo sempre teria um valor desde que não possa ser nulo.
    # Zero conta como um valor e não é `NULL`.
    age = models.IntegerField()
    # Este campo poderia ser desconhecido e conter `NULL`.
    # Na Python, um valor de base de dados `NULL` aparecerá como `None`.
    weight = models.IntegerField(
        null=True
    )
```

{{< web >}}
* `blank` - O atributo `blank` é frequentemente usado em conjunto com o atributo `null`. Enquanto o atributo `null` permita uma base de dados armazenar `NULL` para um campo, `blank` permite a *validação de formulário* aceitar um campo vazio. Isto é usado pelos formulários que são automaticamente gerados pela Django como na aplicação de administração da Django que falaremos sobre no próximo artigo:
{{< /web >}}
{{< book >}}
* `blank` - O atributo `blank` é frequentemente usado em conjunto com o atributo `null`. Enquanto o atributo `null` permita uma base de dados armazenar `NULL` para um campo, `blank` permite a *validação de formulário* aceitar um campo vazio. Isto é usado pelos formulários que são automaticamente gerados pela Django como na aplicação de administração da Django que falaremos sobre no próximo capítulo:
{{< /book >}}

```python
class Pet(models.Model):
    # Nem todos animais de estimação têm cauda
    # então queremos formulários auto-gerados
    # para permitirem a ausência deste valor.
    length_of_tail = models.IntegerField(
        null=True,
        blank=True
    )
```

{{< web >}}
* `choices` - Nós vimos `choices` no artigo de formulários como uma técnica para ajudar os utilizadores a escolherem o valor correto a partir dum conjunto restrito. `choices` pode ser definido no modelo de base de dados. A Django pode fazer a validação no modelo de base de dados que garantirá que apenas valores específicos são armazenados num campo da base de dados:
{{< /web >}}
{{< book >}}
* `choices` - Nós vimos `choices` no capítulo de formulários como uma técnica para ajudar os utilizadores a escolherem o valor correto a partir dum conjunto restrito. `choices` pode ser definido no modelo de base de dados. A Django pode fazer a validação no modelo de base de dados que garantirá que apenas valores específicos são armazenados num campo da base de dados:
{{< /book >}}

```python
class Car(models.Model):
    COLOR_CHOICES = [
        (1, 'Black'),
        (2, 'Red'),
        (3, 'Blue'),
        (4, 'Green'),
        (5, 'White'),
    ]
    color = models.IntegerField(
        choices=COLOR_CHOICES,
        default=1
    )
```

* `help_text` - À medida que as aplicação se tornam maiores ou se trabalharmos numa equipa grande com pessoas a criarem modelos de base de dados da Django, a necessidade de documentação cresce. A Django permite texto de ajuda que podem ser exibido com um valor de campo na aplicação do administrador da Django. Este texto de ajuda é útil para lembrar ao teu futuro eu ou educar um colega de trabalho:

```python
class Policy(models.Model):
    is_section_987_123_compliant = models.BooleanField(
        default=False,
        help_text=(
        'For policies that only apply'
        ' on leap days in accordance'
        ' with Section 987.123'
        ' of the Silly Draconian Order'
        )
    )
```

Estes são os atributos que, na minha opinião os utilizadores têm mais probabilidade de encontrar. Também existem alguns tipos de campos importantes que exigem atenção especial: campos relacionais.

## O Torna Uma Base de Dados "Relacional"?

As bases de dados relacionais tem a habilidade de ligar diferentes tipos de dados entre si. Nós tivemos um breve exemplo disto anteriormente
{{< web >}}
neste artigo
{{< /web >}}
{{< book >}}
neste capítulo
{{< /book >}}
quando considerámos um empregado com vários número de telefone.

Um modelo de base de dados demasiado simplificado para um empregado com vários números de telefone pode parecer-se com o seguinte:

```python
# application/models.py
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    job_title = models.CharField(
        max_length=200
    )
    phone_number_1 = models.CharField(
        max_length=32
    )
    phone_number_2 = models.CharField(
        max_length=32
    )
```

Esta única tabela poderia conter alguns números, mas esta solução tem algumas deficiências:

* E se um empregado tiver mais de dois números de telefone? É possível que uma pessoa tenha vários telemóveis, uma telefone fixo em casa, um número paginador, um número fax, assim por diante.
* Como podemos saber que tipo de número de telefone está em `phone_number_1` e `phone_number_2`? Se puxarmos o registo do empregado para tentar telefonar ao indivíduo e, em vez disso, se marcar um número de fax, teremos dificuldade em falar com eles.

Em vez disso, e se tivéssemos dois modelos de base de dados separados?:

```python
# application/models.py
from django.db import models

class Employee(models.Model):
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    job_title = models.CharField(
        max_length=200
    )

class PhoneNumber(models.Model):
    number = models.CharField(
        max_length=32
    )
    PHONE_TYPES = (
        (1, 'Mobile'),
        (2, 'Home'),
        (3, 'Pager'),
        (4, 'Fax'),
    )
    phone_type = models.IntegerField(
        choices=PHONE_TYPES,
        default=1
    )
```


Temos duas tabelas separadas. Como podemos ligar as tabelas para que um empregado possa ter um, dois, ou duzentos números de telefone? para isto, podemos usar o tipo de campo relacional `ForeignKey`. Cá está uma versão ligeiramente separada da `PhoneNumber`:

```python
...

class PhoneNumber(models.Model):
    number = models.CharField(
        max_length=32
    )
    PHONE_TYPES = (
        (1, 'Mobile'),
        (2, 'Home'),
        (3, 'Pager'),
        (4, 'Fax'),
    )
    phone_type = models.IntegerField(
        choices=PHONE_TYPES,
        default=1
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )
```


Esta atualização diz que cada número de telefone agora deve ser associado a um registo de empregado. `on_delete` é um atributo obrigatório que determina o que acontecerá quando um registo de empregado for eliminado. Neste caso, `CASCADE` significa que a eliminação duma linha dum empregado será feita em cascata e eliminará também todos os números de telefone relacionados com o empregado.

A chave para como isto funciona está em entender *chaves*. Quando criamos um modelo de base de dados da Django, recebemos um campo adicional adicionado ao nosso modelo pela abstração. Este campo é chamado de `AutoField`:

```python
# Isto é o que a Django adiciona ao nosso modelo de base de dados.
id = models.AutoField(primary_key=True)
```

Um `AutoField` adiciona uma coluna à uma tabela de base de dados que atribuirá à cada linha na tabela um único inteiro. Cada nova linha incrementa a partir da linha anterior e a numeração começa em um. Este número é o identificador para a linha e é chamado de *chave primária*.

Se o Tom Bomdadil for o primeiro empregado na tabela, então o valor do `id` da linha seria `1`.

Conhecendo às chaves primárias, estamos preparados para entender os campos de chave estrangeira. No caso do campo de chave estrangeira `PhoneNumber.employee`, qualquer linha de número de telefone armazenará o valor da chave primária de alguma linha de empregado. Isto normalmente é chamado dum relacionamento dum para muitos.

Uma `ForeignKey` é uma relação dum para muitos porque várias linhas duma tabela (neste caso, `PhoneNumber`) podem referenciar uma única linha numa outra tabela, nomeadamente, `Employee`. Em outras palavras, um empregado pode ter vários números de telefone. Se quiséssemos receber os números de telefone do Tom, então uma maneira possível seria:

```python
tom = Employee.objects.get(
    first_name='Tom',
    last_name='Bombadil'
)
phone_numbers = PhoneNumber.objects.filter(employee=tom)
```

A consulta para `phone_numbers` seria:

```sql
SELECT
    "application_phonenumber"."id",
    "application_phonenumber"."number",
    "application_phonenumber"."phone_type",
    "application_phonenumber"."employee_id"
FROM "application_phonenumber"
WHERE "application_phonenumber"."employee_id" = 1
```

Na base de dados, a Django armazenará a coluna de tabela para a chave estrangeira como `employee_id`. A consulta está a pedir por todas as linhas de números de telefone que correspondem quando o identificador do empregado for 1. Uma vez que as chaves primárias têm de ser únicas, este valor de 1 apenas pode corresponder a Tom Bomdadil assim as linhas resultantes serão os números de telefone que estão associados com este empregado.

Existe um outro tipo de campo relacional sobre o qual devemos dedicar algum tempo. Este campo é o `ManyToManyField`. Como podemos imaginar, este campo é usado quando tipos de dados relacionam-se entre si duma maneira de muitos para muitos.

Vamos pensar sobre bairros. Os bairros podem ter uma variedade de tipos de residências misturadas como casas, apartamentos, condóminos e assim por diante, mas para manter o exemplo mais simples, assumiremos que os bairros são compostos de casas. Cada casa num bairro é a casa duma ou mais pessoas.

E se tentássemos modelar isto com campos de `ForeignKey`?:

```python
# application/models.py
from django.db import models

class Person(models.Model):
    name = models.CharField(
        max_length=128
    )

class House(models.Model):
    address = models.CharField(
        max_length=256
    )
    resident = models.ForeignKey(
        Person,
        on_delete=models.CASCADE
    )
```

Esta versão mostra um cenário onde uma casa pode apenas ter um único morador. Uma pessoa poderia ser o morador de várias casas, mas estas casas seriam muito solitárias. E se colocássemos a chave estrangeira no outro lado da relação de modelação?:

```python
# application/models.py
from django.db import models

class House(models.Model):
    address = model.CharField(
        max_length=256
    )

class Person(models.Model):
    name = models.CharField(
        max_length=128
    )
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE
    )
```

Nesta versão, uma casa pode ter vários moradores, mas uma pessoa apenas pode pertencer à uma única casa.

Nenhum destes cenários representa bem o mundo real. No mundo real, as casas podem albergar e albergam muitas vezes várias pessoas. Simultaneamente, muitas pessoas no mundo têm uma segunda casa como uma casa de praia ou uma casa de campo de verão no bosque. Ambos lados do relacionamento do modelo de base de dados podem ter muitos do outro.

Com um `ManyToManyField`, podemos adicionar o campo à ambos lados. Eis a nova modelação:

```python
# application/models.py
from django.db import models

class Person(models.Model):
    name = models.CharField(
        max_length=128
    )

class House(models.Model):
    address = models.CharField(
        max_length=256
    )
    residents = models.ManyToManyField(
        Person
    )
```

Como isto funciona ao nível da base de dados? Nós vimos com as chaves estrangeiras que uma tabela pode segurar a chave primária duma linha de outra tabela nos seus próprios dados. Infelizmente, uma única coluna de base de dados não pode segurar várias chaves estrangeiras. Isto significa que a modelação acima *não* adiciona `residents` à tabela `House`. Ao invés disto, a relação é manipulada adicionando uma *nova* tabela de base de dados. Esta nova tabela contém o mapeamento entre as pessoas e casas e armazena as linhas que contém chaves primárias a partir de cada modelo de base de dados.

Vamos pensar num exemplo para ver o que isto parece. Suponhamos que existem três registos de `Person` com chaves primárias de 1, 2, e 3. Vamos também supor que existem três registos de `House` com chaves primárias de 97, 98, e 99. Para provar que o relacionamento de muitos para muitos funciona em ambas direções, assumiremos que estas condições são verdadeiras:

* Pessoas com chaves primárias de 1 e 2 residem na casa 97.
* A pessoa com a chave primária 3 é dono da casa 98 e 99.

Os dados na nova tabela de mapeamento entre `Person` e `House` conteria dados como:

```text
Person | House
-------|------
1      | 97
2      | 97
3      | 98
3      | 99
```

Por causa da tabela de junção, a Django é capaz de consultar qualquer um dos lados da tabela para obter as casas ou os moradores relacionados.

Nós podemos acessar o lado "muito" de cada modelo de base de dados usando um conjunto de consulta. `residents` será um `ManyRelatedManager` e, tal como outros gestores, podemos fornecer conjuntos de consultas usando certos métodos de gestão.

Obter a direção inversa é um pouco menos óbvios. A Django adicionará um outro `ManyRelatedManager` ao modelo de base de dados `Person` automaticamente. O nome deste gestor é o nome do modelo de base de dados combinado com `_set`. Neste caso, este nome é `house_set`. Nós também podemos fornecer um atributo `related_name` ao `ManyToManyField` se quisermos um nome diferente como se quiséssemos chamá-lo `houses`:

```python
house = House.objects.get(
    address='123 Main St.'
)
# Nota o uso de `all()`!
for resident in house.residents.all():
    print(resident.name)

person = Person.objects.get(name='Joe')
for house in person.house_set.all():
    print(house.address)
```

Entender os campos `ForeignKey` e `ManyToManyField` dos modelos de base de dados da Django é um importante passo para modelar bem o nosso domínio do problema. Ao ter estas ferramentas disponíveis para nós, podemos começar a criar muitos dos relacionamentos de dados complexos que existem com problemas do mundo real.

## Sumário

{{< web >}}
Neste artigo,
{{< /web >}}
{{< book >}}
Neste capítulo,
{{< /book >}}
exploramos:

* Como configurar uma base de dados para o nosso projeto.
* Como a Django usa classes especiais chamadas de modelos de base de dados para preservar os dados.
* Como executar os comandos que prepararão uma base de dados para os modelos de base de dados que queremos usar.
* Como guardar uma nova informação na base de dados.
* Como pedir da base de dados a informação que armazenamos
* Tipos de campos complexos para modelar problemas do mundo real.

Com esta habilidade de armazenar dados numa base de dados, **temos todas ferramentas principais para construir uma aplicação interativa para os nossos utilizadores!**
{{< web >}}
Nesta série,
{{< /web >}}
{{< book >}}
Neste livro,
{{< /book >}}
examinamos:

* A manipulação de URL
* Visões para executar o nosso código e lógica de negócio
* Modelos de marcação para exibir a nossa interface de utilizador
* Formulários para deixar os utilizadores entrarem e interagirem com a nossa aplicação
* Modelos de base de dados para armazenar dados numa base de dados para armazenamento de longo prazo

Este é o conjunto principal de funcionalidades que a maioria das aplicações de Web têm. Já que vimos os tópicos principais que fazem as aplicações de Django funcionarem, estamos prontos para focar a nossa atenção sobre algumas das outras ferramentas fantásticas que definem a Django para além do pacote.

A primeira na lista é aplicação do administradores da Django embutida que permite-nos explorar os dados que armazenamos na nossa base de dados. Nós cobriremos:

* O que a aplicação de administração da Django é
* Como fazer os nossos modelos de base de dados aparecerem na administração
* Como criar ações adicionais que os utilizadores do administrador podem fazer

{{< web >}}
Se gostarias de seguir juntamente com a série, sinta-se a vontade para inscrever-se no meu boletim informativo onde anuncio todos os meus novos conteúdos. Se tiveres outras questões, podes contactar-me na X onde sou o {{< extlink "https://x.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;

A tradução deste artigo para o português é cortesia de Nazaré Da Piedade.
