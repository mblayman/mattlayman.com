---
title: "Onboarding Continuity - Building SaaS #50"
description: >-
    In this episode,
    we stepped from the welcome onboarding page
    to the first interactive page in the flow.
    I extracted the common banner for each of the templates
    and customized it for each of the steps in the process.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/Zmfb3dVVd5I
aliases:
 - /building-saas/50
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - onboarding
 - CSS

---

In this episode,
we stepped from the welcome onboarding page
to the first interactive page in the flow.
I extracted the common banner for each of the templates
and customized it for each of the steps in the process.

The first thing we did was create a button
on the starting page.
The button connects the welcome page
to the second step
in the flow
where the app will ask for information
about the user's school year.

With the button in place,
we created the new view to handle the school year form.
Before getting into that form,
I extracted the common onboarding banner
into a template fragment.

I cleaned up the banner
to change some of the styles
and make the banner configurable
so that each page can highlight the right segment
in the flow.

To end the stream,
we added the user interface elements
for the school year page
and will add the form in the next stream.
