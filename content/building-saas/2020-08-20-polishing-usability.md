---
title: "Polishing and Usability - Building SaaS #69"
description: >-
    In this episode, we polished some parts of the application.
    Now that my first customer is using the app regularly,
    the feedback is coming in rapidly.
    We worked to fix some of the issues that she found.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/GnOcVBmqYKU
aliases:
 - /building-saas/69
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

In this episode, we polished some parts of the application.
Now that my first customer is using the app regularly,
the feedback is coming in rapidly.
We worked to fix some of the issues that she found.

The first issue that I tackled
dealt with ambiguity
about a course's relationship
to a school year
on the course's detail page.
I fixed this issue
by displaying the grade level
on the course page
to provide all the details.
This change makes it clear
what grade level the course is connected to.
This is useful because courses
in the school year could have the same name
(e.g., "Math").

The next issue that we worked on
was related to the ordering
of data
on the schedule pages.
The schedules pages showed information
for each student in the school.
This was broken for a couple of reasons:

1. The order of students may not match the order
    of grade levels.
    That leads to a mismatch
    when looking at the school year
    versus looking at the schedule view.
2. The schedule would show students
    even if they weren't enrolled
    in the school year.

I fixed the daily and weekly schedule views
by changing the logic
from looping over all the students
to looping over all the enrollments
for a school year.
This change corrected both of the problems
that were present
in the view.

After changing that in two place,
I observed the common implementation
that was duplicated
in two views.
Because of the duplication,
we did some refactoring
to extract that logic
into a shared method
on the `Student` model.

At the end of the stream,
as I cleaned up the code
to prepare to commit it,
we cleaned up some test code
based on some observations
about how the tests behaved
with the new code.
