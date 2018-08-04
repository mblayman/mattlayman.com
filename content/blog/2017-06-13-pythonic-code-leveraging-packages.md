---
title: "Pythonic code: leveraging packages"
description: >-
  In this series of posts,
  I'm going to examine common design patterns
  in Python
  that make Python code feel "Pythonic."
  The sixth and final post explores the Python Package Index,
  and the benefit of using software libraries
  that are written by others
  to make your code more expressive.
image: img/python.png
type: post

---

This post concludes a series
on "Pythonic" code.
Pythonic code is code
that fits well
with the design
of the Python language.
In the last post,
we looked at Python's [standard library](/2017/pythonic-code-using-standard-library.html)
and how the "batteries included" mentality
can take a developer very far with minimal extra effort.
This sixth and final post will discuss the Python Package Index (PyPI)
and ways to make your code richer
and more powerful
by using the amazing work
from the Python community.

1. [The list comprehension](/2017/pythonic-code-the-list-comprehension.html)
2. [The with statement](/2017/pythonic-code-the-with-statement.html)
3. [The property decorator](/2017/pythonic-code-the-property-decorator.html)
4. [Built-in functions](/2017/pythonic-code-built-in-functions.html)
5. [Using the standard library](/2017/pythonic-code-using-standard-library.html)
6. Leveraging packages

## Leveraging packages

Virtually every modern software language has an ecosystem
of extra software
that can be installed
by developers.
For instance,
JavaScript developers can find software
in the [npm](https://npmjs.com/) registry.
Elixir developers have [Hex](https://hex.pm/).
And Python developers can look
at the [Python Package Index](https://pypi.python.org/) (PyPI)
for extra software.

Each language has a common tool
that can be used to download
and install this extra software
for use in a software project.
Generally, the extra software collections are called **packages**.
These common tools that interact
with package registries
to add and remove packages
to a project
are known as *package managers*.

The packages on PyPI
are uploaded by other developers
to solve specialized tasks.
*You can write more Pythonic code
if you learn about some of the most useful packages
that are available.*
Instead of creating your own bespoke solution,
you can use a well known (and well tested) package.
Using shared packages
leads to code that is more accessible
to other Python developers.

The remainder of this post will explain
how to get packages installed,
some useful packages to consider
using in your own projects,
and some resources to help you discover other interesting packages.

### Getting packages installed

PyPI has a long history
and there are a variety of ways to install packages, however,
in 2017,
the recommended way to install packages
from PyPI
is with `pip`.
`pip` is so strongly recommended
that it is included
with the latest versions
of a Python installation.

`pip` is a command line tool
that provides a variety
of subcommands
to do various tasks.
For example,
to install the static site generator tool
that I use to produce this website,
I could run the following from a terminal prompt.

```bash
$ pip install handroll
```

After running that command, the `handroll` package
and all its supporting scripts will be added
to my environment.

`pip` has the ability to install and uninstall packages
as well as search PyPI,
show specific metadata about a package,
and list the packages that are installed in your environment.

### Useful packages

So, once you know how to install packages,
what should you consider installing?
It's challenging to know what is available
because PyPI has over 100,000 registered packages.
The best thing you can do is consider the task
you want to accomplish and search for what is available.
Here are some useful example tasks
that can give you something to play with.

> How do I download data from a web API?

Many websites provide an Application Programming Interface (API)
that can provide a developer with programmatic access
to a website's data.
That's a fancy way of saying that you can get data
from a website.
The most popular package to get this kind of data
is named `requests`.
`requests` gives a very clean syntax
for fetching data.
After you `pip install requests`,
you could write code like:

```python
import requests
response = requests.get('https://www.example.com/api/')
data = response.json()
```

In this example,
the code fetches the data from example.com
and converts it into a dictionary or list
that you can use in the rest of your code.
That's three very powerful lines of code.

> How do I make a dynamic website?

There are many packages you can use
to build a website.
If you need to make a website,
you would be well served with [Django](https://www.djangoproject.com/).
A full website is too large to provide
a concise example
in a blog post,
but you can `pip install Django`
and check out their [excellent tutorial](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)
to get going.

> How do I connect to a database?

Many businesses make heavy use of databases
to store critical business data.
A well crafted Python program can help create a lot of business value
if you could only connect
and query a database.
One excellent tool for communicating with a database is
[SQLAlchemy](https://www.sqlalchemy.org/).
`pip install SQLAlchemy` to get started.

SQLAlchemy gives developers a Python API
to make database queries.
A snippet of code
(borrowed from the SQLAlchemy tutorial)
looks like:

```python
>>> our_user = session.query(User).filter_by(name='ed').first()
>>> our_user
<User(name='ed', fullname='Ed Jones', password='edspassword')>
```

SQLAlchemy connects to a database
and translates its Python API
into database queries
to fetch data.
The sample query above would generate SQL like:

```sql
SELECT users.id AS users_id,
       users.name AS users_name,
       users.fullname AS users_fullname,
       users.password AS users_password
FROM users
WHERE users.name = ?
 LIMIT ? OFFSET ?
('ed', 1, 0)
```

Using the Python API allows developers
to work with code
that models the problem domain
instead of working with raw SQL queries.
You can explore SQLAlchemy
with [their tutorial](http://docs.sqlalchemy.org/en/rel_1_1/orm/tutorial.html).

### More resources

Sometimes knowing the name of a package is the hardest part
for getting started.
Who could guess that [Werkzeug](http://werkzeug.pocoo.org/) is a great set of tools
for working with HTTP?
Unless you're German,
that's an unusual term to search for.
To find some names,
I use a couple of resources.

First,
I like to check [Python 3 Readiness](http://py3readiness.org/).
This site checks the top 360 packages
and their compatibility with Python 3.
As the community transitioned to Python 3,
this site was a very useful tool
to discover which packages made the switch.
Today,
I find that it is a useful list
to know what is popularly downloaded.

The second resource that you might use is
[Awesome Python](https://awesome-python.com/).
Awesome Python breaks down many popular packages
into their related category.
The site links to the package
and includes a brief description
so you might know what the package does.

## Conclusion

This concludes my series
of posts
on Pythonic code.

I began this series
with a zoomed-in view
of Python.
We learned the specifics
of language features like [list comprehensions](/2017/pythonic-code-the-list-comprehension.html),
[the with statement](/2017/pythonic-code-the-with-statement.html),
and [the property decorator](/2017/pythonic-code-the-property-decorator.html).

Then I started to zoom out.
We explored the [built-in functions](/2017/pythonic-code-built-in-functions.html)
to get comfortable with the tools that you don't need to import.
We [used the standard library](/2017/pythonic-code-using-standard-library.html)
to find the "batteries"
that are included
with the language.
Finally,
in this post,
I tried to show how to supercharge your Python
by explaining how to get extra software packages
from this amazing community.

I hope you enjoyed this series
and managed to learn something along the way.
