---
title: "The Home Stretch - Building SaaS #63"
description: >-
    In this episode, we return to the homeschool application that I'm building.
    I'm in the final stretch of changes that need to happen
    to make the product minimally viable. We worked on a template,
    wrote some model methods, and did a bunch of automated testing.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/PtixnbJyxWs
aliases:
 - /building-saas/63
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - models

---

In this episode, we return to the homeschool application that I'm building.
I'm in the final stretch of changes that need to happen
to make the product minimally viable. We worked on a template,
wrote some model methods, and did a bunch of automated testing.

We started by adding students
to the context
of the students index page.
With the students in the context,
we updated the index page
to display the list of students.

After the students were available,
we had to check their enrolled status
in a school year.
That logic doesn't belong
in the template
so we worked out the changes needed
for the view.

I updated the `Enrollment` model
to include an `is_student_enrolled` class method.
This change let us set boolean state
in the template
to decide whether to show an "Enroll" button
or not.

We updated the template again
to show that button.
After creating the button,
I proceeded to create a view
called `EnrollmentCreateView`
that we can connect to the button URL.
We wrote some tests
for the view
and ended the stream
with an unfinished template
for the view.
