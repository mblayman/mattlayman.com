%YAML 1.1
---
blog: True
title: The necessity of software abstraction
date: 2017-01-24T12:00:00Z
summary: >-
  Software abstraction is vital to managing a large application.
  My aim is this post is to combat the belief
  that a developer must understand all the details
  of the abstractions that they work with.
template: writing.j2

---

Tell me if you've heard this one before:
unless you understand how a software abstraction works,
you will not be able to use it well.
I've heard variations
of this declaration
on a number of podcasts
and other tech blogs
and media.
I think this idea is misguided.
To the contrary,
*embracing software abstractions
requires you to accept ultimately
that you will not understand them all.*

Our lives are full of abstractions.
Without them,
we'd have an extremely hard time functioning,
because we'd always need to explain things
from first principles.
Take something as primary as *blue*.
What if you always had to describe it as
"the electromagnetic radiation
oscillating at 650 x 10<sup>12</sup>
oscillations per second?"
Even **that** decomposition of *blue*
into more rudimentary terms
is full of life's abstractions.

> Why then does this sentiment
about deep understanding
of software abstractions
**as a requirement**
gain such traction?

Consider a web developer working
in a web framework.
How far down do we expect that person
to have an intimate understanding
of what is going on?
To display an HTML table
in a browser,
do we expect them to know how
*the browser will process a URL,
build an HTTP request,
transmit the request
through numerous layers
of network protocols,
be received by a server,
that likely handles the data
in a language
that uses a byte code interpreter,
that makes operating system calls,
that get translated into hardware interrupts,
that are handled by numerous layers
of hardware,
that ultimately are logical gates,
built out of transitors,
whose material properties permit flow
of electrons
through various parts
of a circuit?*
Last time I checked,
when I added a CSS gradient
to a page,
I did not need to be aware
of the electron flow
through the transitors
inside of my laptop.
**Where do we draw the line?
What is "good enough?"**

To be clear,
I'm not saying that you should skip learning
how software (or hardware) abstractions work.
In the quest for a deeper understanding
of your profession,
you should *absolutely* try your best
to understand
the software you interact with.
The reason I get so bothered
by this idea that abstractions
must be understood
before they can be used well
is that it is a disservice
to new developers.
Perhaps to a seasoned software veteran,
stating that abstractions
need to be understood
is a trivial thing,
because that veteran already has the years
of applied learning.
To a new developer,
this burden of understanding
might feel like a bludgeoning
over their head.
*How do you not know this yet?*
*You're not qualified to do this
until you get it.*
*What do you mean you don't know
all the details
of this protocol?*
I suspect it leads to feelings
of inadequacy
in their own experience
and likely pushes many away
from the field altogether.

> I think all this means
that we must become comfortable
in our own intellectual shortcomings.
It also means placing a certain degree
of trust
in this collectively awesome mind construct
that we call software.
Embracing software abstractions
let's us thrive
at boundaries.
It permits us
to function
without loading the entire context
of the universe
in our heads.
