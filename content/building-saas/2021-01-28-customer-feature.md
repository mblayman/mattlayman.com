---
title: "Customer Feature - Building SaaS #89"
description: >-
    In this episode, I show you how to take a feature idea
    from nothing to something. We added new UI, wrote a new view, a new form,
    and all the associated test code to prove that the feature works.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/-aQLfHyApGk
aliases:
 - /building-saas/89
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - usability
series: "Building SaaS"

---

In this episode, I show you how to take a feature idea
from nothing to something. We added new UI, wrote a new view, a new form,
and all the associated test code to prove that the feature works.

My customer wants the ability to complete a task
on any day she desires.
The feature flow looks like:

* Click a calendar icon next to a task
    on a student's course page.
* On the following page,
    add the desired date.
* Return to the student course page.

We began by adding the UI
for the new button.
I copied a link and changed the icon
to a calendar icon.
I also update the title tag
for increased accessibility.

Once the button was ready,
I created a URL
and a view
and started writing tests.
By using the tests,
we could follow the errors
to fill in the details
in the "error driven development" style
that I sometimes use.
I created a template
and got the basic GET requests test passing.

With basic tests passing,
I moved onto some of the edge cases
and populated the context data
with the required data.
After setting the context,
I converted the view to a `FormView`.

By doing this conversion to a `FormView`,
we had to take a detour
to create a form
that the view can use.
I used pure Test-Driven Development
to create this new form
and drive the requirements
for it.
I wrote the `clean` method
to check the correctness
of the data.
I also wrote the `save` method
to update or create the right model instance.

Once the form was ready,
I hooked it into the view
and supplied all the correct data.
With that done,
I did some refactoring
because the view was getting fairly messy.
We ran out of time to do the template design
of the feature
by the end of the stream.
