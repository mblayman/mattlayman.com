---
title: "Sending Invites - Building SaaS #77"
description: >-
    In this episode, I worked on the form that will send invites to users
    for the new social network app that I'm building.
    We built the view, the form, and the tests and wired a button to the new view.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/wO2Dy7rKvXY
aliases:
 - /building-saas/77
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - forms
series: "Building SaaS"

---

In this episode, I worked on the form that will send invites to users
for the new social network app that I'm building.
We built the view, the form, and the tests and wired a button to the new view.

The first thing that we do was talk through the new changes
since the last stream.
After discussing the progress,
I took some time
to cover the expected budget
for the application
to get it to an MVP.

Once we covered the budget,
I talked about different strategies
for sending invite emails
and the tradeoffs between sending email
in a request and response cycle
versus using background workers.

After talking through those choices,
I mentioned which path we were going down
and I started writing a new Django view.
We wrote the tests to make the minimum view work.

With the view in place,
I added a new form that the invite view would use.
I wrote more tests
to ensure the form did the proper checking.
