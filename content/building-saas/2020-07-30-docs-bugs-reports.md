---
title: "Docs, Bugs, and Reports - Building SaaS #66"
description: >-
    In this episode, I created documentation for anyone interested
    in trying out the application.
    After documenting the setup, I moved on to fixing a bug
    with the scheduling display of courses.
    In the latter half of the stream,
    we focused on creating a new reports section to show progress reports
    for students.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/nGNXL2s_784
aliases:
 - /building-saas/66
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - views
series: "Building SaaS"

---

In this episode, I created documentation for anyone interested
in trying out the application.
After documenting the setup, I moved on to fixing a bug
with the scheduling display of courses.
In the latter half of the stream,
we focused on creating a new reports section to show progress reports
for students.

One of my patrons requested some documentation
to explain how to get started
with the project.
We updated the `README.md`
to show the commands
that I use
to set up my project.
This includes virtual environment setup,
package installation,
Django bootstraping commands,
and how to run the web server.

After completing some documentation,
we worked on a bug
that my customer discovered
during the last round of feedback
that I collected from her.
The problem was very specific
to how courses would be displayed
in the past.
The customer wants to be able to hide courses
that are complete,
but still show past completed data.
The existing implementation didn't show the past.
I wrote the unit test
and made the code change to fix the issue.

Finally,
we started some new pages.
The customer wants to see progress reports
for students.
I needed a new section
that will display all the available reports
in the future.
I built a new `ReportsIndexView`
that will be the new section
for showing reports.
We added the template view
and started to put in context data.
