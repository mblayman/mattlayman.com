---
title: "Lua Log #3: Logging Without Logging"
description: >-
    In this Lua log entry,
    I explore what I've learned
    about logging and configuration
    and how I built them out
    in my Atlas project.
image: img/2022/log-3.jpg
type: post
categories:
 - Lua
tags:
 - Logging
 - Atlas

---

I suppose this is my meta post
about logging
in my log
of Lua activities.
My goal this week was to fix this:

```bash
$ busted
++++++++++Listening for requests on http://127.0.0.1:5555
+++++++++++++++++++++++++++++++
41 successes / 0 failures / 0 errors / 0 pending : 0.535622 seconds
```

If you poke around
in the source code
of my
{{< extlink "https://github.com/mblayman/atlas" "Atlas project" >}},
you'd find a bunch of `print` function calls.
The "Listening for requests..." message above
was one of those `print` calls.
My problem with these `print` calls
is that the Busted test runner does nothing
to suppress or capture the stdout stream.
I concluded that I would need to introduce logging
to solve this.

## Building a Logger

Initially,
I didn't want to figure out logging.
From a priorities perspective,
I had the sense that it was a low value feature
of a web framework.
And,
to a large degree,
I think that is true.
There are plenty of very successful apps out there
that use little to no logging.

At the same time,
I didn't want to mess
with Busted configuration
since capturing stdout is not an out-of-the-box feature.
Since I knew I'd probably need some version of logging anyway,
I decided that I should take the detour
and add in some logging capability.

Logging is an area that is not built
into the Lua standard library.
The entire spirit of my web framework is to build a bunch
of the components myself
for the joy of learning,
so I chose to write my own logging implementation.

Where I landed is an API
that shares some characteristics
with Python's `logging` module,
but ignores a lot of the complexity.
Remember,
this is a low priority goal for me,
so I'm ok with an 80% solution
for logging at the moment.

My API has a couple of important characteristics:

* The API expects a user to get a logger with a certain namespace.
  I believe this will let me do some more advanced log filtering
  in the future and namespaces are generally useful.
  A logging namespace will help users know where the log message comes from
  in their app.
* The API can route log messages to different destinations.
  The default destination is stdout.
  Since I'm ultimately aiming for apps
  that work with the
  {{< extlink "https://12factor.net/" "12-factor app" >}} style,
  this is what I'll need most of the time.

The API ultimately looks like this.

```lua
local logging = require "atlas.logging"
local logger = logging.get_logger("my.module")
logger.log("Hello world!")
```

## Configuration As a Side Effect

I just indicated that the default
of my new logging system is to use stdout.
Because of this,
switching from `print` to `logger.log` would have no effect
on my test suite
unless I introduced another concept: configuration.

A web framework is all about serving a wide variety of needs
to build something on the web.
The primary difference between a framework
and a library
is the "Hollywood Principle."

> Don't call us. We'll call you.

Applied to web applications,
this means that a framework will call user defined code
like a Django view
or a Ruby on Rails controller.
Conversely,
a library is something that developers are expected
to use and call
within their own code.

Since the operating principle
of a web framework is to let it do most
of the work
of calling different parts
of the application,
our ability to influence that behavior
comes from the controls
that the framework exposes.
These controls are configuration.

In my earlier logging example,
I want to influence the output
of the test runner.
I can do that if I can configure an alternative place
to write log messages output.

How can we allow users
to change the configuration
of the framework?
This is an area where I don't want to be creative or revolutionary.
I decided to follow a similar pattern to what Django does.

In Django,
configuration is called settings.
Django developers define a settings module
that describes which settings they want to change.
At runtime,
Django mixes the framework's defaults
with the user defined values
to create the application's configuration.

I applied this same pattern for Atlas.
By defining an environment variable named `ATLAS_CONFIG`
that is a module path
to the configuration,
Atlas can create the app config
in the same manner
by overriding user-defined configuration
on top of the default config.

Now, I can create a configuration for the test runner
that will capture stdout
to a file
and give me the clean dots
that I want from the test run.

Before I finished this feature,
I encountered a meta problem:
am I in an app building context
or a framework building context?

## Framework Building Vs. App Building

I configured my environment such that test runs produce clean output
because, most of the time, I'm running tests.
But then I ran my fledgling web server
and all my output was gone.
Doh!
My test configuration was in use
when I need a mode
to run the framework
as a user.

This is an interesting space
that I don't find myself in often.
Usually, most of my code is written
from the user side
of a framework.
I'm rarely in a position
(though I have contibuted to some Django packages)
where I need to write a tool
with another developer in mind
as a consumer.

I think this raises some interesting questions.

* How I can keep the split between framework code
    and app code so that the framework doesn't accidentally depend
    on code written for an app?
* How do I manage and gracefully switch between modes
    as I both implement the framework
    and consume the framework's features?

One way that I think help manage this is with packaging.
A tool that I love in the Python world is `tox`.
With `tox`,
I can run tests against a built package
and do it in isolation.
The benefit is that if there are bugs
in the package
that would manifest and break for other users,
then testing against the packaged version helps shake out those bugs.

I don't think that there is a tool like `tox`
in the Lua ecosystem.
Admittedly,
I haven't looked yet,
so I could be wrong about that.
My next goals for Atlas are to build a real package.
By doing that,
I can enforce this separation early
to help ensure
that I keep the firewall between framework and app code.

Thanks for reading!
Have questions?
Let me know on Twitter at
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
