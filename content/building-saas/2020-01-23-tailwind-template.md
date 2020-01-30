---
title: "Use Tailwind On A Template - Building SaaS #43"
description: >-
    In this episode, we worked on the template styles of a tabular view.
    We also made some context data adjustments to include header rows
    and column highlighting.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/rXdYhEjYgzo
aliases:
 - /building-saas/43
categories:
 - Twitch
 - Python
 - Django
tags:
 - Django
 - Tailwind
 - templates

---

In this episode, we worked on the template styles of a tabular view.
We also made some context data adjustments to include header rows
and column highlighting.

I started by showing the template
that I already created.
It was rough.

Before changing anything,
I took the time to explain the modeling
in use for this project
and the context passed to the view.
The models mostly form a tree
in the a hierarchy.
Here is the top to bottom list
of the models in use:

```text
SchoolYear -> GradeLevel -> Course -> CourseTask -> Coursework
```

The view is showing a lot of data
in a tabular structure
so I walked through the logic
to put that together in the view.

After explaining the data,
I added week date headers to the table.
Then we used Tailwind to set some styling on them.

The next task was to make the table aware of week dates
to show column highlighting
of the current day.
We added the date to each cell
to make it possible to test if it should be highlighted.
I also made some style changes
to round off the corners of the columns.
This small detail actually required a suprising amount
of template adjustment.

At the end,
I discussed the next pieces
that will be going into the app.
