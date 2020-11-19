---
title: "Reordering Models - Building SaaS #80"
description: >-
    In this episode, we looked at an UpdateView for the GradeLevel model
    in the homeschool application.
    Along the way, I had to display some UI elements on the grade
    to give users the ability to adjust the ordering
    of courses within their grade level.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/owCJHnd5Oiw
aliases:
 - /building-saas/80
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

In this episode, we looked at an UpdateView for the GradeLevel model
in the homeschool application.
Along the way, I had to display some UI elements on the grade
to give users the ability to adjust the ordering
of courses within their grade level.

We started by adding the icon link
that I wanted to use
to give users access
to the edit page.
Once the link was in place,
I created the URL
and copied an existing view
as a starting point
for the `UpdateView`.

As I got into the development
of the `UpdateView`,
I discovered
that the template
and the form already existed!
I had the proper form
for a pre-existing `CreateView`.
All I had to add was a bit
of context data
to conditionally display "Add" vs. "Update"
in the UI.
I also added a "Cancel" button
to the view
that was missing before.

Once the view was in place,
I wrote all the unit tests
to prove that the code worked.
I do this because it acts as my safety net
for future changes.

The final change that I made was
to display a table of courses
that the user will be able
to move each course up and down.
I showed some other up and down movement views
from course tasks
rather than showing how to implement
the movement views
during the stream.
