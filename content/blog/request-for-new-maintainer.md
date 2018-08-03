---
title: RFNM - Request For New Maintainer
date: 2018-05-15
summary: >-
  What do you do
  when you know
  that you are no longer a good maintainer
  for a open source software project?
  You can step away gracefully
  by requesting help
  from the community.
  This post will discuss one way to request that help.
image: img/2018/rfnm.jpg
type: post

---

The Pull Requests piled up.
Each new PR added to the weight reminding me
that I was not being a responsive maintainer.
I felt **guilty**.

> **Guilt**: A feeling held by many open source maintainers
> who can't (or don't want to) continue
> on a project
> that they manage.

Feeling guilty about contributing to open source is terrible.
You feel like you're letting people down
or like you owe them something more.
I think I did something good for the open source community
so *why do I feel this way?*
***How could I fix this?***
Let's see how I got here to begin with.

Some years ago,
I started an ambituous side project
called [College Conductor](https://www.collegeconductor.com/).
The project uses [Django](https://www.djangoproject.com/)
and [Ember](https://emberjs.com/).

While building out my project,
I used a Python package
([this one](http://django-rest-framework-json-api.readthedocs.io/en/stable/))
and found a bug.
Since I care about open source,
I filed an issue on GitHub
and documented the details
of the problem I found.
Time passed
and the bug remained open
so I tried to do some work to shepherd the issue to release.

Fast forward past the details
and I found that ***I*** was the person doing new releases
for the project.

My role was declared publically
and simply:
I agreed to manage PR reviews
from community contributed PRs
and periodically do releases.
I was a project **steward**.

As a maintainer, I had a fairly typical experience:

* New features went out.
  The project stayed up-to-date
  with the ecosystem.
  I felt good about my contributions
  with each release.
* Issues had conflicting opinions.
  Discussions got heated.
  Communication broke down.
  Apologies happened.

Although I wasn't a perfect steward,
I thought I did a fine job making sure the project stayed alive.

Then things in my life started to change.
Other interests and obligations pulled me away
from College Conductor.
Also, I concluded
that my technology stack was not a good fit
for what College Conductor needed.

> I no longer used the Python project
that I helped to maintain.

That's when my response time on Pull Requests slowed.
The queue of PRs, which was once cleared out, filled again.

When enough PR weight was on me,
I finally stopped to ask the question I started with
at the beginning
of this post:
*How can I fix this?*

The way I solved my troubles was by *treating my maintainership
as a bug.*
The most natural thing I could do
for a GitHub project
was file an issue.
I titled the issue **Request for new maintainer**
and attached a **help wanted** label.

The issue details included:

* My reason for wanting to step down.
* The obligations of the role
  for any new maintainer.
* An offer to aid any new maintainers
  with whatever help or training was needed.

To my surprise,
**two** people stepped up
*within a day*
and offered to move into a maintainer role!
They are users of the project
and want to see it continue.

For me,
that's largely the end of my journey.
I'm still chiming in
as we work through the details
of the transition,
but I'm no longer regularly active
with the project.

Maybe some of you are maintainers
and worried about the other possible outcome
if you tried this
on your project:
**what if no one steps up?**

If you're running a Python project,
consider [JazzBand](https://jazzband.co/).
JazzBand is focused
on collective ownership
of established projects
that need light maintenance
and can be managed
by a **group**
of maintainers.
Such a group might be a great fit
for your project.
If you're outside
of the Python ecosystem,
there might be a group
like JazzBand
in your community.

Others of you might have a strong attachment
to your project
and are wrestling
with ceding control
to other people.
Maybe you're afraid of the project moving
in a direction you don't agree with.
For you,
I'm afraid I don't have a great answer.
I would suggest weighing the emotional cost
like guilt and anxiety
against the value of keeping project control.

Being a maintainer can be really rewarding,
but I think it's important to remember
that it doesn't have to be forever.
Any struggling maintainers should consider being honest and open
with their community
and **ask for help**
if they need it.
Maybe a RFNM issue is exactly the thing you need
to breathe new life
into your project
by passing maintainership
to someone who is in a better position
to take care of it.

Finally,
it would be terrible of me
to finish this post
without saying thanks.
So,
thanks to
[n2ygk](https://github.com/n2ygk)
and [sliverc](https://github.com/sliverc)
for their willingness
to take over Django REST Framework JSON API
as maintainers.
I'm extremely grateful.
