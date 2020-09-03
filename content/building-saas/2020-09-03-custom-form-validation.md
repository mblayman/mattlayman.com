---
title: "Custom Form Validation - Building SaaS #71"
description: >-
    In this episode,
    I added some custom checking to ensure that students may only be enrolled
    in a single grade level for a school year.
    We talked about form cleaning and wrote a for unit test to prove
    that the change worked.
    After that change, we switched to a template and wrote copy
    for when no progress reports are viewable for users.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/fPFEh5MDMIY
aliases:
 - /building-saas/71
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

In this episode,
I added some custom checking to ensure that students may only be enrolled
in a single grade level for a school year.
We talked about form cleaning and wrote a for unit test to prove
that the change worked.
After that change, we switched to a template and wrote copy
for when no progress reports are viewable for users.

With the first issue,
I needed to update a form
that enrolls students.
I wanted to ensure
that students can't be enrolled
in more than one grade level
in a single school year.
I updated the `clean` method
of the `EnrollmentForm`
to check that no other enrollments
exist for the school year.

We added a new test case
and created a test
to check that the form change was correct.

With that change done,
we moved onto template work.
The reports index page has nothing valuable
to show
until certain data exists
in the system.
To provide something visual
when that data doesn't exist,
we added an empty page
so that new users
won't see a blank page.
