---
title: "Debugging Tips And Techniques"
description: >-
    Your Django app is up.
    You've got users.
    Your users are hitting bugs.
    How do you debug
    to fix the problems?
    That's the focus of this Understand Django article.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - debugging
series: "Understand Django"

---

In the last
{{< web >}}
[Understand Django]({{< ref "/understand-django/_index.md" >}})
article,
{{< /web >}}
{{< book >}}
chapter,
{{< /book >}}
we looked at security.
How does a Django site stay safe
on the big, bad internet?
{{< web >}}
The article explored some core elements
{{< /web >}}
{{< book >}}
The chapter explored some core elements
{{< /book >}}
for making a Django app more secure.

{{< web >}}
With this article,
{{< /web >}}
{{< book >}}
With this chapter,
{{< /book >}}
we will investigate problem solving techniques
for Django apps.
The goal is to equip you with tools
to fix the real problems
that you'll hit when building your Django site.

{{< understand-django-series "debugging" >}}

## Systematic Problem Solving

When you have real users using your website
and they report problems with the site,
what can you do to fix the problems?
Having a mental framework
for how to fix problems is really useful,
because it provides a repeatable process
that you'll be able to use as long
as you're building on the web.
Let's discuss the mental framework
that I use,
which I think of as *systematic problem solving*.

The first thing to drill into your head is
that computers are deterministic.
Given a set of inputs,
they will produce a repeatable output.
This is crucial to remember
because the art of problem solving
with computers
is about sleuthing the state
of your system
(i.e., a Django website in this context)
to determine why a given set of inputs
produced an undesirable output,
also known as a *bug*.

When debugging a problem,
the challenge is figuring out what all those inputs are.
The inputs can vary wildly.
Successful problem solvers are those
who can find the inputs
that caused the bad output.

This is the core of systematic problem solving.
With systematic problem solving,
you want repeatable patterns
that help you build up a mental model
of how a problem occurred.
Once you understand the problem,
you'll be ready to create the solution
and fix your bug.

*How do you repeatably figure out problems with a website?*

In my experience,
the most fruitful way to understand a problem is to reproduce it.
To reproduce a problem requires context and data
about what happened in the first place.

What are the sources of this data?

{{< web >}}
* Error monitoring services like Rollbar or Sentry can be a fantastic source
    of data.
* Log data, which we'll discuss later in this article, can be another excellent source.
{{< /web >}}
{{< book >}}
* Error monitoring services like Rollbar or Sentry can be a fantastic source
    of data.
* Log data, which we'll discuss later in this chapter, can be another excellent source.
{{< /book >}}

Error monitoring services help show what happened.
These services will collect tracebacks of Python exceptions
and display them in context
of a particular request.
Some of these tools can even show the sequence of events
that led to the failure case.

My favorite strategy for cases like this is to produce
an automated test
that can trigger the same exception
as the one reported by the error monitoring service.
This is often a mechanical transformation
of the data provided on an error report page
into the setup data
of a unit test.

The great part about having a unit test is that you now have something
that you can repeat with ease.
This is a lot better than clicking around on your site
and trying to recreate a problem manually.
Because you've captured the problem scenario in test code,
you can know *exactly* when you've **fixed** the problem.
You can work on the site's code and run the test over and over
until you've devised a solution
that overcomes your error.

This process is a systematic approach
that you can apply again and again
to solve problems.
The process in a nutshell looks like:

* Collect data from the failure scenario
* Transform that data into an automated test
    that demonstrates the problem in a repeatable fashion.
* Fix your site's code until the test passes
    and the problem is resolved.

The secondary benefit of this systematic model is
that your site has a passing unit test when you're done.
This test acts as a guard against future failures
of a similar kind (i.e., a "regression" test).

I don't want to oversell the value
of these kinds of tests.
Regression tests can be useful,
but in my experience,
I've rarely seen regression tests fail
after the offending code is fixed.
Nonetheless,
if the test is fast enough,
these kinds of tests are worth keeping
in your automated test suite
for those rare cases where you *do* encounter a regression failure.

Maybe my unit testing approach doesn't appeal to you.
That's fine.
Do what works well for you.
My larger point is that you should try to take a systematic approach
to problem solving.
**Find repeatable patterns that you can apply to your context.**

Approaching problems with a process in hand helps you avoid feeling stuck.
Having methods for solving problems also helps
when the pressure is on,
and you're trying to fix a critical and time sensitive bug
for your customers.
Not knowing what to do in a high pressure scenario can add even more stress
to an already stressful situation.

## `print` Without Shame

In the previous section,
I wrote "Fix your site's code until the test passes,"
but I didn't explain how you'd actually do that.

When you're working with a failing test
and you're trying to make it pass
to solve a problem,
you have to understand the scenario
at a pretty deep level.

One tool to reach for is the `print` function.
You can sprinkle some calls to `print`
into the code you're working with
to gain an understanding
of what is happening.

In your journey in programming,
you'll run across this idea
that "print debugging" is a bad idea.
Not everyone espouses this idea,
but it exists out there.
In the same breath,
you'll read that you should be using a debugger instead
or some other tool.

Debuggers,
which are great tools
that we'll cover shortly,
are not the only tool worth knowing.
In fact,
in many cases,
debuggers are a terrible tool for the job.

What does the `print` function do
that makes it so useful?
**`print` provides a chronology.**

With the `print` function,
you can observe changes *over time*.
The `print` function can answer questions like:

* What is the value of my variable
    in each iteration through the loop?
* Is this block of code even reached
    by the interpreter?
* What is the before and after state
    after a section of code executes?

The nice part about using `print`
in an automated test is that you can see all the data,
all at once.
The results of a handful of `print` calls starts
to tell a story
of what happened during execution.
If your "story" isn't rich enough and meaningful enough
to understand what's happening,
you add more `print` calls
and run the test again.

I'd estimate that I am able to use `print`
for 70-80% of my debugging needs.

What should you print?

* One simple strategy is to print a number sequence.
    Adding `print(1)`, `print(2)`, or more
    to various lines
    can show what parts of code are executing
    or what patterns are happening in loops.
* Sometimes I'll print the values of conditionals
    for branches that I'm interested in.
    This helps me figure out when certain branches
    in the code are taken versus when they are not.
* Other times I'll add prints
    with a bunch of newlines
    to visually separate things.
    `print('\n\nHERE\n\n')` is surprisingly effective.

The answer to "what should you print?" is really
"what do you want to know?"
As you use `print`,
you'll develop a good feel
for what information you find most useful.

Tip: As of Python 3.8,
you can print the variable name
in an f-string along with its value:

```python
>>> foo = 5
>>> print(f'Hello world {foo=}')
Hello world foo=5
```

`print` is pretty great,
but it isn't always my tool
of choice.
For instance, `print` is not the best tool
when problem solving a live site.
`print` also doesn't work as well
when I need to get really detailed information
about the state of my program.

When do I reach for something else?
Let's look at debuggers next.

## Debuggers

If 70-80% of the time I can get away with `print`,
what about the rest of the time?

Sometimes I'll use a debugger.
A debugger is a specialized tool
that allows you to go through your Python code,
one line at a time.

Considering how much code we write
and how much we use from other packages,
this means that a debugger can be a slow tool
to utilize.
A debugger makes up for this slowness
with an unparalleled amount
of information
about what is going on
at the exact moment
that the Python interpreter executes a line of code.

How do you use a debugger?

Assuming that you're following my strategy
of writing an automated test
when you're working on a problem,
the simplest way to start a debugger is
by adding `breakpoint()`
before the code you want to check.

In a standard Python installation,
adding this function call will pause your program
by running the Python debugger, `pdb`,
starting from the call to `breakpoint`.

If you do this, you'll be left at a prompt
that starts with `(Pdb)`.
From here,
you'll need to know some commands
to navigate within the debugger.
I'll cover the primary commands I use here,
but you can type `h`
to see a list of the available commands
with instructions for how to get more help info.

My natural inclination in the debugger is to know where I am.
The `l` command will *list* code
that the interpreter is about to execute,
along with an arrow showing the next line
that Python will run.
I may also want to know where I am in the call stack
(i.e., the history of calls that go back all the way
to the main function
that started the Python process).
By using the `w` command to show *where* I am,
pdb will show the call stack
with the current line of code listed last
by the prompt
and the oldest function listed
at the top of the output.
These two commands give me the context
at any particular moment.

Next,
I'll often want to know the values
of local variables
when I'm debugging.
I can either use `p` to *print* the value
or `pp` to *pretty print*
in cases when I have a structure like a list or dictionary.

All the previous commands orient me
to where my code is and what values are in the data structures.
With that context,
I'm ready to work through my code
with two additional commands.
In a debugger,
you advance the Python interpreter a line at a time.
There are two styles to do this.

One way is with the `n` command
to go to the *next* line.
This command is what you want
when you don't really care about how a line runs.
For instance,
if the line calls a function that you know works,
`n` is the way to pass that line
to let it execute in its entirety.

The other command to advance the interpreter is the `s` command.
The `s` command lets you *step* through the code
at the smallest possible increment.
That means if you're on a line
with a function call,
the `s` command will move *into* the function call
to show what's executing inside of it.
I view the step command as the very fine adjustment command
to run as I get close to the problem area
in my code.

Whenever I'm done debugging my code
and have seen all that I need to see,
I finish with the `c` command
to *continue* normal execution.

What's great about having a unit test is that I can run the debugger
in a very coarse way
by liberally using the `n` command.
As I hit the error state
(like an exception happening),
I can continue,
restart the test,
then quickly return to right before the point in time
when the error occurs.
At that juncture,
I switch to the `s` command
until I find the exact moment
when something goes wrong.
This process helps me avoid wasting time
by stepping through parts of the code that don't matter.

The debugger has more interesting features
like setting breakpoints
and checking data at different parts
of the call stack,
but I hope this description gives you an idea
of how to apply a debugger
in your workflow.

Learn more about the debugger and `pdb`
by checking out the
{{< extlink "https://docs.python.org/3/library/pdb.html" "pdb standard libary documentation" >}}.

## Use The Source, Luke

At times,
you're going to run into problems
with code
that is not part of your project.
This might be code
in the Django source
or it might be code
from some other library
that you happen to use in your project.

What I have found over time is
that many less experienced developers
will hit this situation
and suddenly freeze.
There's some kind of mental barrier preventing them
from looking any further
than the boundary
of their own code.

Here's my tip: **don't freeze!**

When you wake up
to the reality
that it's all just code
that people wrote,
you cross that mental barrier
and move into realms
that others may fear to tread.
The funny part is that this code is often no more special
than anything that you might write yourself!
In fact,
many open source developers are fantastic programmers,
and fantastic programmers often know how to write clear,
maintainable,
and well-documented code.

So,
listen to your inner "Obi-Wan"
and use the *source*, Luke!

* If you're hitting a problem with a package,
    look at the source code on GitHub
    (or wherever the code is hosted).
    You can study the modules and trace through how the code would execute.
* If that's not enough,
    don't be afraid to step through functions
    in other libraries
    with your debugger
    as you are testing out whatever problem
    that you are trying to fix.
* Remember `print` debugging?
    Who says you can't do that with other software?
    If I've got a virtual environment
    and I need to figure out what's going on
    with how my software interacts with a library,
    I will sometimes add `print` statements directly
    to the library files
    in my virtual environment's `site-packages` directory.
    This is a great trick!

There are limitations to this approach because some packages
will include code sections that are compiled with C.
That kind of code is harder to peek into,
but I've found that the majority of Python packages
that you find on PyPI are Python-only.
That makes most packages great candidates
for digging into the source code.

## Logging Chronology

Logging is a topic that we will only scratch the surface of,
but the subject is important
to round out a discussion of debugging tools.

A logging system provides the ability to record messages
during the execution
of your application.
The easiest way to think of logging is as a permanent set
of `print` calls
that record information every time your functions or methods
call the logging system.

When logging is used in an application,
you can capture what happened within your app
even if you weren't there to observe the system
at the moment that it happened.
The logging system forms a chronological log
of events
that happen within a system.

This has some big benefits,
but comes with some tradeoffs
to consider.

* **Pro**: When you have sufficient logging,
    you can see what is happening in the app
    when your users are working in the app.
* **Pro**: More advanced logging configurations
    can include metadata that you can filter on
    to look for specific kinds of activity.
    This can aid your diagnostic abilities.
* **Con**: Logging generates data.
    While this enables the points above,
    you now have a new challenge
    of *managing* this new source of data.
* **Con**: Log management is even more of a challenge
    as an application system grows.
    When you have multiple servers,
    where does all that log data go?

This concept of logging is not a Django-specific idea.
In fact,
you can find a `logging` module
in the Python standard library
that serves as the basis
for logging in the Python world.
Django builds its logging features
on top of the `logging` module.

The short version of logging
in Django
is that you can use logging
by configuring the `LOGGING` settings
in your Django settings module.
This process is described
in the documentation
at {{< extlink "https://docs.djangoproject.com/en/4.1/howto/logging/" "How to configure and use logging" >}}.

In a basic workflow,
logging can be little more
than writing lines
of data
to a log *file*.
If you're running an app
on a VPS
like Digital Ocean
and have control over your filesystem,
this is a good starting option.
If you choose that path,
keep in mind that disk space is a limited resource.
One way to tank your app is to fill your machine's disk
with logging data.
To prevent this,
you should investigate how to use logrotate.
{{< extlink "https://linux.die.net/man/8/logrotate" "logrotate" >}} is a command
that can archive your log data
on whatever frequency you desire
and clean up old data
to prevent your storage from filling completely.

You may follow a path like I've recommended frequently
and deploy your app on a Platform as a Service (PaaS) like Heroku.
In that kind of environment,
you have less control over the tools that are available
to run your application.
In the case of Heroku,
the platform does not guarantee
that your app will stay on the same machine.
Because of that constraint,
you can't rely on a log file
on the machine.
Instead,
you would need to add an additional service
to the application
that will store logs
for your later use.
{{< extlink "https://www.papertrail.com/" "Papertrail" >}} is an example
of a log aggregation service
that works with Heroku.

As you can see,
logging brings some complexity to manage
if you choose to use it.
Logs can be a great tool
to understand what happened
when a user used your app,
especially if there was an error
that didn't raise an exception.
For me, personally,
I *don't* reach for logging right away.
While logging can be useful,
it can be an overwhelming amount of data
that can turn debugging
into a "needle in a haystack" problem.
Logging is still a potentially useful tool
for your toolbox
as you think about how to debug your apps.

## Summary

{{< web >}}
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
we saw debugging tips, tools, and techniques
to make you a bug crushing machine
in Django.
We discussed:

* A systematic method for finding and fixing bugs in your app
* How `print` is an awesome debugging tool
    that should be used without shame
* Debugging with a "proper" debugging tool
    for particularly thorny problems
* Using the source code of packages you didn't write
    to figure out what's going on
* Logging and the ability to see a history
    of activity in your application

{{< web >}}
That's the end of this series!
{{< /web >}}
{{< book >}}
That's the end of this book!
{{< /book >}}
Can you believe there are still more topics
{{< web >}}
that this series could cover?
{{< /web >}}
{{< book >}}
that this book could cover?
{{< /book >}}
Django has so much available that,
{{< web >}}
even after twenty articles,
{{< /web >}}
{{< book >}}
even after all these chapters,
{{< /book >}}
I've not covered everything.
But this is the end
of the line for me.

{{< web >}}
I knew when I started this series
{{< /web >}}
{{< book >}}
I knew when I started this book
{{< /book >}}
that I was going to cover a huge number
of topics.
What I didn't know when I started this in January of 2020
is how wacky the world would be.
{{< web >}}
I thought that I might produce an article every other week
{{< /web >}}
{{< book >}}
I thought that I might produce a chapter every other week
{{< /book >}}
and be done in less than a year.
*How wrong I was!*
More than two years later,
I'm writing the words
{{< web >}}
of this last article.
{{< /web >}}
{{< book >}}
of this last chapter.
{{< /book >}}

{{< web >}}
As I wrap up this series,
{{< /web >}}
{{< book >}}
As I wrap up this book,
{{< /book >}}
my hope is that you,
dear reader,
have come to understand Django better.
Django is a web framework written
by people like you and me.
That community,
through years of collaboration,
polished a tool
that can bring your ideas
to life on the web.

While the framework might initially seem magical
in all that it is able to do,
we can see through study
and examination
that the code is comprehensible.
The magic becomes less magical,
but we can grow
in our respect
for those who contributed untold hours
to making something so useful
for others
(for *free* in most cases!).

{{< web >}}
I would like to conclude this series
{{< /web >}}
{{< book >}}
I would like to conclude this book
{{< /book >}}
by thanking all of you readers out there.
Along this lengthy journey,
so many of you have reached out
{{< web >}}
and told me how this series has helped you grow
{{< /web >}}
{{< book >}}
and told me how this book has helped you grow
{{< /book >}}
as a Django developer.
I'm hopeful that developers have used these words
to learn and create websites
that help their own communities.
Knowing that I've impacted some of you
and, by extension, the communities
that you've helped,
{{< web >}}
made writing this series worth it.
{{< /web >}}
{{< book >}}
made writing this book worth it.
{{< /book >}}

> Thank you for reading!

{{< web >}}
If you have questions,
you can reach me online
on X
where I am
{{< extlink "https://x.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;
