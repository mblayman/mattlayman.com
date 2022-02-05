---
title: "Lua Log #4: Build a (Terrible) Package"
description: >-
    Another week,
    another bit of Lua progress.
    This week,
    I got into building a Lua package.
    Let's cover some things
    that I learned.
image: img/2022/log-4.jpg
type: post
categories:
 - Lua
tags:
 - Packaging
 - Atlas

---

I have weird vision
that, someday,
my
{{< extlink "https://github.com/mblayman/atlas" "Atlas project" >}}
will be useful to others.
This is a particularly weird vision
because the project is mostly
for me to explore building a web framework.
Realistically,
I don't expect any kind of consumer audience
for a long time,
if ever.

Even if there is no plan
on the horizon
to have something useful for others,
I wanted to learn how to distribute code
in the Lua ecosystem.
My logic is that building a package now
while the framework is small and simple
will help ensure
that I maintain a package going forward
as complexity increases.

In Lua,
the most common distribution system
that I see is
{{< extlink "https://luarocks.org/" "LuaRocks" >}}
(get it? Lua means "moon" in Portuguese
so Lua packages are "moon rocks," essentially).
To build a rock,
I had to create a "rockspec" file.

I can create a rockspec,
then upload my rock
to LuaRocks
so that users can run:

```bash
luarocks install atlas
```

This works today!
You can see the details
about my rock
at the
{{< extlink "https://luarocks.org/modules/mblayman/atlas" "LuaRocks's atlas page" >}}.

> From now on, I'm a rock polisher. :)

Creating a rockspec offers me some benefits beyond easy distribution.
Primarily,
the rockspec provides tools for managing dependencies.
As much as I'm trying to do stuff
on my own,
there are things that my project depends upon.

* `argparse` - For command line flag handling
* `inspect` - For pretty printing Lua tables
    (The default table printing will only print a memory address.
    That's not very useful.)
* `lpeg` - A PEG parser tool that I use as the backbone
    of my template engine
* `luv` - Lua bindings to the popular `libuv` project
    that I use as the basis for the web server

With these packages added to the rockspec,
I can run

```bash
luarocks make atlas
```

and get all of my dependencies installed locally
with minimal fuss.

So,
why is my package *terrible*
as mentioned in the title?
Atlas does nothing useful currently.
It won't help you with your next web project.
The tools inside of it aren't even close
to finished.
I even messed up my handling of `ATLAS_CONFIG`
so that the `atlas` command will not output help information
without setting a non-obvious environment variable.

The nice part about putting out a terrible package is
that I can only go up from here. 😜

## Quirks

Using LuaRocks has some quirks
that I had to get used to
for my project.

Lua lacks a great isolated environment story.
When I work with Python,
I can create a virtual environment
with the `venv` module
and use that environment
so that all the packages
that I install stay contained
to that project.
Similarly with JavaScript,
if I'm doing some kind
of frontend development,
npm will prefer
to install packages locally
in a `node_modules` directory.
With npm,
you must choose to install globally.

With LuaRocks,
the system prefers to install
to a global location by default.
In the LuaRocks parlance,
rocks are installed in a "tree."
I'm amused by the visual image
of trees on the moon
or the image of rocks
in a tree,
but, whatever,
that's the name.
To work around this global by default preference,
I can use the `--tree` option
on `luarocks` commands.
I've added some local aliases
to work around this limitation,
but that was the first quirk I encountered.

The next quirk was with handling the rockspec file itself.
`luarocks` includes a command named `write_rockspec`.
This command will provide a template
of a rockspec
that you can fill with details
about your package.

One detail that surprised me was the inclusion
of a `modules` list.
The modules list was a literal mapping
of a Lua module name
to the location
of the associated source file.
Managing this kind of list struck me
as a particular kind of insanity.
The configuration would look something like:

```lua
  modules = {
    ["atlas.main"] = "src/atlas/main.lua",
    ["atlas.templates.code_builder"] = "src/atlas/templates/code_builder.lua",
    ["atlas.templates.environment"] = "src/atlas/templates/environment.lua",
    ["atlas.templates.parser"] = "src/atlas/templates/parser.lua",
    ["atlas.templates.template"] = "src/atlas/templates/template.lua"
    -- And so on.
  },
```

Who wants to manually update a manifest
whenever you create a new file?
The process is so susceptible to mistakes
that I concluded that there must be another way.
As I read LuaRocks docs,
I learned that LuaRocks can build the list automatically
(much like the template command originally did).

To use this feature,
I thought I only needed to remove `modules`
from my rockspec.
**That's wrong.**
The reality is that this auto-modules feature is only available
if I declare a newer `rockspec_format`.
For some reason, `write_rockspec` doesn't do this by default.
After updating my file to include
`rockspec_format = "3.0"`,
the package built correctly
without the explicit `modules` list.

Another quirk about rockspecs is that they are version specific
*in the filename*.
This is different behavior
from my packaging experience with Python, Perl, Ruby,
and some other languages where I've used packaging systems.
I'm not sure why LuaRocks uses this methodology,
but that was another one
that I have to get used to.
Mercifully,
there is a command called `new_version`
to generate a new rockspec
from a previous one.

The final quirk that I struggle with is some command confusion.
LuaRocks includes three commands named `make`, `build`, and `pack`.
These commands are so close in function
with each other
that it's hard to keep track of the differences
in behavior.
One of the most useful documentation pieces
that I discovered was
{{< extlink "https://github.com/luarocks/luarocks/wiki/luarocks#overview-of-the-difference-between-make-build-install-and-pack" "a table comparing these commands" >}}.
This table leads me to conclude
that this confusion is a common problem
for LuaRocks.

## Other Things This Week

My editor was driving me crazy!
I'm using Neovim
for this project
because Neovim went all in
with Lua
as its language of choice
for configuration.
Because of this choice,
the Language Server Protocol (LSP) support
with Lua
is pretty solid.
Unless you're using the Busted test runner.

Busted uses a BDD style.
My tests are full of `describe`, `it`, and `assert.*` calls.
Unfortunately,
these functions are inserted globally
into scope by Busted
when it runs.
Since there is no library to `require`,
I had warning messages all over my test files
about undefined fields and functions.

I worked around the biggest ones
by adding `describe` and `it`
to my LSP configuration
as globals that it should accept.
I could have done this with `assert`,
but `assert` is one of the built-in functions
*and* Busted adds attributes
so that users will call things
like `assert.equal` or `assert.truthy`.

My epiphany this week is that Busted is doing nothing more
than importing my `assert` table
on my behalf.
To make my LSP client happy,
all I needed to do was `require` the `assert` directly.

```lua
-- my_module_test.lua
local assert = require "luassert.assert"

describe('Thingy', function()
  it('works', function()
    assert.equal(42, 42)
  end)
end)
```

This revelation made working with my tests far more enjoyable
because I no longer have warnings
of undefined fields
next to all my `assert` statements.
It's great!

This week I'm going to focus my attention
on how to write asynchronous test code.
My project will use a lot of async work
with coroutines.
I need to determine how to control an event loop
in my test runs
so that the synchronous test runner
will play nicely with the asynchronous code.
Busted provides an `async/done` pair of functions
where `done` is supposed to be called when the async work is complete.
I probably need to hook
into those APIs is some fashion.

I'm going to do this kind of testing
so that I can checking that my logger works asynchronously.
The challenge will be combining Lua coroutines,
the libuv event loop,
and Busted's async API.

I'll report back when I've figured some of this stuff out.

Thanks for reading!
Have questions?
Let me know on Twitter at
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
