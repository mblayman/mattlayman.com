---
title: "Squashing Bugs - Building SaaS #87"
description: >-
    In this episode, I fixed some critical issues that my customer discovered.
    My customer is putting the app through its real paces for a school year
    and since this is the first run, there were bound to be some bugs.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/INVjPIuIjXo
aliases:
 - /building-saas/87
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - bugs
series: "Building SaaS"

---

In this episode, I fixed some critical issues that my customer discovered.
My customer is putting the app through its real paces for a school year
and since this is the first run, there were bound to be some bugs.

We began with an explanation of the issues
that my customer encountered.
The problems related to scheduling.

* First, the daily page skipped a task
    and showed the task
    that was meant for two days in the future.
    It appeared to be an off by one error.
* Second, the student's course view showed tasks sharing the same date
    when one task was completed
    and the other should have appeared
    on the next day.

Then I proceeded to drill into the code
until I could find the problem.
The error for the first issue was a miscalculation
of the index that was the offset to search
in the task table in the database.

The root of the problem was that the index calculation did not properly account
for completed tasks.
I wrote a new method on the `Student` model
that considered completed tasks as well,
then did some additional test to ensure that the solution generalized.
After fixing this issue,
I wrote test code to prove it worked.

Then we moved onto the second issue.
When I analyzed it,
I found that the `planned_date` calculation also failed
to account for completed tasks.
I wrote some new code to increment the date counter
when a student completed work for that day.
We fixed another test
that touched the code path
to maintain 100% code coverage.

To finish the stream,
I worked on a third bug
that I found
*as I was trying to create test data for the other two bugs*.
The onboarding flow created a course,
but the data was incorrect
and certain fields weren't set
that should have been.
Thankfully,
the change to correct the issue was a few additions
of hidden input fields.
