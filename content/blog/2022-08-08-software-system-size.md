---
title: "Huge Software Systems"
description: >-
    How can you work
    with a huge software system?
    Wrangling a large software systems carries significant challenges.
    This article looks at some
    of the areas to consider.
image: img/2022/brain.jpg
type: post
categories:
 - Software
tags:
 - brain dump
 - systems

---

My employer is a mid-sized company
with a fair number
of engineers.
We have a big software system
with a service oriented architecture
and *hundreds* of code repositories.

The system has multiple monoliths,
multiple monorepos,
standalone service repositories,
internal libraries,
data science repositories,
and many other kinds
of software.
*How do you manage a system like that?*

This is one of the interesting problems
that I am faced with daily
in my role.
With this much code,
it's challenging to answer seemingly simple questions like:

* Which team owns this repo?
* Where is the documentation for this?
* What is the health of this service?
* What services depend on this?

When I've worked on smaller teams,
these kinds of questions didn't matter much
because the answer was usually obvious.
But on bigger teams,
scale becomes a problem.

Part of the reason is that bigger teams aren't monolithic.
A bigger team is most likely an aggregate
of small teams working in conjunction with each other.
In this world,
you don't work closely with everyone
because that's an unreasonable thing to do.
If you did so,
there would be too many communication pathways.
Information would be repeated too often
between different pathways
and the messages would change
like a game of telephone.

Instead,
bigger teams need to work through clearer,
and often more formal, channels.
This is a world where interfaces matter much.
Documentation is far more valuable.
Clear division of responsibilities
and ownership are critical markers
to successful teamwork
in this type of environment.

We set up more formal structures
so that we can get better leverage
in our systems.
For instance,
if my team makes gRPC APIs
which utilize Protobufs
and your team makes REST APIs
using JSON,
then we may lose out
on the chance to share data quickly.
You could surely add support for Protobufs
and I could add support for JSON,
but what if another team uses GraphQL
and still another team uses Avro.
We'll have built up a technological Tower of Babel.

Even a light degree of formality can help teams agree
to common formats and conventions.
Adopting a reduced set of common interchanges
can lead to systems that can share and collaborate more easily.

The challenge is that people have mixed opinions
on technology.
Language choices can influence execution and preferred interface styles.
The constant tension in a large system is how to allow some amount
of freedom
and constrain the solution space,
so there is hope that a solution might look as if it were constructed
by a team that swims in the same direction.

I think this is where system design moves more into the realm of art and taste
over science.
When an architecture is overspecified,
a team can miss opportunities
by having too many constraints.
A team that chooses to pick only a single language,
perhaps Ruby,
might miss out on amazing technology
from other languages.
But if you allow *any* language,
then you may discover a problem hiring people
when no one is around
to work on that one service
that some solo developer decided to write in Cobol.

Where are good places to introduce constraints?

*Interfaces* are a great place to start.
Find a style or two and try to stick with it,
but don't be dogmatic.
At work,
we try to use GraphQL for most synchronous communication
between services.
With most everything talking over the federated GraphQL graph,
we gain a lot of consistency.
Even with that preference,
our team acknowledges that GraphQL isn't the best fit for everything.
On an as-needed basis,
we'll examine an alternative approach
and go with it
if the circumstance is unique enough.
This isn't my ringing endorsement
of GraphQL as The One True Way™.
Our team made a choice that fits our needs,
but your choice could certainly be different.

*Languages* are also a reasonable thing to constrain.
On a big enough team,
there are going to be common things
that code will need over and over again.
Logging,
authentication / authorization,
feature flags,
third party library support,
and so on
will be needed by each language
that contributes to your system.
If you have a platform team or a tools team
that is trying to support all the other developers,
a multiplicity of languages can become a real burden
as the matrix of languages to required libraries grows.
Strategically limiting the number of languages
to a handful of use cases can help keep one dimension
of that matrix in check.

*Service size* may also be worth constraining
until your team has a really solid understanding
of your problem domain.
There may be systems out in the wild
that consist of swarms of tiny, one function services,
but I'd be skeptical of that.
If your team has scaled
and you're not going to invest
in the majestic monolith,
then having a manageable amount of services will be an area
of consideration.
I would bias toward "macro" services
instead of "micro" services.
Services that serve multiple, but related, domains may be easier
to work with
than the fleet of individual, single purpose, services.
If your team is working with some amazing platform
with a phenomenal deployment model,
I could be wrong on this one.

Large software systems present all kinds of challenges
like what I've presented here
and so much more.
The domain modeling itself is another area
that can be difficult to corral
when so many teams are involved.
Throw in a company merger or two
with all their associated legacy software,
and you'll really spice up your design space.
