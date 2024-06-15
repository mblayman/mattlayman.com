---
title: "Lua Log #9: HTTP Parser"
description: >-
    In the last entry,
    I concluded that I wanted to build my own HTTP parser.
    This post looks at how I did the parser building
    and what's next
    for my Lua web framework.
image: img/2022/log-9.jpg
type: post
categories:
 - Lua
tags:
 - Lua
 - HTTP
 - Parser

---

As both a web framework
*and a web server*,
{{< extlink "https://github.com/mblayman/atlas" "Atlas" >}}
needs to parse HTTP requests.

My approach to this project is to build just enough
of what I need before I can move
onto the next piece
of the project.
I'm trying to reach a stage
where the framework is actually useful
for someone,
even if there are lots of sharp edges
and unhandled corner cases.

What is a "just enough" HTTP parser
at such an early stage?
When I thought through that question,
I found that what my parser really needs to implement
from the start
is the request line
of an HTTP message.

The
{{< extlink "https://httpwg.org/specs/rfc7230.html" "HTTP Message Syntax and Routing" >}} specification
includes an Augmented Backus-Naur Form (ABNF)
of the HTTP message.
Maybe you've never encountered ABNF before.
ABNF is a technique
for describing the structure
of something.
The form can describe things like programming languages
and message formats.
ABNF is a structured and consistent way
of breaking a high level concept
(such as an HTTP message)
into its constituent pieces.

I'll use the ABNF to show you how I picked the part
that matters for Atlas currently.
Here's the ABNF of the HTTP message,
taken directly from the specification:

```text
  HTTP-message   = start-line
                   *( header-field CRLF )
                   CRLF
                   [ message-body ]
```

This says that a message must

* include a `start-line`
* include zero or more `header-field` lines that end
    with a CRLF
    (i.e., a "carriage return" character and "line feed" character,
    which is `"\r\n"` in Lua and many other languages)
* include a CRLF by itself as a separator or terminator
* optionally include a `message-body`

The job of the specification is to describe
in detail
what all those pieces mean.
Let's keep digging.
What's in the `start-line`?

```text
  start-line     = request-line / status-line
```

In this format,
the slash (`/`) means "OR."
Since `HTTP-message` describes both the request format
and the response format,
the `start-line` is where there is differentiation.
I'm building an HTTP parser
that needs to route incoming requests,
so I care about the `request-line` currently.

```text
  request-line   = method SP request-target SP HTTP-version CRLF
```

This is starting the look like the pieces
that are required.
The routing layer
that I built for Atlas is concerned
with two kinds
of information:

* The HTTP request method
* The HTTP request path

"Method" and "path" are part of the language used
by the ASGI specification.
`method` is the proper source
to match the ASGI "method"
and maps to HTTP method names
like `GET`, `POST`, and so on.

For "path," we have to keep going.

```text
  request-target = origin-form
                 / absolute-form
                 / authority-form
                 / asterisk-form
```

This is when we start seeing the different kinds
of HTTP scenarios pop up.
I'll save you the trouble of reading this part
of the spec
and tell you that the `origin-form` is what I was after.

```text
  origin-form    = absolute-path [ "?" query ]
```

So,
that's all the spec pieces.
What is "just enough" to get through
this stage?
I built the parser to read the method and path
from the `request-line`.

* Method comes from the `method` in the `request-line`.
* Path comes from the `absolute-path` in the `origin-form`.

In my research,
I found multiple ways to handle parsing.
A more advanced approach seems to use a state machine
to iterate over the incoming network bytes
to determine the parts
of this request.
This approach probably involves the least amount
of overall work and buffering
because these state machines can look at the bytes once
to determine what they are for.

I'm using a less elegant approach to start.
With my approach,
I'm using the pattern matching capabilities of Lua
to look for a valid `request-line`.

Here are the relevant snippets.

```lua
local REQUEST_LINE_PATTERN = "^(%u+) ([^ ]+) HTTP/([%d.]+)\r\n"

function Parser.parse(_, data) -- self, data
  local meta = {type = "http"}
  local method, target, version = string.match(data, REQUEST_LINE_PATTERN)

  -- ...
end
```

I didn't hightlight this early,
but the request line *requires* 2 space characters (`SP`)
between the different parts.
Spaces are *not* allowed
in the other pieces of `request-line`,
so that makes the Lua pattern easier to construct.

Somewhat hilariously,
this is pretty much where I can stop
on this parser for now.
I did some extra error handling that you can check out,
but this is the very basics
of request handling.
For the time being,
I'm ignoring query strings,
encoding,
and probably a ton of other details
that I'm not even aware of.

With a super basic HTTP parser in Atlas,
what's next?

I think it's time for me to return
to the template system
in my web framework.
This is where I started
with Atlas over six months ago.
Like much of the project,
the templates are functional,
but extremely limited.

The next steps with templates are twofold:

1. Create a `render` function
    that wraps up all the details
    of finding the template file,
    rendering the output,
    and packaging the output
    into an HTTP `Response` object.
2. Extend the template system
    to display context data
    inside of template expressions
    (e.g., `{{ foo.bar }}`).

Once all that is done,
I think I might be ready to venture
into the area
that I have feared to tread:
Object Relational Mappers (ORM).
I have *no* idea how to build an ORM
and my raw SQL skills are definitely not as strong
as I would like.

One of the excellent things about this project is
that's it's forcing me to grow my knowledge.
It's extremely unlikely
that I would have read the HTTP specs
without a project to drive that.
Atlas is also going to push me
into obtaining a deeper understanding
of data modeling and SQL.
That's an exciting part
of this effort.

Thanks for reading!
Have questions?
Let me know on X at
{{< extlink "https://x.com/mblayman" "@mblayman" >}}.
