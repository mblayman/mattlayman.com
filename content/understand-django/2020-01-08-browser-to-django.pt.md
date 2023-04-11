---
title: "Do Navegador à Django"
description: >-
    A Django ajuda-te a construir aplicações de Web em Python. Como ela funciona? Nesta série, exploraremos a Django desde a parte de cima até o fundo para mostrar-te como construir a aplicação de Web que tens desejado. Começaremos desde o princípio com o navegador.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django

---

É possível que tenhas ouvido falar sobre a {{< extlink "https://www.djangoproject.com/" "Django" >}} e que pode ajudar-te a construir aplicações de Web. Tu podes ser principiante para Python, novo para o desenvolvimento da web, ou novo para a programação.

{{< web >}}
Esta nova série, [Entendendo a Django]({{< ref "/understand-django/_index.pt.md" >}}), mostrar-te-á sobre o que a Django se trata. Ao longo desta série,
{{< /web >}}
{{< book >}}
Este livro mostrar-te-á sobre o que a Django se trata. Nos capítulos seguintes,
{{< /book >}}
Eu revelarei como a Django é uma ferramenta poderosa que pode desbloquear o potencial de qualquer um interessado em criar aplicações na internet. A Django é usada por empresas como Instagram, Eventbrite, Disqus, e Udemy, e é também um excelente ferramenta para indivíduos como tu.

Iremos tomar uma abordagem de alto nível para aprender a Django. No lugar de começar desde fundo com todos os pedaços da Django, dar-te-ei um grande panorama, depois explorar cada camada com mais detalhes para revelar o quanto a Django faz pelos programadores e o poder que a Django tem nos bastidores.

Começaremos desde a parte mais de cima da experiência de internet do utilizador: no navegador da web.

{{< understand-django-series-pt "browser" >}}

## Fazendo Uma Requisição de Navegador

A Django é uma abstração de web, mas o que diabo isto significa?
Como é que as aplicações de web funcionam? Eu não serei capaz de caminhar através de todos os detalhes,
{{< web >}}
mas esta publicação
{{< /web >}}
{{< book >}}
mas este capítulo
{{< /book >}}
estabelecerá as migalhas para construir o teu entendimento. Olharemos para a maneira que o teu navegador da web requisita os dados da internet e a "canalização" necessária para fazer isto funcionar. Equipado com as palavras-chaves e acrónimos encontrados neste capítulo, serias capaz de começar a tua própria investigação sobre testes tópicos.

A internet funciona compensando um desejo do utilizador por enviar e receber informação. Esta "informação" toma muitas formas diferentes. Ela pode ser:

* Vídeos de gato na YouTube
* Incoerências políticas de media social
* Perfis de outras pessoas em locais de encontro

Qualquer coisa que as pessoas estiverem a procura, a informação é transferida através dos mesmos mecanismos. No dizer da internet, todos os tipos de informação e dado caiem sobre o mesmo nome de *recurso*.

A maneira que recebemos os recursos são com os localizadores de recursos uniformes ou URL {{< extlink "https://en.wikipedia.org/wiki/URL" "Uniform Resource Locators" >}}, para abreviar. Tu sabes o que as URLs são, ainda que não as conhecias pelo nome.
* {{< extlink "https://en.wikipedia.org/" "https://en.wikipedia.org/" >}}
* {{< extlink "https://www.djangoproject.com/" "https://www.djangoproject.com/" >}}
* {{< extlink "https://www.mattlayman.com/img/django.png" "https://www.mattlayman.com/img/django.png" >}}

Estes são todos os exemplos de URLs. Frequentemente os chamamos de endereços de web porque são muito parecidos com os endereços postais. Uma URL é o endereço de algum recurso na internet. Quando pressionas *Enter* na barra de endereço do teu navegador, estás a dizer "Navegador faz o favor de ir buscar-me isto." Em outras palavras, fazemos uma *requisição* a partir do navegador. Esta requisição inicia uma grande corrente de eventos a partir do teu navegador para o local na web naquela URL para que o recurso do local possa ser visto pelos teus olhos.

O que é esta corrente de eventos? *Montes de coisas estão lá!* Omitiremos muitas das camadas nesta discussão porque suponho que não planeias descer até o nível de como os sinais elétricos funcionam nos cabos de rede. No lugar disto, vamos nos focar em duas partes primárias da corrente por agora: **DNS** e **HTTP**.

### Nomes Nomes Nomes

Uma URL representa um recurso que queres a partir da internet. Como é que a internet sabe de onde o recurso vem? É onde o DNS entra. DNS significa {{< extlink "https://en.wikipedia.org/wiki/Domain_Name_System" "Domain Name System" >}} ou Sistema de Nome de Domínio.

Em um endereço postal (pelo menos a partir de uma perspetiva dos Estados Unidos da América), existe a rua, cidade, e estado. Nós o escrevemos como:

```text
123 Main St., Springfield, IL
```

Este endereço vai desde o mais estreito ao mais largo. 123 Main St. é na cidade de Springfield no estado de Illinois (IL).

Do mesmo modo, uma URL ajusta-se em um formato parecido:

```text
www.example.com
```

A terminologia é diferente, mas o conceito de ir do mais estreito ao largo é o meso. Cada pedaço entre os pontos finais é um tipo de *domínio*. Vamos olhá-los em ordem inversa.

* `com` é considerado um {{< extlink "https://en.wikipedia.org/wiki/Top-level_domain" "Top Level Domain" >}}, TDL ou Domínio de Alto Nível. Os domínios de alto nível são cuidadosamente administrados por um grupo especial chamado {{< extlink "https://www.icann.org/" "ICANN" >}}.
* `example` é o nome de domínio. Isto é a identidade primária de um serviço na internet embora seja o identificador específico que um utilizador provavelmente reconheceria.
* `www` é considerado o *subdomínio* de um domínio. Um domínio pode ter muitos destes como `www`, `m`, `mail`, `wiki` ou tudo aquilo que um proprietário de domínio quiser nomeia-los. Os subdomínios também podem ser mais de um nível de profundidade assim `a.b.example.com` é válido, e `a` é um subdomínio de `b.example.com` e `b` é um subdomínio de `example.com`.

Os nomes de domínios *não* são como os computadores comunicam. O nome de domínio é algo "amigável" para um humano. Os sistemas de rede são desenhados para funcionar com números assim estes nomes de domínio devem ser traduzidos em algo que o sistema de rede possa usar. Para fazer isto, a internet usa um sistema de servidores de DNS para atuar como camada de tradução entre os nomes de domínio e os números que as redes de computadores usam. Um servidor é um computador de propósito especial desenhado para fornecer serviços para outros dispositivos chamados de clientes.

Talvez tens visto estes números de rede. Os números são chamados de endereços de IP, abreviação para endereços de {{< extlink "https://en.wikipedia.org/wiki/Internet_Protocol" "Internet Protocol" >}} ou Protocolos de Internet. Os exemplos comuns incluiriam:

* `127.0.0.1` como o endereço que o teu computador tem *para si* na sua rede interna.
* `192.168.0.1` como um endereço padrão que um roteador de cada pode usar.

Os exemplos de endereço de IP acima são especiais porque estes endereços são especialmente denominados {{< extlink "https://en.wikipedia.org/wiki/Subnetwork" "subnetworks" >}} ou  subredes, mas definiremos esta tangente à parte. Tu podes vasculhar mais a fundo neste tópico por conta própria se gostarias.

As redes privadas têm endereços de IP como os dois exemplos que listei acima. As máquinas em redes públicas também têm endereços de IP. Por exemplo, `172.253.115.105` é um endereço de IP para `www.google.com` no momento desta escrita.

Se gostarias de compreender o endereço de IP de um nome de domínio, podes instalar uma ferramenta popular chamada `dig`. Eu descobri o endereço de IP da Google executando este comando:

```bash
dig www.google.com
```

O sistema pega os nomes de domínio e preserva uma tabela de roteamento distribuído dos nomes para o endereço de IP através da coleção de servidores de DNS. **Espera, o quê?**

Os servidores de DNS empilham-se em uma hierarquia gigantesca. Quando o teu navegador faz uma requisição, ele pedi o servidor de DNS mais próximo da tua máquina para o endereço de IP do nome de domínio que requisitaste. O servidor de DNS mantém uma tabela de consulta de nomes de domínio para os endereços de IP por um período de tempo. Se o nome de domínio não estiver na tabela, ele pode pedir um outro servidor de DNS numa cadeia que continuará a procurar pelo endereço de IP do domínio. Isto conduz à um alguns resultados:

* Se nenhum dos servidores puder encontrar o domínio, o navegador desiste e mostra-te uma mensagem como "Hum. Estamos tendo problemas em encontrar este local." (a partir da página Não Encontrada do servidor do Firefox).
* Se o navegador receber o endereço de IP a partir do servidor de DNS, ele pode prosseguir com a requisição.

A hierarquia é gigantesca, mas é extensa, não profunda. Em outras palavras, existem muitas máquinas que participam no DNS (como o teu roteador de casa), mas o número de ligações na cadeia para fazer uma requisição desde o teu computador aos servidores de raiz no sistema é relativamente pequeno.

Isto é simplificado para excluir algumas das partes defeituosas do DNS. A página da Wikipedia que liguei no princípio desta seção cobre o DNS em detalhes ainda maiores se estiveres interessado em aprender mais.

### O Que Nós Estamos a Enviar?

O outro pedaço essencial que precisamos de explorar é o HTTP, ou o {{< extlink "https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol" "Hypertext Transfer Protocol" >}} ou Protocolo de Transferência de Hipertexto. Esta parte da comunicação de internet descreve como o conteúdo é transferido entre navegadores e servidores. O protocolo usa um formato padrão e um conjunto de comandos para comunicar. Alguns dos comandos comuns são:

* `GET` - Pedi um recurso existente
* `POST` - Cria ou atualiza um recurso
* `DELETE` - Elimina um recurso
* `PUT` - Atualiza um recurso

Uma requisição de HTTP é como enviar um ficheiro de texto sobre a rede. Se visitares a minha página em `https://www.mattlayman.com/about/`, o teu navegador enviará uma requisição como:

```http
GET /about/ HTTP/1.1
Host: www.mattlayman.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
```

Existem outras partes que tenho omitido, mas esta permite-nos começar. A linha acima fornece o comando, o caminho para um recurso particular sobre a página (por exemplo, `/about/`, e uma versão do protocolo para usares).

Depois da primeira linha existe uma lista de *cabeçalhos*. Os cabeçalhos são dados adicionais que dizem ao servidor mais sobre a requisição. O cabeçalho `Host` é obrigatório porque nomeia a página à extrair (mais de uma página pode existir no mesmo endereço de IP), mas qualquer outro cabeçalho é opcional.

No exemplo, também mostrei o cabeçalho `Accept`. Este cabeçalho diz ao servidor qual é o tipo de conteúdo o navegador pode receber como resposta. Existem outros cabeçalhos que podem dizer à um servidor que mais ele deveria "saber". Estes cabeçalhos podem:

* Indicar qual é o tipo de navegador que está fazer o requisição (isto é o cabeçalho `User-Agent`).
* Dizer quando o recurso foi requisitado anteriormente para determinar se uma nova versão deveria ser retornada (o cabeçalho `Last-Modified`).
* Declarar que o navegador pode receber dados compactados os quais pode descompactar depois de receber para guardar sobre a largura de banda (o cabeçalho `Accept-Encoding`).

A maioria dos cabeçalhos são manipulados automaticamente pelos navegadores e servidores, mas veremos exemplos onde queremos usar estes cabeçalhos nós mesmos então é bom saber que existem.

## Servindo Uma Resposta

É hora de falar de Django! Agora temos uma ideia grosseira do que os navegadores fazem. Um navegador envia uma requisição de HTTP para uma URL que é resolvida pelo sistema de DNS. Esta requisição chega em um servidor que está conectado ao endereço de IP do nome de domínio. A Django mora em tal servidor e é responsável por responder as requisições com uma *resposta* de HTTP.

A resposta é o que o utilizador do navegador queria. As respostas podem ser imagens, páginas de web, vídeos, ou quaisquer formatos que um navegador puder manipular.

Antes da Django puder lidar com uma requisição, existe mais uma camada à atravessar: o servidor de web da Python.

### Onde a HTTP Encontra a Python

Um servidor de web é um software sobre uma máquina desenhada para lidar com as requisições de HTTP do exterior. Algumas vezes esta terminologia pode ser confusa porque as pessoas também podem aplicar o nome "servidor de web" à uma *máquina* inteira que está a servir o tráfego de web. Neste exemplo, estou a referir-me a um programa real ouvindo e respondendo às requisições de web.

Uma abstração de web de Python como Django executa com um servidor de web. O papel do servidor de web é traduzir a requisição de HTTP crua em um formato que a abstração entenda. No mundo de Python, existe um formato específico usado para que qualquer servidor de web possa falar com qualquer abstração de web de Python. Este formato é o {{< extlink "https://wsgi.readthedocs.io/en/latest/what.html" "Web Server Gateway Interface" >}} ou Interface de Portal de Servidor de Web, WSGI em Inglês (o qual é frequentemente pronunciado como "wiz-gee").

{{< web >}}
{{< figure src="/img/2020/wsgi.jpg" caption="Web Server Gateway Interface" >}}
{{< /web >}}

A WSGI ativa servidores de web comum como {{< extlink "https://gunicorn.org/" "Gunicorn" >}}, {{< extlink "https://uwsgi-docs.readthedocs.io/en/latest/" "uWSGI" >}}, ou {{< extlink "https://modwsgi.readthedocs.io/en/develop/" "mod_wsgi" >}} para comunicar com abstrações de web de Python como a Django, {{< extlink "https://palletsprojects.com/p/flask/" "Flask" >}}, ou {{< extlink "https://trypyramid.com/" "Pyramid" >}}. Se realmente quiseres saber mais a fundo, podes explorar todos os detalhes deste formato no {{< extlink "https://www.python.org/dev/peps/pep-3333/" "PEP 3333" >}}.

### A Tarefa da Django

Assim que o servidor de web enviar uma requisição, a Django precisa de retornar uma *resposta*. O teu papel como um programador de Django é definir os recursos que estarão disponíveis a partir do servidor. Isto significa que deves:

* Descrever o conjunto de URLs para os quais a Django reagirá.
* Escrever o código que alimenta estas URLs e retornam a resposta.

Existe uma tonelada para desempacotar nestas declarações assim exploraremos os tópicos individualmente  
{{< web >}}
nos futuros artigos.
{{< /web >}}
{{< book >}}
nos futuros capítulos.
{{< /book >}}
Por agora, espero que tenhas uma ideia de como uma requisição sai do teu navegador para um máquina executando a Django. 
{{< web >}}
{{< figure src="/img/2020/request-response.jpg" caption="Vida de uma requisição de navegador" >}}
{{< /web >}}

{{< web >}}
Este artigo está relativamente livre
{{< /web >}}
{{< book >}}
Este capítulo está relativamente livre
{{< /book >}}
de exemplos de código, e por boa razão. Já existem conceitos suficientes para debater-se e não queria adicionar complexidade de código sobre isto. Escrever este código será o foco 
{{< web >}}
desta séries de artigos
{{< /web >}}
{{< book >}}
deste livro 
{{< /book >}}
então poderemos responder questões como:

* Como é que construímos páginas de web e damos a tudo uma aparência comum?
* Como é que os utilizadores podem interagir com uma aplicação e enviar dados com os quais a aplicação possa reagir?
* Como é que a Django armazena e recupera dos dados para tornar os páginas dinâmicas?
* Quem pode acessar a aplicação e como é que este acesso é controlado?
* Que segurança precisamos de adicionar para garantir que a informação dos nossos utilizadores está segura e privada?

A Django tem respostas para todas estas questões e muito mais. A filosofia da Django é de incluir todos os pedaços necessários para fabricar uma aplicação completa de web para a internet. Esta filosofia de "baterias inclusas" é o que torna a Django tão poderosa. A mesma filosofia também pode fazer a Django parecer avassaladora. 
{{< web >}}
O meu objetivo nesta série é introduzir pedaço após pedaço
{{< /web >}}
{{< book >}}
O meu objetivo neste livro é introduzir pedaço após pedaço 
{{< /book >}}
para construir o teu entendimento de Django para que assim possas ser produtivo e possas construir a tua própria aplicação de web. 

{{< web >}}
No próximo artigo, o nosso foco será nestas URLs para as quais a nossa aplicação responderá. Nós veremos:

* Como declarar as URLs.
* Como agrupar conjuntos de URLs relacionadas.
* Como extrair informação das URLs que possa ser usada pelo código que retorna respostas.

Se gostarias de seguir com a série, podes inscrever-te no meu boletim informativo onde anuncio todos os novos conteúdo. Se tiveres outras questões, podes contactar-me online na Twitter onde sou o {{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
{{< /web >}}

Finalmente, existe mais um tópico de bónus...

## Começar a Configurar a Django

{{< web >}}
Na série,
{{< /web >}}
{{< book >}}
No livro,
{{< /book >}}
veremos muitos exemplos de código, mas não configuraremos a Django desde zero repetidamente. As seguintes instruções de configuração ajudar-te-ão a começar com cada exemplo futuro.

> O objetivo desta seção não é ser uma descrição fidedigna de como configurar o teu ambiente de Python. Eu estou a assumir que tens algum conhecimento de como executar código de Python. Se precisares de um guia mais descritivo, eu sugeriria o artigo [Instalando a Python 3](https://training.talkpython.fm/installing-python) do Michael Kennedy e o [Compêndio sobre Ambientes Virtuais](https://realpython.com/python-virtual-environments-a-primer/) da Real Python. Estes artigos entram na discussão da configuração muito mais do que estou a fazer justiça aqui.

Usaremos um terminal para executar os comandos. Windows, MacOS, e Linux são todos um pouco diferentes. Estou a mostrar o terminal de MacOS porque é o que uso. O sinal de dólar (`$`) é o carácter inicial tradicional para um terminal de bash então quando eu listar os comandos, não digite este carácter. Tentarei dar indicações e realçar as diferenças quando puder.

Nós precisamos de um lugar para colocar o nosso trabalho.
{{< web >}}
Já que esta séria é chamada de "Entendendo a Django"
{{< /web >}}
{{< book >}}
Já que este livro é chamado de "Entendendo a Django,"
{{< /book >}}
Usarei este nome, mas em Inglês. Tu podes nomear o teu projeto de maneira diferente se preferires:

```bash
$ mkdir understand-django
$ cd understand-django
```

A seguir, instalaremos a Django em um ambiente virtual assim mantemos as dependências do nosso projeto separadas do resto dos pacotes de Python instalados na nossa máquina. Ter esta separação de outros pacotes instalados é uma boa maneira de evitar conflitos com outros projetos de Python que podes estar a executar no teu computador.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Isto pode mudar o pronto do teu terminal para que agora comece com `(venv)` para dizer-te que o ambiente virtual está em uso. Outros sistemas operativos ativam o ambiente virtual de maneira diferente. Consulte a {{< extlink "https://docs.python.org/3/library/venv.html" "documentação do módulo venv" >}} por mais informações sobre o teu sistema operativo.

Agora podes instalar a Django, e o código da abstração Django será adicionado ao ambiente virtual:

```bash
(venv) $ pip install Django
```

A Django inclui algumas ferramentas que podemos usar começar um projeto rapidamente. Executaremos um único comando gerar o projeto:

```bash
(venv) $ django-admin startproject project .
```

Este comando diz "começar um projeto *nomeado* 'project'" no diretório atual (`.`)." A escolha de "project" como nome é intencional. `startproject` criará um diretório nomeado `project` que conterá vários ficheiros que usarás para configurar o teu aplicação de web inteira. Tu podes nomear o teu projeto como queiras, mas considero que usar o nome genérico torna a minha vida muito mais fácil visto que alterno entre diferentes aplicações de web em Django. Eu sempre sei onde os ficheiros relacionados ao meu projeto residem. Depois daquele comando estiver terminado, deves ter alguns ficheiros e uma estrutura que parece-se com:

```bash
(venv) $ ls
manage.py project venv
```

Repara que, além do diretório `project`, a Django criou um ficheiro `manage.py`. Este ficheiro é um programa que ajudar-te-á a interagir com a Django. Aprenderás mais sobre `manage.py` a medida que formos avançando. Para verificar se as bases estão a funcionar, experimente:

```bash
(venv) $ python manage.py runserver
...
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Quando inicializares o servidor de web, provavelmente verás uma mensagem como:

```text
You have ## unapplied migration(s).
Your project may not work properly
until you apply the migrations for app(s):
<a list of names here>
```

Exploraremos o tópico de migrações depois, então não te preocupes com aquela mensagem por agora.

Se copiares e colares aquela URL (por exemplo, `http://127.0.0.1:8000/`) para o teu navegador, deves ver uma página inicial de boas-vindas! Além disto, se olhares para trás no teu terminal, encontrarás `"GET / HTTP/1.1"`. Esta mensagem está a indicar que a Django respondeu à uma requisição de HTTP. Espetacular!

A outra coisa que precisamos é de uma aplicação ou "app". Isto é (talvez confusamente) o nome de um componente de Django num projeto. O que precisas de lembrar é que um projeto de Django *contém* um ou mais aplicações. As aplicações segurarão a maior parte do teu código que precisas de escrever quando trabalhas com a Django.

Depois tens que parar o servidor, podes criar uma aplicação com a qual trabalhar através do seguinte comando:

```bash
(venv) $ python manage.py startapp application
```

Isto gerará um outro conjunto de ficheiros que segue a estrutura padrão de um componente de aplicação de Django dentro de um diretório chamado `application`. Este exemplo usa um nome aborrecido, mas ao contrário de `project`, deverias escolher um nome que faça sentido para a tua aplicação de web (por exemplo, `movies` seria um bom nome para uma aplicação de web que é sobre cinema). Todos estes ficheiros serão discutidos em detalhes num tópico futuro.

Finalmente, devemos prender esta aplicação nas definições de projeto da Django. As definições de projeto permitem-te configurar a Django para ajustar-se às tuas necessidades. Abra `project/settings.py`, encontre `INSTALLED_APPS` e anexe o nome da tua aplicação à lista assim ela parece-se com isto:

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

Isto é o quanto precisamos para avançar para começar com os nossos exemplos de código
{{< web >}}
no próximo artigo.
{{< /web >}}
{{< book >}}
no próximo capítulo.
{{< /book >}}
`application` será a nossa aplicação de referência. O código nos tópicos futuros não é um passo-a-passo, mas usarei a `application` ocasionalmente para orientar-te onde encontrarias os ficheiros na tua própria aplicação de web de Django. Nós temos um projeto de Django que podemos executar localmente para testagem e está configurado com a sua primeira aplicação.
{{< web >}}
Até à próxima para falarmos sobre a criação de URLS e recursos!
{{< /web >}}
