---
title: "Handle Default Values - Building SaaS #65"
description: >-
    In this episode,
    I updated a model to handle the default duration of new tasks.
    This default needed to come from the Course model instead
    of the CourseTask model so we had to determine how best
    to set that data in various forms.
    I also fixed some drop down selection bugs that populated a form
    with the wrong data. We made sure that all the code was well tested.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/6hTpxgI0ZZU
aliases:
 - /building-saas/65
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

In this episode,
I updated a model to handle the default duration of new tasks.
This default needed to come from the Course model instead
of the CourseTask model so we had to determine how best
to set that data in various forms.
I also fixed some drop down selection bugs that populated a form
with the wrong data. We made sure that all the code was well tested.

I created a new `default_task_duration` field
to the `Course` model.
The field records the number of minutes
that will be set
when create a new task.
We added the field
and wrote some model tests
to confirm the behavior.

Then we updated the `Course` creation and edit forms.
To do this,
I needed to add the new field
to the `CourseForm` model form
and update the template
to include the new field.
After that,
I fixed the POST tests that broke
because the required field was missing.

Once the `Course` form was done,
I moved on to the `CourseTask` views.
We had to use `get_initial`
to populate the `CourseTask` form
with the right data
from the `Course`.
The data in `get_initial` was also needed
by `get_context_data`
so I created a `cached_property`
to store the course
and save an extra SQL query.

The next issue that I fixed was a problem
with the selector
for the task form.
The form would display the wrong grade levels
when a task could be added to multiple grades.
The code pulled the grades
from the current school year
instead of the pulling the grade levels
from the schoool year associated
with the course.
We found the error
in the code
and corrected the queries
that were needed.
After correcting the code,
I added some test code
to confirm that the problem was fixed programmatically.

At the end of the stream,
I answered some questions
from the stream
about software interviews and portfolios.
