%YAML 1.1
---
blog: True
title: 2 Critical Python packaging tools
date: 2017-01-17T12:00:00Z
summary: >-
  Python packaging is a challenging process.
  Many tools can help you make a package,
  but I'll describe the tools
  that I think are the most important.
template: writing.j2

---
<img class='book' src='/images/python.png'>

At last week's
[Python Frederick](https://www.meetup.com/python-frederick/) meetup,
I gave a talk
on Python packaging.
My aim was to cover how packaging works
and how to build a basic package.
Over the course
of the talk,
we used a couple of tools
that I think are critical
for releasing a Python package
to PyPI.
*I'll describe these tools
and why I think they are critical*.

## tox

[tox](https://tox.readthedocs.io/en/latest/)
is a fantastic tool
for *testing packaging*.
With the `tox` command,
a developer can build a package,
install it into a virtual environment
for a speific Python version,
and run the package
through its test suite.

The short version of running tox looks like:

```bash
$ tox -e py36
```

This command will run a package's test suite
against Python 3.6.
I love it
when commands are that elegant.
To make that possible,
the developer must tell tox
how to run the test suite.
This configuration is done in a `tox.ini` file.
A minimal file could look like:

```ini
[tox]
envlist = py36

[testenv]
commands = python -m unittest discover \
    -s {envsitepackagesdir}/whirlygig
```

In this example,
you would change `whirlygig`
to the name
of your project.
This is enough information
to inform tox
about how to run your test suite.

I find that using tox saves me
from hard to catch packaging bugs
(did you know those exist?)
and is generally awesome
for testing against multiple versions of Python.

## twine

[twine](https://pypi.python.org/pypi/twine)
is a critical tool
in a packager's toolbelt
for one reason:
*it let's you upload to PyPI
over HTTPS*.
In contrast,
`python setup.py upload` uses insecure HTTP
for many versions of Python.

Even though it seems silly,
you need a separate package to upload securely
over HTTPS.
I presume there are good reasons
for that requirement
that I'm unaware of.

`python setup.py sdist bdist_wheel`
creates a `dist` directory
with the packages to upload.
You can perform your upload with:

```bash
$ twine upload dist/*
```

## Summary

The Python ecosystem has excellent documentation
about packaging at the
[Python Packaging User Guide](https://packaging.python.org/).
This post was meant to be a gentle introduction
to a couple of very valuable tools
when you want to work
with packages.

(Yes,
I know a "package" is technically called a "distribution"
in proper Python lingo,
but I used the term as it is more broadly accepted
among many programming languages.)
