---
title: "Empty States - Building SaaS #83"
description: >-
    In this episode, I returned to the onboarding flow and start to polish some
    of the extra pages. We filled the pages with special copy
    and a call to action to each page to help customers be successful.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/_k3ayh6J_hc
aliases:
 - /building-saas/83
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

In this episode, I returned to the onboarding flow and start to polish some
of the extra pages. We filled the pages with special copy
and a call to action to each page to help customers be successful.

I started with the pages that displays the school years.
We added a chunk of template from the onboarding process
that asks the user to create a school year.
I modified the template chunk
to make it fit in the context
of the page.

Next,
I moved onto the index page
that lists all the students
in a user's account.
I took another chunk
from my main app view,
refactored it
into a partial template
and then used it
in two places.
I did some testing to make sure that the old view continued to work.

After completing that empty state,
I tackled another logical state
when the user wants to view their weekly schedule,
but they have no enrolled students.
This is another state that can't show the full schedule,
so I added more help
and another call to action
to help users along
in the process.

To finish off the stream,
I tried to add pytest-xdist
to make the test suite run in parallel
and run faster.
I found that the extra process overhead negated the speed boost
for my small test suite.
