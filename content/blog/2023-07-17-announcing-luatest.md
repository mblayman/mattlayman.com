---
title: "Announcing luatest: A Lua test runner inspired by pytest"
description: >-
    luatest is a brand new test runner
    that is heavily inspired
    by pytest.
    It's got the speed you love about Lua
    with the DX you love from pytest.
image: img/2023/lua-pytest.png
type: post
categories:
 - Lua
 - Python
tags:
 - Lua
 - pytest
 - luatest

---

I'm pleased to announce a new test runner
for the Lua programming language:
{{< extlink "https://github.com/mblayman/luatest" "luatest" >}}.
luatest draws deep inspiration
from {{< extlink "https://docs.pytest.org/en/7.4.x/" "pytest" >}}
in the Python ecosystem.

Why should you care?

* You're tired of BDD-style test runners in Lua for your projects.
* You want a fast, no nonsense test runner.

The internet loves an unfair benchmark,
so here goes.
I converted the test suite for my side project,
{{< extlink "https://github.com/mblayman/atlas" "atlas" >}},
from {{< extlink "https://lunarmodules.github.io/busted/" "busted" >}}
to luatest.
The execution time of the suite's 109 tests went
from an average of **1.326** seconds
to **0.084** seconds!
That's not a misplaced zero! [^1]

> luatest is roughly 15.8 times faster than busted.

The test suite went from feeling _fast_
to feeling _instant_.

Intrigued? Get started with:

```bash
luarocks install luatest
```

You can also learn more about luatest
on the
{{< extlink "https://github.com/mblayman/luatest" "GitHub repo page" >}}.

## Compared to pytest

luatest is inspired by pytest,
but it is missing some of pytest's headline features.
luatest does **not** include:

1. `assert` rewriting - pytest is awesome because most
    of the API consists of taking a comparison
    and throwing `assert` at the beginning.
    luatest doesn't have that,
    but does have the excellent `luassert` library
    for all your assertion needs.
2. fixtures - pytest's popular fixture feature is not present.
    Lua lacks the native reflection abilities to make the parameter-style insertion
    into test functions possible.
3. plugins - At this time,
    there is no formalized plugin mechanisms to hook
    into the test lifecycle phases.
    This limits luatest's current extensiblity.

So what _does_ luatest bring to the table?
Aside from a lightning quick runtime,
luatest uses the same style of test identification
using a double colon.
This enables the test filtering that you may know and love from pytest.
A filtered test run could look like:

```text
luatest tests/test_some_module.lua::test_something
```

I think these test identifiers are a massively underrated feature of pytest
and I hope that using them in luatest will provide similar benefits.
Having a clear and unique identifier provides the ability to filter tests
for some tricky situations.

Have you ever tried to fix some test pollution between multiple tests
and need to bisect the problem until you find the smallest set of tests
that can reproduce an issue?
These test identifiers make that problem much more tractable.

By following this style of identifiers,
integrating luatest into an editor's test execution tooling should be very doable.
I've already done this myself
for vim-test.
You can checkout my vim-test
{{< extlink "https://github.com/mblayman/dotfiles/blob/main/nvim/autoload/test/lua/luatest.vim" "luatest plugin" >}}
(which I will try to get upstreamed to vim-test some day).

## Compared to busted

busted has a much longer history
and is full of features
that don't exist in luatest.
busted is also a BDD-style test runner
using `describe` and `it`.

```lua
describe("Thingy", function()
    it("should frobnicate", function()
        -- test logic here
    end)
end)
```

After using BDD-style runners
for a long time,
I've got a hot take on this.

> 🔥 Test suites that use nested blocks for tests are an anti-pattern
    and should be avoided. 🔥

Why?
Because knowing what you're testing requires mentally stitching
all the `describe` and `it` blocks together to get the full view
of what is happening in the test.
That's not a problem on the toy example presented above,
but a full test suite with multiple levels of `describe`
is much harder to reason about.
The test descriptions lose spatial locality
by being split apart by multiple inter-related `describe` and `it` calls.
You can get the full test description at runtime,
but that's a very late time to see that.

This style also makes it harder to uniquely identify a test.
And I say this as the person who implemented the test discovery
for individual tests for
{{< extlink "https://github.com/vim-test/vim-test/pull/598" "vim-test for busted" >}}!
It was painful to get that code right!

I don't mean to dunk on busted completely,
but I have definitely soured over the years
on the style of automated test
that busted and other runners use.

Something that busted and luatest share is built-in support
for LuaCov for measuring code coverage.
luatest includes a `--cov` flag
that will provide an lcov-based coverage file
that can be processed by services like Codecov.

## Summary

luatest is the test runner for Lua
that I wanted to exist in the world.
Now it exists.

The next steps for luatest are to get the runner put through its paces
and surface what features are vital
for a successful ecosystem.
Give it a try for your Lua project and enjoy!

Check out all the details I've left out on
{{< extlink "https://github.com/mblayman/luatest" "GitHub" >}}.

[^1]: The results of my benchmarking are available in the {{< extlink "https://github.com/mblayman/atlas/pull/33" "PR" >}}
that switched to luatest.
