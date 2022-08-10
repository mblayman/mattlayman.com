---
title: "Brute Force Development"
description: >-
    Some tasks are laborious.
    With this article,
    I describe my attitude
    that I will apply on occasion
    to handle these tasks.
image: img/2022/brain.jpg
type: post
categories:
 - Software
tags:
 - brain dump
 - development

---

Some software development tasks are boring
and laborious.

Here are some examples:

* Adding a linter and fixing *all* the issues.
* Adding type hints to all Python function signatures
    and fixing *all* the issues.
* Upgrading dependencies and packages in a project.
* Fixing all the deprecation warnings coming from a test suite.

The pain of these types of tasks often grows
with the size of the software system
that you're operating on.
How can you deal with problems like this?

* Ignore the task and hope that someone else will do it.
* Write an automated script that will do the work.
* Roll up your sleeves and do it yourself.

Let's focus on the third option.
First, when is elbow grease superior to automation?
Thankfully for developers,
there are still many tasks
that computers cannot completely automate.
Our jobs are safe for now
because translating a solution to a problem
into software is still a very messy task.

In my experience,
many kinds of linting errors are good candidates
for tasks that require a human eye.
While you *could* use scripts and tools
to update source code,
this can be very challenging to get right
and can require deep knowledge
of abstract syntax tree parsers
and the like.

You might not be in a mental space
to think of automation tools
as the solution to a problem.
I've been in team environments
where the demonstrated behavior was to ignore a task
because individuals felt overwhelmed
by the thousands
of errors and warnings coming out of linters.
Manual effort works well
with this kind of task
because you can immediately work to shrink the problem.

> Don't be dumb if you choose to tackle a problem manually!

In team environments
where these broad problems are hampering team performance,
how can you avoid being dumb
while fixing a problem manually?

1. Stop the bleeding.
2. Be systematic.

Many of the manual tasks
that I'm describing
come about
because of software entropy.
Even though software is very precise in its construction,
over time,
the system *around* the software evolves
in a way
that degrades the software itself.
New language versions arise
that change core things (hello Python 3!).
Libraries change APIs.
Operating Systems evolve.
Sometimes the entropy happens
by changes from well intentioned developers
who write code that goes against norms
and expectations
of a language community.

Whatever the case,
when you're dealing with a task
that is fighting software entropy
and the mess caused
by the advancement
of time,
you should try to prevent further degradation.

Let's assume
that you've got a big project
and you think the code is a mess,
so you want to add a code linter
(like `flake8`)
to add some level of consistency.
When you run the linter,
the tool catches thousands
of things to change.
This was exactly the kind of situation
that I faced
with one of my teams.
I had recently joined a team
and `flake8` was a new part
of the tech stack.

The team was not stopping the bleeding.
Instead,
`flake8` was in a reporting mode
and it wasn't mandatory
for merging code.
Because of the thousands of messages
and the non-enforcement,
it was virtually impossible
to recognize if your change made the situation better or worse.
You could,
in theory,
run `flake8` against the latest commit
from the main branch
and again from your feature branch,
but nobody did that in practice.

So I changed the configuration of `flake8`
for the project.
The first thing I did was update the configuration
of `flake8` to ignore every category
of *existing* error.
I updated the config until I got to zero reported errors
rather than thousands.
Importantly,
with this configuration,
I updated Continuous Integration
so that `flake8` *must* pass.
**Why?**
This seemingly simple change did a couple of things:

1. It changed the expectations for my teammates.
    Rather than drowning in a sea of error messages
    that they were unsure if they contributed to or not,
    a developer's pull request would fail
    if any errors appeared.
    The developer would know immediately
    that the error was caused *by their code change*.
    Since we stated explicitly that we would not merge a change
    unless `flake8` was passing,
    the developer had motivation to fix the problem.
2. Any category of error that wasn't on the initial list
    that was ignored *could never become a problem for the codebase*.
    All code had to go through a PR
    and `flake8` was required.
    Thus,
    we eliminated whole categories of linting problems.

This is how we stopped the bleeding,
for the most part.
Developers could still add more issues
to the pile of categories
that we were ignoring,
but they could create new failure modes
for the other categories
that `flake8` scanned for.

Now we can come back to the "Be systematic" part of my advice.
The ignored categories
in the `flake8` configuration file
became the punch list
for fixing all the lint errors.
The process to enable all of `flake8` lint checks looked like this:

* In a new branch,
    change the config file to enable *one*
    of the ignored checks.
* Run the linter against all the code
    to get the list of all violations.
* Fix all the violations that show up.
    Since the category of error is all the same,
    once you determine the solution,
    it often becomes very doable to replicate
    for each of the violations.
* Repeat the process for the next category
    of lint check error.

This technique of enforcing a tool
in a small way,
then progressively expanding its utilization
is something that I have applied time and again
in different work settings.
I've found that it works so well
because it decomposes the problem
into smaller pieces
that are far more manageable.

I've seen this strategy work with lint,
type hints,
deprecation warnings,
test coverage,
and compliance checks.
Give it a try the next time you're trying to improve the quality
of your software project.

The original idea
for this brain dump is around brute forcing development tasks.
Not every task fits
into the scheme that I just presented.
"Stop the bleeding" and "be systematic" doesn't generalize,
but I think virtually all laborious tasks can benefit
from that second part of being systematic.

Any time you can take a task,
however boring it may be,
and break it down and knock it out,
I think you can be a huge force
for good in your organization.
Boring tasks can exist
because there isn't enough organizational willpower
to change.
Some of these tasks may be minor annoyances.
Some of these tasks may span so much
of a system that no portion
of the team feels that they can own the problem
to fix it.
If you can fix the areas,
you may unlock new options for your team.

Maybe this brain dump would have been better titled
as "Tortoise Driven Development."
The tortoise took the slow and steady approach
to win the race.
When I'm faced with a boring task
or I'm faced with a laborious task,
I like to think of myself as the tortoise.

> I'm going to win the race,
one step at a time.
