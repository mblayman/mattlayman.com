---
title: "Bread and Butter Django - Building SaaS #58"
description: >-
    In this episode, I worked on a views and templates.
    There are a number of core pages that are required
    to flesh out the minimal interface for the app. We're building them.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/SVrJayVduiM
aliases:
 - /building-saas/58
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - templates

---

In this episode, I worked on a views and templates.
There are a number of core pages that are required
to flesh out the minimal interface for the app. We're building them.

I began by showing the page
that we were going to work on.
I outlined the changes I planned to make,
then we started.

The first thing we added was data
about the school year,
the main model on display
in the page.
I showed how to mock
in the elements
before adding real data.

Once the data was mocked in,
I wrote some model methods
on `SchoolYear` to get the data
that I needed to display.
I created a `display_days` method
that will show the days
that the school year runs on.

After I had the new method,
we plugged it in
and continued to expand the remainder
of the template.
I used the Django `date` template tag
to format some dates.

Then we added buttons for the action elements
that the page will have.

To finish the stream,
we set the grid layout
of where the courses will display
for each grade level.
