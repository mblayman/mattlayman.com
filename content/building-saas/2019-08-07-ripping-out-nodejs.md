---
title: "Ripping Out Node.js - Building SaaS #30"
description: >-
  In this episode,
  we removed Node.js from deployment.
  We had to finish off an issue with permissions first,
  but the deployment got simpler.
  Then we continued on the steps to make deployment do even less.
type: video
image: img/2019/nodejs.png
video: https://www.youtube.com/embed/PyZDK-D0eWE
aliases:
 - /building-saas/30
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Node.js
 - Ansible

---

In this episode,
we removed Node.js from deployment.
We had to finish off an issue with permissions first,
but the deployment got simpler.
Then we continued on the steps to make deployment do even less.

Last episode,
we got the static assets
to the staging environment,
but we ended the session
with a permissions problem.
The files extracted
from the tarball
had the wrong user and group permissions.

I fixed the permissions
by running an Ansible task
that ran `chown` to use the `www-data` user and group.
To make sure that the directories had proper permissions,
I used `755` to ensure they were executable.

Then we wrote another task
to set the permission of non-directory files to `644`.
This change removes the executable bit
from regular files
and reduces their security risk.

We ran some tests to confirm the behavior of all the files,
even running the test that destroyed all existing static files
and starting from scratch.

With the permissions task complete,
we could move onto the fun stuff
of ripping out code.
Since all the static files are now created
in Continuous Integration,
there is no need for {{< extlink "https://nodejs.org/en/" "Node.js" >}}
on the actual server.
We removed the {{< extlink "https://www.ansible.com/" "Ansible" >}} galaxy role
and any task that used Node.js
to run JavaScript.

Once Node was out of the way,
I moved on to other issues.
I had to convert tasks that used `manage.py`
from the Git clone
to use the manage command
that I bundled into the {{< extlink "https://shiv.readthedocs.io/en/latest/" "Shiv" >}} app.
That work turned out to be very minimal.

The next thing that can be removed is the Python virtual environment
that was generated on the server.
The virtual environment isn't needed
because all of the packages
are baked into the Shiv app.
That means that we must remove anything
that still depends on the virtual environment
and move them into the Shiv app.

There are two main tools that still depend
on the virtual environment:

1. {{< extlink "http://www.celeryproject.org/" "Celery" >}}
2. {{< extlink "https://github.com/wal-e/wal-e" "wal-e" >}}
    for {{< extlink "https://www.postgresql.org/" "Postgres" >}} backups

For the remainder of the stream,
I worked on the `main.py` file,
which is the entry point
for Shiv,
to make the file able to handle subcommands.
This will pave the way
for next time
when we call Celery
from a Python script
instead of its stand-alone executable.
