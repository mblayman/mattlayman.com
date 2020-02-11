---
title: "Episode 1 - Get To Know Django"
aliases:
 - /django-riffs/1
 - /djangoriffs/1
description: >-
    Django Riffs is
    a podcast for learning web application development
    in Python
    using the Django web framework.
    We explore all of Django's features
    to equip listeners
    with the knowledge
    to build a web app.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django

---

Welcome to the show notes
for the first episode
of Django Riffs!

Django Riffs is
a podcast for learning web application development
in Python
using the Django web framework.

Listen at {{< extlink "https://djangoriffs.com/episodes/get-to-know-django" "djangoriffs.com" >}}.

## Who Is This For?

This podcast is for absolute Django beginners.
No prior knowledge of Django
or web development is expected.

Experienced users may learn something new
or get a good refresher from topics they might have missed
in the documentation.

As a pre-requisite,
knowledge of Python is expected.
Describing code in audio will be super hard
to understand
if you don't know any Python.

## Who Am I?

I'm Matt Layman,
a software developer
with over five years of Django experience.
I've worked in the software industry since 2006.

## What's The Format?

Django Riffs is an educational podcast.
It's not a Django interview or news show.
For that type of show,
check out {{< extlink "https://djangochat.com/" "Django Chat" >}}.

The show will teach Django
from a top-down approach.
We'll start with the overview,
then dive into the details.

Each episode will focus on a single topic.
I hope this will help avoid overloading listeners.

The episodes will have actual code examples
described in audio
and presented here
in the show notes.

## What Is Django?

Django is a web framework.
There's two parts to that: *web* and *framework*.

"Web" implies that Django is a tool
for building websites.
This can include sites you may access
with your browser
or mobile applications
that use Django as a backend
to fetch data.

Django powers websites
like {{< extlink "https://www.instagram.com/" "Instagram" >}},
{{< extlink "https://www.pinterest.com/" "Pinterest" >}},
or, my own employer, {{< extlink "https://doctorondemand.com/" "Doctor on Demand" >}}.

"Framework" is the other half.
Frameworks are often compared to software libraries.
Software libraries are chunk of code
that you call.
Frameworks, in contrast, are systems
that call your code.
Django, as a framework, gives you a core foundation
that you can build your code on top of.

## What Does Django Do?

This can be understood in the context
of what a browser does.

A browser works by making requests
with
{{< extlink "https://en.wikipedia.org/wiki/URL" "URLs" >}}
(Uniform Resource Locators)
which are places on the internet
where you can find something.

URLs get responses
from other websites
by using
{{< extlink "https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol" "HTTP" >}}
(Hypertext Transfer Protocol).
HTTP is the format that describes
how browsers talk to other sites.
HTTP uses common commands like `GET`
so many of the requests
that your browser makes are actually `GET` requests.

When working with the request,
the browser must translate the URL name
that you supplied
into a numeric scheme that computers and networks understand.
This is done with the
{{< extlink "https://en.wikipedia.org/wiki/Domain_Name_System" "Domain Name System" >}} (DNS).
Browsers will work with a DNS server
to get one of these numbers
which are called called IP addresses,
short for {{< extlink "https://en.wikipedia.org/wiki/Internet_Protocol" "Internet Protocol" >}} addresses.

With the IP address available,
the browser will connect to the server machine.
In the context of Django,
this machine will run a Python web server.
Web servers listen for HTTP requests
and issue HTTP responses.
The web server translates an HTTP request
into a format that a web *application* can handle.

Django is that web application.
The web server hands the web request to Django
over a format called WSGI,
which is the {{< extlink "https://wsgi.readthedocs.io/en/latest/what.html" "Web Server Gateway Interface" >}}.
WSGI is the universal interface
between Python web servers and Python web applications.

Django's job is to take the request
and produce some kind of response.
Django has to handle URLs
and the path that comes after the main portion
of the URL
(e.g., the part after `.com`).

As the developers,
we must define what URLs Django will respond to.
We must also write the code
that will power those URLs.
Django provides supporting code
to make writing the responses easier.

## Where Does Django Fit In The Web Ecosystem?

Django is a "batteries-included" framework.
Django gives you a lot of tools in a single package
so you don't have to put a bunch of things together
for yourself.
Other similar frameworks include
{{< extlink "https://rubyonrails.org/" "Ruby on Rails" >}}
for the Ruby language
or
{{< extlink "https://laravel.com/" "Laravel" >}}
for the PHP language.

Django is a server-side rendered framework.
Most of the work is done on the server
so a full webpage is sent to a user.

A contrasting design style is a client-side rendered framwork.
These frameworks use JavaScript to display the layout
in a user's browser
and fetch data
from a backend.

Django is a simpler model
than client-side rendering
because there is only one component doing the work
rather than an information exchange
between a backend and a client system.

## Next Time

In the next episode,
we'll look at URLs
and how to build them
into your application.

You can follow the show
on {{< extlink "https://djangoriffs.com" "djangoriffs.com" >}}.
Or follow me or the show
on Twitter
at
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}
or
{{< extlink "https://twitter.com/djangoriffs" "@djangoriffs" >}}.

Please rate or review
on iTunes, Spotify,
or from wherever you listen to podcasts.
Your rating will help others discover the podcast,
and I would be very grateful.

Django Riffs is supported by listeners like *you*.
If you can contribute financially
to cover hosting and production costs,
please check out my {{< extlink "https://www.patreon.com/mblayman" "Patreon page" >}}
to see how you can help out.
