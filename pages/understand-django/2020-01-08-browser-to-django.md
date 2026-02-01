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
image: /static/img/django.png
slug: browser-to-django
date: 2020-01-08
categories:
 - Python
 - Django
tags:
 - Python
 - Django

---

Maybe you have heard about
[Django](https://www.djangoproject.com/)
and that it can help you build websites.
You might be new to Python,
new to web development,
or new to programming.

This new series,
[Understand Django](/understand-django/about),
will show you what Django is all about.
Throughout this series,
I will reveal how Django is a powerful tool
that can unlock the potential
of anyone interested
in making applications
on the internet.
Django is used
by companies
like Instagram,
Eventbrite,
Disqus,
and
Udemy,
and is also a great tool
for individuals like you.

We're going to take a high-level approach to learning Django.
Rather than starting
at the bottom
with all the pieces
of Django,
I'll give you the big picture,
then explore each layer in more detail
to reveal how much Django does
for developers
and the power Django has
under the hood.

Let's get started
from the very top
of a user's internet experience:
at the web browser.

1. From Browser To Django
2. [URLs Lead The Way](/understand-django/urls-lead-way)
3. [Views On Views](/understand-django/views-on-views)
4. [Templates For User Interfaces](/understand-django/templates-user-interfaces)
5. [User Interaction With Forms](/understand-django/user-interaction-forms)
6. [Store Data With Models](/understand-django/store-data-with-models)
7. [Administer All The Things](/understand-django/administer-all-the-things)
8. [Anatomy Of An Application](/understand-django/anatomy-of-an-application)
9. [User Authentication](/understand-django/user-authentication)
10. [Middleware Do You Go?](/understand-django/middleware-do-you-go)
11. [Serving Static Files](/understand-django/serving-static-files)
12. [Test Your Apps](/understand-django/test-your-apps)
13. [Deploy A Site Live](/understand-django/deploy-site-live)
14. [Per-visitor Data With Sessions](/understand-django/sessions)
15. [Making Sense Of Settings](/understand-django/settings)
16. [User File Use](/understand-django/media-files)
17. [Command Your App](/understand-django/command-apps)
18. [Go Fast With Django](/understand-django/go-fast)
19. [Security And Django](/understand-django/secure-apps)
20. [Debugging Tips And Techniques](/understand-django/debugging-tips-techniques)

## Making A Browser Request

Django is a web framework,
but what the heck does that even mean?
How do websites work?
I'm not going
to be able to walk
through all the details,
but this post
will lay down the breadcrumbs
to build your understanding.
We'll look at the way your web browser requests data
from the internet
and the "plumbing" needed
to make that work.
Equipped with the key words
and acronyms found in this chapter,
you should be able
to start your own research
on these topics.

The internet works
by fulfilling a user's desire
for sending and receiving information.
That "information" takes many different forms.
It might be:

* Cat videos on YouTube
* Political ramblings from social media
* Profiles of other people on dating sites

Whatever people are looking for,
the information is transferred
via the same mechanisms.
In internet-speak,
all types of information and data
fall under the name *resource*.

The way we get resources are with
[Uniform Resource Locators](https://en.wikipedia.org/wiki/URL)
or URLs,
for short.
You know what URLs are,
even if you didn't know them by name.

* [https://en.wikipedia.org/](https://en.wikipedia.org/)
* [https://www.djangoproject.com/](https://www.djangoproject.com/)
* [https://www.mattlayman.com/static/img/django.png](https://www.mattlayman.com/static/img/django.png)

These are all examples
of URLs.
Often we call them web addresses
because they're very similar to postal addresses.
A URL is the address
of some resource
on the internet.
When you hit *Enter*
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
from your browser
to the website at that URL
so that the resource
from the site
can get to your eyeballs.

What's in this chain of events?
*Loads of things are there!*
We'll gloss over many of the layers
in this discussion
because I'm guessing you aren't planning
to get down to the level
of how electrical signals work
in networking cables.
Instead,
let's focus
on two primary parts
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
[Domain Name System](https://en.wikipedia.org/wiki/Domain_Name_System).
The important word there is "Name."
Let's return to the address analogy.

In a postal address
(at least from a US perspective),
there is the street, city, and state.
We might write it like:

```text
123 Main St., Springfield, IL
```

This address goes from most narrow to most broad.
123 Main St. is in the city
of Springfield
in the state of Illinois (IL).

Likewise,
a URL fits into a similar format.

```text
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

* `com` is considered a [Top Level Domain](https://en.wikipedia.org/wiki/Top-level_domain), TLD.
    TLDs are carefully managed by a special group
    called [ICANN](https://www.icann.org/).
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
    and `a` is a subdomain of `b.example.com`
    and `b` is a subdomain of `example.com`.

Domain names are *not* how computers communicate.
The domain name is something "friendly"
for a human.
Networking systems are designed to work
with numbers
so those domain names must be translated
into something the networking system can use.
To do this,
the internet uses a system
of DNS servers
to act as the translation layer
between domain names
and the numbers that computer networks use.
A server is a special purpose computer
designed to provide services
for other devices called clients.

Maybe you've seen these networking numbers.
The numbers are called IP addresses,
short for [Internet Protocol](https://en.wikipedia.org/wiki/Internet_Protocol) addresses.
Common examples would include:

* `127.0.0.1` as the address that your computer has
    *for itself*
    on its internal network.
* `192.168.0.1` as a default address
    that a home router might use.

The IP address examples above are special
because those addresses are in specially designated [subnetworks](https://en.wikipedia.org/wiki/Subnetwork),
but we'll set that tangent aside.
You can delve deeper
on that topic
on your own
if you would like.

Private networks have IP addresses
like the two examples I listed above.
Machines on public networks also have IP addresses.
For instance, `172.253.115.105` is an IP address
for `www.google.com`
at the time of this writing.

If you'd like to figure out the IP address
of a domain name,
you can install a popular tool named `dig`.
I found Google's IP address by running this command:

```bash
dig www.google.com
```

The system takes domain names
and keeps a distributed routing table
of names to IP addresses
across the collection
of DNS servers.
**Wait, what?**

DNS servers stack up into a gigantic hierarchy.
When your browser makes a request,
it asks the closest DNS server
to your machine
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

The hierarchy is gigantic,
but it is wide, not deep.
In other words,
there are many machines
that participate in DNS (like your home router),
but the number of links in the chain
to make a request from your computer up
to the root servers in the system
is relatively small.

This is simplified
to exclude some
of the warty corners
of DNS.
The Wikipedia page
that I linked at the start
of this section covers DNS
in much greater detail
if you're interested
in learning more.

### What Are We Sending?

The other vital piece that we need to explore is HTTP,
or the [Hypertext Transfer Protocol](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol).
This part of internet communication describes
how content transfers
between browsers
and servers,
or,
more generally,
between any computers
that use the protocol.

The protocol uses a standard format
and a set of commands
to communicate.
A few of the common commands are:

* `GET` - Fetch an existing resource
* `POST` - Create or update a resource
* `DELETE` - Delete a resource
* `PUT` - Update a resource

An HTTP request is like sending a text file over the network.
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
Headers are extra data
that tell the server more about the request.
The `Host` header is required
because it names the website to retrieve
(more than one website can exist on the same IP address),
but any other header is optional.

In the example,
I also showed the `Accept` header.
This header tells the server
what kind of content the browser can receive
as a response.
There are other headers
that can tell a server what else it should "know."
These headers can:

* Indicate what kind of browser is making the request
    (this is the `User-Agent` header).
* Tell when the resource was requested previously
    to determine if a new version should be returned
    (the `Last-Modified` header).
* Declare that the browser can receive compressed data
    which it can decompress after receiving
    to save on bandwidth
    (the `Accept-Encoding` header).

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
there is a specific format used
so that any web server
can talk to any Python web framework.
That format is the [Web Server Gateway Interface](https://wsgi.readthedocs.io/en/latest/what.html),
or WSGI
(which is often pronounced "wiz-gee").

![Web Server Gateway Interface](/static/img/2020/wsgi.jpg)

WSGI enables common web servers
like
[Gunicorn](https://gunicorn.org/),
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/),
or [mod_wsgi](https://modwsgi.readthedocs.io/en/develop/)
to communicate
with common Python web frameworks
like Django,
[Flask](https://palletsprojects.com/p/flask/),
or [Pyramid](https://trypyramid.com/).
If you really want to nerd out,
you can explore all the details
of that format
in [PEP 3333](https://www.python.org/dev/peps/pep-3333/).

### Django's Job

Once the web server sends a request,
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
in future articles.
By now,
I hope you have an idea
of how a request gets
from your browser
to a machine running Django.

![Life of a browser request](/static/img/2020/request-response.jpg)

This article is relatively free
of code examples,
and for good reason.
There are already enough concepts
to wrestle with
and I didn't want to add code complexity
on top of it.
Writing that code will be the focus
of this article series
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
My goal in this series is to introduce piece after piece
to build your understanding of Django
so you can get productive and get going
on your own web application.

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

If you have questions,
you can reach me online
on X
where I am
[@mblayman](https://x.com/mblayman).

Finally,
there is one more bonus topic...

## Getting Django Set Up

In the series,
we'll be looking at plenty of code examples,
but we won't be setting up Django from scratch each time.
The following setup instructions will help you get started
with each future example.

> The goal of this section is not meant to be an authoritative description
of how to set up your Python environment.
I am assuming that you have some knowledge of how to run Python code.
If you need a more descriptive guide,
I'd suggest Michael Kennedy's
[Installing Python 3](https://training.talkpython.fm/installing-python) article
and Real Python's
[primer on virtual environments](https://realpython.com/python-virtual-environments-a-primer/).
These article go into the discussion of setup far more
than I'm doing justice here.

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
Since this series is called "Understand Django,"
I'm going to use that name.
You can name your project differently if you prefer.

```bash
$ mkdir understand-django
$ cd understand-django
```

Next,
we install Django
into a virtual environment
so we keep our project dependencies separate
from the rest
of the installed Python packages
on our machine.
Having this separation
from other installed packages
is a good way to prevent conflicts
with other Python projects
that you may be running
on your computer.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

This may change your terminal prompt
so that it will now start with `(venv)`
to tell you that the virtual environment is in use.
Other operating systems activate the virtual environment differently.
Check the [venv module documentation](https://docs.python.org/3/library/venv.html)
for more information
on your operating system.

Now you can install Django,
and the Django framework code will be added
to the virtual environment.

```bash
(venv) $ pip install Django
```

Django includes some tools
which we can use
to get a project started quickly.
We'll run a single command
to get it going.

```bash
(venv) $ django-admin startproject project .
```

This commands says
"start a project
*named* 'project'
in the current directory (`.`)."
The choice of "project" as the name is intentional.
`startproject` will create a directory
named `project` that will contain various files
that you'll use to configure your entire web app.
You can name your project whatever you like,
but I find that using the generic name makes my life easier
as I switch between different Django web apps.
I always know where my project related files reside.
After that command is finished,
you should have some files
and a layout that looks like:

```bash
(venv) $ ls
manage.py project venv
```

Notice that,
in addition to the `project` directory,
Django created a `manage.py` file.
This file is a script that will help you interact
with Django.
You'll learn a lot more about `manage.py`
as we get farther along.
To check if the basics are working,
try:

```bash
(venv) $ python manage.py runserver
...
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

When you start the web server,
you will likely see a message
like:

```text
You have ## unapplied migration(s).
Your project may not work properly
until you apply the migrations for app(s):
<a list of names here>
```

We'll explore the migrations topic later,
so don't worry about that message for now.

If you copy and paste that URL
(i.e., `http://127.0.0.1:8000/`)
into your browser,
you should see a welcoming start page!
Also,
if you look back at your terminal,
you'll find `"GET / HTTP/1.1"`.
This message is showing that Django responded
to an HTTP request.
Neat!

The other thing that we need is an "app."
This is (perhaps confusingly) the name
of a Django component
in a project.
What you need to remember is
that a Django project *contains* one or more apps.
Apps will hold most
of your code
that you need to write
when working with Django.

After you have quit the server,
you can create an app to work with:

```bash
(venv) $ python manage.py startapp application
```

This will generate another set of files
that follow the standard structure
of a Django application component
inside a directory called `application`.
This example uses a boring name,
but,
unlike `project`,
you should pick a name
that makes sense for your web app
(e.g., `movies` would be a good name
for a web app that is about movies).
All of these files will be discussed
in detail in a future topic.

Finally,
we must hook that app
into Django's project settings.
The project settings allow you to configure Django
to suit your needs.
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
in the next article.
`application` will be our reference app.
The code in future topics is not a tutorial,
but I will use `application` on occasion
to orient you to where you would find files
in your own Django web app.
We have a Django project
that can run locally
for testing
and is configured
with its first app.
See you soon
to talk about making URLs and resources!
