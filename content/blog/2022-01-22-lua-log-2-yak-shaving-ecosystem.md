---
title: "Lua Log #2: Yak Shaving the Ecosystem"
description: >-
    As I progress on my Atlas project,
    I'm finding holes in the Lua ecosystem
    with the tools that I'm using.
    This article discusses how I filled some
    of those holes.
image: img/2022/log-2.jpg
type: post
categories:
 - Lua
tags:
 - Tools
 - Atlas

---

I picked Lua for my hobby project deliberately.
I chose Lua because it's a fast and small interpreted language.
I also chose the language *because* it is a smaller ecosystem
than the Python ecosystem
that I usually work in.

On the
{{< extlink "https://www.tiobe.com/tiobe-index/" "Tiobe Index" >}},
Python is in the pole position at #1,
while Lua is not even in the top 25.
Lua sits at 30th rank on the index.

From my point of view,
this means that there are more unexplored areas
for the Lua ecosystem.
While Python is great for grabbing packages
that are at the ready,
this story is not so similar
for Lua.
Since my project is all about exploring the language space,
having unexplored areas leaves a lot of options open,
if I'm willing to put in the work.

On the flip side,
trailblazing comes at a cost
for some things
that are unrelated to my project,
but I would like to have
for nicer developer ergonomics.

This has led me to do some yak shaving
of the Lua ecosystem.

> **Yak Shave**:
> Doing a task that leads to another task
> that leads to another task and so
> until you find yourself working
> on tasks that are distant
> from your original goal.

## The First Yak - Testing

My first yak shave came about
with my test tools.
In the Lua ecosystem,
{{< extlink "https://olivinelabs.com/busted/" "Busted" >}}
seems to be one of popular unit testing libraries.
When I write my code in Vim,
I like to have my primary source file
in one split window
and my unit test file
in an adjacent split.
I use {{< extlink "https://github.com/vim-test/vim-test" "vim-test" >}}
to trigger my unit tests directly
in Vim.
This feedback loop is so fast
because I never have to leave my text editor
while working with my code.

On my Python projects,
I can press my leader key
(mine is mapped to the space bar),
followed by `t`
to run the exact unit test
that my cursor is nearest to.
If you can't run a single unit test
with a keyboard shortcut,
then I strongly recommend you try it out.
I think it might transform your workflow
as much as it transformed mine
once upon a time.

Anyway,
when I tried the same thing as I started on the template engine
of my
{{< extlink "https://github.com/mblayman/atlas" "Atlas" >}}
web framework,
my shortcut ran the entire file of tests
instead of a single test.
I went to the vim-test source code and confirmed that, sure enough,
the `:TestNearest` command was only able to detect the test file name.
Therefore,
the granularity of my test command was limited to whatever test file
I tried to run.

This constraint made decent sense to me
because of the way Busted works.
Unlike pytest,
Busted is a Behavior Driven Development (BDD) style test framework.
In practice,
that means that instead of having test code like:

```python
def test_some_function():
    result = do_stuff()
    assert result == 42
```

The test code looks like:

```lua
describe("Thing", function()
    it("does stuff", function()
        local result = do_stuff()
        assert.equal(42, result)
    end)
end)
```

I'll argue that the former style is easier for test tools
to find individual tests
than the latter style.
The reason is because `test_some_function` is a clear identifier
that can be discovered by testing tools.
In contrast,
the function in the BDD-style is `it`.
When you have more than one test in pytest,
you'll need functions with different names
or else Python will think there is only a single function definition.
With Busted, tests will have multiple `it` calls
and that is perfectly normal.

The support for pytest in vim-test will put together the unique identifier
(e.g., `test_file.py::test_some_function`)
and invoke pytest with that identifier
as the argument.

At first glance,
it doesn't seem like there is much that could be done
to work around this problem for Busted.
Then I found that Busted has a `--filter` option.
The filter option takes a Lua pattern
and runs tests whose *string description* matches the pattern.
So,
I concluded that I can't match on the `it` function name,
but I could possibly match
on the `"does stuff"` description.
My solution wouldn't be perfect because two tests could have the same description,
but it would be better than running the whole file.

The outcome of my effort was the
{{< extlink "https://github.com/vim-test/vim-test/pull/598" "vim-test/vim-test#598" >}}
Pull Request.
Essentially,
the feature does a Vim regex search to find the description
of a test,
then transforms that description
into a Lua pattern
that can be passed to the `--filter` option.
Along the way,
I learned a few things.

* Writing Vimscript is painful.
* Lua patterns have a number of escape characters that must be matched
    if you want to match an exact description.
    The escape character is a `%` instead of a `\`
    like many other languages.
    This creates funny scenarios
    because Vim treats `%` as the current file name
    when executing external commands.
* If you have to deal with escaping across multiple languages
    *and* a shell, good luck.
    My head wanted to explode at times
    while trying to reason about all the escaping.
* The Moon dialect of Lua is pretty nice.
    vim-test's Lua support works for Moon too,
    so I had to devise a pattern that worked
    with both dialects.
* The vim-test test suite uses {{< extlink "https://github.com/kana/vim-flavor" "vim-flavor" >}},
    which is written in Ruby.

For those keeping score at home,
that means that, to add this feature,
I had to work with:

* Lua
* Vimscript
* Shell
* Moon
* and Ruby

This Yak was hairy.
Happily,
the feature got merged,
and I can run individual unit tests
in my project now
with a couple of keystrokes.

## The Second Yak - Pre-commit Linting

I'm a huge believer
in using linting tools
that can either automate away drudgery
like code formatting
or spot problems
using static analysis techniques
like finding unused variables.
Code tools are what give developers most
of our superpowers
as we put computers to work
on tasks that we stink at.

I set up Continuous Integration early
in my project
on GitHub Actions
to keep me honest.
My GitHub Actions setup:

* runs all my unit tests,
* builds my Luarock (Lua's packaging format),
* statically analyzes with Luacheck,
* and checks code formatting with LuaFormatter.

Having CI is great.
Having CI that is often failing on you is not great.
I kept making mistakes
because I didn't have all my linters set up
in Vim.

Wouldn't it be great
if I could run my lint checks *before* I push code
to GitHub?
Most certainly!

Thankfully,
I know of a great tool
to help with this:
{{< extlink "https://pre-commit.com/" "pre-commit" >}}.
pre-commit installs a Git hook
that will cause the tool to run every time
that I run `git commit`
on my project.
When the pre-commit tool runs,
it can execute a set of user defined hooks
that I set in a `.pre-commit-config.yaml` file.
Super,
I can add Luacheck and LuaFormatter
to pre-commit
and prevent an entire category of errors
from reaching GitHub Actions.

I checked the list of support languages and...
Lua wasn't there.
Then I checked the list of supported hooks.
Luacheck and LuaFormatter *were* there,
but the definitions use the `system` option.
This means that the hooks could work,
but the hooks assume that you have a working `luacheck`
and `lua-format`
on your `PATH`.
One of my favorite things about pre-commit is that most
of the hooks will do all the setup for you.
`system` is the escape hatch
that punts on that quality.
I wanted native hooks to exist
because I thought that would be nicer
for future Lua pre-commit users.

I made a small contribution to pre-commit years ago,
but not to support a new language.
Looking at the source,
I saw that adding a new language was a well scoped activity
if I could implement the required hooks
that plug into the core of pre-commit.

With my
{{< extlink "https://github.com/pre-commit/pre-commit/pull/2158" "pre-commit/pre-commit#2158" >}} PR,
I helped get Lua added as a supported language.
Ultimately,
the diff for that change is not huge,
but I'm grateful
for all the help
that the maintainer,
{{< extlink "https://twitter.com/codewithanthony" "Anthony Sottile" >}},
provided while working through the change set.
The process of figuring out package isolation
with Luarock trees,
setting the right `LUA_PATH` and `LUA_CPATH`,
and getting appropriate test coverage
was a fairly involved process.

To close out my effort,
I {{< extlink "https://github.com/pre-commit/pre-commit.com/pull/622" "added the docs" >}}
for
{{< extlink "https://pre-commit.com/" "pre-commit.com" >}}.
I believe that a feature doesn't really exist
unless it's documented and users know it is available.

Once pre-commit 2.17.0 was out,
I could add hook definitions
to Luacheck and LuaFormatter.
By adding the hook definitions to the core projects,
users can use pre-commit directly from the canonical source repos.
Fortunately,
hook definitions are the easiest part
of the process.
I completed my pre-commit yak shave with the
{{< extlink "https://github.com/lunarmodules/luacheck/pull/48" "lunarmodules/luacheck#48" >}}
and
{{< extlink "https://github.com/Koihik/LuaFormatter/pull/236" "Koihik/LuaFormatter#236" >}}
PRs.

## What's Next?

I think I'm done yak shaving for a while.
The tools that I now have in place are mostly sufficient.
There is one more project
that I might pursue in the future
to improve LuaCov
and enforce a coverage percentage
on my code,
but I've
{{< extlink "https://github.com/mblayman/atlas/blob/38b6777bd8ce13d32363be4adb7ba521079b7a62/.github/workflows/tests.yml#L36" "hacked together" >}}
a workaround for now.

My next goal in my project is to design a logging scheme
for Atlas.
I've been using the very lazy strategy
of calling `print`
for some debug logging,
but the output shows up in my test runs
because Busted doesn't capture stdout.

The thing that I enjoyed about these yak shaves
(aside from the very tangible benefits
that I made for myself and the community)
is that this deepens my knowledge
of the Lua language ecosystem.
My hope is that this knowledge will benefit me
as a build out my web framework.

Thanks for reading!
Have questions?
Let me know on Twitter at
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
