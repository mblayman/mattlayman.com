---
title: "Check Web App Security With Bandit - Building SaaS #74"
description: >-
    In this episode,
    I integrated the bandit static analysis tool
    to do automated security checking of my code before each commit.
    We talked about pre-commit and how to add in a new hook.
    After finishing that tool addition,
    we got deep into Django while removing some messages inserted
    by django-allauth on sign up.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/ruZerJltbA4
aliases:
 - /building-saas/74
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

In this episode,
I integrated the bandit static analysis tool
to do automated security checking of my code before each commit.
We talked about pre-commit and how to add in a new hook.
After finishing that tool addition,
we got deep into Django while removing some messages inserted
by django-allauth on sign up.

We began by talking about what the bandit tool does
and how it works.
Once I explained bandit,
I focused on the bandit documentation
to see how to add the tool.
We found the pre-commit config hook
in the bandit README docs.

I set bandit
in my `.pre-commit-config.yaml`.
Then we ran all the files through bandit
to check the code
with:

```bash
(venv) $ pre-commit run -a bandit
```

Bandit reported an error type
in my code
related to inclusion
of `assert` statements.
Since those `assert` statements are only found
in my test code,
I added a configuration file
so I could skip the false positive errors.

Thankfully,
that was the only issue
in my project
so we wrapped up
that tool addition
and moved onto a different topic.

After adding bandit,
I turned my attention back
to the onboarding process.
In my sign up flow,
the django-allauth packages added alert messages
when a user signs up
for the first time.
This was a poor experience
for the onboarding process
that I want to present
to my future users.

To make the change,
I needed to remove certain cookies
from the start page.
Ultimately,
I discovered
that the cookie must be removed
from the request and the response
of the view.

The real challenge
in this work
turned out to be the test
to prove that the change worked.
We spent a lot of time looking
at the Django source code,
the django-allauth code,
and the django-test-plus code.
It was quite an adventure!
