---
title: "Create A Form Template - Building SaaS #78"
description: >-
    In this episode, I created a template for one of my new forms
    on the new social media app that I'm building.
    We talked about context data, template styling,
    and special considerations for forms in templates.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/0Cm1R4aGLoY
aliases:
 - /building-saas/78
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

In this episode, I created a template for one of my new forms
on the new social media app that I'm building.
We talked about context data, template styling,
and special considerations for forms in templates.

I had an empty template
for the invite sending form
to begin.

I filled in a first attempt
at the template
with a header
and displaying form errors.
While building that,
I added some context information
that was needed
for the display.

Since this is a new app,
I created new styles that didn't exist yet.
We needed a disabled button style
for the scenario
when the user can't send an invite.

After styling things,
I added the hidden form data
that the Django view expected to receive
before sending an invite
to another user.

Once the form was functional,
we updated the template
to include informational copy
to make the page more understandable.
In the process
of adding that copy,
I added some dynamic data
to show how many remaining connections the user had available.

I put this new data
on the `User` model
and wrote some tests for this.
