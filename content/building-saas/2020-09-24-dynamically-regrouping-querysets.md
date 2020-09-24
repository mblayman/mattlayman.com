---
title: "Dynamically Regrouping QuerySets In Templates - Building SaaS #73"
description: >-
    In this episode, we worked on a new view to display course resources.
    While building out the template,
    I used some template tags to dynamically regroup a queryset
    into a more useful data format for rendering.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/8uwGj5z7qic
aliases:
 - /building-saas/73
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

In this episode, we worked on a new view to display course resources.
While building out the template,
I used some template tags to dynamically regroup a queryset
into a more useful data format for rendering.

I started a new view
before the stream
to display content,
but I had not filled it in
before the stream started.

We added new data
to the context,
and did some adjustments
to the URL based
on the required inputs for the view.

Once I had the data,
I quickly iterated
in the template
to see the parts
that I included.
I needed to display the course resources
in a different way
from how the queryset provided them
so I used the built-in `regroup` template tag
to organize the data differently.
`regroup` saved me
from doing a bunch of manipulation
in the view code.

To finish off the feature,
I added some automated tests
to cement the view
so I can be confident
in changing it in the future.
