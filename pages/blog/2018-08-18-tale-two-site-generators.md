---
slug: tale-two-site-generators
title: "A tale of two site generators"
date: 2018-08-18
description: >-
  I switched my website from a custom made tool, handroll,
  to a very popular static site generator, Hugo.
  Why would someone switch from something tailor-made
  to a different tool?
  I explore what I've learned
  from going my own way
  for many years.
image: img/2018/hugo.png
aliases:
 - /archive.html
categories:
 - Software
tags:
 - Hugo
 - static site generators
 - handroll

---

I made my website
back in 2008
as a way to build an online presence.
The site began as a WordPress blog
hosted on [wordpress.com](https://wordpress.com/).
After years of living at wordpress.com,
I moved to my own server for a short stint.
Eventually,
I discovered GitHub Pages
and started my journey
into static site generators
to avoid the burden
of managing my own hardware.
Today,
I've moved from a custom static site generator
to [Hugo](http://gohugo.io/).
This post explores *why* I would make that kind of change.

In 2013,
the landscape of static site generators was different.
There were not a ton of choices.
I really wanted to run a Python tool
and my best option was [Pelican](https://blog.getpelican.com/),
which I ran on my own server
and even [contributed back code](https://github.com/getpelican/pelican/pull/586).
Unfortunately,
I wanted something more than a blog,
and I couldn't figure out how to make Pelican work in the way I needed.

Without a tool to do want I wanted,
the most fun thing I could think to do was **build my own**.
Making my own tool would be a great way to learn
about the specifics of static site generators
and get something that did exactly what I desired.

The result of my effort was [handroll](https://github.com/handroll/handroll).
Today,
handroll has all sorts of features that I've needed for my site. Features like:

* Markdown, reStructuredText, and Textile support
* A development server that does incremental build updates
* Blog plugin to generate feeds and listing pages
* OpenGraph and X metadata plugins
* [Jinja2](http://jinja.pocoo.org/docs/2.10/) templating
* Sass support
* A plugin and extension system with well documented extension points

handroll served me well,
but I gave up on it
a few weeks ago.
*Why would I do that?*

The short answer is **community**.

> Never underestimate the power of a robust community.

When I created handroll,
I tried to build a community
by documenting the tool well on [Read the Docs](https://handroll.readthedocs.io/en/latest/).
I even attempted to add translations to the command line interface
for a large number of languages.
Google Translate was the source of the translations
so I apologize for anyone looking at those strings today.
**handroll never got traction.**
It's hard to get noticed
even when something is pretty good.

Because handroll never established a community,
it meant that I was doing everything.
A competent developer working
in his spare time
can't compete
with a massive community
of people
focused on a single project.
Many hands make light work or something.

In contrast,
Hugo took off in popularity.
The project has 540 contributors
and 28k stars on GitHub.
That kind of attention helps remove all the rough edges.

Having lots of users causes these kinds of changes
to happen
(to an average project):

* The user experience is better.
* The documentation is better.
* The amount of help on Stackoverflow is better.
* The diversity of contributions is better.

That last bullet is the one that won the day for Hugo for me
against my own project.

My site was looking fairly stale from a design perspective.
I have a reasonable skillset with CSS,
but I'm not a designer.
Without a community,
there was no hope of handroll ever having a set
of themes
built by designers.
Because Hugo is so popular,
it attracted the attention
of developers
and designers alike.
Hugo has an entire [Themes page](https://themes.gohugo.io/)
that shows off many high quality themes
that are ready to use.
*This was super appealing to me.*

I set out and created a branch that would try to use Hugo.
My posts were already in Markdown
with a YAML frontmatter
so my conversion process
was pretty easy.

As a bonus,
I got to add things like tags and categories
that I never had time to implement myself
for handroll.

Now, you're reading the result. I'm really loving two things about this:

1. I don't have to maintain a tool just to maintain a website.
2. The speed and features of Hugo are really nice.

Thanks to the Hugo community for making something easy and fun to use!
