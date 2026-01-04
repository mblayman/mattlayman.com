---
slug: handroll-1-1-released
title: handroll 1.1 released
date: 2014-06-01
description: A release announcement for handroll 1.1
aliases:
 - /2014/handroll-1-1-released.html
categories:
 - Python
 - Open source
tags:
 - handroll
 - static site generators

---

I have released the 1.1 version of my static website generator. This version
contains quite a few new features which are documented in the [release history](http://handroll.readthedocs.org/en/latest/releases.html#version-1-1-released-june-1-2014).
Essentially, the 1.1 release adds the level of polish that
users should probably expect from a product.

The features included in this releases were driven by what I actually needed
for this website. This includes code highlighting, file skipping, and handling
for non-ASCII characters (thanks ØMQ book!).

Under the hood, I added support for a plugin architecture so that anyone can
write plugins for handroll.

Finally, I added documentation at [Read the Docs](http://handroll.readthedocs.org/en/latest/)
and introduced better testing
with [Travis CI](https://travis-ci.org/mblayman/handroll). These were added
because of lessons learned from other projects.

You can download handroll from [PyPI](https://pypi.python.org/pypi/handroll) or
install it with:

```console
$ pip install handroll
```
