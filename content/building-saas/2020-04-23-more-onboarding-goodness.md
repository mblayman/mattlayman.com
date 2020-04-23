---
title: "More Onboarding Goodness - Building SaaS #53"
description: >-
    In this episode, we continued with onboarding.
    I added unit tests for the new form
    and explained how foreign keys are wired through in CreateView.
    Then we marched on to the next template in the flow.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/FXRsPsmwhdQ
aliases:
 - /building-saas/53
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - onboarding
 - forms

---

In this episode, we continued with onboarding.
I added unit tests for the new form
and explained how foreign keys are wired through in CreateView.
Then we marched on to the next template in the flow.

In the last stream,
we set all the context data
for the view
that shows the form
to create a grade level for the school.
With the context in place,
and the form structure set,
I added the form class
that will create the `GradeLevel` record.

We used Test Driven Development (TDD)
to ensure that the form works.
Once the happy path was in place,
I wrote some additional tests
to guard against some edge cases
to guarantee that the user's data is safe.

Once the grade level form was complete,
I started on the template for the course form.
I finished the stream
by getting the basic template structure
in place
for that step.
