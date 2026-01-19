---
title: "Lua Log #7: Routing Requests"
description: >-
    Do you know the feeling
    when a project starts coming together
    and things seem exciting and electric?
    I had some of that feeling this week
    as I figured out how to route requests
    in my web framework.
image: /static/img/2022/log-7.jpg
categories:
  - Lua
tags:
  - Lua
  - Routing
slug: lua-log-7-routing
date: 2022-03-06
---

Any web framework
that wants to be useful
needs some kind of mechanism
to take HTTP request paths
and map those requests
to some kind of code
that can return a response.
That's the functionality
that I added to [Atlas](https://github.com/mblayman/atlas)
this week.

Generally,
in my experience with web frameworks,
this concept of connecting HTTP requests
to the right handling code
is called *routing*.

I've seen a couple of big ways to handle routing.
Let's consider the ways,
then I'll talk about my choice.

One option is to create a tree structure.
In this model,
there is a root node
that maps to the `/` path,
and child nodes can handle more detailed paths.
This this model a request walks
through this tree structure
until it encounters the node
that maps to the path.
From there,
the node can delegate
to some code that can handle the request
and generate a response.

Another option is to create a flat list
of objects
that match to paths,
often using regular expressions
to do pattern matching.
A primary difference in this model is
that path segments don't need
to match to individual nodes.
Stated differently,
in this model,
a path like `/some/long/path/to/something`
can match to a single object
instead of traversing six nodes corresponding
to `/`, `some`, `long`, `path`, `to`, and `something`.

Of those two options,
I picked the latter path.

An Atlas app will look something like this:

```lua
-- app/main.lua

local Application = require "atlas.application"
local Route = require "atlas.route"

local controllers = require "app.controllers"

local routes = {
  Route("/", controllers.home),
  Route("/about", controllers.about),
}
app = Application(routes)

return {app = app}
```

The `app` object handles the LASGI (Lua AGSI) interface
that I implemented recently.
In the context of a single HTTP request,
the Atlas app will loop
through each of the `Route` instances,
and try to find a match.
If no match is found,
the app will return a `404 Not Found` response.

This example is very simplistic
because it tries to match one
of two literal routes.
There are some other core features
that I've built into the `Route` class.
A common activity
in routing
is to extract information
from the path itself.

For instance,
maybe you have public profiles
for users
on a website.
What if you want to support something
like `/users/mblayman`?
In this case,
`mblayman` is a bit of dynamic data
that the handling code will need to use
to look something up in a database
or some other data storage.

Atlas routes can use converters
to extra this data.

```lua
local Route = require "atlas.route"

local controllers = require "app.controllers"

Route("/users/{username:string}", controllers.user_profile),
```

With this `Route` definition,
a string value can be pulled
from a request
and passed
to the handling code
(which I'm calling a controller,
named after the Model View Controller design pattern
that I'm attempting to follow).
The controller will receive
that string as an argument.

```lua
-- app/controllers.lua

local function user_profile(request, username)
  -- do stuff
end

return {user_profile = user_profile}
```

Currently,
I have added two types of converters
for routes: `string` and `int`.
That seemed like a enough
to make routes generally useful,
and I can create more converters over time.

Under the hood,
the route path of `/users/{username:string}`
is converted into a Lua pattern.

That Lua pattern would be

```lua
^/users/([^/]*)$
```

The collection of routes gets processed
by a router.
The router has the job of

* Receiving a request path
* Iterating over the routes to find a match
* Invoking the route to run with the request data

All of the core routing functionality is in place and operational!
I have a more that I could do with routing,
but I want to keep moving for now.
The most notable missing thing is a way to group a bunch
of related routes.
Grouping will be a nice feature
as I try to create a more modular design
in the future.

My next goal is to put into place the `Request` and `Response` interfaces
that will be crucial abstractions
when working with HTTP.
When I complete those,
I'll have a minimally viable application system
that can receive requests,
route a request to a controller,
and return a response.