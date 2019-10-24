---
title: "Deploying WhiteNoise - Building SaaS #35"
description: >-
  In this episode, we updated Continuous Integration, Nginx,
  and the Ansible deployment tasks to use WhiteNoise.
  With all the changes in place,
  we tested things out to verify that WhiteNoise served up the CSS, JS, and image files.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/fHTJYlpxjvo
aliases:
 - /building-saas/35
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - WhiteNoise

---

In this episode, we updated Continuous Integration, Nginx,
and the Ansible deployment tasks to use WhiteNoise.
With all the changes in place,
we tested things out to verify that WhiteNoise served up the CSS, JS, and image files.

We started with Circle CI.
First, I fixed the JS assets cache
because the cache key never changed
and Circle did not save fresh assets each build.

After completing the assets cache,
I created a new cache that stored all the static files
after running `collectstatic`.
This new cache was necessary
for the package step.

Since we were condensing two build artifacts
(one for the static files
and one for the Python code)
into one,
the package script needed all the static files
at packaging time.
Because Circle splits everything between jobs,
this meant that we had to cache all the static files.

Once we fixed up Circle CI
and pushed up the changes,
we ran an Ansible deploy
to the staging site.

From some inspection
of the Circle CI build
and the Shiv app
on the staging server,
I confirmed that the Circle CI changes did what we wanted.

The next major step
in the process
was Nginx configuration changes.
In this new model,
the Django application will serve the static assets.
That means that Nginx should stop serving those files.
This change was a quick removal
in the Nginx configuration file
of this section:

```nginx
    location /static/ {
        alias /var/www/conductor/;
        expires max;
        add_header Cache-Control public;
    }
```

By removing this `location` block,
Nginx passes all `/static/` requests
to the Django application.
We did another deploy
and confirmed
that the Django application served the assets.
Ultimately,
I confirmed this
by observing that static files used Brotli compression.
This was one of the new features
that WhiteNoise brought
to the table.

The remainder of the stream was a cleanup
of Circle CI and Ansible.
I realized that the Circle CI pipeline had an extra job
that we didn't need.
We removed the extra job,
then turned our attention to Ansible.

I removed Ansible tasks
that touched anything related to separate static directories.
This cleaned out `static_root` and `static_url`
in Ansible
so that only Django has to care about those things.

On the next stream,
we're going to dig into a new tool
to manage settings
and split settings and configuration apart cleanly.
