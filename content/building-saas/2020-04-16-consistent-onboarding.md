---
title: "Consistent Onboarding - Building SaaS #52"
description: >-
    In this episode, we glued together some of the onboarding steps.
    I added data validation
    so that future steps depend on data existing from previous steps.
    Then we added page messaging to direct users to a proper page.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/RY8NtEUaAv4
aliases:
 - /building-saas/52
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

In this episode, we glued together some of the onboarding steps.
I added data validation
so that future steps depend on data existing from previous steps.
Then we added page messaging to direct users to a proper page.

We reviewed the way that the form validates certain data
from the form submission
so that data is kept safe between users.
I showed how I switched
from the `model` and `fields` attributes of `CreateView`
to a `form_class` containing the form
that does the necessary validation.

We talked about how the onboarding flow is interconnected.
With that context,
I updated the first step
to ensure that the school year data can only be created once.

We also updated the second step
to ensure that a user can't proceed
until the necessary data from the previous step is present.

I added tests to check the various conditions
and updated templates to render the right thing
for the various states.
