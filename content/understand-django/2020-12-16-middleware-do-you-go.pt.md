---
title: "Intermediário, Vais Embora?"
description: >-
    O tópico para este artigo da Entenda Django é intermediário. Veremos o que o intermediário é, para que serve num projeto de Django, e como escrever o nosso próprio.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - middleware
 - intermediário
series: "Understand Django"

---

{{< web >}}
No artigo anterior da série [Entender a Django]({{< ref "/understand-django/2020-11-04-user-authentication.pt.md" >}}), cobrimos o sistema de autenticação embutido. Este artigo nos deu a oportunidade de ver o modelo de base de dados `User`, maneiras de iniciar a sessão dos utilizadores com as ferramentas de autenticação da Django, e as funcionalidades que fazem os controlos de autorização funcionarem. Neste tópico, o intermediário surgiu como um componente integral. Agora aprenderemos mais sobre o intermediário e sua função dentro de um projeto de Django.
{{< /web >}}
{{< book >}}
Neste capítulo, aprenderemos mais sobre o intermediário e sua função dentro de um projeto de Django.
{{< /book >}}

{{< understand-django-series-pt "middleware" >}}

## Como Devo Pensar em Intermediário?

Para começar este tópico, descubramos onde o intermediário existe num projeto de Django.

O intermediário é o código que existe no meio. “No meio de quê?”, podemos perguntar. O “meio” é o código executado entre quando uma `HttpRequest` é criada pela abstração e quando o código que escrevemos é chamado pela Django. O “meio” também pode referir-se ao código executado *depois* que a nossa visão completa, mas antes da Django traduzir a `HttpResponse` em bytes para enviá-la através da rede a um navegador.

Já alguma vez comemos um Rebuçado Eterno? Não, não falo daquele do Willy Wonka que dura para sempre. Um Rebuçado Eterno é um doce duro, em camadas, que muda de cor e sabor à medida que o mantemos na boca até chegarmos finalmente a um centro macio.

O intermediário é uma espécie de camada de doces e o código da nossa visão é como o centro macio. Minha analogia é quebrada quando pensamos em como alguém come o rebuçado.

Com o doce, experimentamos uma camada de cada vez até chegarmos ao meio, e já está. Uma comparação mais adequada com o intermediário seria escavar *através* das camadas e sair do outro lado, experimentando as mesmas chamadas na ordem oposta à maneira como entrámos.

O que é mostrado abaixo é um diagrama de todo o intermediário padrão incluído quando executamos o comando `startproject`. Se formos aprendizes visuais que não acharam útil a analogia do rebuçado, então espero que esta imagem seja mais ilustrativa:

{{< web >}}
```text
               +--------- SecurityMiddleware --------------+
               |+-------- SessionMiddleware --------------+|
               ||+------- CommonMiddleware --------------+||
               |||+------ CsrfViewMiddleware -----------+|||
               ||||+----- AuthenticationMiddleware ----+||||
               |||||+---- MessageMiddleware ----------+|||||
               ||||||+--- XFrameOptionsMiddleware ---+||||||
               |||||||                               |||||||
HttpRequest =================> view function ==================> HttpResponse
               |||||||                               |||||||
```
{{< /web >}}
{{< book >}}
```text
        Middleware layers
        +------- Security ------------+
        |+------ Session ------------+|
        ||+----- Common ------------+||
        |||+---- CsrfView ---------+|||
        ||||+--- Authentication --+||||
        |||||+-- Message --------+|||||
        ||||||+- XFrameOptions -+||||||
        |||||||                 |||||||
request ========> view function=======> response
        |||||||                 |||||||
```
{{< /book >}}

Como a Django faz esta estratificação funcionar? Quando iniciamos a Django com um servidor de aplicações como o Gunicorn, nós temos que dar ao servidor de aplicações o caminho para o nosso módulo da Interface de Porta de Entrada do Servidor da Web (WSGI). Cobriremos servidores de aplicação num tópico posterior, mas, por enquanto, saibamos que um servidor de aplicação pode executar a nossa aplicação de Django. Se o nosso diretório de projeto que contém o nosso ficheiro de definições se chama `project`, então chamar o Gunicorn é como:

```bash
$ gunicorn project.wsgi
```

Teríamos esta configuração se executássemos `django-admin startproject project .` (incluindo o último ponto), mas o que é realmente necessário para o servidor de aplicação é onde quer que o nosso ficheiro `wsgi.py` estiver localizado no nosso projeto, *na forma de caminho de módulo*.

Precisamos lembrar, lá atrás
{{< web >}}
no primeiro artigo da série,
{{< /web >}}
{{< book >}}
no primeiro capítulo,
{{< /book >}}
que  WSGI significa Web Server Gateway Interface (Interface de Porta de Entrada do Servidor da Web) e é uma camada comum que aplicações síncronas da Web de Python devem implementar para trabalhar com os servidores de aplicação da Python. Dentro deste módulo `project.wsgi` existe uma função chamada `get_wsgi_application`, importada de `django.core.wsgi`.

A `get_wsgi_application` faz duas coisas:

{{< web >}}
* Chama `django.setup` que faz toda a configuração de inicialização que vimos no último artigo
* Retorna uma instância de `WSGIHandler`
{{< /web >}}
{{< book >}}
* Chama `django.setup` que faz toda a configuração de inicialização que vimos no último capítulo
* Retorna uma instância de `WSGIHandler`
{{< /book >}}

Como podemos imaginar, a `WSGIHandler` está desenhada para fazer a interface de porta de entrada do servidor da Web funcionar, mas também é uma subclasse de `django.core.handlers.base.BaseHandler`. Esta classe manipuladora de base é onde a Django lida com a configuração do intermediário.

A manipuladora de base inclui um método `load_middleware`. Este método tem a função de iterar por todos os intermediários listados na nossa configuração `MIDDLEWARE`. Ao iterar através da `MIDDLEWARE`, o objetivo principal do método é incluir cada intermediário na *cadeia de intermediário*.

> A cadeia de intermediário é o rebuçado da Django.

A cadeia representa cada instância do intermediário da Django, em camadas, para produzir o efeito desejado de permitir que uma requisição e uma resposta passem por cada intermediário.

Além de construir a cadeia de intermediário, a `load_middleware` deve fazer algumas outras configurações importantes.

{{< web >}}
* O método lida com intermediário síncrono e assíncrono. Conforme a Django aumenta o seu suporte ao desenvolvimento assíncrono, os internos da Django precisam gerir as diferenças. A `load_middleware` faz algumas alterações dependendo do que esta pode descobrir sobre uma classe intermediária.
* O método regista um intermediário com determinados *conjuntos* de intermediário com base na presença de vários métodos gatilhos. Falaremos sobre estas funções gatilhos mais adiante neste artigo.
{{< /web >}}
{{< book >}}
* O método lida com intermediário síncrono e assíncrono. Conforme a Django aumenta o seu suporte ao desenvolvimento assíncrono, os internos da Django precisam gerir as diferenças. A `load_middleware` faz algumas alterações dependendo do que esta pode descobrir sobre uma classe intermediária.
* O método regista um intermediário com determinados *conjuntos* de intermediário com base na presença de vários métodos gatilhos. Falaremos sobre estas funções gatilhos mais adiante neste capítulo.
{{< /book >}}

Isto explica a estrutura do intermediário e como todo intermediário interage com o ciclo de vida da requisição e da resposta, mas o que o intermediário faz?

Podemos utilizar o intermediário para uma grande variedade de objetivos. Devido à cadeia de intermediário, uma requisição de protocolo de hipertexto bem-sucedida passará por todos os intermediários. Esta propriedade do intermediário torna-o ideal para código que queremos executar globalmente para o nosso projeto de Django.

Por exemplo,
{{< web >}}
pensemos no nosso último artigo sobre [Autenticação do Utilizador]({{< ref "/understand-django/2020-11-04-user-authentication.pt.md" >}}).
Naquele artigo,
{{< /web >}}
{{< book >}}
pensemos no nosso último capítulo, Naquele capítulo,
{{< /book >}}
observamos que o sistema de autenticação da Django é dependente da `AuthenticationMiddleware`. Este intermediário tem o trabalho individual de adicionar uma propriedade `user` a cada objeto de `HttpRequest` que passa pela aplicação antes que a requisição chegue ao código de visualização.

A `AuthenticationMiddleware` destaca algumas qualidades boas do intermediário na Django.

* Idealmente, um intermediário deve ter um objeto objetivo restrito e individual.
* Um intermediário deve executar uma quantidade mínima de código.

*Por quê?* Mais uma vez, a resposta está relacionada com a cadeia de intermediário. Uma vez que a requisição de protocolo de hipertexto passará por todos os intermediários da cadeia, podemos ver que *cada intermediário será executado para cada requisição*. Por outras palavras, cada intermediário tem um custo adicional de desempenho para cada requisição.

*Há* uma exceção a este comportamento da cadeia. Um intermediário no início da cadeia pode impedir a execução de intermediário mais tarde na cadeia.

Por exemplo, o `SecurityMiddleware` é o primeiro na cadeia de intermediário predefinida de um projeto gerado pelo `startproject`. Este intermediário está desenhado para efetuar algumas verificações para manter a aplicação segura. Uma verificação consiste em procurar uma conexão segura (ou seja, uma requisição que utilize o protocolo de hipertexto seguro) se o protocolo de hipertexto seguro estiver configurado. Se uma requisição chegar à aplicação e utilizar o protocolo de hipertexto em vez do protocolo de hipertexto seguro, o intermediário pode retornar um `HttpResponsePermanentRedirect` que redireciona para o mesmo endereço de localização de recurso com `https://` e impede a execução do resto da cadeia.

Para além deste comportamento excecional no intermediário, é importante lembrarmos que, na maioria das circunstâncias, cada intermediário executar-se-á para cada requisição. Devemos ter em conta este aspeto do desempenho quando criarmos o nosso próprio intermediário.

Agora estamos prontos para aprender sobre como podemos criar o nosso próprio intermediário!

## Como Posso Escrever O Meu Próprio Intermediário Personalizado?

Assumiremos que encontrámos um bom caso para criar um intermediário. Precisamos de algo que aconteça com todos os pedidos e que esta funcionalidade tenha um objetivo restrito.

Podemos começar com uma definição de intermediário vazia. No meu exemplo, coloraremos o intermediário num ficheiro `middleware.py`:

```python
# project/middleware.py
class AwesomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(
            request
        )
```

Depois de criar o intermediário, adicionamo-lo às nossas definições:

```python
# project/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    ...,
    'middleware.AwesomeMiddleware',
]
```

*E pronto!* Este intermediário personalizado não faz nada, exceto diminuir ligeiramente o desempenho porque é uma chamada de método adicional em cada requisição. Visto que coloquei o intermediário no final da lista `MIDDLEWARE`, este será o último intermediário a executar antes duma visão receber uma requisição e o primeiro intermediário com a oportunidade de processar uma resposta.

Podemos explicar como esta classe funciona:

* O método `__init__` obtém um objeto executável que é de maneira convencional chamado de `get_response`. O intermediário é criado durante `load_middleware` e o objeto executável é uma parte chave do que faz cadeia de intermediário funcionar. O objeto executável chamará o intermediário seguinte ou a visão, dependendo da posição do intermediário atual na cadeia.
* O método `__call__` transforma a própria instância do intermediário num objeto executável. O método deve chamar `get_response` para garantir que a cadeia não seja interrompida.

Se quisermos fazer um trabalho adicional, podemos fazer alterações ao método `__call__`. Podemos modificar `__call__` para processar alterações antes ou depois da chamada de `get_response`. No ciclo de vida do pedido ou resposta, as alterações anteriores a `get_response` ocorrem antes da visão ser chamada, enquanto as alterações posteriores tratar da própria `response` ou de qualquer outro processamento posterior ao pedido.

Digamos que queremos que o nosso intermediário de exemplo registe algumas informações de tempo. Podemos atualizar o código para que fique com o seguinte aspeto:

```python
# project/middleware.py
import logging
import time

logger = logging.getLogger(__name__)


class AwesomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        before_timestamp = time.time()
        logger.info(
            f"Tracking {before_timestamp}"
        )

        response = self.get_response(request)

        after_timestamp = time.time()
        delta = after_timestamp - before_timestamp
        logger.info(
            f"Tracking {after_timestamp} for a delta of {delta}"
        )

        return response
```

Nós ainda não falámos sobre o registo mas podemos entendê-lo como a gravação de mensagens para uma fonte de saída, como um ficheiro.

Este exemplo atua como um monitor de desempenho rudimentar. Se quiséssemos medir o tempo de resposta duma visão, este intermediário fá-lo-ia. A desvantagem é que não nos diz *qual* visão é registada. Ei, deixa-me em paz, este é um exemplo ridículo! 🤪

Esperemos que estejamos a começar a ver como o intermediário pode ser útil. Mas espera! Há mais coisas que o intermediário pode fazer.

Um intermediário de Django pode definir qualquer um dos três diferentes métodos gatilhos que a Django executará em diferentes partes do ciclo de vida do pedido ou resposta. Os três métodos são:

* `process_exception` — Esta função gatilho é chamada sempre que uma visão levantar uma exceção. Isto poderia incluir uma exceção não capturada da visão, porém a função gatilho também receberá exceções, intencionalmente levantadas, como `Http404`.
* `process_template_response` — Esta função gatilho é chamada sempre que uma visão retornar uma resposta que se parece com uma resposta do modelo de marcação (ou seja, o objeto da resposta tem um método `render`).
* `process_view` — Esta função gatilho é chamada imediatamente antes da visão.

Voltando ao nosso exemplo ridículo, podemos torná-lo menos ridículo usando a função gatilho `process_view`. Veremos o que podemos fazer:

```python
# project/middleware.py
import logging
import time

logger = logging.getLogger(__name__)


class AwesomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        before_timestamp = time.time()
        logger.info(
            f"Tracking {before_timestamp}"
        )

        response = self.get_response(request)

        after_timestamp = time.time()
        delta = after_timestamp - before_timestamp
        logger.info(
            f"Tracking {after_timestamp} for a delta of {delta}"
        )

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        logger.info(
            f"Running {view_func.__name__} view"
        )
```

Agora, o nosso intermediário usa as capacidades de reflexão da Python para registar o nome da visão. Se acessarmos a administração da Django com um utilizador não autenticado, o histórico de registo pode registar algo como:

```text
Tracking 1607438038.232886
Running login view
Tracking 1607438038.261855 for a delta of 0.02896881103515625
```

Este intermediário ainda poderia beneficiar-se de muito polimento, mas podemos como as funções gatilhos possibilitam que um intermediário tenha uma funcionalidade mais avançada.

Como um exemplo do intermediário `process_exception`, consideremos um serviço que coleta e reporta exceções para rastrear a saúde da nossa aplicação. Existem muitos destes serviços, como o {{< extlink "https://rollbar.com/" "Rollbar" >}} e o {{< extlink "https://sentry.io/welcome/" "Sentry" >}}. Sou um utilizador da Rollbar, por isto comentarei esta questão. Podemos ver no {{< extlink "https://github.com/rollbar/pyrollbar/blob/8d116a374f2c54da886972f7da7c289e317bbd8a/rollbar/contrib/django/middleware.py#L268" "código da pyrollbar" >}} que o serviço envia informações de exceção da função gatilho `process_exception` para o Rollbar através da função `rollbar.report_exc_info`. Sem intermediário, capturar e reportar exceções seria *significativamente* mais difícil.

Quer saber mais sobre as funções gatilhos? Podemos ver todos os detalhes sobre estas funções gatilhos na {{< extlink "https://docs.djangoproject.com/en/4.1/topics/http/middleware/#other-middleware-hooks" "documentação do intermediário" >}}.

## Que Intermediário a Django Inclui?

Analisámos o modelo mental do intermediário e todos os detalhes do funcionamento de um intermediário específico. Qual intermediário a Django inclui na abstração?

A lista completa de intermediário embutido está disponível na {{< extlink "https://docs.djangoproject.com/en/4.1/ref/middleware/" "referência do intermediário" >}}. Descreverei o que acho que são as classes de intermediário mais comuns e úteis que a Django inclui.

{{< web >}}
* `AuthenticationMiddleware` — Já encontrámos este intermediário na exploração do sistema de autenticação. O trabalho deste intermediário é adicionar o atributo `user` a um objeto `HttpRequest`. Este pequeno atributo `user` é responsável por muitas das funcionalidades do sistema de autenticação.
* `CommonMiddleware` — O intermediário comum é um pouco estranho. Este intermediário lida com uma variedade de definições da Django para controlar certos aspetos do nosso projeto. Por exemplo, a definição `APPEND_SLASH` redirecionará um pedido como `example.com/accounts` para `example.com/accounts/`. Esta configuração só funciona se o `CommonMiddleware` estiver incluído.
* `CsrfViewMiddleware` — No artigo de formulários, mencionei o símbolo de falsificação de pedidos entre sítios (ou CSRF). Relembraremos que se trata duma funcionalidade de segurança que ajuda a proteger o nosso projeto contra origens maliciosas que pretendem enviar dados incorretos ao nosso sítio. O `CsrfViewMiddleware` garante que o símbolo de falsificação de pedidos entre sítios está presente e é válido nas submissões de formulários.
* `LocaleMiddleware` — Este intermediário serve para tratar das traduções se optarmos por internacionalizar o nosso projeto.
* `MessageMiddleware` — O intermediário de mensagens é para “mensagens instantâneas”. Estas são mensagens pontuais que provavelmente veríamos após submeter um formulário, embora possam ser utilizadas em muitos lugares. Falaremos mais sobre as mensagens quando chegarmos ao tema das sessões.
* `SecurityMiddleware` — O intermediário de segurança inclui uma série de verificações para ajudar a manter o nosso sítio seguro. Vimos o exemplo de verificação do protocolo seguro de hipertexto (HTTPS) anteriormente neste artigo. Este intermediário também lida com coisas como infiltração entre sítios (XSS), segurança de transporte restrito do protocolo de hipertexto (HSTS), e uma série de outros acrónimos (😛) que serão vistos no futuro tópico de segurança.
* `SessionMiddleware` — O intermediário de sessão gere o estado da sessão para um utilizador. As sessões são cruciais para muitas partes da Django, como a autenticação de utilizadores.
{{< /web >}}
{{< book >}}
* `AuthenticationMiddleware` — Já encontrámos este intermediário na exploração do sistema de autenticação. O trabalho deste intermediário é adicionar o atributo `user` a um objeto `HttpRequest`. Este pequeno atributo `user` é responsável por muitas das funcionalidades do sistema de autenticação.
* `CommonMiddleware` — O intermediário comum é um pouco estranho. Este intermediário lida com uma variedade de definições da Django para controlar certos aspetos do nosso projeto. Por exemplo, a definição `APPEND_SLASH` redirecionará um pedido como `example.com/accounts` para `example.com/accounts/`. Esta configuração só funciona se o `CommonMiddleware` estiver incluído.
* `CsrfViewMiddleware` — No capítulo de formulários, mencionei o símbolo de falsificação de pedidos entre sítios (ou CSRF). Relembraremos que se trata duma funcionalidade de segurança que ajuda a proteger o nosso projeto contra origens maliciosas que pretendem enviar dados incorretos ao nosso sítio. O `CsrfViewMiddleware` garante que o símbolo de falsificação de pedidos entre sítios está presente e é válido nas submissões de formulários.
* `LocaleMiddleware` — Este intermediário serve para tratar das traduções se optarmos por internacionalizar o nosso projeto.
* `MessageMiddleware` — O intermediário de mensagens é para “mensagens instantâneas”. Estas são mensagens pontuais que provavelmente veríamos após submeter um formulário, embora possam ser utilizadas em muitos lugares. Falaremos mais sobre as mensagens quando chegarmos ao tema das sessões.
* `SecurityMiddleware` — O intermediário de segurança inclui uma série de verificações para ajudar a manter o nosso sítio seguro. Vimos o exemplo de verificação do protocolo seguro de hipertexto (HTTPS) anteriormente neste capítulo. Este intermediário também lida com coisas como infiltração entre sítios (XSS), segurança de transporte restrito do protocolo de hipertexto (HSTS), e uma série de outros acrónimos (😛) que serão vistos no futuro tópico de segurança.
* `SessionMiddleware` — O intermediário de sessão gere o estado da sessão para um utilizador. As sessões são cruciais para muitas partes da Django, como a autenticação de utilizadores.
{{< /book >}}

Como podemos ver nesta lista incompleta, o intermediário da Django pode fazer muito para enriquecer o nosso projeto numa grande variedade de maneiras. O intermediário é um conceito extremamente poderoso para projetos de Django e uma ótima ferramenta para estender o tratamento de pedidos da nossa aplicação.

Lembremos que o intermediário tem um custo de desempenho, pelo que devemos evitar a tentação de colocar demasiadas funcionalidades na cadeia de intermediário. Desde que estejamos conscientes das vantagens e desvantagens, o intermediário é uma ótima ferramenta para o nosso cinto de ferramentas.

## Sumário

{{< web >}}
Neste artigo,
{{< /web >}}
{{< book >}}
Neste capítulo,
{{< /book >}}
vimos o sistema de intermediário da Django.

Discutimos:

* O modelo mental para considerar o intermediário
* Como escrever o nosso próprio intermediário
* Algumas classes de intermediário que vêm com a Django

{{< web >}}
Da próxima vez, analisaremos os ficheiros estáticos.
{{< /web >}}
{{< book >}}
No próximo capítulo, abordaremos os ficheiros estáticos.
{{< /book >}}
Os ficheiros estáticos são todas as imagens, `.js`, `.css`, ou outros tipos de ficheiros servidos pela nossa aplicação, sem modificações, a um utilizador.

Precisamos de entender:

* Como configurar os ficheiros estáticos
* A maneira de trabalhar com os ficheiros estáticos
* Como lidar com os ficheiros estáticos ao implantar o nosso sítio na Internet

{{< web >}}
Se gostarias de seguir juntamente com a série, sinta-se a vontade para inscrever-se no meu boletim informativo onde anuncio todos os meus novos conteúdos. Se tiveres outras questões, podes contactar-me na X onde sou o {{< extlink "https://x.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;

A tradução deste artigo para o português é cortesia de Nazaré Da Piedade.
