---
title: handroll 1.1 released
description: A release announcement for handroll 1.1
type: post
aliases:
 - /2014/handroll-1-1-released.html

---
I have released the 1.1 version of my static website generator. This version
contains quite a few new features which are documented in the {{< extlink "http://handroll.readthedocs.org/en/latest/releases.html#version-1-1-released-june-1-2014" "release history" >}}.
Essentially, the 1.1 release adds the level of polish that
users should probably expect from a product.

The features included in this releases were driven by what I actually needed
for this website. This includes code highlighting, file skipping, and handling
for non-ASCII characters (thanks ØMQ book!).

Under the hood, I added support for a plugin architecture so that anyone can
write plugins for handroll.

Finally, I added documentation at {{< extlink "http://handroll.readthedocs.org/en/latest/" "Read the Docs" >}}
and introduced better testing
with {{< extlink "https://travis-ci.org/mblayman/handroll" "Travis CI" >}}. These were added
because of lessons learned from other projects.

You can download handroll from {{< extlink "https://pypi.python.org/pypi/handroll" "PyPI" >}} or
install it with:

```console
$ pip install handroll
```
