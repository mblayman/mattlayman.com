---
title: "Lessons From A Failed SaaS - Building SaaS #37"
description: >-
  In this episode,
  we talked about the things I learned from my SaaS project
  and some of the reasons why it failed to succeed financially.
  We dug into the technical and marketing challenges that I faced
  and what went wrong.
type: video
image: img/2019/failure.jpg
video: https://www.youtube.com/embed/mUyFEaAdYiM
aliases:
 - /building-saas/37
categories:
 - Twitch
 - Python
 - Django
tags:
 - SaaS
 - failure
 - retrospective

---

In this episode,
we talked about the things I learned from my SaaS project
and some of the reasons why it failed to succeed financially.
We dug into the technical and marketing challenges that I faced
and what went wrong.

I'm shutting down my side project,
College Conductor.
The SaaS never achieved a sustainable level
of success.
I started the site
to help my wife
with her college consulting business.
As you can see
from what follows,
the site didn't mange to deliver what she
(or anyone else)
really needed.

The format of this stream was different
from usual
in that we weren't looking
at code.
We did a retrospective.
Retrospectives are a fairly common practice
in the software industry.
They are a chance to reflect
on what you did
to analyze the good
or bad
of a project
to learn from it.
Most retrospectives occur
at the end of a release cycle
(often 2 week for an "Agile" team).

So, *what did I learn
from this SaaS product?*
A lot.

## Boring technology

We started the discussion covering my initial inspriration
and approach
with this article
on {{< extlink "https://mcfunley.com/choose-boring-technology" "choosing boring technology" >}}.
The article discusses picking safe technology
so you can focus
on the real core
of the product.
It also includes the idea
of innovation tokens.
These tokens are a fixed supply
of novel things that you can include
in your project
before you are overcome
by the risk
of the novel solution space.

I thought I spent an innovation token
on {{< extlink "https://emberjs.com/" "Ember" >}},
but what I failed to realize was all the extra stuff
that using Ember brought along.
My lack of knowledge slowed me down
when speed was paramount
to deliver value
on the product.

Because I over-architected my software design,
I spent way too much time developing features
that I could have produced faster
with a simpler approach.

## Rolling your own deployment

I also talked about the drag
from doing all the deployment myself.
Starting your own server
and maintaining it
can be fun,
but it's definitely a headwind
if you're trying to produce a product quickly.
Over time,
my deployment tool
of {{< extlink "https://www.ansible.com/" "Ansible" >}}
hindered me
because I had to focus on stupid little tasks
when I should have been focused on the product.

I also did a bunch
of new things
(and spent more innovation tokens)
on Let's Encrypt,
Postgres database backups,
server hardening,
and other tasks
that all distracted me
from delivering.
By the time I had these things configured,
I lost my wife's interest
in the product
and never recovered.

## Wrong focus

My biggest take-away from the whole experience
was that I focused
on the wrong things.
Technology sucked me
and I failed to create a Minimum Viable Product.

I learned a ton about development
with the project
that will help me in the future,
but College Conductor is never going to be a true success story.

## The future

In the next stream,
we're going to start a brand new project!
I'll outline the goals
for the project
and describe what I'm going to differently
to give a better chance
of success.
