---
title: "A Week At A Time - Building SaaS #46"
description: >-
    In this episode, we worked on a weekly view for the Django app.
    We made navigation that would let users click from one week to the next,
    then fixed up the view to pull time from that particular week.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/DMe7CeAxWwc
aliases:
 - /building-saas/46
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - views

---

In this episode, we worked on a weekly view for the Django app.
We made navigation that would let users click from one week to the next,
then fixed up the view to pull time from that particular week.

The first thing that I did was focus
on the UI required
to navigate to a new weekly view
in the app.
We mocked out the UI
and talked briefly
about the flexbox layout
that is available
to modern browsers.

From the UI mock up,
I changed the view code
to include a `previous_week_date` and `next_week_date`
in the view context
so we could change the links
to show real dates.

From there,
we needed a destination URL.
I create a new `path`
in the URLconf
that connected the weekly URL
to the existing app view
that shows the week data.

After wiring things together,
I was able to extract the week date
from the URL
and make the view pull from the specified day
and show that in the UI.

Finally,
we chatted about the tricky offset calculation
that needs to happen to pull the right course tasks,
but I ended the stream
at that stage
because the logic changes
for that problem are tedious
and very specific
to my particular app.
