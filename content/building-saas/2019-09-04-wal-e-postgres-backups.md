---
title: "wal-e Postgres Backups - Building SaaS #32"
description: >-
  In this episode,
  we worked on Postgres database backups and modified the backup tool, wal-e,
  to use the Shiv app format.
type: video
image: img/2017/postgresql.png
video: https://www.youtube.com/embed/bValji0iK6s
aliases:
 - /building-saas/32
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Postgres
 - wal-e

---

In this episode,
we worked on Postgres database backups and modified the backup tool, wal-e,
to use the Shiv app format.

{{< extlink "https://github.com/wal-e/wal-e" "wal-e" >}} is Postgres database backup tool
that works by managing the Write-Ahead Log (WAL)
that a Postgres database produces.
The WAL is the log of recent changes that happened
in the database.
If you have access to a full WAL,
then you can conceivably reproduce a Postgres database's data.

When I switched the deployment to use a Shiv app,
we now have to remove every use of the existing virtual environment
in the system.
The `wal-e` executable is installed in the `bin` directory
of the virtual environment
so we need another way to access it.

The way that the Shiv app can execute other binaries is
with the `{{< extlink "https://shiv.readthedocs.io/en/latest/#shiv-entry-point" "SHIV_ENTRY_POINT" >}}` environment variable.
Using the setuptools-style link
of `wal_e.cmd:main`,
we can run the wal-e executable
that is available to the Shiv app.
Because I already use the `envdir` command,
we only had to make two changes:

1. Replace `{{ venv_path }}/bin/wal-e`
    with `/srv/apps/conductor.pyz`.
2. Add a `SHIV_ENTRY_POINT` file
    to `/etc/wal-e/env` with the appropriate setuptools-style value.

Once we made the changes,
I deployed things
to the staging site
with Ansible.
From there,
we verified
that the cron entry was changes with:

```bash
$ sudo su -  # change to root
$ su - postgres  # change to postgres account
$ crontab -l  # list cron entries
```

With the wal-e updates in place,
nothing used the Python virtual environment
so we could finally delete it!

In the next stream,
we're going to begin the process
of removing the Git clone
to complete the process of simplifying deployment.
