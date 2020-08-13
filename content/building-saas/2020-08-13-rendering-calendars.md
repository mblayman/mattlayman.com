---
title: "Rendering Calendars - Building SaaS #68"
description: >-
    In this episode,
    I worked on rendering a calendar of important events in a school year.
    We built out the appropriate data structures,
    and I wrote some new model methods and added tests.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/m5DzshHHX_w
aliases:
 - /building-saas/68
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
I worked on rendering a calendar of important events in a school year.
We built out the appropriate data structures,
and I wrote some new model methods and added tests.

On the last stream,
I created a new model to track breaks
in the school year.
The app now shows the calendar
for the school year,
and I want to display the breaks
on the calendar.

Before digging too far
into the code,
I provided my thoughts
about using Docker for development
from a question
that came from the chat.

I created some breaks so that we could see the data
on the calendar.
Then we made some changes
to the calendar builder
to include the break days.
To do that,
I needed a new model method
to query the school year
for any breaks that happen
on a particular date.
We added unit tests to the new method.

Once the date was available,
I adjusted the templates
to display the school breaks
and style them in a nice manner.
