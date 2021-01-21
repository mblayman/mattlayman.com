---
title: "Customer Requests - Building SaaS #88"
description: >-
    In this episode, I worked on some customer requests now
    that I've finished launching the product.
    These requests improved the usability of the application
    in a few spots that were lacking.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/mU7jOUM0tWc
aliases:
 - /building-saas/88
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - usability
series: "Building SaaS"

---

In this episode, I worked on some customer requests now
that I've finished launching the product.
These requests improved the usability of the application
in a few spots that were lacking.

The first request
from the customer
was to make it clear
on the daily view
when tasks are graded or not.
Before I could change the template,
I need to add a new method
to the `CourseTask`
to check if the task is graded.
Once that interface was done,
I was able to update the styling
of the template
to include grades.
To finish the change,
we had to make some changes
to make sure that the page still prints properly.

The second request was
to make deleting a task return
to the place where the user started.
This change required me
to include a `next` query parameter
on some URLs
so that the delete confirmation page can redirect back
to the original page.

The third and final request
was to include a link back
to the main application
from the documentation page.
Unfortunately,
the Sphinx theme did not make this possible by default.
I had to override the theme
by extending one
of the theme templates
and changing a template block
to have the link
that I expected.
