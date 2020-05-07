---
title: "Remodeling Data Relationships - Building SaaS #55"
description: >-
    In this episode, we're remodeling!
    I changed the model relationship between GradeLevel and Course
    from a ForeignKey (1 to many) to a ManyToManyField.
    We talked through the change and started fixing all the tests that broke.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/qQdBcj02J60
aliases:
 - /building-saas/55
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - models

---

In this episode, we're remodeling!
I changed the model relationship between GradeLevel and Course
from a ForeignKey (1 to many) to a ManyToManyField.
We talked through the change and started fixing all the tests that broke.

After explaining the change
that I wanted to make
and why I want to make it,
I explained how a foreign key
and many to many relationship
at the database level.

Once we had the conceptual foundation
in place,
I started with the documentation.
We looked at the `ManyToManyField`
and what changes were needed
to convert a `ForeignKey`
to a `ManyToManyField`.

After the change,
we immediately saw the value
of having a test suite
that runs all the code.
We ran the tests
and see the test suite light up
like a Christmas tree
with errors.

For the remainder
of the stream,
I worked to fix errors
in the suite
by fixing the broken code
and the broken tests.
