---
title: "Pythonic code: using the standard library"
description: >-
  In this series of posts,
  I'm going to examine common design patterns
  in Python
  that make Python code feel "Pythonic."
  The fifth post peeks
  at Python's standard library
  and how the "batteries included" mindset
  can make developers super productive
  with no setup.
image: img/python.png
type: post
aliases:
 - /2017/pythonic-code-using-standard-library.html
categories:
 - Python
tags:
 - Design
 - standard library

---

This post continues a series
on "Pythonic" code.
Pythonic code is code
that fits well
with the design
of the Python language.
The previous post explored the possibilities
with Python's [built-in functions]({{< ref "/blog/2017-04-24-pythonic-code-built-in-functions.md" >}}).
This fifth post will peek
into the standard library
and highlight how many amazing tools are available
with no setup.

1. [The list comprehension]({{< ref "/blog/2017-03-28-pythonic-code-the-list-comprehension.md" >}})
2. [The with statement]({{< ref "/blog/2017-04-04-pythonic-code-the-with-statement.md" >}})
3. [The property decorator]({{< ref "/blog/2017-04-11-pythonic-code-the-property-decorator.md" >}})
4. [Built-in functions]({{< ref "/blog/2017-04-24-pythonic-code-built-in-functions.md" >}})
5. Using the standard library
6. [Leveraging packages]({{< ref "/blog/2017-06-13-pythonic-code-leveraging-packages.md" >}})

## Using the standard library

To quote from the {{< extlink "https://docs.python.org/3/" "Python documentation" >}}:

> keep this under your pillow

Python is an extremely productive programming language.
Its visual style lends itself to great readability and clarity.
Its {{< extlink "https://www.python.org/dev/peps/pep-0020/" "guiding principles" >}}
are beautiful ambitions for programming language design.
And its included software,
known as the standard library,
is meant to make *you* as productive as possible
with minimal effort.

The main reason that the standard library requires minimal effort
is because it comes installed
with the Python language.
The Python community likes to say
that the language has "batteries included."

This batteries included philosophy gives developers a wide choice
of software
that solves many problems.
Having so much software introduces a challenge.
In my last post on {{< extlink "/2017/pythonic-code-built-in-functions.html" "built-in functions" >}},
I noted that I covered less than 10%
of the built-ins.
That challenge is amplified
to an even bigger extent
for the standard library
since there are well over 200 modules.

For this post,
I'd like to give you,
dear reader,
an idea of some tasks
that the standard library can handle.
With this idea in hand,
I hope you'll be inspired
to browse {{< extlink "https://docs.python.org/3/library/index.html" "the documentation" >}}
when trying to solve some of your own problems.

Making use of the standard library
will certainly make your code more Pythonic.
Let's look at some examples
to see why.

## The Excel task

Microsoft Excel has an unbelievable influence
on the world.
It is a very powerful tool
that small and large businesses alike
use regularly
to manage data.
I have personally witnessed brilliant people
do amazing things with Excel
and its rich functions and tools.
In spite of that,
Excel has limitations
where a general progamming language
like Python
does not.

When you encounter some data task
that Excel can't handle,
you may want to consider the {{< extlink "https://docs.python.org/3/library/csv.html" "csv" >}}
module.
Exporting your data to CSV format
and manipulating it in Python
opens up all the expressive options
of the language.

```python
import csv

with open('financials.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['profit'], row['revenue'])
```

This example shows financial data
added to standard Python dictionary objects.
The keys to the dictionary are determined
by the first row of the CSV file.
You could imagine forecasting
or mixing the data with other sources
to do complex analysis,
and determine the traits
that help contribute
to the success
of the company.
The `csv` module may be your best friend
to ingest that data.

## Filepalooza

Once upon a time,
I wrote Perl code.
This Perl code was used to manage the complexity
of IBM Rational ClearCase,
a beast of a version control system
(if you think Git is complicated,
please allow me to introduce you to ClearCase. :) ).
The Perl code that I wrote targeted a UNIX-like operating system,
and I was tasked with adding cross-platform support on Windows.
The ensuing experience was horrible.
The team I was on made heavy use of
{{< extlink "http://search.cpan.org/dist/PathTools/lib/File/Spec.pm" "File::Spec" >}},
but it was still painful.

When I started doing development
in Python,
I learned about modules that made file handling much better:
{{< extlink "https://docs.python.org/2/library/os.html" "os" >}}
and
{{< extlink "https://docs.python.org/3/library/shutil.html" "shutil" >}}.

`os` and its buddy module {{< extlink "https://docs.python.org/3/library/os.path.html" "os.path" >}}
make file management doable.

The documentation for `os` is *completely* intimidating,
but there are very handy functions in there.
You can remove files (`os.remove`),
make directories (`os.mkdir`),
and take action on every file in a directory
by "walking" through it (`os.walk`).

`os.path` includes functions
to manipulate file paths.
The cool part is that file paths are handled
in a cross-platform way
by default.

```python
# Don't do this.
path = 'path/to/data.csv'
# Instead, do this.
path = os.path.join('path', 'to', 'data.csv')
```

The `os.path.join` version is a bit longer,
but you know that it will produce `path/to/data.csv`
on Linux and macOS
and `path\to\data.csv`
on Windows.

`shutil` is a module that I use specifically
for two functions:
`shutil.copytree`
and `shutil.rmtree`.
These two functions let you copy or delete
an entire directory and all its contents.

The newest module to shake things up
in file handling is {{< extlink "https://docs.python.org/3/library/pathlib.html" "pathlib" >}}.
I don't have much experience with this
because I haven't written much Python 3 *only* code,
but it seems really powerful.

```python
>>> from pathlib import Path
>>> p = Path('data')
>>> q = p / 'to' / 'data.csv'
>>> q
PosixPath('data/to/data.csv')
```

## The programmer's chainsaw: regular expressions

A chainsaw can make short work
of cutting down a tree
*or it can saw off your arm*.
Handle a chainsaw well
and you'll be rewarded.
Be careless with it
and it will cause you serious pain.
Regular expressions are exactly like that.
A regular expression is a powerful developer tool
that can save or ruin your day
depending on how you wield it.
The goal of a regular expression
is to find a pattern
in data
and do something
if there is a match to the pattern.

Python includes the {{< extlink "https://docs.python.org/3/library/re.html" "re" >}} module
as your gateway to handling regular expressions.
The documentation for this module is possibly *more* intimidating
than the `os` module,
but that's because regular expressions are essentially
a {{< extlink "https://en.wikipedia.org/wiki/Domain-specific_language" "domain specific language" >}}
for pattern matching.
If you take the time to learn regular expressions,
you can get some really cool things done.

Let's consider an introductory example for regular expressions:

```python
>>> import re
>>> pattern = re.compile('abc')
>>> bool(pattern.match('abcde'))
True
>>> bool(pattern.match('def'))
False
>>> bool(pattern.match('ABC'))
False
>>> pattern = re.compile('abc', re.IGNORECASE)
>>> bool(pattern.match('ABC'))
True
```

We can see how the regular expression pattern can be applied
to various strings
to see if they match.
Also, it's possible to add extra options like `re.IGNORECASE`
to change the behavior of the pattern matching.

Matching is useful,
but it gets even better
when we can pull out information
in the match.
Check this out:

```python
>>> pattern = re.compile('Hi, (\w+)')
>>> match = pattern.match('Hi, Matt')
>>> match.group(1)
'Matt'
```

We extracted a name from a greeting.
This example is a little tame
yet the idea is fierce.
*If you can describe the pattern
that you desire,
you can tear through huge volumes
of data
for your search.*


## Onward

The Python standard library is very useful.
In this post, I've showed that it can:

* Ingest tabular data via CSV for advanced data processing
* Manipulate files on your computer
* Find the proverbial "needle in a haystack"
  with regular expressions

These examples barely cover what is available.
Describing each of these modules would take many years
of posts.
If you want to learn more,
I can suggest you read the
{{< extlink "https://pymotw.com/3/" "Python 3 Module of the Week" >}} series
from Doug Hellmann.
Doug covers a number of popular modules
in great depth,
and they are worth a read.

In my next Pythonic code post,
we're going to explore writing Pythonic code
by using packages
from the Python Package Index
(a.k.a. PyPI).
Thanks for reading!
