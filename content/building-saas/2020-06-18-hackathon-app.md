---
title: "Hackathon App - Building SaaS #61"
description: >-
    In this episode, we took a break from the regular app
    to work on an app for a local hackathon that I'm participating in.
    My team is building a mobile web app for the homeless around Frederick, MD.
    In this stream, we cranked through some modeling, admin building,
    a couple of pages, tests, and templates! We got a lot done!
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/gHf2CJSM6g8
aliases:
 - /building-saas/61
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - hackathon

---

In this episode, we took a break from the regular app
to work on an app for a local hackathon that I'm participating in.
My team is building a mobile web app for the homeless around Frederick, MD.
In this stream, we cranked through some modeling, admin building,
a couple of pages, tests, and templates! We got a lot done!

The virtual hackathon running in Frederick
is split into multiple teams
serving three different community groups
around Frederick county.
My team is working on an mobile responsive web app
for SHIP,
the Student Homelessness Initiative Partnership.
After explaining the basics
of what the app should do,
we got started.

I made a new app called `announcements`
to provide a good home
for an `Announcement` model
that will be one of the big features
of the app.
I wrote tests for the model,
added a factory,
and created the admin interface.

Once the basics of the model were set,
I added `ordering` on the model
because the display of announcement should be ordered
by the expiration date.

We finished the model
and switched to building a page.
The first page needed was a page
to display a service category.
I used a `DetailView`,
connected it to the index page
via a hyperlink
in the template,
then proceeded to write the tests
to build out the view.
I also showed how to add additional context
to the view
to also display the services
related to the category.

The last thing we did was build another page
to show details
about a particular service.
This page was similar to the `ServiceCategory` page
so this view was quick to crank out.
