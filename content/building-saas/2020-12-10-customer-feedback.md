---
title: "Customer Feedback - Building SaaS #82"
description: >-
    In this episode, I worked on feedback from my primary customer.
    We fixed a couple of issues that she reported,
    then moved on to more of the onboarding flow.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/PAZq0rcKP7E
aliases:
 - /building-saas/82
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

In this episode, I worked on feedback from my primary customer.
We fixed a couple of issues that she reported,
then moved on to more of the onboarding flow.

Before getting to the code,
we chatted about ways
to learn to code.
I linked to a popular book,
Automate the Boring Stuff with Python,
and some good web tutorials
for learning Django.

The first bit of customer feedback
that I worked on
was to add a back link
from a course details
to get a user back
to the grade level
that holds the course.
I added the appropriate anchor tag
in the destination template.
We tested the URL manually
to confirm that a properly crafted link
would behave as we expect.
Then I switched
to the course detail page,
found the spot in the UI
that needed the new link,
and added the link back
to the anchor tag
that I added in the other template.

I took a break
to have a discussion
on a question
from the chat
about JavaScript versus Python.
I tried to compare the languages fairly,
even though I have an obvious bias.

After that break,
I moved to my next customer issue.
The customer wanted the ability
to print out one
of the page,
but the page wasn't designed
for printing
so the output looked terrible.
I went into the template
and added some CSS classes
to improve the print layout
of the page.

For my final change
for the stream,
we returned to the onboarding work.
I need to add some polish
to filling in pages
when there is no data
to guide users
on what to create and why.
I worked on my main page
and added some template work
for the scenario
when the user has no students.
I completed the template
to finish off the stream.
