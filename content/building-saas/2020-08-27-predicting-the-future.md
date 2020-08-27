---
title: "Predicting The Future - Building SaaS #70"
description: >-
    In this episode, we worked on two issues.
    The first issue was fixing incorrect projected completion dates of tasks.
    We used test driven development to reveal the bug and work on the fix.
    The second issue add some extra data to display on a page.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/LjWeKqK6H-A
aliases:
 - /building-saas/70
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - views
series: "Building SaaS"

---

In this episode, we worked on two issues.
The first issue was fixing incorrect projected completion dates of tasks.
We used test driven development to reveal the bug and work on the fix.
The second issue add some extra data to display on a page.

We picked a couple of tasks
at random
to fix
for this stream session.

The first issue related
to the course view
when paired
with what the student's actions.
This view shows the projected completion dates
for individual tasks.
When the school year was set to start
in the future,
this view was incorrect.

My local test data didn't have this same setup
so we started by writing a unit test
to prove that the view was broken.
After writing the test,
the fix was very straightforward to add.

For the second issue
that I picked,
we worked directly on the code
because I knew
that there was already test code
in place
to guide the changes.
The issue was that the student index page did not display the grade level
for each enrolled student.
We modified the context
of the view
to include enrollment data
so that the template could show the grade level.
