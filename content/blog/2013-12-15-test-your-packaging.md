---
title: Test your packaging
description: Using Travis CI and Tox to test Python packaging
image: img/2013/travis.png
type: post
aliases:
 - /2013/test-your-packaging.html
categories:
 - Open source
tags:
 - Python
 - testing

---
Software development is a process rife with errors. We generally call them
bugs, but that's so developers don't feel as bad for messing up. It's much
easier to say "oh, that's just a bug" instead of "oh, that's an error."

I made an error not too long ago. In fact, it was an egregious one. The
software that I released for MarkWiki had broken packaging. This means ***it
was completely broken for anyone who attempted to install it***. Oops. Because
of that, I likely lost the confidence of many people who were willing to
install it. According to download statistics, over 300 hundred people probably
saw my mistake immediately as MarkWiki crashed the moment they tried to run it.

The mistake was completely avoidable. All I needed to do was run the test suite
against an installed version, and the error would have smacked me in the face
like it did for the 300 other people.

When someone kindly {{< extlink "https://github.com/mblayman/markwiki/issues/13" "pointed out the error via GitHub" >}},
I decided I should fix
the problem to avoid such future embarrassment. The solution to this packaging
issue comes via {{< extlink "https://travis-ci.org/" "Travis CI" >}},
{{< extlink "http://tox.readthedocs.org/en/latest/" "Tox" >}}, and
{{< extlink "http://virtualenv.readthedocs.org/en/latest/" "virtualenv" >}}. Travis is a service
for doing automated builds using "Continuous Integration." All this means is
that every source commit to GitHub will trigger Travis to build MarkWiki and
run the tests. The automated build is run inside a virtual environment with
virtualenv so that each build is isolated (i.e., stuff from one build can't
leak into another and affect the build process). Finally, I used Tox. Tox is
neat because it is designed to do testing against *installed* packages (sounds
appropriate for me, right?).

The process looks something like this:

1. I finish a feature for MarkWiki and push it to GitHub.
2. GitHub tells Travis about the change.
3. Travis creates a virtual environment and calls Tox.
4. Tox builds a MarkWiki package, downloads all the dependencies, and runs the
   tests.
5. Travis emails me if something fails.

The configuration in my repository was super simple. And the Travis CI team
has great documentation for how to connect GitHub and their service.

I needed to add two files to my repository: **.travis.yml** and **tox.ini**.
The entire files are listed below. First, the Travis file:

```yaml
language: python
env:
  - TOX_ENV=py27
  - TOX_ENV=py26
install:
  - pip install tox
script: tox -e $TOX_ENV
```

Second, the Tox file:

```ini
[tox]
envlist = py26, py27

[testenv]
deps = nose
       coverage
commands = nosetests --with-coverage --cover-package=markwiki
```

The setup is simple and future embarrassment is minimized. So, **test your
packages!**
