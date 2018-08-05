---
title: Extending handroll for fun
description: Show how to create an entire handroll extension from scratch
image: img/2015/outlet.jpg
type: post
aliases:
 - /2015/extending-handroll.html
categories:
 - Guide
 - Python
 - Open source
tags:
 - handroll
 - static site generators

---
I released handroll 2.0 with a shiny new extension interface.
This post will make a new extension from soup to nuts
to demonstrate the ease of such a task.
We'll call it the `ObnoxiousExtension`.
Our extension will make some noise on the console.

Let's start with the code.
[Download the extension](/2015/obnoxious.py)
to play with it yourself.

```python
from handroll.extensions.base import Extension


class ObnoxiousExtension(Extension):
    handle_pre_composition = True
    handle_frontmatter_loaded = True
    handle_post_composition = True

    def on_pre_composition(self, director):
        print 'Let\'s get this party started!'

    def on_frontmatter_loaded(self, source_file, frontmatter):
        print 'YO! Da front matter loaded.'

    def on_post_composition(self, director):
        print 'Peace out, homeslice!'
```

An extension must do two things:

1. Declare what signals it should be notified about.
2. Do its work in a signal handler method.

To express interest a signal,
set the `handle_*` class attribute to `True`.
This will cause the extension to register with the signal
and receive events when they occur.

The extension can process a signal with the handler method.
The handler method has a set signature,
but anything goes in the body of the method.
In the example,
I did a boring `print` statement.

All the signals and handler methods that you can use
are in the {{< extlink "http://handroll.readthedocs.org/en/latest/extensions.html" "extension documentation" >}}.
Any work that you do beyond the class attributes
and handlers is entirely in your hands.

Once your extension is ready,
you need to hook it in using a setuptools entry point.
I created a minimal `setup.py` file
(which is also [available for download](/2015/setup.py))
to show that setuptools configuration.

```python
from setuptools import setup

setup(
    name='handroll-obnoxious',
    version='0.1',
    install_requires=['handroll'],
    py_modules=['obnoxious'],
    entry_points={
        'handroll.extensions': [
            'obnoxious = obnoxious:ObnoxiousExtension',
        ]
    },
)
```

In this entry point,
`obnoxious` on the left hand side is the name of the extension.
`obnoxious` on the right hand side is the module name
and `ObnoxiousExtension` is the class name.

That's it for code.
If you followed along,
`python setup.py sdist` should create a source distribution to use.
You can install the newly minted package
and make your handroll site generation obnoxious.

To use the extension,
add `with_obnoxious = True`
to the `[site]` section of your `handroll.conf`.
While editing this post with the extension enabled,
I got this output
whenever I saved the source file.

```
Let's get this party started!
YO! Da front matter loaded.
Peace out, homeslice!
```

I hope this gives you a clear idea
of how to make a handroll extension.
The source distribution for this little example
is [available for download](/2015/handroll-obnoxious-0.1.tar.gz).
