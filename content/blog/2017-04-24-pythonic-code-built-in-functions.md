---
title: "Pythonic code: built-in functions"
description: >-
  In this series of posts,
  I'm going to examine common design patterns
  in Python
  that make Python code feel "Pythonic."
  This fourth post turns our attention
  to the built-in functions
  and the power of knowing what is immediately
  at your fingertips.
image: img/python.png
type: post

---

This post continues a series
on "Pythonic" code.
Pythonic code is code
that fits well
with the design
of the Python language.
The last post examined the
[property decorator](/2017/pythonic-code-the-property-decorator.html)
as a technique to make beautiful classes.
This fourth post will dive into Python's built-in functions.

1. [The list comprehension](/2017/pythonic-code-the-list-comprehension.html)
2. [The with statement](/2017/pythonic-code-the-with-statement.html)
3. [The property decorator](/2017/pythonic-code-the-property-decorator.html)
4. Built-in functions
5. [Using the standard library](/2017/pythonic-code-using-standard-library.html)
6. [Leveraging packages](/2017/pythonic-code-leveraging-packages.html)

## Built-in functions

A couple of years ago,
I made a challenge for myself
to read through all of Python's standard library.
Today,
I would generally suggest that people **don't** do that
(for reasons I documented
in a [blog post about the readthrough experience](/2016/readthrough-python-standard-library.html)).

Even with that caution,
there **is** some documentation
that you *absolutely* should read:
[the built-in functions reference](https://docs.python.org/3/library/functions.html).

The built-in functions are the set
of functions that do not need to be imported.
They are globally available
in any Python source file.
As of this writing
(with Python 3.6.1 documentation),
the set includes 68 functions.
Some of these functions are extremely common
and well known to proficient Python programmers
like `len` and `open`.
If you want to move
from proficient to expert,
using a majority
of these functions
will make your Python code far more Pythonic.

I'm going to describe a few of my favorites
to give you an idea
of what is available.
Once you look at these examples,
I'd really encourage you to read
the built-in function reference
so you can discover your own favorites!

Let's look at these:

* `any`
* `enumerate`
* `print`
* `range`
* `sorted`

## `any`

The `any` function takes a list
and returns `True`
if anything in the list evaluates to `True`.
This is a useful function
for reducing a bunch
of boolean checks
into a single value.
I think I've used `any` most often in cases
where I'm checking permissions
or other business rules.

```python
>>> checks = [False, False, True, False]
>>> status = any(checks)
>>> status
True
```

## `enumerate`

If you ever have a loop
and you also need an incrementing counter
for the body of your loop,
then `enumerate` is your friend.
The function can return pairs
that contain an index
and the value
in the list.
You can also set a `start` keyword argument
to modify the starting value of your index.

```python
>>> fruits = ['apple', 'orange', 'kiwi', 'pear']
>>> for index, fruit in enumerate(fruits, start=1):
...     print(index, fruit)
...
(1, 'apple')
(2, 'orange')
(3, 'kiwi')
(4, 'pear')
```

## `print`

The humble `print` statement became a `print` function
in Python 3.
There are plenty
of grumpy Python 2 developers
whose muscle memory
prevent them from typing the function correctly
(I'm often one of them),
but the `print` function is pretty great.
By making `print` a function instead of a keyword,
developers gets all the great benefits
that come from using Python functions.
For example,
the `print` function adds a lot of clarity
for writing to a different file stream
by using the `file` keyword argument
rather than the odd `print >> sys.stderr 'help me'` style.

```python
>>> print('Hello World')
Hello World
>>> import sys
>>> print('An error', file=sys.stderr)
An error
```

## `range`

`range` is great for producing lists of values.
I don't have much to say about it.
This one is fairly self-explanatory. :)

```python
>>> range(10)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> range(5, 10)
[5, 6, 7, 8, 9]
>>> range(0, 10, 2)
[0, 2, 4, 6, 8]
```

## `sorted`

Lists in Python have an included `sort` method.
The downside of this method is that this list will be sorted
in place.
If you don't like that behavior,
you can get a new list
by passing your original list
through the `sorted` function.
This function also has the ability
to take a `key` function
that will decide how things are sorted.
Have a list of colors that you wanted sorted
into a rainbow?
That's entirely possible
if you're `key` function knows how to sort colors
that way.

```python
>>> numbers = [5, 2, 3, 1, 4]
>>> ordered = sorted(numbers)
>>> ordered
[1, 2, 3, 4, 5]
>>> numbers
[5, 2, 3, 1, 4]
>>> numbers.sort()
>>> numbers
[1, 2, 3, 4, 5]
```

## So much more!

Covering five example functions doesn't even reach 10%
of what Python has built in to the core.
I believe your code will be way better
if you can learn some of these functions
and how to apply them regularly
as you make new things.

Be sure to
[check out the docs](https://docs.python.org/3/library/functions.html)
to boost your skill set,
and check back in next time
when I illuminate
how cool the standard library is.
