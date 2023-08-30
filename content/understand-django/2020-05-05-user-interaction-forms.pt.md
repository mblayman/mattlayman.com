---
title: "Interação do Utilizador com os Formulários"
description: >-
    Como os utilizadores fornecem dados à tua aplicação para que possas interagir com eles? Nós podemos responder esta questão explorando o sistema de formulário da Django, e as ferramentas que a Django fornece para simplificar a tua aplicação a medida que envolveres-te com os teus utilizadores.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - forms

---

{{< web >}}
No artigo anterior da série [Entendendo a Django]({{< ref "/understand-django/_index.pt.md" >}}), vimos como os modelos de marcação da Django trabalham para produzir uma interface de utilizador. Está muito bem se apenas precisas de exibir uma interface de utilizador, mas o que fazes
{{< /web >}}
{{< book >}}
O que fazes
{{< /book >}}
se precisares que a tua aplicação interaja com os utilizadores? Tu usas o sistema de formulário da Django!
{{< web >}}
Neste artigo,
{{< /web >}}
{{< book >}}
Neste capítulo,
{{< /book >}}
focaremos-nos em como trabalhar com os formulários da Web usando o sistema de formulário da Django.

{{< understand-django-series-pt "forms" >}}

## Formulários da Web 101

Antes de pudermos mergulhar em como a Django lida com os formulários, precisamos de um entendimento dos formulários da HTML em geral. A funcionalidade de formulário da Django baseia-se sobre os formulários da Web então este tópico não fará sentido sem um conhecimento básico do tópico.

A HTML pode descrever o tipo de dado que podes querer que os teus utilizadores enviem para a tua aplicação. A coleta deste dado é feito com uma mão cheia de marcadores. Os marcadores de HTML primários à considerar são `form`, `input`, e `select`.

Um marcador de `form` é o contentor para todos os dados que queres que um utilizador envie para a tua aplicação. O marcador tem dois atributos críticos que dizem ao navegador como enviar os dados: `action` e `method`.

`action` seria melhor nomeado como "destination" ou "url". Infelizmente, estamos presos ao `action`. Este atributo do marcador `form` é para onde os dados do utilizador deveriam ser enviados. Também é útil saber que omitir `action` ou usar `action=""` enviará qualquer dado de formulário como uma requisição de HTTP para a mesma URL em que o navegador do utilizador está ligado.

O atributo `method` dita qual método de HTTP usar e pode ter um valor de `GET` ou `POST`. Quando emparelhado com `action`, o navegador sabe como enviar uma requisição de HTTP formatada apropriadamente.

Vamos dizer que temos este exemplo:

```html
<form method="GET" action="/some/form/">
    <input type="text" name="message">
    <button type="submit">Send me!</button>
</form>
```

Quando o método do formulário for `GET`, os dados do formulário serão enviados como parte da URL numa sequência de caracteres de consulta. A requisição `GET` enviada para o servidor parecer-se-á com `/some/form/?message=Hello`. Este tipo de submissão de formulário é muito útil quando não precisamos de guardar os dados e estamos a tentar fazer algum tipo de consulta. Por exemplo, poderias dar à tua aplicação alguma funcionalidade de pesquisa com uma URL como `/search/?q=thing+to+search`. Estas ligações poderiam ser marcadas facilmente e são um ajuste natural para este tipo de função.

O método `POST` de envio de dados de formulário destina-se a dados que queremos que sejam seguros ou guardados dentro duma aplicação. Com uma requisição `GET`, o dado de formulário na sequência de caracteres de consulta é exposto num número de lugares (consulte {{< extlink "https://owasp.org/www-community/vulnerabilities/Information_exposure_through_query_strings_in_url" "mais informações" >}} do Projeto Aberto de Segurança de Aplicação de Web (OWASP, sigla em Inglês)). Por outro lado, `POST` envia os dados no corpo da requisição de HTTP. Isto significa que se aplicação estiver segura (por exemplo, usando HTTPS), então os dados são encriptados enquanto viajam dum navegador para um servidor.

Se alguma vez iniciares a sessão numa aplicação de Web e submeteres uma palavra-passe num formulário, podes ter quase a certeza de que o formulário é enviado com a opção de método `POST` (e se não for, fuja!).

Vimos que `form` é o contentor que orienta como enviar os dados do formulário. `input` e `select` são os marcadores que permitem-nos exibir um formulário significativo ao utilizador.

O marcador mais predominante é `input`. Com o marcador `input`, os autores do formulário definirão principalmente o `type` e `name`. O atributo `type` diz ao navegador qual tipo de entrada a exibir:

* Precisamos duma caixa de confirmação? `type="checkbox"`
* Precisamos dum campo de palavra-passe que esconde caracteres? `type="password"`
* E uma caixa de texto clássica? `type="text"`

Tu podes consultar uma lista completa de tipos na página da {{< extlink "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input" "documentação do elemento de entrada da MDN" >}}.

O outro atributo, `name`, é o identificador que o formulário emparelhará com os dados do utilizador. O servidor usa o identificador para que possa distinguir entre os pedaços de dados que uma submissão de formulário possa incluir.

Um outro marcador que os teus formulários podem usar é o marcador `select`. Este tipo de marcador é menos frequente do que o marcador `input`. O marcador `select` permite os utilizadores fazerem uma escolha a partir duma lista de opções. A interface de utilizador do navegador padrão para este marcador é um menu deslizante.

Com estes elementos principais de formulários de HTML, estamos equipados para entender as capacidades de formulário da Django. Vamos mergulhar!

## Formulários da Django

A funcionalidade de formulário da Django atua como uma ponte entre os formulários de HTML e as classes da Python e os tipos de dados. Quando representamos um formulário ao utilizador através duma visão, o sistema de formulário é capaz de exibir os marcadores de formulário de HTML e estruturas apropriadas. Quando recebemos os dados deste formulário a partir duma submissão do utilizador, o sistema de formulário pode traduzir os dados de formulário crus do navegador em dados de Python nativos que podemos usar.

Nós podemos começar com a classe `Form`. Uma classe de formulário representa a declaração de dados daqueles dados que precisamos da parte do utilizador. Cá está um exemplo que podemos examinar:

```python
# application/forms.py

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100
    )
    email = forms.EmailField()
    message = forms.CharField(
        max_length=1000
    )
```

* Os formulários da Django definidas pelo utilizador devem ser subclasse da classe `Form`. Esta classe adiciona muitas funcionalidades poderosas que nos ajudarão a medida que exploramos mais.
* Os dados que queremos coletar estão listados como atributos de nível de classe. Cada campo do formulário é um certo tipo de campo que tem suas próprias características para ajudar a traduzir dados de formulário crus em tipos de dados com os quais queremos trabalhar nas visões.

Se pegarmos este formulário e o adicionarmos ao contexto da visão como `form`, então podemos desenhá-lo no modelo de marcação. A interpretação padrão do formulário usa uma tabela de HTML, mas podemos desenhar os campos num formato mais simples com o método `as_p`. Este método usará os marcadores de parágrafo para os elementos de formulário. Se o modelo de marcação parecer-se com isto:

{{< web >}}
```django
{{ form.as_p }}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{{ form.as_p }}
```
{{< /book >}}

Então a Django desenhará:

```html
<p><label for="id_name">Name:</label>
  <input type="text" name="name" maxlength="100" required id="id_name"></p>
<p><label for="id_email">Email:</label>
  <input type="email" name="email" required id="id_email"></p>
<p><label for="id_message">Message:</label>
  <input type="text" name="message" maxlength="1000" required id="id_message">
</p>
```

Possibilitar a submissão do formulário, precisamos envolver esta saída desenhada com um marcador `form` e incluir um botão submeter e um sinal de CSRF.

Huh? *sinal de CSRF?* infelizmente, o mundo está cheio de pessoas malvadas que adorariam piratear a tua aplicação para roubar dados dos outros. Um sinal de CSRF é uma medida de segurança que Django inclui para dificultar os atores maliciosos de falsificar os dados do teu formulário. Falaremos mais sobre segurança 
{{< web >}}
num artigo futuro.
{{< /web >}}
{{< book >}}
num capítulo futuro.
{{< /book >}}
Por agora, borrife o sinal nos teus formulários com o marcador de modelo de marcação embutido da Django e tudo deve funcionar:

{{< web >}}
```django
<form action="{% url "some-form-url" %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <p><input
        type="submit"
        value="Send the form!"></p>
</form>
```
{{< /web >}}
{{< book >}}
```djangotemplate
<form action="{% url "some-form-url" %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <p><input
        type="submit"
        value="Send the form!"></p>
</form>
```
{{< /book >}}

É assim como um formulário é exibido. Agora vamos olhar uma visão que manipula o formulário apropriadamente. Quando trabalhamos com visões de formulário, frequentemente usaremos uma visão que é capaz de manipular ambas requisições de HTTP `GET` e `POST`. Cá está uma visão completa que podemos decompor pedaço por pedaço. O exemplo usa uma visão de função por questões de simplicidade, mas poderíamos fazer algo semelhante com uma visão baseada em classe:

```python
# application/views.py

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import ContactForm

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Fazer algo com os dados do formulário
            # como enviar um correio-eletrónico.
            return HttpResponseRedirect(
                reverse('some-form-success-url')
            )
    else:
        form = ContactForm()

    return render(
        request,
        'contact_form.html',
        {'form': form}
    )
```

Se começarmos pensando sobre o ramo `else`, podemos ver o quão pouco esta visão faz numa requisição `GET`. Quando o método de HTTP for um `GET`, cria um formulário vazio sem dados passados ao construtor e desenha um modelo de marcação com o `form` no contexto.

`contact_form.html` contém o modelo de marcação da Django acima para exibir o formulário de HTML ao utilizador. Quando o utilizador clicar em "Send the form!", uma outra requisição vai para visão, mas desta vez o método é um `POST` de HTTP e contém os dados submetidos.

A requisição de `POST` cria um `form`, mas existe uma diferença em como é construído. Os dados de submissão do formulário são armazenados no `request.POST`, que é um objeto parecido com dicionário que deparamos-nos primeiro
{{< web >}}
no artigo de visões.
{{< /web >}}
{{< book >}}
no capítulo de visões.
{{< /book >}}
Com a passagem de `request.POST` ao construtor do formulário, criamos um formulário com dados. Na documentação da Django, verás isto a ser chamada como um *formulário vinculado* porque os dados estão *vinculados* ao formulário.

Com o formulário pronto, a visão verifica se os dados são válidos. Falaremos sobre a validação de formulário em detalhe depois
{{< web >}}
neste artigo.
{{< /web >}}
{{< book >}}
neste capítulo.
{{< /book >}}
Neste exemplo, podemos ver que `is_valid` poderia retornar `False` se os dados do formulário contivessem "I am not an email address" no campo `email`, por exemplo.

* Quando o formulário é válido, a visão faz o trabalho adicional representado pelo comentário e redireciona para uma nova visão que pode mostrar algum tipo de mensagem de sucesso.
* Quando o formulário é inválido, a visão sai da cláusula `if` e chama `render`. Já que os dados estão vinculados ao `form`, o formulário de contacto tem informação suficiente para mostrar quais campos de formulário causaram os erros que tornaram o formulário inválido.

Este é o cerne da manipulação de formulário! A visão apresentada é um padrão comum para manipular as visões de formulário na Django. De fato, este padrão de visão é tão comum que a Django fornece uma visão embutida para implementar o que é feito no exemplo nomeada `FormView`:

```python
# application/views.py

from django.views.generic import FormView
from django.urls import reverse

from .forms import ContactForm

class ContactUs(FormView):
    form_class = ContactForm
    template_name = 'contact_form.html'

    def get_success_url(self):
        return reverse(
            'some-form-success-view'
        )

    def form_valid(self, form):
        # Fazer algo com os dados do formulário
        # como enviar um correio-eletrónico.
        return super().form_valid(form)
```

A `FormView` espera uma classe de formulário e o nome de modelo de marcação e fornece alguns métodos à sobrepor para os lugares comuns onde a lógica da nossa própria aplicação deveria viver.

## Campos de Formulário

Com os fundamentos da manipulação de formulário prontos, podemos voltar a nossa atenção aos tipos de campos que os formulários podem usar. A extensa lista de campos está na {{< extlink "https://docs.djangoproject.com/en/4.1/ref/forms/fields/" "documentação da Django" >}}, e olharemos alguns dos mais comuns
{{< web >}}
neste artigo.
{{< /web >}}
{{< book >}}
neste capítulo.
{{< /book >}}

A primeira coisa à lembrar sobre os campos de formulário da Django é que convertem dados de formulário de HTML em tipos de dados de Python nativos. Se examinarmos os dados duma submissão de formulário, descobriremos que cada valor é essencialmente uma sequência de caracteres por padrão. Se a Django não fizesse nada por nós, então teríamos de converter constantemente para os tipos de daos que queremos. Ao trabalhar com os campos de formulário, esta conversão de dados é automaticamente manipulada por nós. Por exemplo, se escolhermos um `BooleanField`, depois do formulário da Django ser validado, o valor deste campo será ou `True` ou `False`. 

Um outro item importante a saber sobre os campos é que estão associados com os acessórios de Django particulares. Os acessórios são a maneira de controlar o que a Django desenha quando desenhamos um formulário. Cada campo de formulário tem um tipo de acessório padrão. Continuando com `BooleanField`, o seu acessório padrão é um `CheckboxInput` que desenhará um marcador `input` com um tipo de `checkbox` (por exemplo, nosso formulário de confirmação padrão).

Os campos são a interseção critica entre o mundo do navegador e a HTML, e o mundo da Python com todos os seus tipos de dados robustos.

Quais são os campos mais procurados? E o que precisamos de definir nesses campos?

### `CharField`

`CharField` é um verdadeiro cavalo de batalha para os formulários da Django. O `CharField` captura a entrada de texto e usa um marcador `input` padrão com um tipo de `text`. Se quisermos reunir mais texto, como num formulário de reação ou comentário, podemos mudar do acessório de `TextInput` padrão para um acessório de `Textarea`. Isto fará o nosso formulário desenhar um marcador `textarea` que dará muito mais espaço para qualquer entrada:

```python
# application/forms.py

from django import forms

class FeedbackForm(forms.Form):
    email = forms.EmailField()
    comment = forms.CharField(
        widget=forms.Textarea
    )
```

### `EmailField`

O `EmailField` é como uma versão especializada do `CharField`. O campo usa um marcador de `input` com um tipo de `email`. Muitos navegadores modernos podem ajudar verificar que endereços de correio-eletrónico são fornecidos. Além disto, quando este campo é validado dentro da abstração, a Django também tentará validar o endereço de correio-eletrónico no caso do navegador não ter sido capaz de fazê-lo.

### `DateField`

Um `DateField` é um outro campo que é na sua maioria como um `CharField`. O campo até usa o tipo de `input` de `text` quando desenhado. A diferença com este campo vem do tipo de dado que o formulário fornecerá depois de ser validado. Um `DateField` converterá {{< extlink "https://docs.djangoproject.com/en/4.1/ref/settings/#datetime-input-formats" "uma variedade de formatos de sequência de caracteres" >}} num objeto `datetime.date` da Python.

### `ChoiceField`

Um `ChoiceField` é útil quando queremos que um utilizador faça uma escolha a partir duma lista de opções. Para este tipo de campo, devemos fornecer uma lista de escolhas da qual o utilizador pode escolher uma ou mais. Suponha que queremos perguntar aos utilizadores qual é a sua refeição favorita do dia. Cá está um formulário que pode fazer isto: 

```python
# application/forms.py

from django import forms

class SurveyForm(forms.Form):
    MEALS = [
        ("b", "Breakfast"),
        ("l", "Lunch"),
        ("d", "Dinner")
    ]
    favorite_meal = forms.ChoiceField(
        choices=MEALS
    )
```

Isto conterá um formulário com um marcador `select` que parece-se com:

```html
<p>
  <label for="id_favorite_meal">Favorite meal:</label>
  <select name="favorite_meal" id="id_favorite_meal">
    <option value="b">Breakfast</option>
    <option value="l">Lunch</option>
    <option value="d">Dinner</option>
  </select>
</p>
```

Este punhado de campos lidarão com a maioria das necessidades do formulário. Certifica-te de explorar a lista completa do que está disponível para se equipar com outros tipos benéficos.

Os campos do formulário partilham alguns atributos comuns para coisas que cada necessidade do campo.

O atributo `required` é um booleano que especifica se um campo deve ter um valor ou não. Por exemplo, não faria muito sentido se a nossa aplicação tivesse um formulário de suporte que planeamos usar para contactar as pessoas através de correio-eletrónico, e um campo de `email` no formulário fosse opção.

O `label` define qual texto é usado para o marcador `label` que é desenhado com um `input` de formulário. No exemplo da refeição, poderíamos usar o atributo `label` para mudar "Favorite meal" para "What is your favorite meal?" Que tornaria uma experiência de inquérito muito melhor.

Algumas vezes os formulários podem não ser claros e os utilizadores precisam de ajuda. Nós podemos adicionar um atributo `help_text` que desenhará um texto adicional ao nosso campo de formulário envolvido num marcador `span` com uma classe `helptext` se quisermos estilizá-lo com a CSS.

Uma vez que os formulários são uma das maneiras principais que os utilizadores terão para fornecer informação à nossa aplicação, o sistema de formulário é rico em funcionalidades. Nós podemos aprender mais sobre a Django mergulhando profundamente nesta porção da documentação.

Vamos mudar o nosso foco para validação de formulário uma vez que a mencionamos algumas vezes de passagem.

## Validando Formulários

No exemplo da visão, mostramos um formulário que chama o método `is_valid`. Num alto nível, podemos entender o que este método está a fazer; está a determinar se o formulário é válido ou não.

Mas o que é que `is_valid` faz realmente? Ele faz muita coisa!

O método lida com cada um dos campos. Conforme vimos, os campos têm um tipo de dado final (como com `BooleanField`) ou uma estrutura esperada (como com `EmailField`). Este processo de converter tipos de dados e validar os dados do campo é chamado de limpeza. De fato, cada campo de ter um método `clean` que o formulário chamará quando `is_valid` for chamado.

Quando `is_valid` é `True`, os dados do formulário estarão num dicionário nomeado `cleaned_data` com chaves que correspondem aos nomes de campo declarado pelo formulário. Com os dados validados, podemos acessar `cleaned_data` para fazer o nosso trabalho. Por exemplo, se tivermos algum tipo de integração com sistema de bilhete de suporte, talvez o nosso `FeedbackForm` acima é manipulado na visão como:

```python
if form.is_valid():
    email = form.cleaned_data['email']
    comment = form.cleaned_data['comment']
    create_support_ticket(
        email,
        comment
    )
    return HttpReponseRedirect(
        reverse('feedback-received')
    )
```

Quando `is_valid` é `False`, a Django armazenará os erros encontrados num atributo `errors`. O atributo será usado quando o formulário for redesenhado na página (porque, se nos lembrarmos do exemplo da visão, o padrão da visão do formulário devolve um formulário vinculado através duma chama de `render` no caso de fracasso).

Uma vez mais, a Django está a fazer muito trabalho pesado por nós para tornar o trabalho com formulários mais fácil. O sistema *também* permite que os programadores adicionarem lógica de validação personalizada.

Se tivermos um campo de formulário, podemos adicionar personalização escrevendo um método na classe de formulário. O formato do método deve corresponder ao nome do campo e prefixar `clean_`. Vamos supor que queremos uma aplicação para o Bobs. Para registar-se na aplicação de Web, o nosso endereço de correio-eletrónico deve incluir "bob". Nós podemos escrever um método de limpeza para verificar isto:

```python
# application/forms.py

from django import forms

class SignUpForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if 'bob' not in email:
            raise forms.ValidationError(
                'Sorry, you are not a Bob.'
            )
        return email
```

Existem alguns pontos importantes sobre isto:

* `clean_email` apenas tentará limpar o campo `email`.
* Se a validação falhar, o nosso código deve levantar um `ValidationError`. A Django lidará com isto e colocará o erro no formato correto no atributo `erros` do formulário.
* Se tudo estiver bem, devemos nos certificar de retornar os dados limpados. Esta é a parte da interface que a Django espera por métodos limpos.

Estes métodos `clean_<field name>` são gatilhos que permitem-nos incluir verificação adicional. Este sistema de gatilho dá-nos o lugar perfeito para colocar a lógica de validação para os dados que é específica à nossa aplicação. Mas e se validássemos vários pedaços de dados? Isto pode acontecer quando os dados tiverem algum tipo de relacionamento entre si. Por exemplo, se estivermos a montar uma aplicação de genealogia, podemos ter um formulário que regista as datas de nascimento e falecimento. Nós podemos querer verificar estas datas:

```python
# application/forms.py

from django import forms

class HistoricalPersonForm(forms.Form):
    name = forms.CharField()
    date_of_birth = forms.DateField()
    date_of_death = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        date_of_death = cleaned_data.get('date_of_death')
        if (
            date_of_birth and
            date_of_death and
            date_of_birth > date_of_death
        ):
            raise forms.ValidationError(
                'Birth date must be before death date.'
            )
        return cleaned_data
```

Este método é semelhante ao `clean_<field name>`, mas devemos ser mais cuidadosos. As validações de campos individuais executam primeiro, mas podem ter falhado! Quando os métodos de limpeza falharem, o campo do formulário é removido da `cleaned_data` então não podemos fazer um acesso de chave direto. O método de limpeza verifica se as duas datas são verdadeiras e se cada uma tem um valor, depois faz a comparação entre elas.

A validação personalizada é uma excelente funcionalidade para melhorar a qualidade dos dados que coletamos dos utilizadores da nossa aplicação.

## Sumário

É como os formulário tornam possível coletar dados dos nossos utilizadores para que a nossa aplicação possa interagir com elas. Nós vimos:

* Formulários da Web e o marcador de HTML `form`
* A classe `Form` que a Django usa para lidar com os dados de formulário na Python
* Como os formulários são desenhados para os utilizadores pela Django
* Como controlar quais campos estão nos formulários
* Como fazer a validação de formulário.

Agora que sabemos como coletar dados dos utilizadores, como podemos fazer a aplicação guardar estes dados para eles?
{{< web >}}
No próximo artigo,
{{< /web >}}
{{< book >}}
No próximo capítulo,
{{< /book >}}
nós começaremos a armazenar dados numa base de dados. Trabalharemos com:

* Como configurar uma base de dados para o nosso projeto.
* Como a Django usa classes especiais chamadas de modelos de base de dados para preservar dos dados.
* Como executar os comandos que prepararão uma base de dados para os modelos de base de dados que queremos usar.
* Como guardar nova informação na base de dados.
* Como perguntar a base de dados pela informação que guardamos.

{{< web >}}
Se gostarias de seguir juntamente com a série, sinta-se a vontade para inscrever-se no meu boletim informativo onde anuncio todos os meus novos conteúdos. Se tiveres outras questões, podes contactar-me na Twitter onde sou o {{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;
