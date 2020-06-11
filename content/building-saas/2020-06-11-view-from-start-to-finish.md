---
title: "A View From Start To Finish - Building SaaS #60"
description: >-
    In this episode,
    I created a view to add students from beginning to the end.
    I used Error Driven Development to guide what I needed to do next
    to make the view, then wrote tests,
    and finished it all off by writing the template code.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/nLG017x0yys
aliases:
 - /building-saas/60
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - views

---

In this episode,
I created a view to add students from beginning to the end.
I used Error Driven Development to guide what I needed to do next
to make the view, then wrote tests,
and finished it all off by writing the template code.

At the start of the episode,
I gave a quick overview
of the models
in my application
and which models I planned to focus on
for the stream.

We worked on a view to add students.
I did this using a technique
that I called *Error Driven Development*.
With this strategy,
I started with what I wanted
and followed the error messages
to drive to what I needed
to write.
Django's error messages are good enough
to show what was needed
for each step.

After creating a view
that didn't error anymore,
I filled in some tests
to prove
that the view behaved
in the way I wanted.

Finally,
I wrote the template
that provides the proper data
for the newly created view.

Once the template was complete,
I did one manual end-to-end test
to confirm that the template
and view worked together.
I verified in the Django admin
that the view created a new student.
