---
title: "Most Abstract Function First Is Better"
description: >-
    How should you order your functions
    in a file?
    Should helper functions go first
    or should you put them after a public interface?
    In this article,
    I'll explain why I think putting the most abstract function first
    is better.
image: img/2022/better.jpg
type: post
categories:
 - Opinion
 - Python
tags:
 - Opinion
 - Programming

---

Python is one of many languages
that will let you define your module's functions
in whatever order you want.
*If your language of choice allows functions
to be order independent,
what order should you choose?*

Let's illustrate what I'm talking about
so that we're all on the same page.
First,
here's a Python example that puts the helper function first.

```python
def child():
    print("hello world")

def parent():
    child()

parent()
```

And here's a version that does the opposite.

```python
def parent():
    child()

def child():
    print("hello world")

parent()
```

Both versions work.
*I believe the latter version is better*.
Here's why.

## Rationale

My assertion seems rather arbitrary,
so what is it about the latter version
that makes it better?

In my example, `parent` is a more abstract function.
In the call stack,
it's the first to be called,
and its implementation is a call to another function.
I think that having a more abstract function first allows you
to spend less time thinking about the code.
How so?

I think we need a more involved example
because the short version is too short
to reveal any problems.

Imagine that your working at a pizzeria software company
and your customers are reporting a problem
with your system
(work with me here).
**The complaint**: any order for pepperoni topping produces a pizza
with anchovies instead.

Your boss has asked you to fix the problem.
The entire company runs on a single Python module
and the moneymaker is your proprietary `make_pizza` function
(is this absurd enough yet?)

```python
# pizzeria.py

def make_pizza(order):
    pizza = toss_dough()
    pizza = add_toppings(pizza, order)
    bake(pizza)
    package(pizza)
    deliver(pizza, order)

# Thousands of lines of code below here,
# including toss_dough, add_toppings, bake, etc.
```

Each of those five helper functions has dozens
of their own helpers.
The process of calling `make_pizza` is positively labyrinthine.

Did I mention this is your first day
at the job
and you don't know this code yet?
It sounds silly,
but I can confidently say
that, as a professional software developer,
you encounter code all the time
that you've never seen before.
Software systems are generally big.

If you needed to solve this problem quickly,
where would you look to start?

By putting the most abstract function first,
you can immediately understand the high level flow through the system.
The function acts like a table of contents
of whatever else you're bound to find.

Knowing that you need to deal with toppings,
you can dig into `add_toppings`
as you're debugging through the problem
and continue to dig through the layers
which get progressively farther and farther into the file.

What if this problem was flipped around
and all the helper functions were first?
I think you'd likely take longer to orient yourself,
since you wouldn't have seen the main `make_pizza` function
until you reach the bottom
of the file.
Further,
you'd lack the context about the pieces
and be building up your mental model
from the entire tree of functions
from the bottom of the call stack.

Most importantly,
with most abstract at the bottom,
you're reading stuff
that you didn't need to read.
Your mission is to fix whatever is wrong
with toppings.
If the helpers were roughly in clusters associated
with the five main functions
in `make_pizza`,
then, at minimum,
you had to get through `toss_dough` helpers
before you got to `add_toppings`.
With the most abstract first ordering,
you can avoid this problem
and jump straight to the functions
that are most relevant to the task
(especially when using the jump to definition features available
to most IDEs or text editors).

> The most abstract function first ordering means
that you are better able to get into the abstractions
that are pertinent
and skip the other abstractions
and irrelevant implementation details.

## But...

I hope you noticed that this is an opinion piece.
While I think having the most abstract functions first is better,
there are times when it's not appropriate.

First,
your language may not support this ordering.

I've been working with Lua recently,
and function order matters in that language!

```lua
-- example.lua
local function parent()
    child()
end

local function child()
    print("hello world")
end

parent()
```
This version is broken!

```bash
$ lua example.lua
lua: example.lua:2: global 'child' is not callable (a nil value)
stack traceback:
	example.lua:2: in local 'parent'
	example.lua:9: in main chunk
	[C]: in ?
```

Second,
try to respect the conventions
of existing projects.

I'm trying to get Lua support included
with pre-commit
with
{{< extlink "https://github.com/pre-commit/pre-commit/pull/2158" "this PR" >}}.
In my initial implementation,
I goofed up and put the most abstract functions first
and failed to notice
that other modules did the opposite.
{{< extlink "https://x.com/codewithanthony" "Anthony" >}},
pre-commit's maintainer, pointed out the difference
in the review,
and I was happy to correct my mistake.
*Sometimes,
consistency is a better quality to maintain
than some personal design ideal.*

Those are my thoughts on this design subject.
I hope these ideas help you think through this topic too.
Disagree with me?
That's cool with me.
If I helped you solidify your ideas,
mission accomplished.

Thanks for reading!
Chat with me about this
{{< extlink "https://x.com/mblayman" "on X" >}}!
I'm curious what you think.
