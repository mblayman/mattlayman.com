---
title: "Enrolling Students - Building SaaS #64"
description: >-
    In this episode, we worked on a view to enroll students
    into a grade level for the school year.
    I added all the context data and used Tailwind to design the form layout
    to pick from a list of available grade levels.
    We added a variety of unit tests to prove the correctness.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/h0eEg3gkkYw
aliases:
 - /building-saas/64
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - templates

---

In this episode, we worked on a view to enroll students
into a grade level for the school year.
I added all the context data and used Tailwind to design the form layout
to pick from a list of available grade levels.
We added a variety of unit tests to prove the correctness.

The enrollment page needed three pieces
of data
in the context
to complete the form.
We added the `student`, `school_year`, and `grade_levels` data
to the context
and wrote tests
to show the data in there.
We also protected that data
from any erroneous access
by another user.

When the data was set,
we worked on the template
for the form.
I set the header
to make the enrollment action clear
and created the radio input selectors
to show the different grade level options.
We cleaned up the design
and user experience
by including some Tailwind CSS classes
which made the radio inputs
much easier to select.

At the end of the stream,
we wrote the happy path test
for the POST request
to prove that the enrollment record exists
after submission.
