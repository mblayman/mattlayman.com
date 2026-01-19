---
title: "Lua Log #6: LASGI - ASGI in Lua"
description: >-
    In my limited time this week,
    I built out the interface
    between the web server and my application.
    I'm leaning heavily on work done
    in Python
    by implementing ASGI in Lua.
image: /static/img/2022/log-6.jpg
categories:
  - Lua
tags:
  - Lua
  - ASGI
  - Atlas
slug: lua-log-6-lasgi
date: 2022-02-27
---

In [Atlas](https://github.com/mblayman/atlas),
I'm implementing a full web framework.
I'm also taking on the challenge of building a web server
to pair with the web framework
and the application that the framework produces.

*How I should I connect the web server and the web application?*
There's an interface between those two systems.
Since I know a lot about the Python web ecosystem,
I know that some very smart developers have given considerable thought
to the interface layer between servers and applications.
In fact,
I know that the current standard,
[ASGI](https://asgi.readthedocs.io/en/latest/index.html),
took years to draft and develop.

Knowing that,
I decided that the quickest way to get a working interface is to try to get ASGI
to work in a Lua context.
I've branded my effort as LASGI
for **Lua's Asynchronous Server Gateway Interface**.

There are some fundamental differences between Python and Lua
that mean that LASGI has to adapt
from the ASGI spec.

* Lua doesn't have `async` and `await`.
* Lua doesn't have the bytes and Unicode string separation
    that Python 3 has.

In the ASGI interface,
an ASGI application is called with three things:

* A dictionary of `scope` with information about the incoming connection.
* A `receive` and `send` pair of awaitable callables.

Because of Lua's lack of `async` and `await`,
I need to make the `receive` and `send` functions work
as coroutines in their implementation.
I showed how that's possible
in my last log entry
when I adapted callback interfaces
to look like synchronous code.
The nice part about applying this pattern
for the LASGI interface
is that these functions should appear like synchronous code
to the calling application.

I'm not sure how I'm going to deal with the bytes and strings differences
between Python and Lua.
I imagine that the experience will be something like Python 2
when Python strings lacked the same distinction
between bytes and Unicode
like how Lua strings behave.
I'll probably ignore the problem for now
(and regret it later).

By the end of the week,
I got the interface into place
with stubbed out behavior
on both the server side
and the application side.

On the server side,
I have hardcoded the `scope` table containing all the request information.
The `receive` callable is also hardcoded
to provide virtually no useful data
to the application
that is suppose to call that function
and process the resulting event.
I *have* handled the `send` callable
for basic HTTP responses.
The server can handle a response event
that the application passes to `send`
and transform the event
into the HTTP data
that goes on the wire
to the browser.

On the application side,
the application is sending a hardcoded "Hello World!" response back
to the server.
The application also followed the ASGI spec for HTTP
and calls `receive` once
and `send` twice
(for the `http.response.start` and `http.response.body` events).

My favorite part of this process so far is to fire up the server
and use `hey` to see what responses come back.
At this stage,
benchmarks are completely rubbish
since the framework doesn't do anything useful,
but it's fun to see the server "handle" real traffic.

```bash
atlas git:(main) hey http://127.0.0.1:8000

Summary:
  Total:	0.0095 secs
  Slowest:	0.0051 secs
  Fastest:	0.0002 secs
  Average:	0.0019 secs
  Requests/sec:	21110.0933

  Total data:	2400 bytes
  Size/request:	12 bytes

Response time histogram:
  0.000 [1] 	|
  0.001 [13]	|■■■■■■
  0.001 [25]	|■■■■■■■■■■■
  0.002 [89]	|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.002 [2] 	|■
  0.003 [19]	|■■■■■■■■■
  0.003 [25]	|■■■■■■■■■■■
  0.004 [11]	|■■■■■
  0.004 [9] 	|■■■■
  0.005 [3] 	|■
  0.005 [3] 	|■

Latency distribution:
  10% in 0.0008 secs
  25% in 0.0012 secs
  50% in 0.0013 secs
  75% in 0.0028 secs
  90% in 0.0034 secs
  95% in 0.0040 secs
  99% in 0.0049 secs

Status code distribution:
  [200]	200 responses
```

The next phase of this journey is a deep dive
into the application and framework side.
My focus will be on building out the routing layer
that process and incoming connection,
look for a matching route,
and pass off to a controller
that will handle an HTTP request
to return a response.