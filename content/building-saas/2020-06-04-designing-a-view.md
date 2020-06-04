---
title: "Designing A View - Building SaaS #59"
description: >-
    In this episode,
    I focused on a single view for adding a course to a school year.
    This view is reusing a form class from a different part
    of the app and sharing a template.
    We worked through the details of making a clear CreateView.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/xL4gIx1bLaE
aliases:
 - /building-saas/59
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
I focused on a single view for adding a course to a school year.
This view is reusing a form class from a different part
of the app and sharing a template.
We worked through the details of making a clear CreateView.

The stream started with me answering a question
about how I design a new feature.
I outlined all the things
that I think through
for the different kinds
of features
that I need to build.

After that discussion,
I introduced the view
that I needed to add.
It's a `CreateView`
for a `Course` model
that's an extension
of an existing `UpdateView`.

I pulled together the set
of unit tests
that will prove
that the view will behave
as I expect it to.

Once we had the tests to work from,
I updated the underlying `CourseForm`
for the extra data
that the model needs
on creation.

We found that some logic was embedded
into a view
that we needed for the new view,
and we refactored the view code
to move that logic to a model method.

For the rest of the stream,
we worked through the issues
that popped up
before the tests could pass.
