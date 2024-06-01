---
title: "Lua Log #5: Callbacks to Coroutines"
description: >-
    I've been working on how to avoid callbacks
    in my web framework.
    My goal with Atlas is to produce interfaces
    that look like synchronous calls,
    but utilize cooperative scheduling
    (coroutines)
    under the hood
    to handle work asynchronously.
image: img/2022/log-5.jpg
type: post
categories:
 - Lua
tags:
 - Callbacks
 - Coroutines
 - Atlas

---

When I interact with my
{{< extlink "https://github.com/mblayman/atlas" "Atlas project" >}}
as a user,
I don't want to work
with callbacks.
Using callbacks is a fairly confusing mechanism
compared to synchronous lines of code.
Compare:

```lua
local function callback()
  do_stuff_later()
end

do_stuff_now(some_argument, callback)
```

Versus:

```lua
do_stuff_now(some_argument)
do_stuff_later()
```

To my eye,
the latter version is astoundingly better.

The challenge that I have on my project is that I'm using Lua's binding library
to `libuv` called `luv`,
and `luv` makes heavy use of callbacks.
For instance,
even writing to a file-like interface like `stdout` requires a callback
with `luv`.
If I have a logging interface,
I don't want to force users
to create a callback function every time they want to log something.
That's totally overkill.

With some clever use of coroutines,
I can make the kind of interface that feels natural.
The key to my strategy is to make the `luv` event loop run inside
of a coroutine.
I also nested another coroutine inside of my framework
so that every TCP client that handles separate requests runs inside
of a coroutine.

The flow is something like this:

1. The main coroutine runs and registers a listener to listen
    for TCP connections for future HTTP traffic.
2. The event loop within that coroutine starts.
3. On a client connection, a new coroutine is created
    for the life of that client connection.
4. At any point, if the client does something
    that uses `luv` callbacks (like logging to stdout),
    the coroutine yields back to the main loop.
5. Control returns back to the main coroutine
    and loop processing can continue.
6. Eventually, the activity (like logging waiting for the file system) will finish
    and the loop will invoke the callback.
7. The callback is carefully crafted to resume the client's coroutine.
8. The client coroutine can continue processing.

The wrapping pattern to make this transparent to users looks like:

```lua
local function make_callback()
  local thread = coroutine.running()
  return function(err, _)
    assert(not err, err)
    coroutine.resume(thread)
  end
end

function synchronous_looking_interface(arg1, arg2)
  luv.some_async_interface(arg1, arg2, make_callback())
  return coroutine.yield()
end
```

There are two key elements to make this work:

* The call to the `synchronous_looking_interface` must be in a coroutine itself.
    This isn't a problem because I'm wrapping every client connection
    in a coroutine.
* The `make_callback` is taking advantage of a closure.
    `coroutine.running` returns the currently running coroutine.
    The newly created callback function locks in that coroutine,
    so that the system knows what to resume
    when the event loop calls this callback.

I'm sure I'll find flaws in this scheme
as I develop more code
(for instance,
it's not immediately clear to me how I'll return results back
if I need to).
I'm hoping that this pattern will work,
but I need to write more code to see how well it stands up.

Now that I have this pattern to get rid of callbacks,
I'm ready to start building more interfaces
that framework users would use.
I have a stub response that the server is returning.
I think my next goal is to get back to the ASGI-like interface
and see if I can push the stub response
into the application layer (where responses *should* be coming from).

In my repository,
I have a sample app in an `app` directory
that sits next to my `src` directory
for the framework.
I think this separation gives me the place to start proving out
how the framework will plug in an app.
Seeing the framework start to emerge
from the application side will be really neat to see.

Thanks for reading!
Have questions?
Let me know on X at
{{< extlink "https://x.com/mblayman" "@mblayman" >}}.
