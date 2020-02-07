---
title: "Fast Forms With UpdateView - Building SaaS #44"
description: >-
    In this episode, we worked on an edit view.
    We used Django's generic UpdateView to add the process
    and test drove the creation of the view
    to verify things every step of the way.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/aSE7vQKAFs8
aliases:
 - /building-saas/44
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - forms

---

In this episode, we worked on an edit view.
We used Django's generic UpdateView to add the process
and test drove the creation of the view
to verify things every step of the way.

We worked on a view to make it possible
to edit the `CourseTask` model
that are the actions
that a student must complete
for a course.

To complete the form quickly,
I took advantage
of Django's `ModelForm` views.
These views are designed to make forms rapidly
from existing models.

The first thing I did was create a test
that would try to edit a course task
from the URL
where the task can be edited.
The first test was a `GET` request
to make sure that we can render a form
for the given task.

We took a break to chat
about other frameworks
and philosophies around those choices.

On the new view,
I used `get_queryset`
to filter to the tasks
associated with the user's school.
To connect the view
to the view's URL `uuid` parameter,
we had to set `slug_field` and `slug_url_kwarg` to `uuid`.
Finally,
I set the `fields`
that we want to edit
on the model record.

After that was done,
the view required the creation
of a `courses/coursetask_form.html` template.
We created an empty file
and the initial test passed!

With the happy test done,
I added more tests
to check the other constraints
that the view needs to have.

Before jumping into the template
of the form,
I modified the daily view
that is supposed to link to this view
to do the proper linking.

To finish the stream,
I spent a bit of time
adding initial styles and structure
to the form view templates.
