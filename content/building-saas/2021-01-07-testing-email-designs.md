---
title: "Testing Email Designs - Building SaaS #86"
description: >-
    In this episode, I worked on the sign up confirmation email design.
    We customized the template and used MailHog to test the flow
    and see how the email appeared. After working on the email design,
    we switched to the landing page of the site to work on the pricing information.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/m8JLQd4CSQQ
aliases:
 - /building-saas/86
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - email
series: "Building SaaS"

---

In this episode, I worked on the sign up confirmation email design.
We customized the template and used MailHog to test the flow
and see how the email appeared. After working on the email design,
we switched to the landing page of the site to work on the pricing information.

I started the stream by explaining
that I'm working through some final tasks
before launching the app more publicly.
I covered why I am planning to send a sign up email
and why I want to customize it.

While building the email,
I made a mistake in the file naming
and had to dig through the django-allauth source code
to try to figure out what went wrong.
Sometimes exploring source code
of other projects is what you need to do.

Once I corrected the mistake,
I showed how to use MailHog
to act as a local email receiver
with a web-based viewer.
By using MailHog,
we checked the styling
of the email to make sure it matched my expectations.

Before moving on,
I made sure to build the plain text version
of the email
as well as the HTML version.

After finishing the email,
I switched over to the landing page
and turned my attention to the pricing section.
I spent the rest of the stream trying to style the pricing section
to my liking.
