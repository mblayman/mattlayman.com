---
title: Using Pipfile for fun and profit
description: >-
  Python has many methods
  to manage software package dependencies.
  The Python Packaging Authority proposed a new standard format
  called a Pipfile.
  Let's explore the reasons and benefits
  of a Pipfile
  and walk through
  converting a project to use one.
image: img/python.png
type: post
aliases:
 - /2017/using-pipfile-for-fun-and-profit.html

---

**Managing dependencies is deceptively hard.**
Need proof?
Talk to anyone who has to manage a `package.json`
in JavaScript.
I'm sure they'll have stories.

Python is not immune to this hard problem.
For years, the community rallied around the `requirements.txt` file
to manage dependencies,
but there are some subtle flaws
that make dependency handling more confusing
than necessary.
To fix these issues,
the [Python Packaging Authority](https://github.com/pypa),
which is the group responsible
for many things including `pip` and [PyPI](https://pypi.python.org/pypi),
proposed a replacement for `requirements.txt`
called a `Pipfile`.
*We're going to look
at the two file formats
to see why a `Pipfile` is a better fit
for the community
in the future
and how you can get started using one.*

## requirements.txt

Let's look at `requirements.txt` to see
where the flaws are.

A `requirements.txt` file has a very primitive structure.
Here's a sample file from the [handroll](https://github.com/handroll/handroll) project
that I work on.

```
Jinja2==2.8
Markdown==2.4
MarkupSafe==0.23
PyYAML==3.11
Pygments==2.1.3
Werkzeug==0.11.4
argh==0.26.1
argparse==1.2.1
blinker==1.4
docutils==0.12
mock==1.0.1
pathtools==0.1.2
textile==2.2.2
watchdog==0.8.3
```

The core requirement is that
each line in the file specifies one dependency.

The example adds a version specifier
for each package
even though that is not required.
The file could have said `Jinja2` instead of `Jinja2==2.8`.
In that small detail,
we can begin to see weaknesses in the structure.
Which is more correct, to specify versions or not?
*It depends.*

Specifying the version of a package is called *pinning*.
Files that pin versions for *every* dependency
make it possible to reproduce the environment.
This quality is very valuable for operating
in a production scenario.

**What's the downside?**
It's very hard to determine which packages are the direct dependencies.
For instance, handroll directly uses `Jinja2`,
but `MarkupSafe` is only listed
because it is a dependency of a dependency.
`Jinja2` depends on `MarkupSafe`.
Thus, `MarkupSafe` is a *transitive dependency*
of handroll.

The reason to include the transitive dependency
comes back to reproducing the environment.
If we only listed `Jinja2`,
it's possible for an updated version
of `MarkupSafe` to be installed
that could break handroll.
That leads to a bad user experience.

We've reached the core problem
of the older format:
*`requirements.txt` is attempting to be two views of dependencies.*

1. A pinned `requirements.txt` acts as a manifest
   to reproduce the operating environment.
2. An unpinned `requirements.txt` acts as the logical list
   of dependencies that a package depends on.

There is also a secondary problem related to the audience.
If I'm a user of handroll,
I only care about the dependencies that make the tool work.
If I'm a developer for handroll,
I *also* would like the tools needed for development
(e.g., a linter, translation tools, upload tools for PyPI).

At this stage, conventions begin to break down
in the community.
Some projects use a `requirements-dev.txt` file
for developer-only dependencies.
Others opt for a `requirements` directory
that contain many different files
of dependencies.
Both are imperfect solutions.

We're now positioned to consider what a `Pipfile`
brings to the problem.

## Pipfile

A `Pipfile` handles the problems
that `requirements.txt` does not.
It is important to note that a `Pipfile` is *not* a novel creation.
Pipfile is a Python implementation of a system that appears
in Ruby, Rust, PHP, and JavaScript.
[Bundler](http://bundler.io/),
[Cargo](https://crates.io/),
[Composer](https://getcomposer.org/),
and [Yarn](https://yarnpkg.com/en/)
are tools
from each of those languages
that follow a similar pattern.
*What traits do these systems have in common?*

1. Split logical dependencies and a dependency manifest
   into separate files.
2. Separate the sections for user
   and developer dependencies.

### `Pipfile` and `Pipfile.lock`

The `Pipfile` manages the logical dependencies
of a project.
When I write "logical,"
I'm referring to the dependencies
that a project directly
depends on
in its code.
One way to think about the logical dependencies
is as the set of dependencies
**excluding** the transitive dependencies.

Conversely,
a `Pipfile.lock` is the set
of dependencies
**including** the transitive dependencies.
This file acts as the dependency manifest
to use when building an environment
for a production setting.

> The `Pipfile` is for people. The `Pipfile.lock` is for computers.

Having a clear distinction between files
offers a couple of benefits.

1. People can read and reason about the `Pipfile`.
   There is no need to guess if a dependency is a direct dependency
   of a project.
2. Extra metadata can be stored in the `Pipfile.lock`.
   The metadata can include things like `sha256` checksums
   that help verify the integrity
   of a package's content.

### Users and developers

The other trait of a `Pipfile` is the split
between user and developer dependencies.
Let's look at the `Pipfile`
for [pytest-tap](https://github.com/python-tap/pytest-tap),
a project that I converted recently to the `Pipfile` format.

```toml
[[source]]
url = "https://pypi.python.org/simple"
verify_ssl = true

[dev-packages]
babel = "*"
flake8 = "*"
mock = "*"
requests = "*"
tox = "*"
twine = "*"

[packages]
pytest = "*"
"tap.py" = "*"
```

Because `Pipfile` uses [TOML](https://github.com/toml-lang/toml),
it can include sections
when a `requirements.txt` file could not.
The sections give a clear delineation
between user packages and developer packages.

pytest-tap is [pytest](https://docs.pytest.org/en/latest/) plugin
that produces [Test Anything Protocol (TAP)](http://testanything.org/) output.
It is a natural fit to depend on `pytest`
and `tap.py`, a TAP library.

The other dependencies do developer specific things.
`tox` and `mock` help with test execution,
`twine` is for uploading the package to PyPI,
and so on.

I hope that you could have an intuition
about pytest-tap dependencies
even without my prose descriptions.
Additionally,
splitting things out permits regular users
to skip installing extra packages.
That's the power
of a `Pipfile`.

### pipenv

Now that we've covered the benefits,
*how do you create a `Pipfile`
for your own project?*
Enter pipenv.

Kenneth Reitz, of `requests` fame,
created [pipenv](http://docs.pipenv.org/en/latest/),
a tool to manage a `Pipfile`.
pipenv helps users add and remove packages
from their `Pipfile` (and `Pipfile.lock`)
in conjunction
with a virtual environment.

Rather than manipulating a virtual environment and pip directly,
you use the `pipenv` command,
and it will do the work for you.
If you come from the Ruby world,
this is very similar to `bundle`.

Suppose you have a project
that depends
on Django.
You could prepare your Django project
with these commands:

```bash
$ pipenv --three
$ pipenv install Django
$ pipenv lock
```

Those steps would:

* create a Python 3 virtual environment
* install Django and add it to a `Pipfile`
* generate a `Pipfile.lock`

Once the files are created,
you can share your work,
and others should be able to recreate your environment.

### Summary

`Pipfile` is still an emerging standard.
In spite of that,
it is very promising
and solves some problems
that arise when working
with packages.
We saw how `Pipfile` beats out the venerable `requirements.txt` file,
and we're equipped with pipenv
to make `Pipfile`s for our projects.

I hope you learned something
about Python dependencies
and the brighter future
that is accessible today.
