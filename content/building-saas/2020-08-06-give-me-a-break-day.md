---
title: "Give Me A Break... Day - Building SaaS #67"
description: >-
    In this episode, we did some Django model development.
    I created a new model to track break days in a school year.
    This model will be critical to fill in vacations and holidays
    so that the scheduling functionality works properly.
    I added the model, the tests, the admin page, and the create view
    to create break days in the app.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/nr9b4-Nc7x4
aliases:
 - /building-saas/67
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - models
series: "Building SaaS"

---

In this episode, we did some Django model development.
I created a new model to track break days in a school year.
This model will be critical to fill in vacations and holidays
so that the scheduling functionality works properly.
I added the model, the tests, the admin page, and the create view
to create break days in the app.

We started by picking a model name
and discussing naming in programming.
I used test-driven development (TDD)
to build the model
that I named `SchoolBreak`.
We created a model factory
to build out the full model class.
I added attributes for the day, a description,
a foreign key to a `SchoolYear`,
and a UUID.

After working on the model,
I started working on the CRUD interfaces
for the `SchoolBreak`.
We created a button to get to the create page
on the school year page.

Once the button was complete,
I added a `SchoolBreakCreateView`
that followed a very similar pattern
as the `GradeLevelCreateView`.
We worked through all the tests
to ensure that the new view behaves properly.

Finally,
I made a Django admin so I could view school breaks.
With the admin in place,
I could use the create view
and verify that I created an actual break record
in the database.

On future streams,
we will work on hooking up the remaining parts
of CRUD
and add the ability to read, update, and delete school breaks.
