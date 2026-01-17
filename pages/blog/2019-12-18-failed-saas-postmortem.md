---
title: "A Failed SaaS Postmortem"
description: >-
    My Software as a Service failed.
    After three years of running College Conductor,
    I'm shutting it down.
    The service failed
    for a host of reasons,
    and this article details
    what I learned
    from the whole experience.
image: img/2019/conductor.svg
slug: failed-saas-postmortem
date: 2019-12-18
categories:
  - Python
  - Opinion
tags:
  - SaaS
  - Python
  - Django
---

My Software as a Service failed.
After three years of running College Conductor,
I'm shutting it down.
The service failed
for a host of reasons,
and this article details
what I learned
from the whole experience.
This is a chance for me to reflect,
and give you some ideas
of what pitfalls can happen
if you're planning to build a SaaS.

## The vision

Before getting to the lessons,
let's look
at my vision
for the service
so you have some context
of what I was building.

College Conductor was a tool
for college counselors,
and,
more specifically,
for independent education consultants,
which is a group that included my wife.
Back when I started,
my wife lamented
about the quality
of the online tools available
to help her run her business.

She wanted a tool
that could keep track
of the students she worked with.
Independent educational consultants focus
on helping students find the right college or university
for them.
My wife observed that the existing tools
for IECs
(as the industry calls them)
felt dated and clunky.
She desired a tool
that would keep track
of all the schools
that a student wanted to attend
so she could manage college applications, deadlines,
and all the other details
that go with the job.

As a software engineer,
I saw the chance to create something
in a narrow vertical
that could serve this industry.

## The initial plan

My initial plan sounded simple:
*build an app
that would track schools
and admissions deadlines.*

In the spirit of [doing things that don't scale](http://paulgraham.com/ds.html),
I planned to get as many US colleges and universities as I could
into a database.
From there,
I would operate as the Wizard of Oz
and manually look up the admissions deadlines
for a school
whenever my wife added the school
to a student's list.
(Adding the school to a list would trigger a "back office" task to inform me
that I had work to do.)
To me,
this felt like the scrappy kind of attitude
that I needed
to build something quickly.

For the technology side,
I wanted to make choices
that would be with me
for the long haul
(which you will see is ironic later).
My short list
of technology looked like:

* [Django](https://www.djangoproject.com/) to power an API.
* [Ember](https://emberjs.com/) as the client app.
* [Semantic UI](https://semantic-ui.com/) for the look and feel.
* [Ansible](https://www.ansible.com/) for handling deployment.

Ember and Semantic UI were new to me,
but I figured
that some technical risk
on those choices would pay off
in the long run.
I was wrong,
and we'll dig into why.

## Not-so-boring technology choices

When I started,
I wanted to follow the advice to 
[choose boring technology](https://mcfunley.com/choose-boring-technology).
For me,
this meant:

* Deploy to a virtual machine.
* Use a relational database like [PostgreSQL](https://www.postgresql.org/).
* Stick with a mature framework like Django.

In the boring technology article,
the author, Dan McKinley, writes:

> Let’s say every company gets about three innovation tokens.
You can spend these however you want, but the supply is fixed for a long while.

In my mind,
if I used Ember and Semantic UI,
then I've only used two innovation tokens
so I should still be in good shape
to make rapid progress.
*Wow, was I wrong. So wrong.*

Ember and Semantic were, indeed, innovation tokens
that I spent.
Ember wasn't new,
but it was new to me,
and it has a steep learning curve
to be deeply productive
with the framework.
Semantic *was* on the newer side
so I was learning its patterns
as the UI toolkit evolved.

Where I was horribly wrong was in thinking
that Ember and Semantic were the only pieces
of new technology
that I needed.
The list was so much longer
and included:

* [Datadog](https://www.datadoghq.com/) for infrastructure monitoring.
* [DigitalOcean](https://www.digitalocean.com/) for virtual machine hosting.
* [Django REST Framework](https://www.django-rest-framework.org/) for APIs.
* [Drip](https://www.drip.com/) for marketing email campaigns.
* [Jekyll](https://jekyllrb.com/) for the marketing site.
* [JSON API](https://jsonapi.org/) as a communication protocol.
* [Let's Encrypt](https://letsencrypt.org/) for TLS certificates.
* [Mailgun](https://www.mailgun.com/) for transactional emails.
* [Mixpanel](https://mixpanel.com/) for behavior analysis.
* [Rollbar](https://rollbar.com/) for error tracking.
* [Segment](https://segment.com/) for data aggregation.
* [Stripe](https://stripe.com/) for recurring payments.
* [wal-e](https://github.com/wal-e/wal-e) for database backups.
* [webpack](https://webpack.js.org/) for JavaScript asset bundling.

For some of those tools,
I had some experience,
but the depth of my knowledge was lacking
since I am a company of one.
These were all technologies
that I had to learn
and configure myself.
While I succeeded
at integrating each
of these things,
I did so at the cost of *a lot* of time.

So, here's a first lesson:

> When starting out, keep your technology stack to a bare minimum
and follow the **YAGNI** (You Ain't Gonna Need It) principle.

## The upgrade treadmill

After assembling all of these tools together,
I finally felt like I had a base
to work from.
My project was moving
and I began to build the critical features needed
to make a minimum viable product.
Then I fell into a trap.

The trap looks like this:

1. Time is ultra-limited
    because this is a nights and weekends side project.
2. Software moves fast
    and new versions of tools constantly release
    (this is especially true in the JavaScript ecosystem).
3. I'm eager to keep the software up-to-date
    to ensure that the large base I built stays "modern."

With these three conditions in place,
I spent way too much time piddling
with package upgrades.
I'm guessing you can see
how this might happen.
I'd spend a long day working
at my day job
and doing a lot of software development there.
Then I wouldn't have the energy
to make **real** progress
on my app,
so I'd tell myself
that upgrading one of the packages
that was out-of-date was a good use
of my time.

*Wrong.
Again,
I was so wrong.*
I wasted so many nights updating small packages
for zero benefit.
To make the issue worse,
some of these minor updates would break things
(because [SemVer is a lie](https://x.com/dhh/status/1015206151384952834)).
Upgrading these packages was a treadmill
that got me nowhere.
That brings me to lesson two:

> Software package upgrades suck the wind out of your sail.
Until you have a minimum viable product
with customers,
pick a package version and stick with it.
Only upgrade **when you have to.**

## Switching horses mid-race... twice!

Remember how I mentioned picking Semantic UI and Ember?
Check out the [College Conductor repo](https://github.com/mblayman/conductor)
and you'll be hard pressed
to find either of them.

At some point during development,
I realized how hard I was fighting
with my tool choices.
Semantic UI wouldn't play nicely
with Ember's build system,
and the components and extensibility
of Semantic were not working
for me.
This friction affected my ability
to make UI elements that I needed
for features.

I won't blame Semantic
because it was more likely my deep inexperience
with the toolkit
that was the problem.
With Semantic troubling me
and me having do all the other parts
of the system development too,
I pulled the ripcord
and switched to [Bootstrap](https://getbootstrap.com/).
I sacrificed more novel styling
for a system I knew.
And, guess what?
I saw the immediate productivity boost
from using a tool
from my toolbox!

Eventually,
I made a similar choice
to remove Ember.
I tried to use Ember
for nearly two years.
I read a large amount
of the documentation,
wrote articles
about what I learned
on my journey,
and stayed up-to-date
with all the EmberConf content
and news coming out
of that community.
I *really* like Ember.
So why would I cut it loose?

**Development velocity**

As a one person team,
I had to develop the backend logic,
database models,
and everything that comes
with backend development.
I *also* had to develop
the entire user interface.
I discovered that creating a backend API
and rich client side single page app (SPA)
came with a ton of overhead.

My flow with Ember was like:

1. Figure out the data model for the next feature.
2. Create models in Django.
3. Create JSON APIs in Django.
4. Create models *again* on the client side
    with [Ember Data](https://guides.emberjs.com/release/models/).
5. Decide on the routes and controllers
    to finish the user interface for the feature.

Between step three and four,
I would lose most of my motivation
and jump back on the upgrade treadmill.
As a team of one,
it felt like drudgery
to recreate models
for a client side representation.

The decision to remove Ember was really tough.
The [sunk cost fallacy](https://en.wikipedia.org/wiki/Sunk_cost) hit me hard.
I delayed removing Ember
for many months
because I convinced myself
that it would take a long time
to redo all the work
that I finished so far.

*Then I removed it.*
What do you think happened?
I removed so much extra stuff
and simplified my technology stack so tremendously
that I implemented *all*
of my original features
within *two weeks.*
Two weeks of effort
to replicate two years
of previous development.

Does this mean that Ember is bad and you shouldn't use it?
**No!**

Ember was a bad fit
for me,
at that time,
with my level of experience with it,
and no support
from other team members.
Also,
I switched to using Django
for the user interface
with server side rendering,
and I was extremely comfortable
with that
because I use Django daily
in my day job.

Lesson three:

> **Use the tools that are already in your toolbox!**
You'll need all your extra brain capacity
for solving the business problem.

## Ignoring customer development

If you look back
at the vision
that I wanted for the project,
you'll see
that I hoped to make something useful
for my wife.
Up to this point,
I've written about the technical failings
of the project.
This is an emblematic example
of why the project failed.
*I didn't help my customers
and was too focused on the technology.*

At the start of the effort,
I asked my wife questions
about what she needed
and what would help her
and other educational consultants
like her.
She told me the things
that she was looking for directly.
But it took forever
to have something tangible
to show her.

If someone shows up to a restaurant,
expresses what they want,
then the chef takes four hours
to prepare the meal,
will that customer be happy?
I think not.

I was the slow chef.
All the time I invested
in building the "right" thing was wasted
because I didn't do customer development.
**I didn't produce the simplest version
of the product
that would provide value.**
It did not take long
before I completely lost my wife's interest.
To stick with the four hour meal analogy,
my patient customer left
after the meal wasn't ready
in the first hour.

As developers and technologists,
many of us enjoy steeping
in the technology
purely for the sake of it.
There is so much to learn
and so many ways to apply software
that it is easy to lose yourself
in that tinkering.
While that's personally useful,
especially if you need to grow your skills,
staying in that space
is not helping others.

So,
what did I take away from that?
That would be the next lesson:

> Get your product to be something useful for others
**as fast as possible**.
Until you deliver something valuable,
you only have a hobby.

Without serious interest from my first customer
(and no other strong ties to her industry),
I was missing a good voice to drive the product forward.
Because she was disinterested,
there was no external pressure on me
to deliver something.
My project got nowhere fast.

## The end

If there is anything redeeming about College Conductor,
it was as a teaching tool.
I've done a lot of Django code
for work,
and I brought that same thoroughness
to this project.
After listening to an episode
of The Changelog
about [live streaming software development on Twitch](https://changelog.com/podcast/288),
I started to share my efforts
on College Conductor live.

Over a year later,
I have [streamed nearly 40 lessons](/blog/building-saas)
in an episodic format
to teach people about Django
and building real projects.
My service may have had no real customers,
but the techniques I apply
to building things are very much the techniques
that I use at work.

Where does that leave me?

* I've learned a lot.
* I've taught a lot.
* College Conductor was a financial failure.
* College Conductor was a successful teaching tool.

I hope you're able to learn a bit
from my experience
with building my first SaaS project.

For those jumping straight to the end,
here are the lessons
that I learned.

1. When starting out, keep your technology stack to a bare minimum
    and follow the **YAGNI** (You Ain't Gonna Need It) principle.
2. Software package upgrades suck the wind out of your sail.
    Until you have a minimum viable product
    with customers,
    pick a package version and stick with it.
    Only upgrade **when you have to.**
3. **Use the tools that are already in your toolbox!**
    You'll need all your extra brain capacity
    for solving the business problem.
4. Get your product to be something useful for others
    **as fast as possible**.
    Until you deliver something valuable,
    you only have a hobby.

If you want to watch me build my second SaaS,
please join me
on [Twitch](https://www.twitch.tv/mblayman)
on Wednesdays
at 9pm ET.
Hopefully, I'll make fewer mistakes this time around.

**Note**: As of late 2021,
I'm still streaming,
but I moved from Twitch
to [streaming on YouTube](https://www.youtube.com/c/MattLayman/live).

If you have questions
or enjoyed this article,
please feel free to message me on X
at [@mblayman](https://x.com/mblayman)
or share if others might be interested too.
