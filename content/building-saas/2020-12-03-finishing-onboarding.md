---
title: "Finishing Onboarding - Building SaaS #81"
description: >-
    In this episode, I completed the last form that completes the last step
    on my Django app's onboarding process.
    We built up the view, wrote the tests,
    and worked through the templates changes.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/FhTrNoW4n9s
aliases:
 - /building-saas/81
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - templates
series: "Building SaaS"

---

In this episode, I completed the last form that completes the last step
on my Django app's onboarding process.
We built up the view, wrote the tests,
and worked through the templates changes.

I started with a discussion
of what the onboarding flow does
and what was left.
I needed to make a form
that creates a task for a course.

For the first chunk of code,
we added some tests
to cover all the scenarios
that are important
for the view.
Once the tests had the right setup,
I wrote the view,
added the context,
and wired in the form
to make the view create a task.

With the view done,
I moved onto a new template.
The template displays the form
and shows some other messages
when different data is present.

That wrapped up the stream
and we discussed what I'm going
to work on next time
to polish the onboarding flow.
