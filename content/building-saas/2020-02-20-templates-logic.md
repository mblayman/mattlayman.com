---
title: "Templates and Logic - Building SaaS #45"
description: >-
    In this episode,
    we added content to a template
    and talked about the N+1 query bug.
    I also worked tricky logic involving date handling.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/iQhAelHVF-E
aliases:
 - /building-saas/45
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - templates

---

In this episode,
we added content to a template
and talked about the N+1 query bug.
I also worked tricky logic involving date handling.

The first change was
to update a course page
to include a new icon
for any course task
that should be graded.
After adding this,
we hit an N+1 query bug,
which is a performance bug
that happens
when code queries a database
in a loop.
We talked about why this happens
and how to fix it.

After finishing that issue,
we switched gears
and worked
on a tricky logic bug.
I need a daily view
to fetch data
and factor in the relative time shift
between the selected day and today.
We wrote an involved test
to simulate the right conditions
and then fixed the code
to handle the date shift properly.
