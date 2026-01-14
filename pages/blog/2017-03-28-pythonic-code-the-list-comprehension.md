---
slug: pythonic-code-the-list-comprehension
title: "Pythonic code: the list comprehension"
date: 2017-03-28
description: >-
  In this series of posts,
  I'm going to examine common design patterns
  in Python
  that make Python code feel "Pythonic."
  This first post will cover list comprehensions,
  a powerful way to build a Python list data structure.
image: img/python.png
aliases:
 - /2017/pythonic-code-the-list-comprehension.html
 - /pythonic-code/the-list-comprehension
categories:
 - Python
tags:
 - Design

---

At the next
[Python Frederick](https://www.meetup.com/python-frederick/) meetup,
I'm going to speak
about "Pythonic" code.
Pythonic code is code
that fits well
with the design
of the Python language.
Some people might call this *idiomatic* Python.
These design patterns give Python some
of its elegant feeling.
Since I'm going to do an entire talk
on Pythonic code,
I've decided to put together a series
of posts
that will explore some of the patterns
in greater depth.

To start,
let's talk about *list comprehensions*.

1. The list comprehension
2. [The with statement](/blog/pythonic-code-the-with-statement)
3. [The property decorator](/blog/pythonic-code-the-property-decorator)
4. [Built-in functions](/blog/pythonic-code-built-in-functions)
5. [Using the standard library](/blog/pythonic-code-using-standard-library)
6. [Leveraging packages](/blog/pythonic-code-leveraging-packages)

## List comprehensions

A list is one of Python's core data structures.
Along with its buddies,
dictionaries and tuples,
you can get a ton of amazing stuff done
with the language.

```python
# A list example
some_numbers = [1, 2, 3, 4, 5]
```

You can learn a lot about lists
by reading the
[Python tutorial on data structures](https://docs.python.org/3/tutorial/datastructures.html),
but this post will cover one of the list's more iconic features,
list comprehensions.

If you are working
with a list of data,
you may eventually want to modify it.
Let's work with some numbers.
What would you do if you want to double your values?

Here's a first attempt:

```python
numbers = [1, 2, 3, 4, 5]
doubled = []
for number in numbers:
    doubled.append(2 * number)
```

This works,
but it manages to feel a bit clunky.
A list comprehension is a way
to build a new list
with a more compact syntax.

Let's make our doubled list with a list comprehension.

```python
numbers = [1, 2, 3, 4, 5]
doubled = [2 * number for number in numbers]
```

With a list comprehension,
the `for` loop has moved *inside* the list's constructor syntax
(i.e., `[]`).
We saved two lines of code
and avoided the explicit use of `append`.
I think we can confidently say that the code is cleaner.

If that's all that list comprehensions could do,
it would a nice little syntax addition,
but might feel like a parlor trick.
Thankfully,
list comprehensions can do more.
They can also *filter*
if they are provided
with a predicate.
For instance,
maybe you want odd numbers
instead of doubled values.
For that, you'd write:

```python
numbers = range(10)
odds = [number for number in numbers if number % 2 != 0]
```

This example uses `range` to create a list of numbers
from `0` to `9`.
The list comprehension builds the `odds` list
and only includes `number`
when it is odd
(`number % 2 != 0` checks that a number is odd).

One more feature
of list comprehensions
that is probably less used
is the ability
to use multiple `for` loops.

Imagine that you need a list of coordinate pairs
in an x/y plane.
Instead of writing nested `for` loops, like so:

```python
xs = range(10)
ys = range(10)
pairs = []
for x in xs:
    for y in ys:
        pairs.append((x, y))
```

You can write the more concise version.

```python
xs = range(10)
ys = range(10)
pairs = [(x, y) for x in xs
                for y in ys]
```

We've covered a few key attributes list comprehensions.

1. They're a concise way to build new lists.
2. They enable elegant filtering.
3. They permit nested looping in a clear style.

List comprehensions are a fantastic way to clean up your loops.
Once you start using them,
you'll be on your way to writing more Pythonic code.
