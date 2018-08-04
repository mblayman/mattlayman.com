---
title: "Pythonic code: the with statement"
date: 2017-04-04T12:00:00Z
description: >-
  In this series of posts,
  I'm going to examine common design patterns
  in Python
  that make Python code feel "Pythonic."
  This second post covers Python's with statement,
  a syntax to elegantly handle code
  that requires set up and tear down.
image: img/python.png
type: post

---

This post continues a series
on "Pythonic" code.
Pythonic code is code
that fits well
with the design
of the Python language.
Previously,
I wrote about
[list comprehensions](/2017/pythonic-code-the-list-comprehension.html)
as a powerful way to manipulate Python's list data structure.
This post will cover the `with` statement.

1. [The list comprehension](/2017/pythonic-code-the-list-comprehension.html)
2. The with statement
3. [The property decorator](/2017/pythonic-code-the-property-decorator.html)
4. [Built-in functions](/2017/pythonic-code-built-in-functions.html)
5. [Using the standard library](/2017/pythonic-code-using-standard-library.html)
6. [Leveraging packages](/2017/pythonic-code-leveraging-packages.html)

## The `with` statement

One task that you are likely to encounter
while programming Python
is the need to open a file.
That file might contain tables of data
or pictures of kittens.
Whatever you find yourself doing,
you'll come across the `open` function.
Let's work through a thought experiment
which can help explain why you should use `with`.

If you're brand new to Python,
you might open a file like so:

```python
f = open('kitteh.jpg', 'rb')
cat_pic = f.read()
# Do other stuff with the cat picture.
```

After speaking with a friend
with more Python experience than you,
you learn that you're supposed to close files
or else the operating system will eventually run into trouble
(because it can only track a limited number of open files).
You rewrite your code:

```python
f = open('kitteh.jpg', 'rb')
cat_pic = f.read()
# Do other stuff with the cat picture.
f.close()
```

Then you learn that errors can happen.
Being a good developer,
you attempt to handle any errors.

```python
try:
    f = open('kitteh.jpg', 'rb')
    cat_pic = f.read()
    # Do other stuff with the cat picture.
    f.close()
except:
    print('oops, something went wrong.')
```

Your friend tells you that you've added a bug.
What?
How could that be?
She tells you
that an error can happen
before the file is closed.
You go read more Python documentation
and learn about `finally`.
The code is reworked again to look like:

```python
try:
    f = open('kitteh.jpg', 'rb')
    cat_pic = f.read()
    # Do other stuff with the cat picture.
except:
    print('oops, something went wrong.')
finally:
    f.close()
```

This code is not stellar.
If you had to write 200 lines
of extra code
for "doing other stuff,"
then there is a lot of distance
between opening and closing the file.
Viewed another way,
there is a lot space
between setting something up
and tearing it down later.

This is a perfect place to use `with`.
Let's restate the code with the `with` statement.

```python
with open('kitteh.jpg', 'rb') as f:
    cat_pic = f.read()
try:
    # Do other stuff with the cat picture.
except:
    print('oops, something went wrong.')
```

At first,
you might be suspect
of this code.
Where did the `close` call go?
The `with` statement used an extra concept
called a
[context manager](https://docs.python.org/3/reference/datamodel.html#context-managers).
Context managers are designed
to handle setup and tear down
for anything that needs it.
A context manager is some code
that implements an `__enter__` and `__exit__` method.

When `open` is used with a `with` statement,
a special context manager is called.
After the scope of the `with` block passes
(i.e., reading the file content into `cat_pic`),
the interpreter will execute an `__exit__`
method on the context manager.
The `open` context manager will close the file
in `__exit__`.
All of this work is neatly tucked away
from the developer.
You have the guarantee
that the file gets closed
and do not have to do that work
on your own.

The `open` context manager is probably the most common usage
of the `with` statement.
Other uses of `with` can include threading locks,
timers,
or even nicer interfaces for unit testing exceptions.
Finally,
Python let's you create your own context managers.
Check out [contextlib](https://docs.python.org/3/library/contextlib.html)
for more info.
I've included this example to give you a quick idea in action.

```python
>>> from contextlib import contextmanager
>>> @contextmanager
... def praise():
...     print('You can do it.')
...     yield
...     print('You made it.')
...
>>> with praise():
...     print('I am trying to code.')
...
You can do it.
I am trying to code.
You made it.
```

The `with` statement is another valuable tool
for your Python programmer toolbelt.
The key thing to remember is that it can help you clean up any code
where you need to set things up
or tear things down.
