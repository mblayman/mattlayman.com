---
title: "Onboarding Forms - Building SaaS #51"
description: >-
    In this episode,
    we added the first form to collect data in the onboarding flow.
    We used a CreateView and defined all the fields that are needed in the HTML form.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/K-BaV7At_So
aliases:
 - /building-saas/51
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - onboarding
 - forms

---

In this episode,
we added the first form to collect data in the onboarding flow.
We used a CreateView and defined all the fields that are needed in the HTML form.

I started by filling in the HTML form structure
of the page.
Once the dummy version was in place,
we changed from a `TemplateView`
to a `CreateView`
and began fixing each configuration error
that the new view type reported as missing
like missing a `model` field declaration.

With the form in a working state,
I created the next view in the sequence
and wired the success state
of the form
to a redirect to the next step.

At the end of the stream,
I talked about the polish that is needed
before the page is complete.
