---
title: "Switch A Django Project To Use Pytest - Building SaaS #57"
description: >-
    In this episode,
    I replaced the default Django test runner to use pytest.
    We walked through installation, configuration, how to change tests,
    and the benefits that come from using pytest.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/3UdD-nFXUlw
aliases:
 - /building-saas/57
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - pytest
 - testing

---

In this episode,
I replaced the default Django test runner to use pytest.
We walked through installation, configuration, how to change tests,
and the benefits that come from using pytest.

We started by looking at the current state
of the test suite
to provide a baseline
to compare against.
After that,
I went to PyPI
to find the version of `pytest-django`
that we wanted to install.
I added the package to my `requirements-dev.txt`
and installed the update.

```bash
$ pip install -r requirements-dev.txt
```

I created a `pytest.ini` file
and configured the package
by setting the `DJANGO_SETTINGS_MODULE`.
I initially typed the name of the setting incorrectly
(forgetting the second `S`)
so we debugged the failure case too.

Once pytest was running,
we observed that all the tests passed.
This behavior surprised me
because I thought that the test would need to be marked
to use a database.
We dug into the details
of the test execution
to see which Python fixtures were used.
We talked a bit
about how fixtures worked.

I finished the stream
by going through some tests
and switching the assertion styles.
We compared and contrasted assertions
from `unittest` style tests
versus pytest assertions.
