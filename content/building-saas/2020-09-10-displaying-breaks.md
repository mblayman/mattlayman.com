---
title: "Displaying Breaks - Building SaaS #72"
description: >-
    In this episode, I worked to add breaks to the display of the week schedule.
    We had to update context to include the break information into the schedules.
    I refactored a method out of the calendar display code
    to make some reusable logic for handling breaks.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/EEQFXjovTt4
aliases:
 - /building-saas/72
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

In this episode, I worked to add breaks to the display of the week schedule.
We had to update context to include the break information into the schedules.
I refactored a method out of the calendar display code
to make some reusable logic for handling breaks.

The app needs to display breaks
on the schedule
and adjust what is displayed
based on when the breaks are.
I started
with changing the background color
of the break days.
The break days were added
to the context
of the view.
Once in the context,
I adjusted the colors
to show the breaks.

The next change was to change the styling
of the background color
to round the edges
of each break day.
Because breaks can be variable
in length,
I needed to add special logic
to consider the different states
that a day can be in.
