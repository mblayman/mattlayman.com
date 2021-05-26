---
title: "Quick and dirty mock service with Starlette"
description: >-
  Have you ever needed to mock out a third party service
  for use in a large testing environment?
  I recently did,
  and I used Starlette,
  a new async Python web framework,
  to do it.
  See what Starlette offers!
image: img/2019/starlette.png
type: post
categories:
 - Python
tags:
 - Python
 - Starlette
 - Testing

---

I had a challenge at work.
The team needed to mock out a third party service
in a testing environment.
The service was slow
and configuring it was painful.
If we could mock it out,
then the team could avoid those problems.

The challenge with mocking out the service
is that part of the flow needs to invoke a webhook
that will call back to my company's system
to indicate that all work is done.
Additionally,
the webhook call must be after a delay
because the service we're simulating takes a long time
(i.e., more than 60 seconds).

> **The Problem:** Run a mocked third party service
    with a delayed webhook callback.

The solution needs to:

* Respond to a POST request and return a `200 OK` status.
* Call a webhook back to the system
    that will include extra identifiers
    to connect the webhook call to the original request.
* Be as simple as possible
    because this is not the core product.

## Solution options

The Python ecosystem is full of strong options
to address the first part of the solution.
Django, Flask, Pyramid, Bottle,
and any other web framework you can think of
would handle that with ease.

The second part of the solution is harder.
If I'm not careful,
then being simple goes out the window,
and I've destroyed the third objective.

### Background task tools

As much as I love Django,
I didn't think it was a good fit.
In my thought process,
calling the webhook later required some kind of background task.
If you know Django,
then you may immediately think
of {{< extlink "http://www.celeryproject.org/" "Celery" >}},
and that was my first thought too.
The problem is that Celery requires a message broker
like {{< extlink "https://www.rabbitmq.com/" "RabbitMQ" >}}.
*With that, the simplicity budget is totally shot.*

An alternative to Celery is {{< extlink "https://python-rq.org/" "RQ" >}},
but it has similar problems
and requires running {{< extlink "https://redis.io/" "Redis" >}}
along with a separate worker process.

> Could we solve this problem
    without using a separate background task tool?

### Sans background task tools

Knowing that simplicity was an important goal,
I really wanted to do this
without a background task tool.

I considered two approaches:

1. Use threads.
2. Use cooperative concurrency (read: asynchronous programming)

I don't like threaded programming in Python.
In fact,
I don't like threaded programming. [^1]
A threaded solution could totally work
by executing the webhook call in a separate thread,
but I was interested in other options.

[^1]: I've been studying Rust on the side
    so maybe that language can change my mind
    about threaded programming,
    but the verdict is still out.

Could I solve the problem
with async programming?
Async programming is much easier
in recent versions of Python.
The language now has built-in keywords
like `async` and `await`
that makes programming
in that style friendlier.
I've assessed a few async web frameworks,
and I recalled a feature that I saw
in the {{< extlink "https://www.starlette.io/" "Starlette" >}} documentation:
{{< extlink "https://www.starlette.io/background/" "Background Tasks" >}}

Starlette is a web framework developed
by the author of {{< extlink "https://www.django-rest-framework.org/" "Django REST Framework (DRF)" >}},
{{< extlink "https://twitter.com/_tomchristie" "Tom Christie" >}}.
DRF is such a solid project.
Sharing the same creator bolstered my confidence
that Starlette will be a well designed piece of software.

I decided to {{< extlink "https://en.wikipedia.org/wiki/Spike_(software_development)" "spike" >}}
on the project
to see if it was a viable path.
A hour later,
I was shocked to see that I had a final, *working*, solution.

The rest of this article will explore what I did
to solve the problem
using Starlette
with a generic version
that skips the boring details
of the third party service.

## Starlette

Since Starlette is an async framework,
the Python tools needed
to support a Starlette application
are different
from a standard {{< extlink "https://www.python.org/dev/peps/pep-3333/" "WSGI" >}} app.

Instead of a *synchronous* web server like {{< extlink "https://gunicorn.org/" "Gunicorn" >}}
or {{< extlink "https://uwsgi-docs.readthedocs.io/en/latest/" "uWSGI" >}},
an *asynchronous* web server is required.
I selected {{< extlink "https://www.uvicorn.org/" "Uvicorn" >}},
a web server similar to Gunicorn
that uses {{< extlink "https://uvloop.readthedocs.io/" "uvloop" >}}
to handle the asynchronous event loop.

To do the webhook callback,
the emulator needs to make HTTP requests.
The natural package to reach for is {{< extlink "https://requests.readthedocs.io/en/master/" "requests" >}},
but `requests` is a synchronous package
that would block the event loop.
I needed an asynchronous HTTP request library.
For that requirement,
I picked {{< extlink "https://www.encode.io/httpx/" "HTTPX" >}}.
HTTPX is a very new library
that shares the same API as `requests`
**and** works with async programming.

If you want to follow along,
first,
install all the necessary dependencies.
You'll need at least Python 3.6.

```bash
$ mkdir mock-service
$ cd mock-service
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install starlette uvicorn httpx
```

For future readers,
here are the versions that the `pip install` command installed
into my local virtual environment
at the time of writing this article.

```bash
$ pip freeze
certifi==2019.6.16
chardet==3.0.4
Click==7.0
h11==0.8.1
h2==3.1.1
hpack==3.0.0
hstspreload==2019.8.20
httptools==0.0.13
httpx==0.7.1
hyperframe==5.2.0
idna==2.8
rfc3986==1.3.2
starlette==0.12.8
uvicorn==0.8.6
uvloop==0.12.2
websockets==7.0
```

Let's start by listing the full example.
I'll break down each part of the app,
but sometimes it helps to get the full picture first.
To try this out yourself,
you can grab {{< extlink "/2019/mock_service.py" "the example script" >}}.

```python
import asyncio
import os
import uuid

import httpx
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
import uvicorn

app = Starlette()
client = httpx.AsyncClient()
CALLBACK_URL = os.environ["CALLBACK_URL"]


@app.route("/api/endpoint", methods=["POST"])
async def fake_endpoint(request):
    identifier = str(uuid.uuid4())
    payload = {
        "identifier": identifier,
        "some_parameter": request.query_params.get("some_parameter"),
    }
    task = BackgroundTask(trigger_webhook, payload)
    return JSONResponse(
        {"identifier": identifier, "success": True}, background=task)


async def trigger_webhook(payload):
    await asyncio.sleep(5)
    params = {
        "success": True,
        "identifier": payload["identifier"],
        "some_parameter": payload["some_parameter"],
    }
    await client.get(CALLBACK_URL, params=params)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Running the code

We can run the code end-to-end
to simulate how this would plug into a real environment.

First,
we need a webhook receiver.
The Python built-in HTTP server is perfectly suited
for this task.
In a separate terminal,
run:

```bash
$ python3 -m http.server 5000
Serving HTTP on 0.0.0.0 port 5000 (http://0.0.0.0:5000/) ...
```

Next,
start the mock service.

```bash
(venv) $ CALLBACK_URL=http://0.0.0.0:5000 python3 mock_service.py
INFO: Started server process [47148]
INFO: Waiting for application startup.
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Notice that I've passed in `CALLBACK_URL` as an environment variable
with the URL from our webhook receiver.
The mock service will use this information
to know where to send the webhook request.

With the core pieces in place,
we need to trigger the mock service.
I like {{< extlink "https://httpie.org/" "HTTPie" >}}
as a friendlier alternative
to {{< extlink "https://curl.haxx.se/" "curl" >}}.

```bash
(venv) $ pip install httpie
```

Now we can get everything moving!
Let's fire off a POST to the mock service.

```bash
(venv) $ http POST :8000/api/endpoint some_parameter==some_value
HTTP/1.1 200 OK
content-length: 68
content-type: application/json
date: Sat, 24 Aug 2019 15:54:07 GMT
server: uvicorn

{
    "identifier": "4a3a0ce2-ae0c-41d3-ba58-89a5a9579692",
    "success": true
}
```

From the mock service,
you will see a log like:

```bash
INFO: ('127.0.0.1', 61647) - \
    "POST /api/endpoint?some_parameter=some_value HTTP/1.1" 200
```

Five seconds later,
the fake webhook receiver should show:

```bash
127.0.0.1 - - [24/Aug/2019 11:54:12] \
    "GET /?success=true&identifier= \
    4a3a0ce2-ae0c-41d3-ba58-89a5a9579692&some_parameter=some_value \
    HTTP/1.1" 200 -
```

I've reformatted the lines so they will fit better
in the article.

**Awesome!**
The mock service did exactly what we wanted.
The POST request got a successful response
and, after a delay,
the webhook got some of the same information.

Now that we've seen things work,
let's break down the code.

### Mock service explanation

We can look at this code
in a few separate chunks.

```python
import asyncio
import os
import uuid

import httpx
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
import uvicorn
```

The import section isn't very exciting.
I've divided the standard library imports
from the third party imports.
If we had more code
in separate files,
then I'd have a third section
for local imports,
but we don't need that
because the entire emulator file fits
in 39 lines.

```python
app = Starlette()
client = httpx.AsyncClient()
CALLBACK_URL = os.environ["CALLBACK_URL"]
```

This section creates the module level globals
that we are going to use.
Sometimes globals are the best tool
for a job
even if they are often frowned upon.
The `CALLBACK_URL` is the only setting
for the emulator.
Notice that I get the value
from `os.environ` with the index syntax
instead of the `os.environ.get('CALLBACK_URL')` syntax.
The index style of fetching will ensure
that we have the value
since it's required to operate the emulator properly.

```python
@app.route("/api/endpoint", methods=["POST"])
async def fake_endpoint(request):
    identifier = str(uuid.uuid4())
    payload = {
        "identifier": identifier,
        "some_parameter": request.query_params.get("some_parameter"),
    }
    task = BackgroundTask(trigger_webhook, payload)
    return JSONResponse(
        {"identifier": identifier, "success": True}, background=task)
```

This async function defines the core route.
The style should be extremely familiar
to Flask users.
The body of the function does a handful of things:

1. Generates an identifier
    that a caller could use
    to associate this call
    with the webhook
    that will follow.
2. Extracts a value from the request's query string, `some_parameter`,
    and stores it
    for the background task.
3. Bundles data
    into a payload
    that will be available
    to the `BackgroundTask`
    which will execute the `trigger_webhook` function.
4. Responds with the identifier
    and sets the background task to run.

One weird aspect of this emulator is that it's handling POST requests,
but there is no POST data processed.
The real third party service included PDF files
in the POST,
but I wanted to ignore that aspect
since it did not illustrate any extra value.

```python
async def trigger_webhook(payload):
    await asyncio.sleep(5)
    params = {
        "success": True,
        "identifier": payload["identifier"],
        "some_parameter": payload["some_parameter"],
    }
    await client.get(CALLBACK_URL, params=params)
```

The webhook trigger sleeps for 5 seconds.
It's important to use `asyncio.sleep`
instead of `time.sleep`.
The sleep function from `time` is a synchronous command
and will block the event loop.
By calling `asyncio.sleep`
with `await`,
the function yields execution back
to the event loop
until 5 seconds pass.

Once the delay is over,
the HTTPX `client` calls
the callback URL
to return the identifier and parameter.
This indicates to the caller
that the emulator is done.

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

The final bit of code connects the app
to Uvicorn
so that Uvicorn will start
when the service is invoked with:

```bash
(venv) $ python3 mock_service.py
```

### Starlette's promising future

Starlette's API made this emulator
as quick to produce as I could possibly hope for.
The framework is still new,
but I think it has a very promising future
in the Python ecosystem.
It already has the best performance
of any Python framework
in the {{< extlink "https://www.techempower.com/benchmarks/#section=data-r18&hw=ph&test=query&l=zijzen-f" "TechEmpower Benchmarks" >}}.

I hope you enjoyed looking at some async programming
in Python.
If you have any questions,
please share on Twitter
and reach me at {{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.

Thanks for reading!
