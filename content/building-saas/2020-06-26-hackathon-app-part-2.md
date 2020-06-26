---
title: "Hackathon App Part 2 - Building SaaS #62"
description: >-
    In this episode, we took a break from the regular app to work on an app
    for a local hackathon that I'm participating in.
    This is the second week for the hackathon and in this stream,
    I apply the final touches to the application.
    We work on models, a template,
    and build an RSS feed using Django syndication contrib app.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/zVERQ1aCbvs
aliases:
 - /building-saas/62
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - hackathon

---

In this episode, we took a break from the regular app to work on an app
for a local hackathon that I'm participating in.
This is the second week for the hackathon and in this stream,
I apply the final touches to the application.
We work on models, a template,
and build an RSS feed using Django syndication contrib app.

The final presentation for the app was the next day
so it was crunch time to finish everything off.
After showing off what was done so far,
I tried to show the new page
and we were met with an exception.
The code was in a half finished state
before I started the stream
because the `Service` model was changed
without an associated migration.

We added a test for the model change
and generated the migration.
After completing the model change,
I talked about working with databases
in Heroku
and why SQLite won't work there.

After finishing the modeling work,
I integrated the remaining design
from my team's designer
and plugged it into the live template.
We had a to polish a couple of edges
on the design to make it fit well
with the rest of the site.

Once the design was finished up,
I showed how to mobile testing with `ngrok`.
We tested the app out on my mobile phone
to ensure everything worked
and looked good.

I explained how to add a sprinkle
of JavaScript
without pulling in `npm`
and a big JavaScript toolchain.

With the UI out of the way,
I needed to work one piece
of non-UI functionality.
The app is going
to have a mailing list
for users to receive announcements.
The announcements also exist
on the site.
To help the administrator avoid creating an announcement
in two places,
we used Django's `syndication` app
to create an RSS feed.
The mailing list service, Mailchimp,
will read from the RSS feed
to send out announcements automatically
from whatever is set in the feed.

I finished the feed
and wrote tests for it.
That completed all the functionality
of the app.
To finish the stream,
I deployed the final version
of the app to Heroku!
