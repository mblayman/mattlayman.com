---
title: No nitpicking in code reviews
description: >-
  Code reviews improve the quality
  of software.
  But a code review can be done badly.
  In this post,
  we'll look at some tools
  to make your code reviews
  as effective as possible.
image: img/2017/nitpick.jpg
type: post
aliases:
 - /2017/no-nitpicking-code-reviews.html

---

*Two hours.*
I sat
in an excruciatingly cold conference room
while enduring the code review meeting
that would never end.
The contract demanded formal code reviews
so we had a room full of engineers
wearing many hats.
A moderator,
lead reviewer,
other reviewers,
scribe
and more "interested" parties
stared at code
on a projector.
The code in question
was thousands of lines long
and was a
big subsystem
in a major satellite software.
This code review was a crucial milestone
before handing off the component
to an integration test team.

*Were we discussing the critical functions
of the code?
Did we explore the best ways to express
the system
to solidify a software component destined
for space?*

**No**, we quibbled
about the lengths
of lines of code
and where to capitalize letters
in variable names.
The group had
to reach a conclusion
about every comment added
to a long spreadsheet
of comments,
and 90% of the comments were **nitpicks**.

> How did a group
of intelligent engineers end up
in this horrible scenario?

I'm sure there were many reasons,
but a big contributor was **failing
to let computers do what computers are good at.**
Computers can automate the boring verification work,
but we didn't use them for that task.

The project demanded
that all code adhere
to a certain style
and conform
in 100% of cases.
The trouble
with the style
is that the team made choices
that were not enforceable
by an automated tool.
The combination
of complete compliance
and not being machine checkable meant
that reviewers had to spend more time examining **the layout**
of the code
instead of **the content**.
*This combo was a massive waste of time.*

> How could this have been different?

We could have improved these reviews
if we selected a coding style
that a computer could verify.

## A "no nitpicking" code review

Let's contrast that terrible code review experience
with a Storybird code review.
At {{< extlink "https://storybird.com/" "Storybird" >}},
all code goes through a GitHub
{{< extlink "https://help.github.com/articles/about-pull-requests/" "pull request" >}}.

In a pull request,
the software runs through a series of checks
in a continuous integration environment.
If any check fails,
we refuse to merge the code.
This philosophy adds an excellent level
of quality control.

What checks do we execute?

* A full run of the Python unit test suite
* A full run of the JavaScript unit test suite
* Style checks for Python code

For this post,
the item to unpack is "Style checks."
The engineering team runs two tools
to check Python code style.
The first is {{< extlink "http://flake8.pycqa.org/en/latest/" "flake8" >}}.
The second tool is {{< extlink "http://isort.readthedocs.io/en/latest/" "isort" >}}.

flake8 is a static analysis tool
that compares Python code
to recommendations made
in the "Style Guide for Python Code"
(often referred to as {{< extlink "https://www.python.org/dev/peps/pep-0008/" "PEP 8" >}}).
Any code that does not match conventions is reported,
and the `flake8` executable exits
with an error code.

isort solves a narrower problem.
When the continuous integration environment runs `isort`,
the program will report any Python imports
that appear in an incorrect order
(where "incorrect" is a standard agreed upon
as a team).
If anything is incorrect,
`isort` also exits
with an error code.

When either of these tools report failure,
the continuous integration build is a failure.
Because Storybird has a policy
to only merge passing builds,
a developer must fix
whatever is reported by the checking tools.

This style of code review offers many benefits.

* *No more nitpicking comments.*
  The developer must make the build pass
  and the tools dutifully report any issues
  without being a nag.
* *Higher quality standard.*
  A zero exception policy
  and machine enforcement
  means that all developers are held
  to a high bar.
* *Better review content.*
  The code reviewers are freed
  from thinking about the little stuff
  and can focus
  on the actual problem to solve.

## A tale of two code reviews

We covered two types of code review:

* The first review was highly manual,
  time consuming,
  and ineffective.
* The other review leveraged computer automation.
  It didn't waste the time
  of engineers
  and helped the team
  more than hurt.

I hope that you've never had a code review experience
like my first example.
If you have,
you probably felt the frustration
that I did.
Changing company culture can be very hard,
but if you can move your team
toward using tools
that function as automated code reviewers,
you'll be more effective
and happier.

For those of you already on a team
with a solid continuous integration practice
and automated code checking,
*be thankful!*
