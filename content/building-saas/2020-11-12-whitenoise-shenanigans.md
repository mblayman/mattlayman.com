---
title: "WhiteNoise Shenanigans - Building SaaS #79"
description: >-
    In this episode, I worked on a method of adding static content
    to a site that didn't involve the staticfiles directory,
    a separate domain, or a reverse proxy like Nginx.
    We had to get clever with Heroku buildpacks and how to configure WhiteNoise.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/WkAQrExP_AE
aliases:
 - /building-saas/79
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - templates
series: "Building SaaS"

---

In this episode, I worked on a method of adding static content
to a site that didn't involve the staticfiles directory,
a separate domain, or a reverse proxy like Nginx.
We had to get clever with Heroku buildpacks and how to configure WhiteNoise.

I want to put a blog
on my side project
for content marketing purposes.

I want the blog
to be statically generated
and have content come
from Markdown
(just like these show notes
that you're currently reading).

My preference is to put the blog
on a path
like `mysite.com/blog/` instead
of using a subdomain
like `blog.mysite.com`.

I could do this easily
if the blog lived at `/static/blog/`
by working
within Django's staticfiles system,
but those URLs look gross.

I could also do this
with a reverse proxy
like Nginx,
but that complicates my Heroku deployment setup.

Instead of picking any
of those strategies,
I wanted to find a way
to make WhiteNoise,
the package that serves static files
in my Django app,
serve the blog.

To get started,
I added a Heroku buildpack
that would run Hugo
to generate the blog output.
This took a while
to get right
because I had to create a Hugo project
in a way that didn't pollute
the root of my project
with a bunch of Hugo directories.

Once I was successful
with Hugo,
we moved on to the WhiteNoise setup.
I created a custom subclass
of the WhiteNoise middleware
so that I could add the blog output
to the set that WhiteNoise would serve.

We got the middleware set up
and I proved that the app could serve the blog.
To finish off the stream,
I did some validation of the cache headers
to see the behavior
of the blog files
and how WhiteNoise would cache the files.
