---
title: "From Browser To Django"
description: >-
    Django helps you build websites
    in Python.
    How does it work?
    In this series,
    we'll explore Django
    from top to bottom
    to show you how to build
    the website you've wanted.
    We'll start
    from the beginning
    with the browser.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django

---

Maybe you have heard about
{{< extlink "https://www.djangoproject.com/" "Django" >}}
and that it can help you build websites.
You might be new to Python,
new to web development,
or new to programming
as a whole.

{{< web >}}
This new series,
[Understand Django]({{< ref "/understand-django/_index.md" >}}),
will show you what Django is all about.
Throughout this series,
{{< /web >}}
{{< book >}}
This book
will show you what Django is all about.
In these chapters,
{{< /book >}}
I hope to reveal how Django is a powerful tool
that can unlock the potential
of anyone interested
in making applications
on the internet.

We're going to take a high level approach to learning.
Rather than starting
at the bottom
with all the pieces
of Django,
I'll give you the big picture,
then explore each layer more and more
to reveal how much Django does
for developers
under the hood.

Let's get started
from the very top
of a user's internet experience:
at the web browser.

{{< understand-django-series "browser" >}}

## Making A Browser Request

Django is a web framework,
but what the heck does that even mean?
How do websites work?
I'm not going
to be able to walk
through all the details,
{{< web >}}
but this post
{{< /web >}}
{{< book >}}
but this chapter
{{< /book >}}
will lay down the breadcrumbs.
We'll look at the way your web browser requests data
from the internet
and the "plumbing" needed
to make that work.
Equipped with these key words
and acronyms,
you should be able
to start your own research
on these topics.

The internet works
by fulfilling a user's desire
for information.
That "information" takes many different forms.
It might be:

* Cat videos on YouTube
* Political rumblings from social media
* Profiles of other people on dating sites

Whatever people are looking for,
the information is transferred
via the same mechanisms.
In internet-speak,
all types of information and data
fall under the name *resource*.

The way we get resources are with
{{< extlink "https://en.wikipedia.org/wiki/URL" "Uniform Resource Locators" >}}
or URLs,
for short.
You know what URLs are,
even if you didn't know them by name.

* {{< extlink "https://www.mattlayman.com/" "https://www.mattlayman.com/" >}}
* {{< extlink "https://en.wikipedia.org/" "https://en.wikipedia.org/" >}}
* {{< extlink "https://www.djangoproject.com/" "https://www.djangoproject.com/" >}}

These are all examples
of URLs.
Often we call them web addresses
because that feels right.
A URL is the address
of some resource
on the internet.
When you hit Enter
on the address bar
of your browser,
you're saying
"Please browser,
go get me this."
In other words,
we make a *request*
from the browser.
This request starts a large chain
of events
so that the resource
at that URL
can get to your eyeballs.

What's in this chain?
*Loads of things are there!*
We'll gloss over many of the layers
in this discussion
because I'm guessing you aren't planning
to get down to the level
of how electrical signals work
in networking cables.
Instead,
let's focus
on these two parts
of the chain
for now: **DNS** and **HTTP**.

### Names Names Names

A URL represents a resource
that you want
from the internet.
How does the internet know
where it comes from?
That's where DNS comes in.
DNS stands for
{{< extlink "https://en.wikipedia.org/wiki/Domain_Name_System" "Domain Name System" >}}.
The important word there is "Name."
Let's return to the address analogy.

In a postal address
(at least from a US perspective),
there is the street, city, and state.
We might write it like:

```text
# Most narrow to most broad
123 Main St., Springfield, IL
```

123 Main St. is in the city
of Springfield
in the state of Illinois (IL).

Likewise,
a URL fits into a similar format.

```text
# Most narrow to most broad
www.example.com
```

The terminology is different,
but the concept of going
from narrow to broad
is the same.
Each piece between periods is a type
of *domain*.
Let's look at them
in reverse order.

* `com` is considered a {{< extlink "https://en.wikipedia.org/wiki/Top-level_domain" "Top Level Domain" >}}, TLD.
    TLDs are carefully managed by a special group
    called {{< extlink "https://www.icann.org/" "ICANN" >}}.
* `example` is the domain name.
    This is the primary identity
    of a service on the internet
    as it is the specific identifier
    which a user would likely recognize.
* `www` is considered the *subdomain*
    of a domain.
    A domain might have many of these
    like `www`, `m`, `mail`, `wiki`
    or whatever a domain owner might want to name them.
    Subdomains can also be more than one level deep
    so `a.b.example.com` is valid,
    and `a` and `b` would both be subdomains of `example.com`.

Domain names are *not* how computers communicate.
The domain name is something "friendly"
for a human.
Computer systems are designed to work
with numbers
so those domain names must be translated
into something manageable.
To do this,
the internet uses a system
of DNS servers (special purpose computers)
to act as the translation layer
between domain names
and the numbers that computer networks use.

Maybe you've seen these networking numbers.
The numbers are called IP addresses,
short for {{< extlink "https://en.wikipedia.org/wiki/Internet_Protocol" "Internet Protocol" >}} addresses.
Common examples would include:

* `127.0.0.1` as the address that your computer has
    *for itself*
    on its internal network.
* `192.168.0.1` as a default address
    that a home router might use.

Those examples are special
because they are in specially designated {{< extlink "https://en.wikipedia.org/wiki/Subnetwork" "subnetworks" >}},
but we'll set that tangent aside.
You can delve deeper
on that topic
on your own
if you would like.

Back to DNS,
the system takes domain names
and keeps a distributed routing table
of names to IP addresses
across the collection
of DNS servers.
**Wait, what?**

DNS servers stack up into a gigantic hierarchy.
When your browser makes a request,
it asks the closest DNS server
for the IP address
of the domain name you requested.
The DNS server keeps a lookup table
of domain names to IP addresses
for a period of time.
If the domain name isn't in the table,
it can ask another DNS server
in a chain
that will continue to look
for the domain's IP address.
This leads to a couple of outcomes:

* If none of the servers can find the domain,
    the browser gives up
    and shows you a message like
    "Hmm. We’re having trouble finding that site."
    (from Firefox's Server Not Found page).
* If the browser gets the IP address
    from the DNS server,
    it can proceed with the request.

This is simplified
to exclude some
of the warty corners
of DNS,
but I hope you get the idea.

### What Are We Sending?

I know we're still not talking to Django yet,
but *I promise we're getting there.*
There are a lot of layers
to go through
when taking the top down approach,
but I think it helps build the foundation
that removes the mystery
of what makes the internet (and Django) work.

The other piece we need to explore is HTTP,
or the {{< extlink "https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol" "Hypertext Transfer Protocol" >}}.
This part of internet communication describes
how content transfers
between browsers
and servers,
or,
more generically,
between any computers
that use the protocol.

The protocol uses a standard format
and a set of commands
to communicate.
A few of the common commands are:

* `GET` - Get a resource
* `POST` - Send data to a resource
* `DELETE` - Request deletion of a resource

If you visit my website
at `https://www.mattlayman.com/about/`,
your browser will send a request like:

```http
GET /about/ HTTP/1.1
Host: www.mattlayman.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
```

There are other parts that I've omitted,
but this gets us started.
The top line provides the command,
the path to a particular resource on the site
(i.e., `/about/`),
and a version of the protocol to use.

After the first line are a list of *headers*.
Average browser users never see headers,
but headers are extra data
that tell the server more about the request.
For HTTP 1.1,
the `Host` header is required
because it dictates
where to make the request,
but any other header is optional.

In the example,
I also showed the `Accept` header.
This header tells the server
what kind of content the browser can receive
as a response.
There are other headers
that can tell a server what else it should "know."
These headers can:

* Indicate what kind of browser is requesting.
* Tell when the resource was requested previously
    to determine if a new version should be returned.
* Declare that the browser can receive compressed data
    which it can decompress after receiving
    to save on bandwidth.

Most of the headers are handled automatically
by browsers and servers,
but we will see instances
where we want to use these headers ourselves
so it's good to know they exist.

## Serving A Response

It's time to discuss Django!
We now have a rough idea
of what browsers do.
A browser sends an HTTP request
to a URL
which is resolved
by the DNS system.
That request arrives at a server
that is connected to the IP address
of the domain name.
Django lives on such a server
and is responsible
for answering requests
with an HTTP *response*.

The response is what the browser user wanted.
Responses can be images, web pages, videos,
or whatever formats a browser can handle.

Before Django can handle a request,
there is one more layer
to traverse:
the Python web server.

### Where HTTP Meets Python

A web server is the software
on a machine designed
to handle the incoming HTTP requests.
Sometimes this terminology can be confusing
because people may also apply the name "web server"
to an entire *machine*
that is serving web traffic.
In this instance,
I'm referring
to the actual program listening and responding
to web requests.

A Python web framework
like Django
runs with a web server.
The web server's role is to translate the raw HTTP request
into a format
that the framework understands.
In the Python world,
there is a specific format
so that any web server
can talk to any Python web framework.
That format is the {{< extlink "https://wsgi.readthedocs.io/en/latest/what.html" "Web Server Gateway Interface" >}},
or WSGI
(which is often pronounced "wiz-gee").

{{< web >}}
{{< figure src="/img/2020/wsgi.jpg" caption="Web Server Gateway Interface" >}}
{{< /web >}}

WSGI enables common web servers
like
{{< extlink "https://gunicorn.org/" "Gunicorn" >}},
{{< extlink "https://uwsgi-docs.readthedocs.io/en/latest/" "uWSGI" >}},
or {{< extlink "https://modwsgi.readthedocs.io/en/develop/" "mod_wsgi" >}}
to communicate
with common Python web frameworks
like Django,
{{< extlink "https://palletsprojects.com/p/flask/" "Flask" >}},
or {{< extlink "https://trypyramid.com/" "Pyramid" >}}.
If you really want to nerd out,
you can explore all the details
of that format
in {{< extlink "https://www.python.org/dev/peps/pep-3333/" "PEP 3333" >}}.

### Django's Job

Once the web server sends request data,
Django needs to return a *response*.
Your role as a Django developer is
to define the resources
that will be available
from the server.
That means you must:

* Describe the set of URLs
    that Django will react to.
* Write the code
    that powers those URLs
    and returns the response.

There is a ton
to unpack in those two statements
so we will explore individual topics
{{< web >}}
in future articles.
{{< /web >}}
{{< book >}}
in future chapters.
{{< /book >}}
By now,
I hope you have an idea
of how a request gets
from your browser
to a machine running Django.

{{< web >}}
{{< figure src="/img/2020/request-response.jpg" caption="Life of a browser request" >}}
{{< /web >}}

{{< web >}}
This article is relatively free
{{< /web >}}
{{< book >}}
This chapter is relatively free
{{< /book >}}
of code examples,
and for good reason.
There are already enough concepts
to wrestle with
and I didn't want to add code complexity
on top of it.
Writing that code will be the focus
{{< web >}}
of this article series
{{< /web >}}
{{< book >}}
of this book
{{< /book >}}
so we can answer questions like:

* How do we build web pages
    and give everything a common look and feel?
* How can users interact
    with an application
    and send data
    that the app can react to?
* How does Django store and retrieve data
    to make sites dynamic?
* Who can access the application
    and how is that access controlled?
* What security do we need to add
    to ensure that our users' information is safe and private?

Django has answers for all these things
and way more.
The Django philosophy is to include all the required pieces
to make a full web application
for the internet.
This "batteries-included" philosophy is what makes Django so powerful.
The same philosophy can also make Django seem overwhelming.
{{< web >}}
My goal in this series is to introduce piece after piece
{{< /web >}}
{{< book >}}
My goal in this book is to introduce piece after piece
{{< /book >}}
to build your understanding of Django
so you can get productive and get going
on your own web application.

{{< web >}}
In the next article,
our focus is going to be
on those URLs
that our application
will respond to.
We will see:

* how to declare the URLs.
* how to group sets of related URLs.
* how to extract information from URLs
    that can be used by the code that returns responses.

If you'd like to follow along
with the series,
please feel free to sign up
for my newsletter
where I announce all of my new content.
If you have other questions,
you can reach me online
on Twitter
where I am
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
{{< /web >}}

Finally,
there is one more bonus topic...

## Getting Set Up

{{< web >}}
In the series,
{{< /web >}}
{{< book >}}
In the book,
{{< /book >}}
I'm going to have plenty of code examples,
but I'm not going to show how to get Django running
from scratch each time.
Instead,
I'll put in some starting instructions
{{< web >}}
in this article
{{< book >}}
in this chapter
{{< /book >}}
so you can follow along
in the future.

We're going to use a terminal to run commands.
Windows, macOS, and Linux are all a bit different.
I'm showing macOS here
because that's what I run.
The dollar sign (`$`) is the traditional starting character
for a bash terminal
so when I list commands,
don't type that character.
I'll try to give pointers
and highlight differences when I can.

We need a place to put our work.
{{< web >}}
Since this series is called "Understand Django,"
{{< /web >}}
{{< book >}}
Since this book is called "Understand Django,"
{{< /book >}}
I'm going to use that name.
Call yours whatever is meaningful to you.

```bash
$ mkdir understand-django
$ cd understand-django
```

Next,
we install Django
into a virtual environment
so we keep our project code separate
from the rest
of the installed Python packages.

```bash
$ python -m venv venv
$ source venv/bin/activate
```

This may change your terminal prompt
so that it will now start with `(venv)`
to tell you that the virtual environment is in use.
Other operating systems activate the virtual environment differently.
Check the {{< extlink "https://docs.python.org/3/library/venv.html" "venv module documentation" >}}
for more information
on your operating system.

Install Django!

```bash
(venv) $ pip install Django
```

Django includes some tools
to get a project started quickly
which we can use.
We'll run a single command
to get it going.

```bash
(venv) $ django-admin startproject project .
```

This commands says
"start a project
*named* 'project'
in the current directory (`.`)."
After that command is finished,
you should have some files
and a layout that looks like:

```bash
(venv) $ ls
manage.py project venv
```

To check if the basics are working,
try:

```bash
(venv) $ python manage.py runserver
...
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

If you copy and paste that URL
into your browser,
you should see a welcoming start page!

The other thing that we need is an "app."
This is (perhaps confusingly) the name
of a Django component
in a project.
What you need to remember is
that a Django project *contains* one or more apps.

Let's create an app to work with:

```bash
(venv) $ python manage.py startapp application
```

Finally,
we must hook that app
into Django's project settings.
Open up `project/settings.py`,
find `INSTALLED_APPS`
and append to the list
so it looks like:

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

That's as far as we need to go
to get started
with our code examples
{{< web >}}
in the next article.
{{< /web >}}
{{< book >}}
in the next chapter.
{{< /book >}}
We have a Django project
that can run locally
for testing
that is configured
with its first app.
{{< web >}}
See you soon
to talk about making URLs and resources!
{{< /web >}}
