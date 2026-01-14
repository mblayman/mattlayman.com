---
slug: pythonic-code-the-property-decorator
title: "Pythonic code: the property decorator"
date: 2017-04-11
description: >-
  In this series of posts,
  I'm going to examine common design patterns
  in Python
  that make Python code feel "Pythonic."
  The third post in the series focuses
  on the property decorator
  as a way to clean up your classes.
image: img/python.png
aliases:
 - /2017/pythonic-code-the-property-decorator.html
 - /pythonic-code/the-property-decorator
categories:
 - Python
tags:
 - Design

---

This post continues a series
on "Pythonic" code.
Pythonic code is code
that fits well
with the design
of the Python language.
My previous post looked at the
[with statement](/blog/pythonic-code-the-with-statement)
and simplifying setup and tear down code.
This third post will examine the `property` decorator.

1. [The list comprehension](/blog/pythonic-code-the-list-comprehension)
2. [The with statement](/blog/pythonic-code-the-with-statement)
3. The property decorator
4. [Built-in functions](/blog/pythonic-code-built-in-functions)
5. [Using the standard library](/blog/pythonic-code-using-standard-library)
6. [Leveraging packages](/blog/pythonic-code-leveraging-packages)

## The `property` decorator

If you've ever taken a class
on object oriented (OO) design,
then you've likely been taught the value
of encapsulation.
You were told that you should keep the state
of your objects private
so that you're free to modify the class internals
as you see fit.
This is a noble goal
and it benefits you immensely.

If the course was in Java,
encapsulation quickly translated itself
to getters and setters
on your classes.
When coming to Python,
maybe your first class looks like this:

```python
class OhMyJava:

    def __init__(self):
        self._foo = ''

    def get_foo(self):
        return self._foo

    def set_foo(self, foo):
        self._foo = foo
```

If I were to review your code,
I might propose an alternative.

```python
class AwwYeah:

    def __init__(self):
        self.foo = ''
```

WHAT!?
But,
how dare I violate encapsulation?
What happens when needs change,
and `foo` needs to be created dynamically from `bar`.
Doesn't that break anyone who used the code?

The Python language designers determined
that getting and setting attributes directly
feels far cleaner
than getter and setter methods.
Contrast these:

```python
obj.set_result(other.get_foo() + other.get_bar())
# vs.
obj.result = other.foo + other.bar
```

I hope you'll agree with the language designers
that the latter is easier to comprehend.
To make that style possible,
the language needed some way to achieve
what they wanted
without violating encapsulation.

Enter the `property` decorator.

The genius move was to add a new language feature
that makes it possible to extend your class
without violating the API
that you've defined.
In our example,
`foo` is the public API.
Let's extend our code.

```python
class AwwYeah:

    def __init__(self):
        self._bar = ''

    @property
    def foo(self):
        return 'More awesome please: {}'.format(self._bar)

    @foo.setter
    def foo(self, value):
        self._bar = '{} is great.'.format(value)

>>> a = AwwYeah()
>>> a.foo = 'Python'
>>> a.foo
'More awesome please: Python is great.'
```

The `property` decorator is our secret weapon
to prevent encapulation blunders.
This new class changes what `foo` means
without breaking any users of the class.

Using `property` as a decorator
creates a getter method.
It's the difference between `a.foo()` and `a.foo`.
That seems minor,
but those parenthesis add up.
The `property` decorator enables a method
to masquerade as a plain object attribute.

Additionally,
you can create a setter method (i.e. `@foo.setter`)
as long as the name before `.setter` matches the method name
of the decorated property.
When you don't include a setter method,
the property is read only
and will raise an `AttributeError`
if you attempt to set it.

Creating getter and setter methods
by adding a decorator
is a powerful tool
that leads to exceptionally clean code.
The `property` decorator unlocks something awesome for us:

*You can do the simplest thing possible
until you need more control*.

This characteristic allows developers
to write code quickly and succinctly.
If you want to know more about `property`,
check out the
[documentation](https://docs.python.org/3/library/functions.html#property).
So, go forth and stop writing Java-style getter and setter methods
in your Python code! :)
