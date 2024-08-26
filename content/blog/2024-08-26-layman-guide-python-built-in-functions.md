---
title: "Layman's Guide to Python Built-in Functions"
description: >-
  This is a plain language guide to every built-in function in Python,
  paired with a simple example that shows each function in action.
image: img/python.png
type: post
categories:
 - Python
tags:
 - Python
 - built-in
 - functions

---

### Quick Jump List

**A:**
[`abs`](#abs),
[`aiter`](#aiter),
[`all`](#all),
[`anext`](#anext),
[`any`](#any),
[`ascii`](#ascii),
**B:**
[`bin`](#bin),
[`bool`](#bool),
[`breakpoint`](#breakpoint),
[`bytearray`](#bytearray),
[`bytes`](#bytes),
**C:**
[`callable`](#callable),
[`chr`](#chr),
[`classmethod`](#classmethod),
[`compile`](#compile),
[`complex`](#complex),
**D:**
[`delattr`](#delattr),
[`dict`](#dict),
[`dir`](#dir),
[`divmod`](#divmod)
**E:**
[`enumerate`](#enumerate),
[`eval`](#eval),
[`exec`](#exec),
**F:**
[`filter`](#filter),
[`float`](#float),
[`format`](#format),
[`frozenset`](#frozenset),
**G:**
[`getattr`](#getattr),
[`globals`](#globals),
**H:**
[`hasattr`](#hasattr),
[`hash`](#hash),
[`help`](#help),
[`hex`](#hex),
**I:**
[`id`](#id),
[`input`](#input),
[`int`](#int),
[`isinstance`](#isinstance),
[`issubclass`](#issubclass),
[`iter`](#iter),
**L:**
[`len`](#len),
[`list`](#list),
[`locals`](#locals),
**M:**
[`map`](#map),
[`max`](#max),
[`memoryview`](#memoryview),
[`min`](#min),
**N:**
[`next`](#next),
**O:**
[`object`](#object),
[`oct`](#oct),
[`open`](#open),
[`ord`](#ord),
**P:**
[`pow`](#pow),
[`print`](#print),
[`property`](#property),
**R:**
[`range`](#range),
[`repr`](#repr),
[`reversed`](#reversed),
[`round`](#round),
**S:**
[`set`](#set),
[`setattr`](#setattr),
[`slice`](#slice),
[`sorted`](#sorted),
[`staticmethod`](#staticmethod),
[`str`](#str),
[`sum`](#sum),
[`super`](#super),
**T:**
[`tuple`](#tuple),
[`type`](#type),
**V:**
[`vars`](#vars),
**Z:**
[`zip`](#zip),
**_:**
[`__import__`](#__import__),

## Motivation

> The Python docs are **ill-suited to novices**.

The content of the [built-in functions documentation](https://docs.python.org/3/library/functions.html)
favors precision and correctness over comprehension
for beginners.
While this style is great for experienced developers
who already understand
the finer points
of Python's design,
the docs are confusing to novice programmers
like a 12 year old
who is not far on his journey
of learning Python.

**This guide is an opinionated and simplified description
of Python's built-in functions.**

My goal is to provide definitions,
in plain English,
of each built-in function
that comes with Python.
Along with each definition is an example that is as simple
as I can think of.
I ran each example against the latest version of Python
as of the time writing this guide.

I want to be able to share this
with my 12 year old son
or my 10 year old daughter,
so that they can understand and use Python.
*My hope is that this guide also serves others
who would like some plain definitions
of what the built-in functions do.*

**A note for pedants**:
I am sacrificing precision and exactness
in favor of comprehension.
That means I will use substitionary language
that I think will communicate more clearly
than the exact terminology.
If you're looking for that level of precision,
please refer to the standard library docs.
Those docs are great for that level of clarity.

For the rest of us, let's go!

<a name="abs"></a>

## abs

`abs` returns the absolute value of a number, which means it 
removes any negative sign. The result is always a positive number or zero.

Example:

```python
>>> abs(-5)
5
>>> abs(3.2)
3.2
```

[Back](#quick-jump-list)

<a name="aiter"></a>

## aiter

`aiter` is the asynchronous version of `iter`.
This allows you to iterate over asynchronous data sources, such as 
streams, one item at a time in an asynchronous loop.

If this example looks intimidating, fear not!
Asynchronous programming is a more advanced Python concept.
You are unlikely to encounter this much in a lot of Python code.

Example:

```python
>>> import asyncio
>>> from collections.abc import AsyncIterable
>>> class AsyncRange(AsyncIterable):
...     def __init__(self, start, end):
...         self.start = start
...         self.end = end
...     async def __aiter__(self):
...         for i in range(self.start, self.end):
...             await asyncio.sleep(0.1)
...             yield i
...
>>> async def example():
...     async for i in aiter(AsyncRange(1, 4)):
...         print(i)
...
>>> asyncio.run(example())
1
2
3
```

[Back](#quick-jump-list)

<a name="all"></a>

## all

`all` returns `True` if all elements in something list-like (such as a 
list or tuple) are "truthy." If any element is false or if the list is 
empty, it returns `False`.

Example:

```python
>>> all([True, True, True])
True
>>> all([True, False, True])
False
>>> all([1, 2, 3])
True
```

[Back](#quick-jump-list)

<a name="anext"></a>

## anext

`anext` is the asynchronous version of `next`.
If the iterator is exhausted, it can raise a `StopAsyncIteration` 
exception unless a default value is provided.

If this example looks intimidating, fear not!
Asynchronous programming is a more advanced Python concept.
You are unlikely to encounter this much in a lot of Python code.

Example:

```python
>>> import asyncio
>>> from collections.abc import AsyncIterable
>>> class AsyncRange(AsyncIterable):
...     def __init__(self, start, end):
...         self.start = start
...         self.end = end
...     async def __aiter__(self):
...         for i in range(self.start, self.end):
...             await asyncio.sleep(0.1)
...             yield i
...
>>> async def example():
...     it = aiter(AsyncRange(1, 4))
...     print(await anext(it))
...     print(await anext(it))
...
>>> asyncio.run(example())
1
2
```

[Back](#quick-jump-list)

<a name="any"></a>

## any

`any` returns `True` if at least one element in something list-like 
(such as a list or tuple) is true. If all elements are false or if the 
list is empty, it returns `False`.

Example:

```python
>>> any([False, False, False])
False
>>> any([False, False, True])
True
>>> any([])
False
```

[Back](#quick-jump-list)

<a name="ascii"></a>

## ascii

`ascii` returns a string containing a printable representation 
of an object. It escapes non-ASCII characters in the string using Unicode 
escape sequences, so the result can be safely printed or used where only 
ASCII characters are allowed.

Example:

```python
>>> ascii('Hello, world!')
"'Hello, world!'"
>>> ascii('Héllo')
"'H\\xe9llo'"
```

[Back](#quick-jump-list)

<a name="bin"></a>

## bin

`bin` converts an integer number to a binary string prefixed 
with `0b`. The result is a string that represents the binary equivalent of 
the number.

Example:

```python
>>> bin(10)
'0b1010'
>>> bin(255)
'0b11111111'
```

[Back](#quick-jump-list)

<a name="bool"></a>

## bool

`bool` converts a value to a Boolean (`True` or `False`).
If the value is considered true (e.g., non-zero numbers, non-empty lists), 
it returns `True`. Otherwise, it returns `False`.

Example:

```python
>>> bool(0)
False
>>> bool(1)
True
>>> bool([])
False
>>> bool([1, 2, 3])
True
```

[Back](#quick-jump-list)

<a name="breakpoint"></a>

## breakpoint

`breakpoint` is used to pause the execution of a program and 
start an interactive debugger at that point. It is helpful for inspecting 
the state of a program during debugging.

Example:

```python
>>> def example():
...     x = 10
...     breakpoint()
...     print(x)
...
>>> example()
> <stdin>(4)example()
(Pdb) x
10
(Pdb) c
10
```

[Back](#quick-jump-list)

<a name="bytearray"></a>

## bytearray

`bytearray` creates a modifiable sequence of bytes. It can be set 
with a string, a sequence of integers, or an iterable of bytes, and allows 
modification of the byte values.

Example:

```python
>>> ba = bytearray('hello', 'utf-8')
>>> ba
bytearray(b'hello')
>>> ba[0] = 72
>>> ba
bytearray(b'Hello')
```

[Back](#quick-jump-list)

<a name="bytes"></a>

## bytes

`bytes` creates an unmodifiable sequence of bytes. It can be initialized 
with a string, a sequence of integers, or an iterable of bytes.
Unlike `bytearray`, the result cannot be modified after creation.

Example:

```python
>>> b = bytes('hello', 'utf-8')
>>> b
b'hello'
>>> b[0] = 72
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'bytes' object does not support item assignment
>>> b = bytes([65, 66, 67])
>>> b
b'ABC'
```

[Back](#quick-jump-list)

<a name="callable"></a>

## callable

`callable` checks if an object appears to be callable, meaning it can 
be called like a function. It returns `True` if the object can be called, and 
`False` otherwise.

Example:

```python
>>> callable(print)
True
>>> callable(42)
False
```

[Back](#quick-jump-list)

<a name="chr"></a>

## chr

`chr` converts an integer (representing a Unicode code point) to 
its corresponding character. It returns the character as a string.
It is the inverse of `ord`.

Example:

```python
>>> chr(65)
'A'
>>> chr(128513)
'😁'
```

[Back](#quick-jump-list)

<a name="classmethod"></a>

## classmethod

`classmethod` is used to define a method in a class that is connected
to the class.
This means that the method receives the class as its first argument
instead of an instance.

Example:

```python
>>> class Example:
...     @classmethod
...     def greet(cls):
...         return f"Hello from {cls.__name__}"
...
>>> Example.greet()
'Hello from Example'
```

[Back](#quick-jump-list)

<a name="compile"></a>

## compile

`compile` builds source code into a code object that can be executed 
by the `exec()` or `eval()` functions. It takes a string of code and returns a 
code object which can be run later.

Example:

```python
>>> code = compile('print("Hello, world!")', '<string>', 'eval')
>>> exec(code)
Hello, world!
```

[Back](#quick-jump-list)

<a name="complex"></a>

## complex

`complex` creates a complex number from a real and an optional imaginary 
part. The result is a number with both real and imaginary components.

In math, you would typically use `i` to represent the imaginary portion.
Because `i` is a common variable name, Python uses `j` instead.

Example:

```python
>>> complex(2, 3)
(2+3j)
>>> complex('1+2j')
(1+2j)
```

[Back](#quick-jump-list)

<a name="delattr"></a>

## delattr

`delattr` removes an attribute from an object. You need to provide 
the object and the name of the attribute as a string. If the attribute does not 
exist, it raises an `AttributeError`.

Example:

```python
>>> class Example:
...     def __init__(self):
...         self.an_attribute = 10
...
>>> example = Example()
>>> delattr(example, 'an_attribute')
>>> example.an_attribute
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Example' object has no attribute 'an_attribute'
```

[Back](#quick-jump-list)

<a name="dict"></a>

## dict

`dict` creates a dictionary, which is a collection of key-value pairs. 
You can initialize it with key-value pairs, or with other mappings or sequences.

More commonly, dictionaries will be constructed from the literal syntax
using `{` and `}`.

Example:

```python
>>> d = dict(a=1, b=2)
>>> d
{'a': 1, 'b': 2}
>>> d = dict([('a', 1), ('b', 2)])
>>> d
{'a': 1, 'b': 2}
>>> d = {'a': 1, 'b': 2}
>>> d
{'a': 1, 'b': 2}
```

[Back](#quick-jump-list)

<a name="dir"></a>

## dir

`dir` returns a list of valid attributes for an object. 
If no object is passed, it returns a list of names in the current local scope.

Example:

```python
>>> class MyClass:
...     def method(self):
...         pass
...
>>> dir(MyClass)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', 
 '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', 
 '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', 
 '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
 '__str__', '__subclasshook__', 'method']

>>> dir()
['__builtins__', '__cached__', '__doc__', '__import__', '__loader__', 
 '__name__', '__package__', '__spec__', '__stderr__', '__stdin__',
 '__stdout__']
```

[Back](#quick-jump-list)

<a name="divmod"></a>

## divmod

`divmod` takes two numbers and returns a tuple containing their quotient 
and remainder.

This is like division before you learned fractions in math class.
In my math memory, I would write something like "9 / 4 = 2r1".
The "2" and the remainder of "1" are what `divmod` returns.

Example:

```python
>>> divmod(9, 4)
(2, 1)
>>> divmod(15, 6)
(2, 3)
```

[Back](#quick-jump-list)

<a name="enumerate"></a>

## enumerate

`enumerate` gives a counting number along with values when looping on something list-like.
You can change where the counting number starts by using the `start` keyword argument.

Example:

```python
>>> for index, value in enumerate(['apple', 'banana']):
...     print(index, value)
...
0 apple
1 banana
>>> for index, value in enumerate(['cherry', 'date'], start=1):
...     print(index, value)
...
1 cherry
2 date
```

[Back](#quick-jump-list)

<a name="eval"></a>

## eval

`eval` evaluates a string containing Python code and returns the result. 
Be careful when using `eval` with untrusted data, as it can execute arbitrary code.

Example:

```python
>>> eval('2 + 3')
5
>>> x = 10
>>> eval('x * 2')
20
```

[Back](#quick-jump-list)

<a name="exec"></a>

## exec

`exec` executes a string containing Python code. Unlike `eval`, which only evaluates 
expressions (i.e., simple code that returns a value),
`exec` can execute complex code including statements, functions, and class definitions. 
Be careful when using `exec` with untrusted data, as it can execute arbitrary code.

Example:

```python
>>> code = '''
... def greet(name):
...     return f"Hello, {name}!"
... '''
>>> exec(code)
>>> greet('Alice')
'Hello, Alice!'
```

[Back](#quick-jump-list)

<a name="filter"></a>

## filter

`filter` takes something list-like and checks every value with a function
that returns either `True` or `False`.
Only the values that return `True` are included in the result.

When the function is `None`, the resulting list only includes items that are truthy.

Example:

```python
>>> def is_even(n):
...     return n % 2 == 0
...
>>> list(filter(is_even, [1, 2, 3, 4]))
[2, 4]
>>> list(filter(None, [0, 1, 2, '', 'hello']))
[1, 2, 'hello']
```

[Back](#quick-jump-list)

<a name="float"></a>

## float

`float` converts a number or a string to a floating-point number. It can handle 
integer values, floating-point literals, and strings representing numbers.

Example:

```python
>>> float(10)
10.0
>>> float('3.14')
3.14
>>> float('1e-4')
0.0001
```

[Back](#quick-jump-list)

<a name="format"></a>

## format

`format` outputs a value according to a specified format string. It allows you 
to control how numbers and strings are presented, such as setting decimal places or padding.

There are lots of options you can learn about to do string formatting.
All the messy details are in the {{< extlink "https://docs.python.org/3/library/string.html#formatspec" "Format Specification" >}}.

Example:

```python
>>> format(123.4567, '.2f')
'123.46'
>>> format(42, '04d')
'0042'
>>> format('hello', '^10')
'  hello   '
```

[Back](#quick-jump-list)

<a name="frozenset"></a>

## frozenset

`frozenset` creates an unmodifiable version of a set.
It can be set with anything list-like, and supports set operations 
like unions and intersections, but without the ability to add or remove elements.

Example:

```python
>>> fs = frozenset([1, 2, 3, 4])
>>> fs
frozenset({1, 2, 3, 4})
>>> fs2 = frozenset([3, 4, 5, 6])
>>> fs | fs2  # Union
frozenset({1, 2, 3, 4, 5, 6})
>>> fs & fs2  # Intersection
frozenset({3, 4})
```

[Back](#quick-jump-list)

<a name="getattr"></a>

## getattr

`getattr` retrieves the value of an attribute from an object. If the attribute does 
not exist, it can return a default value if provided; otherwise, it raises an `AttributeError`.

Example:

```python
>>> class Example:
...     def __init__(self):
...         self.an_attribute = 10
...
>>> example = Example()
>>> getattr(example, 'an_attribute')
10
>>> getattr(example, 'another_attribute', 42)
42
```

[Back](#quick-jump-list)

<a name="globals"></a>

## globals

`globals` returns a dictionary representing the current global symbol table. 
This dictionary contains all the global variables and their values in the current scope.

Example:

```python
>>> x = 10
>>> globals()
{'__name__': '__main__', '__doc__': None,
 '__import__': <built-in function __import__>, 'x': 10, ...}
>>> globals()['x']
10
```

[Back](#quick-jump-list)

<a name="hasattr"></a>

## hasattr

`hasattr` checks if an object has a specified attribute. It returns `True` 
if the attribute exists and `False` otherwise.

Example:

```python
>>> class Example:
...     def __init__(self):
...         self.an_attribute = 10
...
>>> example = Example()
>>> hasattr(example, 'an_attribute')
True
>>> hasattr(example, 'another_attribute')
False
```

[Back](#quick-jump-list)

<a name="hash"></a>

## hash

`hash` returns the hash value of an object, which is an integer used for 
hash-based operations like dictionary key lookups. The object must be immutable
(i.e., unchanging), such as strings, numbers, or tuples containing only immutable elements.

Example:

```python
>>> hash('hello')
-9108665849909559950
>>> hash((1, 2, 3))
529344067295497451
```

[Back](#quick-jump-list)

<a name="help"></a>

## help

`help` provides a helpful summary of information about an object, 
such as a module, function, class, or method.
It displays documentation and usage information.

Example:

```python
>>> help(abs)
Help on built-in function abs in module builtins:

abs(x, /)
    Return the absolute value of the argument.
```

[Back](#quick-jump-list)

<a name="hex"></a>

## hex

`hex` converts an integer to a hexadecimal string, prefixed with `0x`. 
The result represents the number in base-16 notation.

Example:

```python
>>> hex(255)
'0xff'
>>> hex(1234)
'0x4d2'
```

[Back](#quick-jump-list)

<a name="id"></a>

## id

`id` returns a unique identifier for an object. This identifier is a constant integer 
that is guaranteed to be unique and constant for the object during its lifetime.

Example:

```python
>>> x = 'hello'
>>> id(x)
4512339488
>>> y = [1, 2, 3]
>>> id(y)
4513728448
```

[Back](#quick-jump-list)

<a name="input"></a>

## input

`input` reads a line of text from the user and returns it as a string. 
You can provide a prompt string that is displayed to the user before they enter their input.

Example:

```python
>>> name = input('Enter your name: ')
Enter your name: Bob
>>> name
'Bob'
```

[Back](#quick-jump-list)

<a name="int"></a>

## int

`int` converts a number or a string to an integer. It can handle decimal 
numbers and strings representing integers, as well as numbers in other bases if specified.

Example:

```python
>>> int('42')
42
>>> int(3.14)
3
>>> int('101', base=2)  # Convert binary string to integer
5
```

[Back](#quick-jump-list)

<a name="isinstance"></a>

## isinstance

`isinstance` checks if an object is an instance or subclass of a specified class 
or tuple of classes. It returns `True` if the object matches the class, and `False` otherwise.

Example:

```python
>>> isinstance(10, int)
True
>>> isinstance('hello', int)
False
>>> isinstance('hello', str)
True
>>> isinstance(10, (float, int))
True
>>> isinstance([], list)
True
```

[Back](#quick-jump-list)

<a name="issubclass"></a>

## issubclass

`issubclass` checks if a class is a subclass of another class or a tuple of classes. 
It returns `True` if the class is a subclass, and `False` otherwise.

Example:

```python
>>> class A:
...     pass
...
>>> class B(A):
...     pass
...
>>> issubclass(B, A)
True
>>> issubclass(A, B)
False
>>> issubclass(B, (A, object))
True
```

[Back](#quick-jump-list)

<a name="iter"></a>

## iter

`iter` returns an iterator object for something list-like.
Iterators allow you to traverse through items one at a time.

Example:

```python
>>> it = iter([1, 2])
>>> next(it)
1
>>> next(it)
2
>>> next(it)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

[Back](#quick-jump-list)

<a name="len"></a>

## len

`len` (for "length") returns the number of items in something list-like, such as a list, tuple, 
or string. It provides the count of elements or characters contained in the object.

Example:

```python
>>> len([1, 2, 3])
3
>>> len((1, 2, 3, 4))
4
>>> len('hello')
5
```

[Back](#quick-jump-list)

<a name="list"></a>

## list

`list` creates a new list object from an iterable or sequence. If no argument is 
provided, it returns an empty list. It is commonly used to convert other data types into lists.

More commonly, lists are constructed from the literal syntax
using `[` and `]`.

Example:

```python
>>> list('abc')
['a', 'b', 'c']
>>> list((1, 2, 3))
[1, 2, 3]
>>> list(range(3))
[0, 1, 2]
>>> [1, 2]
[1, 2]
```

[Back](#quick-jump-list)

<a name="locals"></a>

## locals

`locals` returns a dictionary representing the current local symbol table. 
This dictionary includes all local variables and their values in the current scope. 

Example:

```python
>>> def example():
...     x = 10
...     y = 20
...     return locals()
...
>>> example()
{'x': 10, 'y': 20}
```

[Back](#quick-jump-list)

<a name="map"></a>

## map

`map` applies a specified function to each item in something list-like
and returns the results. It is useful for processing or transforming 
elements in a collection.

Example:

```python
>>> def square(x):
...     return x * x
...
>>> list(map(square, [1, 2, 3, 4]))
[1, 4, 9, 16]
>>> list(map(str, [1, 2, 3]))
['1', '2', '3']
```

[Back](#quick-jump-list)

<a name="max"></a>

## max

`max` returns the largest item from something list-like or among two or more arguments. 
It can also take a key function to determine the maximum value based on custom criteria.

Example:

```python
>>> max([1, 2, 3, 4])
4
>>> max(10, 20, 30)
30
>>> max(['apple', 'banana', 'pear'], key=len)
'banana'
```

[Back](#quick-jump-list)

<a name="memoryview"></a>

## memoryview

`memoryview` creates a memory view object from a bytes-like object.
This view allows you to access the data without copying it.
It is useful for handling large data buffers more efficiently.

Example:

```python
>>> mv = memoryview(b'hello')
>>> mv[0]
104
>>> mv[1:4].tobytes()
b'ell'
```

[Back](#quick-jump-list)

<a name="min"></a>

## min

`min` returns the smallest item from something list-like or among two or more arguments. 
It can also take a key function to determine the minimum value based on custom criteria.

Example:

```python
>>> min([1, 2, 3, 4])
1
>>> min(10, 20, 30)
10
>>> min(['apple', 'banana', 'pear'], key=len)
'pear'
```

[Back](#quick-jump-list)

<a name="next"></a>

## next

`next` retrieves the next item from an iterator. You can also provide a default value 
to return if the iterator is exhausted; otherwise, it raises a `StopIteration` exception.

Example:

```python
>>> it = iter([1, 2])
>>> next(it)
1
>>> next(it)
2
>>> next(it, 'No more items')
'No more items'
>>> next(it)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

[Back](#quick-jump-list)

<a name="object"></a>

## object

`object` returns a new featureless object.
This is the base for all objects in Python.

Example:

```python
>>> obj = object()
>>> obj
<object object at 0x10bb88a60>
>>> isinstance(obj, object)
True
```

[Back](#quick-jump-list)

<a name="oct"></a>

## oct

`oct` converts an integer to its octal string representation, prefixed with `0o`. 
This string represents the number in base-8 notation.

Example:

```python
>>> oct(8)
'0o10'
>>> oct(64)
'0o100'
```

[Back](#quick-jump-list)

<a name="open"></a>

## open

`open` opens a file and returns a file object. You can specify the mode in which 
the file is opened (e.g., read, write).

Example:

```python
>>> with open('example.txt', 'w') as f:
...     f.write('Hello World')
...
11
>>> with open('example.txt') as f:
...     content = f.read()
...
>>> content
'Hello World'
```

[Back](#quick-jump-list)

<a name="ord"></a>

## ord

`ord` function returns the Unicode code point of a single character string.
This integer represents the character in Unicode.
It is the inverse of `chr`.

Example:

```python
>>> ord('A')
65
>>> ord('😁')
128513
```

[Back](#quick-jump-list)

<a name="pow"></a>

## pow

`pow` calculates the power of a number.
This function behaves like the `**` operator (e.g., `2**3`).

Example:

```python
>>> pow(2, 3)
8
```

[Back](#quick-jump-list)

<a name="print"></a>

## print

`print` outputs text or other data to the console. You can provide multiple arguments, 
and it will convert them to strings and display them, separated by spaces. You can also specify end 
characters and separators.

Example:

```python
>>> print('Hello, world!')
Hello, world!
>>> print('The answer is', 42)
The answer is 42
>>> print('Hello', end='!\n')
Hello!
```

[Back](#quick-jump-list)

<a name="property"></a>

## property

`property` creates a property attribute in a class. This allows you to define methods 
that can be accessed like attributes. You can use it to control access to attributes and define custom 
getter, setter, and deleter methods.

Example:

```python
>>> class Example:
...     def __init__(self, value):
...             self._value = value
...     @property
...     def value(self):
...             return self._value
...     @value.setter
...     def value(self, new_value):
...             self._value = new_value
...
>>> example = Example(10)
>>> example.value
10
>>> example.value = 20
>>> example.value
20
```

[Back](#quick-jump-list)

<a name="range"></a>

## range

`range` generates counting numbers, starting from a specified start value up to,
but not including, an end value. It can also accept a step value to define the increment between numbers. 

Example:

```python
>>> list(range(5))
[0, 1, 2, 3, 4]
>>> list(range(2, 8))
[2, 3, 4, 5, 6, 7]
>>> list(range(1, 10, 2))
[1, 3, 5, 7, 9]
```

[Back](#quick-jump-list)

<a name="repr"></a>

## repr

`repr` returns a string that represents an object in a way that could be used to recreate 
the object, if possible. It is intended for debugging and development, and often includes more details 
than the string representation provided by `str`.

Example:

```python
>>> repr('hello')
"'hello'"
>>> repr([1, 2, 3])
'[1, 2, 3]'
>>> repr({'key': 'value'})
"{'key': 'value'}"
```

[Back](#quick-jump-list)

<a name="reversed"></a>

## reversed

`reversed` returns something list-like in the reverse order.
It does not modify the original.

Example:

```python
>>> list(reversed([1, 2, 3, 4]))
[4, 3, 2, 1]
>>> list(reversed('hello'))
['o', 'l', 'l', 'e', 'h']
```

[Back](#quick-jump-list)

<a name="round"></a>

## round

`round` takes a number and rounds to a specified number of decimal places.
If no number of decimal places is specified, it rounds to the nearest whole number.

Example:

```python
>>> round(3.14159, 2)
3.14
>>> round(2.71828)
3
>>> round(1.5)
2
```

[Back](#quick-jump-list)

<a name="set"></a>

## set

`set` creates a new set from something list-like.
Sets are collections of unique elements and support operations like unions, intersections, and differences.

Sets are commonly constructed from the literal syntax
using `{` and `}`.

Example:

```python
>>> set([1, 2, 3, 2, 1])
{1, 2, 3}
>>> set('hello')
{'h', 'e', 'l', 'o'}
>>> set()
set()
>>> type({1, 2, 3, 4})
<class 'set'>
```

[Back](#quick-jump-list)

<a name="setattr"></a>

## setattr

`setattr` sets the value of an attribute on an object.
If the attribute does not already exist, it is created.
You provide the object, the name of the attribute, and the value to set.

Example:

```python
>>> class Example:
...     def __init__(self):
...         self.an_attribute = 10
...
>>> example = Example()
>>> example.an_attribute
10
>>> setattr(example, 'an_attribute', 20)
>>> example.an_attribute
20
>>> setattr(example, 'another_attribute', 30)
>>> example.another_attribute
30
```

[Back](#quick-jump-list)

<a name="slice"></a>

## slice

`slice` creates a slice object that specifies how to extract part of something list-like.
It takes up to three arguments: start, stop, and step.

More commonly, slices use the literal syntax of `:` for conciseness (e.g., `items[1:4]`).

Example:

```python
>>> s = slice(1, 4)
>>> items = [10, 20, 30, 40, 50]
>>> items[s]
[20, 30, 40]
>>> s = slice(0, 4, 2)
>>> items[s]
[10, 30]
>>> items[1:4]
[20, 30, 40]
```

[Back](#quick-jump-list)

<a name="sorted"></a>

## sorted

`sorted` returns a new list containing all items from something list-like,
sorted in ascending order.
You can also provide a custom sorting function
and specify whether to sort in ascending or descending order.

Example:

```python
>>> sorted([3, 1, 4, 1, 5, 9])
[1, 1, 3, 4, 5, 9]
>>> sorted(['apple', 'banana', 'pear'], key=len)
['pear', 'apple', 'banana']
>>> sorted([3, 1, 4, 1, 5, 9], reverse=True)
[9, 5, 4, 3, 1, 1]
```

[Back](#quick-jump-list)

<a name="staticmethod"></a>

## staticmethod

`staticmethod` defines a method within a class
that does not depend on class or instance-specific data.

Example:

```python
>>> class Example:
...     @staticmethod
...     def greet(name):
...         return f'Hello, {name}!'
...
>>> Example.greet('Mark')
'Hello, Mark!'
```

[Back](#quick-jump-list)

<a name="str"></a>

## str

`str` converts an object to its string representation. This is useful for displaying 
or working with textual data. You can use it to convert numbers, lists, or other objects into strings.

Example:

```python
>>> str(123)
'123'
>>> str(3.14)
'3.14'
>>> str([1, 2, 3])
'[1, 2, 3]'
```

[Back](#quick-jump-list)

<a name="sum"></a>

## sum

`sum` adds up all the items in something list-like containing numbers.

Example:

```python
>>> sum([1, 2, 3, 4])
10
>>> sum((10, 20, 30))
60
>>> sum(range(5))
10
```

[Back](#quick-jump-list)

<a name="super"></a>

## super

`super` returns a proxy object that represents the parent classes of the current class. 
It is used to call methods from a parent class, allowing you to extend or modify inherited methods.

Example:

```python
>>> class A:
...     def greet(self):
...         return 'Hello from A'
...
>>> class B(A):
...     def greet(self):
...         return super().greet() + ' and B'
...
>>> b = B()
>>> b.greet()
'Hello from A and B'
```

[Back](#quick-jump-list)

<a name="tuple"></a>

## tuple

`tuple` creates a new tuple object from something list-like.
Tuples are immutable, meaning their contents cannot be changed after creation.
If no argument is provided, it returns an empty tuple.

Example:

```python
>>> tuple([1, 2, 3])
(1, 2, 3)
>>> tuple('abc')
('a', 'b', 'c')
>>> tuple()
()
```

[Back](#quick-jump-list)

<a name="type"></a>

## type

`type` function returns the type of an object, which is a class that the object belongs to. 

Example:

```python
>>> type(123)
<class 'int'>
>>> type('hello')
<class 'str'>
>>> type([1, 2, 3])
<class 'list'>
>>> class Example:
...     pass
...
>>> type(Example())
<class '__main__.Example'>
```

[Back](#quick-jump-list)

<a name="vars"></a>

## vars

`vars` returns the `__dict__` attribute of an object, which is a dictionary containing 
its writable attributes.
If no object is provided, it returns the `__dict__` of the current local symbol table.

Example:

```python
>>> class Example:
...     def __init__(self):
...         self.an_attribute = 'value1'
...         self.another_attribute = 'value2'
...
>>> example = Example()
>>> vars(example)
{'an_attribute': 'value1', 'another_attribute': 'value2'}
>>> vars()
{'__name__': '__main__', '__doc__': None, '__package__': None, ...}
```

[Back](#quick-jump-list)

<a name="zip"></a>

## zip

`zip` takes two or more list-like things and aggregates their items into tuples. 
Each tuple contains elements from the corresponding positions of the inputs. If the 
inputs are of different lengths, `zip` stops at the shortest one.

Example:

```python
>>> list(zip([1, 2, 3], ['a', 'b', 'c']))
[(1, 'a'), (2, 'b'), (3, 'c')]
>>> list(zip('abc', [1, 2, 3], [True, False, True]))
[('a', 1, True), ('b', 2, False), ('c', 3, True)]
>>> list(zip([1, 2], ['x', 'y', 'z']))
[(1, 'x'), (2, 'y')]
```

[Back](#quick-jump-list)

<a name="__import__"></a>

## \_\_import\_\_

`__import__` is a low-level function used by the `import` statement to load modules. 
It takes a module name as a string and returns the imported module.

You should probably use `import` instead.

Example:

```python
>>> math = __import__('math')
>>> math.sqrt(16)
4.0
>>> os = __import__('os')
>>> os.name
'posix'
```

[Back](#quick-jump-list)
