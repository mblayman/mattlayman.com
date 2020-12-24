---
title: "Refactoring Enrollment - Building SaaS #84"
description: >-
    In this episode, I decided to redesign a portion of the application flow.
    I wasn't pleased with how users would enroll students for their grades
    so I refactored the school year page into a flow that worked better.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/Ix0af3r8Uls
aliases:
 - /building-saas/84
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - logic
series: "Building SaaS"

---

In this episode, I decided to redesign a portion of the application flow.
I wasn't pleased with how users would enroll students for their grades
so I refactored the school year page into a flow that worked better.

Note:
My internet connection was not good
during this stream.
Thankfully,
the audio is fine
and reading code is very possible
because the background doesn't need to change much.
My apologies for the low quality.

I started by deleting an "Enroll Student" button
on the school year detail page.
This involved removing some view context data
and associated tests as well.

After I deleted the old method,
I added some new context that added a boolean
of `has_students` to the grades
that display on the school year page.
I used this context
to control whether to show a call to action
to let user's enroll for a grade level.
