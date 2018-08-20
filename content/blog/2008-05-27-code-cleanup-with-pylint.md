---
title: "Code cleanup with Pylint"
description: >-
  Static analysis is a useful tool to help
  with open source projects.
  This post looks at Pylint,
  a tool for making better Python code.
image: img/2008/pylint.svg
type: post
categories:
 - Python
 - Open source
tags:
 - Python
 - Pylint

---


Entertainer is at a coding crossroads.
Lauri has done a great job
of showing Entertainer as a viable (and beautiful) media center software.
However, a portion of this code is more like prototype code than production code
(probably since Lauri is fairly new to python like myself).
Eventually, this code would become a big maintenance issue.
We can either continue to build upon some weak design areas or break things down
and refactor into something better.
We chose the latter option.

The developers are attacking this issue on two fronts.
First, Paul is overhauling the backend to use an ORM (Object-relational Mapping)
that will consolidate the SQL code.
This ORM will make the backend look more like an object than a database
from the frontend code’s perspective.
Secondly, we are using a source code analyzer
on the frontend to report a gauntlet of possible problems.
This analyzer is called Pylint.

Pylint analyzes source code using a rules file specifically tailored
to the style of the project.
Entertainer is trying to adhere to PEP 8
(Python Enhancement Proposal 8 – Style Guide for Python Code)
so we use a pylint rules file that attempts to follow that guideline.
Pylint is very easy to use and the following is an example of how to run it:

```bash
matt@zion:~/branches/transitions-cleanup/src$ pylint —-rcfile=pylintrc frontend/gui/transitions/fade_transition.py
```

In this example, we do three things:

* Call `pylint`,
* set the rules files (`pylintrc`),
* and specify the source file (`fade_transition.py`).

I ran this command in the source directory so that pylint could find the modules
that are listed in `fade_transition.py`.
If I had run it in the transitions directory,
I might have had import errors because some modules would not be seen
in the python path.
After running the command,
pylint will report any errors, refactorings,
warnings, or convention problems it can find,
and it will generate a score from 0.00 to 10.00.
**How cool is that!?**
It takes so much pain out of debugging potentially unknown problems.

In my opinion,
pylint has a great feature about its reporting that makes this cleanup fun:
It remembers previous runs
and shows side by side comparison of run metrics!
I can make changes to the file,
run the pylint command in another terminal
and watch my checklist of problems shrink and the score go up.
I continue this iterative process to get the satisfaction
of standardizing a file to goals of the project.

Is pylint worth it?
You bet it is.
People make mistakes when coding.
There are no perfect programmers.
The difference I see is that smart programmers will take advantage
of tools like pylint to make life simpler and code cleaner.
