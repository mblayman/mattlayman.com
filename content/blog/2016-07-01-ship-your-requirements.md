---
title: Ship your requirements.txt
description: >-
  Tell the world the versions of your dependencies when you release.
  Software is constantly moving so documenting your dependency versions
  can help future users know what worked.
image: img/python.png
type: post

---
Dependencies: they're always changing.

Software is in such continuous flux.
With this stream of change,
maintainers can take a helpful step
to inform users
of dependency versions
at the time of a release.
By including a `requirements.txt` in a release,
a maintainer can notify users
of the state of the world
when the package was released.

Python packages
(or "distributions" if you want to use the official term)
set dependencies
in the `setup.py` file.
A rule of thumb is to exclude version numbers
in `setup.py`
to avoid causing conflicts between packages.
If my package says it requires `requests==2.10.0`
and your package says it requires `requests==2.9.2`,
then users can run into trouble.
Users who want to have to both my package and your package
may run into trouble when installing.

By including a `requirements.txt`
when you release a Python package
on PyPI,
you can tell users
"Here are the versions of dependencies
that I used
when I declared my software fit for release."
Many strange environments exist in the world
and including your dependency versions
in a separate file
can help future software archeologists
figure out how to make your software work
in strange places.
