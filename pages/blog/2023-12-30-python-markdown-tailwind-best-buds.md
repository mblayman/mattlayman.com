---
title: "Python, Markdown, and Tailwind: Best Buds!"
description: >-
  You are rendering content with Python
  and want to show some Markdown,
  but you style your pages with Tailwind.
  With Tailwind's built-in reset,
  how can you style the tags of your rendered HTML
  that come from Markdown?
  This article shows how that can be done.
image: /static/img/2023/python-tailwind.png
categories:
  - Python
tags:
  - Python
  - Markdown
  - Tailwind
date: 2023-12-30
slug: python-markdown-tailwind-best-buds

---

You are rendering content with Python
and want to show some Markdown,
but you style your pages with Tailwind.
With Tailwind's built-in reset,
how can you style the tags of your rendered HTML
that come from Markdown?
This article shows how that can be done.

Specifically,
I am assuming that you are working with Python's `Markdown` package.

I recently worked on a project
where I needed to render some Markdown descriptions.
`Markdown` is a great package for quickly transforming Markdown content
into standard HTML output.
The big challenge for my project is that the tags were unstyled.
Because of this,
all of the content in my project looked the same.
Since I was using
[Tailwind CSS](https://tailwindcss.com/),
I needed to include classes to make the tags look sharp.

One way that I could have achieved my result would be to wrap these tags
with a container (e.g., `.description`),
then write some custom rules in my CSS file.
Using Tailwind's `@apply` feature,
this is a completely viable path.
In fact,
it's the strategy that I used for *this* site.
But after using this strategy on this site for years,
I've stumbled across various annoyances
that made me want to try a different method.

> To make this work, we'll use a **Markdown Extension**.

By the time we're done,
we'll use our extension like:

```python
import markdown

from .extensions import TailwindExtension

with open('content.md', 'r') as f:
    html_output = markdown.markdown(
        f.read(),
        extensions=[TailwindExtension()]
    )
```

If you
[read about Markdown extensions](https://python-markdown.github.io/extensions/api/),
you'll learn that,
inside of the extension,
you can use one of a variety of processors to manipulate either the input stream
of Markdown data
or the HTML output.

The processor that we need to reach for is a `Treeprocessor`.
Internally,
the Markdown package uses the XML
[ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) API.
The `Treeprocessor` provides access to the root tree
of the HTML output.
*The strategy for our extension is to add classes
to any tag that is found in the tree
that matches what we define classes for.*

First,
we can look at the implementation
of the custom tree processor.

```python
# extensions.py
...

from markdown.treeprocessors import Treeprocessor

...

class TailwindTreeProcessor(Treeprocessor):
    """Walk the root node and modify any discovered tag"""

    classes = {
        "a": "underline text-blue-700 hover:text-blue-500",
        "p": "pb-4 text-normal",
    }

    def run(self, root):
        for node in root.iter():
            tag_classes = self.classes.get(node.tag)
            if tag_classes:
                node.attrib["class"] = tag_classes
```

The processor:

* Implements the required `run` method that gives us access to the `root` node
* Iterates over each tag. The ElementTree API will recurse down
  into the tree automatically.
* Checks the tag name via `node.tag` to see if there are any classes defined
  for that tag.
  The `classes` dictionary specifies the tags that we want to customize.
* Adds the `class` attribute to the tag if any custom classes exist.

And that's it!


Let's complete the picture by showing how the processor is wired
to an extension.

```python
# extensions.py
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class TailwindExtension(Extension):
    """An extension to add classes to tags"""

    def extendMarkdown(self, md):
        md.treeprocessors.register(
            TailwindTreeProcessor(md), "tailwind", 20)


class TailwindTreeProcessor(Treeprocessor):
    """Walk the root node and modify any discovered tag"""

    classes = {
        "a": "underline text-blue-700 hover:text-blue-500",
        "p": "pb-4 text-normal",
    }

    def run(self, root):
        for node in root.iter():
            tag_classes = self.classes.get(node.tag)
            if tag_classes:
                node.attrib["class"] = tag_classes
```

The extension must define `extendMarkdown`
and register the processor.
There are some oddities of where to register
depending on the kind of processor that you use.
In our case,
`md.treeprocessors` is the right place to register our processor.
Check the docs to understand the arguments that go to `register`.

Before we finish,
you'll need one more thing.
Because we are adding classes to this extension file,
we need to make sure that Tailwind is scanning this file.
If you don't do this,
then your built Tailwind CSS file will be missing these classes.
I missed this initially and was puzzled for a bit
until I was missing this config change.
Here's what this configuration change might look like
in your `tailwind.conf.js` file.

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    // There are some Tailwind classes embedded in the Markdown extension.
    "./path/to/extensions.py",
  ],
}
```

I hope this helps get your Markdown content looking great
in your Tailwind-styled project.
