---
title: "How To Style Sign Up - Building SaaS #47"
description: >-
    In this episode, I added styling to the Sign Up page of the site.
    We chatted about CSS tools and frameworks,
    the benefit of feature flags to control what UI is displayed to users,
    and how to use Tailwind CSS to modify a design quickly.
type: video
image: img/2019/tailwind.png
video: https://www.youtube.com/embed/7w33auedQXA
aliases:
 - /building-saas/47
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - CSS
 - template

---

In this episode, I added styling to the Sign Up page of the site.
We chatted about CSS tools and frameworks,
the benefit of feature flags to control what UI is displayed to users,
and how to use Tailwind CSS to modify a design quickly.

In the first portion
of the stream,
we focused on CSS frameworks.
We compared Bootstrap, Semantic UI, and Tailwind CSS.

After that discussion,
I talked about feature flags.
The project uses a feature flag
to protect the sign up page
and only displays the page
when I turn on a flag.
This control will be useful
for me to gate
which new users I would like to allow
into my project
as I open it up to others.

Once the feature flag was on locally,
we worked to style the signup form
that was provided by django-allauth.
I kept the form very basic
with a plan to expand it
in the future.
We also talked about JS frameworks
and my plans for which framework to use.

We finished the development
for the stream
by fixing the notification messages.
While testing the sign up flow,
I noticed that multiple notifications appeared
from django-allauth
and my UI stacked them
in a way that looked off.
We used flexbox to fix the issues
so that multiple notifications could display well together.
