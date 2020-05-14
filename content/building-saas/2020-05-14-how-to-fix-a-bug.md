---
title: "How To Fix A Bug - Building SaaS #56"
description: >-
    In this episode, we picked an issue from GitHub and worked on it.
    I explained the flow of using test driven development
    to show how the bug existed in an automated test.
    We wrote the test, then fixed the code.
    After that, we did some test refactoring to clean things up.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/ozNPXV9_TZU
aliases:
 - /building-saas/56
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - bugs

---

In this episode, we picked an issue from GitHub and worked on it.
I explained the flow of using test driven development
to show how the bug existed in an automated test.
We wrote the test, then fixed the code.
After that, we did some test refactoring to clean things up.

We looked at what the issue was
and how it is related
to the handling
of the `Course` model
in a weekly view
in the app.

I showed how the data model
for the `Course`
handles school days.
Then I wrote the unit test
that would show the failure
for the issue.

Once we had a valid unit test
in place,
I switched to writing code
for the Django view
to make the test pass.
Finally,
we checked the behavior
in the app
to confirm
that I fixed the issue.

With the issue fixed
and the test passing,
I refactored the test code
to make the tests easier
to understand
and work with
in the future.
