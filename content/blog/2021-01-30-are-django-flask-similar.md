---
title: "Are Django and Flask Similar?"
description: >-
    If you're into Python
    and new to web development,
    you may have questions
    about Python's popular web application packages:
    Django and Flask.
    This article compares the two
    so you can figure out which one might be a better fit
    for you.
image: img/2021/django-flask.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - Flask

---

Maybe you're new
to web development
in Python,
and you've encountered the two most popular Python web frameworks,
Django and Flask,
and have questions
about which one you should use.
Are Django and Flask similar tools
for building web applications?

> Yes, Django and Flask share many similarities
    and can **both make great websites**,
    but they have some different development philosophies
    which will attract different types
    of developers.

What do *I* know about this?
I'm a software developer
who has specialized
in web development
for over a decade.
I have over 7 years of experience building Django apps,
and also experience with Flask,
Pyramid,
Twisted,
Pylons,
TurboGears,
and other Python web frameworks.

For the rest of this article,
I'll show some of the core ways
that the tools are similar
and explain the biggest differences.

## How Are Django and Flask Similar?

Let's get the biggest similarity covered
before considering anything else:

> Django and Flask can both help you build **amazing** web applications.

Both tools have extremely supportive communities
and no matter what choice you make
in the end,
you can build something great.

These are the other big similarities
that I see:

* **WSGI** - Both tools communicate
    with the web
    using the Web Server Gateway Interface.
    By using this protocol,
    Django and Flask apps can seamlessly connect
    to Python's most popular web application servers
    like Gunicorn or uWSGI
    without any friction.
* **Request/Response** - The mental model
    for serving traffic
    by handling requests
    and returning responses is the same.
    The mechanics to get the request object vary a bit,
    but the two projects are more similar than not.
* **Routing** - The frameworks both have the notion
    of routing a URL to a function or class
    to handle a request.
    Django separates the route rules from the functions,
    while Flask uses decorators
    on the functions to set routes.
    The end result is the same.
    In fact,
    Django adopted Flask's route syntax style
    because it's awesome.
* **Synchronous** - One of the constraints
    of WSGI is that code must run
    in a synchronous mode
    (i.e. no use of Python's `async`/`await` keywords).
    Frankly,
    I think this makes code easier
    to reason about
    for developers.
    Django has some growing support
    for ASGI
    (where the "A" stands for **a**synchronous).
* **Project Structure** - Each framework gives you tools
    to create a manageable structure
    for your source code
    to group your logic appropriately.
    Django calls the grouping tool "applications,"
    while Flask calls them "blueprints."

## How Are Django and Flask Different?

In spite of all their similarities,
there *are* big differences
between Django and Flask.

* **Small Apps** - Flask is better
    for very small projects.
    An entire Flask application can realistically fit
    into a single file
    if the project has a small enough scope.
    Django *can* fit into a single file,
    but, truthfully,
    it's more of a parler trick,
    and I never encounter single file Django projects
    in reality.
* **Batteries Included** - Django includes a ton
    of features in the core package compared to Flask.
    In practice,
    this means you can install a single package
    before you need to look
    for more packages
    to extend your project.
    The flip side is that there is more
    to learn about Django
    than the core Flask experience.
* **Opinionated** - Between the two frameworks,
    Django makes a lot more design choices
    by including more things
    and connecting those things together.
    If you like those choices,
    then the framework removes a lot
    of work
    from your plate.
    If you don't like the choices,
    you may end up battling the framework
    to bring your own design ideas to bear.
* **External Packages** - Because Flask has a smaller surface area
    of features,
    you have to integrate other features yourself.
    On the bright side,
    you gain a lot of flexibility
    and can include packages
    that you believe are "best of breed."

## Why I Prefer Django

At PyCon US 2019,
I got the chance
to hang out
with the Pallets team
(the umbrella group
that manages a bunch of popular web packages)
during the development sprints,
and they are awesome people!
But when I start a new web project,
I still reach for Django. *Why?*

> **Django's design choices are solid**
and let me spend more time focused
on my project goals versus integrating other packages.

The Django developers have put together
and molded a framework
since 2005.
With the goal
of producing a full-featured framework,
a lot of hard-earned lessons
from years of Django websites
on the internet influenced the choices
that make Django what it is today.

The thoughts of many talented developers produced a framework
that feels like a cohesive whole.
On top of all of that,
learning that framework
becomes transferrable knowledge
since other Django projects will share those patterns
and design choices.

Flask lets you choose your own adventure more than Django.
For some individuals,
that freedom lets them craft exactly the website
that they want,
including all the extra design choices
that they want to make.

I find that the design
of Django
makes me more productive.
I can generate final products to others quickly.
After all,
isn't the ultimate goal
of using a web framework
to make a website
that serves its audience well?

> Whether you pick Django or Flask,
you can rely on the fabulous Python community
to support you on either path.

## Learn More

Those are my thoughts
about the similarities and differences
between Django
and Flask.

Do you want to learn how Django works
or what Django is used for?
Then I suggest you check out my
[Understand Django]({{< ref "/understand-django/_index.md" >}})
series of articles next.
In that series,
I explain Django
to new (and old!) web developers.
I think it will help you
on your journey to becoming a Django dev.

Follow me
{{< extlink "https://x.com/mblayman" "on X" >}}
to learn more about Django
as I release new content.
