---
title: "Add Styles To Templates - Building SaaS #42"
description: >-
    In this episode, I added a CSS framework, Tailwind CSS.
    After working through some issues with the log out feature,
    we started to style the base template of the site.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/XMVLpZS1mCc
aliases:
 - /building-saas/42
categories:
 - Twitch
 - Python
 - Django
tags:
 - Django
 - Tailwind
 - templates

---

In this episode, I added a CSS framework, Tailwind CSS.
After working through some issues with the log out feature,
we started to style the base template of the site.

To stay true to my "make the minimum possible thing
that will work,"
I added Tailwind CSS
from a CDN, content delivery network.

```html
<link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css"
  rel="stylesheet">
```

I described how Tailwind's utility-first approach
makes designing sites a breeze
because of the composition
of small CSS classes.

After adding the CSS,
I explained why the styles changed
so that everything looked very plain.
This conversation explained CSS resets.

We planned to add styles to the login pages
of the site,
but I ran into a weird behavior.
The site was not logging out.
After digging into things,
we figured out that the problem was using a `GET` request
to log out.
`django-allauth` does not want to allow that
because it modifies server state.

After figuring out the issue,
we did some basic styling of the base template.
