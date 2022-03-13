---
title: "Lua Log #8: HTTP Parsing"
description: >-
    My next challenge in my Lua project
    is to parse incoming network data
    into HTTP requests that an application can process.
    In this entry,
    I explore the options available to me
    and why I am making the choice
    to build my own HTTP parser.
image: img/2022/log-8.jpg
type: post
categories:
 - Lua
tags:
 - Lua
 - HTTP
 - Parser

---

Since my last entry about
{{< extlink "https://github.com/mblayman/atlas" "Atlas" >}},
I built a couple of fundamental abstractions
into my framework: a `Request` object and a `Response` object.

At this point in the web framework,
I'm shooting to keep the number of supporting protocols
to a minimum.
Even though the ASGI specification discusses a few different protocols
like HTTP and websockets,
I only intend to focus on HTTP for now.

Because I'm focused exclusively
on HTTP,
I can think about the core semantics
of that protocol.
The request and response are the fundamental
input and output units
for a server.

I created a `Request` object
so that the Atlas framework side will have a consistent interface.
An Atlas application author will write controller functions
that receive a request instance.
The request will hold the HTTP method
(e.g., `GET` or `POST`)
as well as some other attributes
like a request body
if there was submitted data.
I think this will be preferable
over having a framework user deal
with the data structure defined
by the ASGI spec.

The `Response` object is the output side of the equation.
The framework will provide tools to create responses
in the future,
but for now,
an author could directly create a response
and set the content type,
the status code,
and the response body.
Eventually,
I'll hook the response object
to the template engine
to allow a more useful combination
for users.

Before my project even has the possibility
of being useful,
I need to do more work
on the server.
Currently,
the server can only send a hardcoded `Request`
to the application.
The server properly connects
over a TCP socket,
but it ignores any of the incoming data!

The reason that the server ignores the incoming data is
because there is no parsing logic
to handle the HTTP protocol.
My next goal is to add an HTTP parser
that can read the bytes
from the network connection
and translate it into a semantic HTTP request
that can be passed to the app.

Where I can I get a parser from?

* I can use a parser written for Lua by someone else.
* I can use a parser written in a low level language
    and hook it into Lua
    with a "binding" layer.
* I can write my own parser.

I explored all three possibilities this week.

I first looked at what was available in Lua.
I found a couple of intriguing options.
First,
I discovered
{{< extlink "https://github.com/brimworks/lua-http-parser" "lua-http-parser" >}}.
This library is a binding on top of Ryan Dahl's http-parser written in C.
Ryan Dahl is the original author of Node.js
and http-parser was the library used
by Node
for many years.
While researching this library,
I learned that http-parser is no longer used
by Node
and is considered unmaintainable.
That's not the kind of library
that I want to use!

Next,
I looked at
{{< extlink "https://daurnimator.github.io/lua-http/0.4/" "lua-http" >}}.
This Lua library seems promising and well done,
but as I looked into it,
I don't think it would be compatible
with libuv.
lua-http seems to handle the TCP connections
that libuv wants to handle.
I didn't know how to make those things play nicely
with each other.

After exploring the Lua space,
I looked for C-based libraries.
Since Lua is written in C,
it's reasonable to consider using a C library
and using Lua's C API to write a layer
that can expose an interface
into the Lua interpreter.
As mentioned earlier,
http-parser and lua-http-parser do exactly that,
but I didn't want to depend
on an unmaintained library.

Knowing that the http-parser library was unmaintained,
I looked into the successor library
used by Node.js,
{{< extlink "https://llhttp.org/" "llhttp" >}}.
This parser has a ton of nice attributes going for it.
The API is minimal
and it's blazing fast.

At this juncture,
I had a philosophical question to answer.
*What do I want to learn about?*
Do I want to learn how to make a Lua binding library?
Do I want to learn how to handle HTTP myself?

I've faced similar questions
at various stages
of this project.
At different levels in the stack,
I could choose to write something myself
or rely on someone else's tools.
For instance, I made the choice
to use lpeg
to have a parser
for my template engine
instead of writing a parsing library myself.

In this scenario,
I've decided that it would be more fun and interesting
for me to write an HTTP parser
instead of learning how to write a Lua binding.
My C skills are very rusty
and weren't super strong to begin with.
Also,
I'd like to keep my development toolchain simpler
and stick with Lua code exclusively
as long as possible.

Therefore,
I'm now reading HTTP specifications.
I'm positive that whatever HTTP parser I write will be slower
and likely full of bugs
since I don't have a full understanding
of the HTTP specs,
but I'm excited to go on this journey
and see what it take to build a protocol parser
in Lua.

Over the coming weeks,
I'm going to try to balance spec reading
and implementation time.
I don't want to read the entire spec
before writing a line of code.
Engaging with some code
(even if it's wrong)
will help keep my interest level up.
I'd like to get a basic parser working
so I can do some end-to-end testing
with my framework.

Thanks for reading!
Have questions?
Let me know on Twitter at
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
