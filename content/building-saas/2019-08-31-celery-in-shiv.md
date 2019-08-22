---
title: "Celery In A Shiv App - Building SaaS #31"
description: >-
  In this episode,
  we baked the Celery worker and beat scheduler tool into the Shiv app.
  This is one more step on the path to simplifying the set of tools
  on the production server.
type: video
image: img/2019/celery.png
video: https://www.youtube.com/embed/Gt-x9necwI4
aliases:
 - /building-saas/31
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Celery
 - Shiv

---

In this episode,
we baked the Celery worker and beat scheduler tool into the Shiv app.
This is one more step on the path to simplifying the set of tools
on the production server.

I started the stream
by reviewing the refactoring
that I did to `conductor/main.py`.
The main file is used to dispatch
to different tools
with the Shiv bundle.

The refactored version can pass control
to Gunicorn,
the Django management tools,
or Celery.

To make Celery work,
we hooked `{{< extlink "https://celery.readthedocs.io/en/latest/reference/celery.html#celery.Celery.worker_main" "worker_main" >}}`
to the Celery dispatch function.

Once `worker_main` was set,
I generated a new local Shiv app
to test things out.
Since testing could require building the app multiple times,
we took a detour to make the `package.sh` easier to use locally.

Before we started,
the packaging script only worked
in Continuous Integration.
I modified some paths to look somewhere only when CI runs.
Remembering how to do Bash `if` statements is surprisingly difficult
for me.

```bash
if [ -n "${CI}" ]; then
    VENV=venv/bin/
fi
```

To create a new version of the package to test,
we ran:

```bash
$ rm -f conductor-abcd.pyz && CIRCLE_SHA1=abcd package.sh
```

By chaining the commands together,
it's very fast to fetch that command from history
and run all the steps in a single line.

With our testable package available,
we started Celery
with a variety of options.
When I finished,
we settled on an invocation
that looked like:

```bash
$ /srv/apps/conductor.pyz celery \
    --loglevel INFO \
    --concurrency 2 \
    --beat \
    --schedule /tmp/celerybeat-schedule \
    --pidfile /tmp/celerybeat.pid
```

This set of options lets us run a Celery worker
along with the beat scheduler tool.

To finish the GitHub issue,
we deployed this to staging
and checked on the processes.
We looked at the Celery processes with:

```bash
$ ps -ef | grep celery
```

From that output,
I explained how process identifiers (PIDs)
and parent process identifiers (PPIDs) work,
and I covered how Celery creates multiple processes
to increase concurrency.

Next time,
we need to do a similar process
with the Python-based Postgres backup tool, wal-e.
We'll call wal-e from the Shiv app
to eliminate the last usage of the installed virtual environment.
