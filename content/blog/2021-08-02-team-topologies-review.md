---
title: "Team Topologies: a review"
description: >-
    Does your team's organizational structure make sense
    for your company?
    Team Topologies provides a way
    to think about building teams.
    This review blends my own experience
    with the views laid out
    by the authors.
image: img/2021/team-topologies.jpg
type: post
categories:
 - Book reviews
tags:
 - teams
 - organization

---

As a recommendation
from a coworker,
I picked up
{{< extlink "https://www.amazon.com/gp/product/B07NSF94PC/ref=as_li_tl?ie=UTF8&tag=mblayman-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B07NSF94PC&linkId=453263acc174ec93121660b9d52e5b75" "Team Topologies" >}}
by Matthew Skelton
and Manuel Pais.
The topic of team organization is on my mind
because my employer, Doctor On Demand, recently merged
with Grand Rounds Health.
Our engineering teams are coming together,
and the process is bringing about a lot of questions
for merging gracefully.

I'll share some highlights
of what I think about this book.

<div class="w-full py-4">
  <a href="https://www.amazon.com/gp/product/B07NSF94PC/ref=as_li_tl?ie=UTF8&tag=mblayman-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B07NSF94PC&linkId=453263acc174ec93121660b9d52e5b75" target="_blank"><img class="mx-auto" src="/img/2021/team-topologies-full.jpg"></a>
</div>

The core idea with Team Topologies circles around Conway's Law.
Conway's Law says:

> Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's communication structure.
>
> Melvin E. Conway [^1]

[^1]: https://en.wikipedia.org/wiki/Conway%27s_law

The authors of Team Topologies suggest
that we flip this law
on its head.
If we can make teams
that map to the structure
that we *want* our software system
to be like,
then we'll succeed
when Conway's Law kicks in.

Everything else in the book seems to revolve around this central thesis.
All the advice derives
from trying to make your teams look like the system
that you want.

To realize this team design,
the book suggests
that organizations create "stream aligned teams."
These stream aligned teams should be able
to produce a single stream of value.
In simplified language
(Layman's terms?),
a team should be able to produce work
from start to finish.

In my analysis
of this idea,
I wrestled with a few things.

Let's say you're a healthcare company
that's trying to deliver better care
via machine learning
of patient data
to produce an outcome
that can be shown
to patients
in native mobile app and web apps.
To succeed on that vision,
what kind of team would you need?

Here's one possiblity:

* Data scientists for machine learning
* Android developers
* iOS developers
* JavaScript frontend developers
* Backend API developers
* DevOps/Infrastructure developers

That kind of team may be able to produce the desired outcome,
but what is the system design
that will fall out of such a grouping?
Also, if you assume that you'll need more than one
of each of those categories
on the same team,
then you may be looking at 12 engineers
on the team at minimum.

To alleviate these concerns,
the authors describe a cast of supporting teams
that bolster stream aligned teams.
These teams include platform teams
that provide base services,
enabling teams
that are cross cutting
from stream aligned teams
to bring extra support,
and complicated sub-system teams
that address portions
of a system
that require specific domain knowledge.
This is where I start
to get even more concerned
with what is presented.

*Who is the audience?
How big does an organization have to be before these ideas kick in?*
When these other teams appear to be nearly required
for a stream aligned team
to succeed,
something is starting to smell funny.
This advice sounds more and more like it is for larger organizations.
Given that the authors are both consultants,
maybe that's exactly who this book is for.

Aside from the sheer volume of engineers required
to make the proposed organizational structure work,
I believe there are other factors
that might make this approach to team design harder.

Namely:

> **Software is not as malleable as we think it is.**
> It exists in a historic context
> that can apply backpressure
> to our organizational machinations.

In my recollection
of some of the examples presented,
it took companies *years* to transform
into the desired output.
My guess is that this is because real change is hard.
Software that is working for customers might be hard to change,
regardless of how much we shuffle the engineers around
in an org structure.

I don't think this means we are doomed
to whatever (potentially crappy) system architecture
was created during the early life
of a company.
My belief is that there is hope
in team design
by searching for interfaces.
Software systems are complex.
With our observational skills,
we can seek the seams
between different domains
within the system.

Finding these system seams can help wrangle a complex system
into its constituent domain pieces.
From the identification
of domains,
we can cluster engineers
on either side of an interface.
By doing so,
we form teams that can operate
with a narrowed focus
on a paricular domain.

If our goal as engineers
in a company
is to produce something valuable
for our customers,
then I think our team design will be most effective
by adapting our system interfaces
and allowing new teams
to form as a reaction
to that adaptation.

To me,
this idea flows
from one of the tenets
of the Agile manifesto:

> **Responding to change** over following a plan

Organizational change may stem from:

1. Changing business needs
    that necessitate making new teams
    that will influence the system design.
2. Changing software interfaces
    that naturally nudge engineers
    into different communication paths.

My point is that I think there is more to system design
than setting the shape of teams
to create a desired side effect
on system structure.

Do my concerns mean that Team Topologies is a bad book?
No, I don't think so.

For a certain organizational size,
there are valuable patterns described in the book.
For instance,
a platform team (i.e., a team with well defined *interfaces*
into the lower level infrastructure)
is a fantastic type of team to have.

Also,
I don't recall the authors stating
that you can't or shouldn't define stream aligned teams
based on a reaction
to a recognized domain
that emerges
from the system.
It would be unfair of me to ascribe to them something
that they didn't write.
There is some interesting material in the book,
but make sure you're thinking broadly
and not getting sucked
into the template set forth.

These are my thoughts
on Team Topologies.
If you want to pick up a copy,
you can find the book
{{< extlink "https://www.amazon.com/gp/product/B07NSF94PC/ref=as_li_tl?ie=UTF8&tag=mblayman-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B07NSF94PC&linkId=453263acc174ec93121660b9d52e5b75" "on Amazon" >}}.
