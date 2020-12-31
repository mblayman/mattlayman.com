---
title: "Customer Docs - Building SaaS #85"
description: >-
    In this episode, I integrated customer documentation into the app.
    I showed how to build Sphinx documentation into a Django project,
    then created a help view to link to the docs.
    Finally, I added documentation building to the deployment process.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/H4OakvF-UTY
aliases:
 - /building-saas/85
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - documentation
series: "Building SaaS"

---

In this episode, I integrated customer documentation into the app.
I showed how to build Sphinx documentation into a Django project,
then created a help view to link to the docs.
Finally, I added documentation building to the deployment process.

I previously created a Sphinx documentation project
to hold docs
for my app,
but I had not hooked the docs
into my project yet.
Before hooking it in,
I explained how Sphinx works
and how I customized the documentation
to fit with my project.

I started by integrating documentation building
into my Continuous Integration tools.
This will check to make sure that my docs continue
to build
so that I'll know that things are safe to deploy.

After adding to CI,
I plugged the generated documentation
into the Django app
so that WhiteNoise could show the files.
I did this by using my custom version
of the WhiteNoise middleware
that can add any extra static files
that I want.

Once the docs could be served
by the app,
I changed the footer to point
to the documentation.
After playing with that,
I realized that I want a help page
before directing users straight to the documentation.

I created a new view
to describe how users can get help.
In this view,
I included a support email address.
We wrote some tests to make sure it all worked.

To finish off the effort,
I added documentation building
to the deployment process
so that Heroku will also have the generated documentation.
We also added a step
to make sure
that Heroku will have compressed versions
of the documentation
that WhiteNoise can serve
like gzip or brotli versions.

At the end of the stream,
I talked about some
of the projects
that I'm going to tackle
for next year.
