---
title: "User Testing Feedback - Building SaaS #54"
description: >-
    In this episode, we worked on issues found from a round of user testing.
    I talked about how I did user testing with my customer,
    then started to tackle the usability issues that she identified.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/hM2qLCGwAIA
aliases:
 - /building-saas/54
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - user testing

---

In this episode, we worked on issues found from a round of user testing.
I talked about how I did user testing with my customer,
then started to tackle the usability issues that she identified.

We're taking a break
from building the onboarding flow
so that we can take some time
to address feedback
from user testing
with my customer.

I started the stream
by explaining how I set up user testing
and what I got out of the experience.
We talked through the issues
and looked at how they range
in size and complexity.

To get some early wins,
we started
by working on the easiest issues.
I completed four issues
in the stream.

The first issue changed a single template
to alter the sub-navigation
of the interface.
I removed some customization
on the navigation element
and replace the text.

After that short change,
we debugged an issue with a print style.
We talked about print styling
and how to include CSS changes only
when printed
by using the `media="print"` attribute
to the link tab.
After I found the source
of the issue,
I updated the print CSS file and tweaked the template
to fix it.

For the third issue,
I added a new view
with some unit tests
to include a button
to let users get to the page
that lets them enter any missing task grades.

Finally,
we made a broad change on the site
to set the position
of all confirmation buttons
from the left
to the right.
My customer said this was what she naturally expected,
so I styled everything appropriately.
I was grateful
to make this change early
in the project
because it would be quite painful in the future
if there were tons of forms to modify.

On the next stream,
we'll get into more
of the user testing feedback.
