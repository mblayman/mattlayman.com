---
title: "Lua Log #1: Event Loop Adventures"
description: >-
    This is the start of my chronicle
    about my experience developing a web framework
    in Lua.
    This article covers some of my learnings
    about event loops.
image: img/2022/log-1.jpg
type: post
categories:
 - Lua
tags:
 - Event loop
 - Coroutines
 - Atlas

---

Last summer,
I went on a beach vacation
with my family,
and I needed something to do
when we weren't doing family things.
My primary software skills are in the Python and Django world,
and I decided that I want to something very different
to stretch my brain in new ways.
On a whim,
I thought it might be fun to make a web framework
in Lua.

{{< extlink "https://www.lua.org/" "Lua" >}} is a very compact,
interpretted language
that originates
from a group of academics
at a {{< extlink "https://www.puc-rio.br/index.html" "university in Brazil" >}}.
Lua itself is wildly popular as an embedded language
and can be found
in all sorts of games
and other tools.
Lua also has a reputation
for being an extremely fast interpretted language.

I played with Lua a few years ago
and produce a {{< extlink "https://github.com/mblayman/pong" "Pong clone" >}}
using the LÖVE 2D game engine.
With my experience building that game,
I recall that my tests finished
in a blindingly fast amount of time.
This memory is probably what led to my "random" choice
when picking to build a Lua web framework.

My thinking for this project is something like this:

* Learning to make all the pieces of a web framework could be a lot of fun.
* If something fast and useful comes out the other side, great!

My first foray into this project started
with a template rendering engine.
Rather than go with regex pattern matching,
I decided to go into hard mode
and pick a PEG parser.
I spent my beach vacation reading white papers
and twisting my mind to understand how this kind
of parser works.

After a few months of dabbling with the rendering engine,
I felt like I was really limiting what I was able to see.
With the engine,
I reached a level where I will have to implement much
of the expression grammar needed by Lua
in order to parse a template properly
and produce a render function
that will perform its task properly.
That part of the project quickly got into the weeds,
so I made the call to pull back
and think on different areas
of the project.

## Web server

Eventually,
I remembered The Pragmatic Programmer
and the discussion of tracer bullets.
I needed something
that can serve a small slice of functionality
that can go all the way through the system.
Building up this minimal working web framework
should allow me to adapt to the direction I want to go.
This is the idea behind a tracer bullet.
Tracer bullets are used to find a target quickly
by revealing where a weapon is aiming
in a visible way
and making adjustments after that
to reach the target.

If I can build a crude web framework
that reaches the target somewhat,
i.e. responding to a browser request,
then I can fill in the details
after that minimal point.

In researching the Lua ecosystem,
I found nothing like the WSGI/ASGI approach
of the Python web world.
There is no "standard" app server interface.
Because of this,
there is no common web server
that can handle a common web app format.
In other words,
I could build a web framework,
but I had nothing standard to plug it into.

Thus,
my project grew in scope.
In addition to building a web framework,
I've decided to try my hand a building a web server too.
Here is where choice starts to come into the picture.

* Do I build a web server that uses a threaded model
    where a main process farms out connections
    to a set of worker processes?
* Do I build an asynchronous web server
    that uses an event loop
    and runs with cooperative scheduling?

I guess the title of this article is a spoiler.
I went with the async event loop pattern.

## Event loop

The best known aysnc programming model
in the web software world is undoubtedly Node.js.
After some research,
it became clear to me
that the underlying event loop
for Node.js call `libuv` is an equally popular choice
when considering this async style
of programming.

The popular Python async web server,
{{< extlink "https://www.uvicorn.org/" "Uvicorn" >}},
takes this exact approach
of implementing a web server
on top of `libuv`.

I picked `libuv` as my choice,
but then I needed a way to include it
into my Lua project.
Thankfully,
there exists a Lua web framework named
{{< extlink "https://luvit.io/" "Luvit" >}}
that followed a similar path.
Because `libuv` is a C library,
the Luvit developers built a binding libary
to expose `libuv` as a Lua library.
I'm immensely grateful
that I don't have to write that binding layer myself
(my C skills are very rusty
and I was never fantastic at C
to begin with).

One big challenge with `libuv` is
that it operates with a callback model.
In order to enable cooperative scheduling,
any call that would be blocking
in `libuv`
like network I/O
expects to receive a callback.

I would like users (if ever there are any)
of my web framework
to be able to avoid callbacks.
The Uvicorn project is able to get around these callbacks
thanks to the amazing work
of {{< extlink "https://github.com/MagicStack/uvloop" "uvloop" >}}.
uvloop integrates `libuv`
into Python's `asyncio` module.

Here's where I'm starting to run into challenges.
Lua's standard library is *very* small.
There is no concept like `asyncio`.
There are also no Lua language constructs
like `async`/`await`.
Lua has coroutines as its mechanism
for handling cooperative scheduling.
I've basically spent my entire weekend researching
to find good ways of using coroutines
to hide callbacks from calling code.
Ultimately,
I founds some similar patterns in Luvit
that I'm hoping to replicate
to a degree.

My goal now to make a web server
that uses `libuv`
and make an API
that feels like ASGI.
Since I don't have the native `async` and `await` used
by ASGI in Python,
maybe I'll spawn a variant of Lua ASGI.
Perhaps I should call it LASGI.

Where I'm at is building this bridge
from callbacks to coroutines.
Once I have that bridge,
I'll probably focus
on HTTP 1.1 parsing
to get the rough support
that is required by the ASGI interface.

In the spirit of having a tracer bullet,
when I have the most crude thing possible,
I'll switch back to the framework side
and start handling ASGI messages.
That will likely mean building a request router
and some kind of request controller or handler.

I don't know how often I'll write this kinds of entries.
I thought it might be useful to expose others
to the messy process of building a project.
If you're looking for the code
and all my notes,
you can find
{{< extlink "https://github.com/mblayman/atlas" "my project on GitHub" >}}.
