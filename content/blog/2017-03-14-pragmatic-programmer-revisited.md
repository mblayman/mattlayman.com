---
title: The Pragmatic Programmer revisited
description: >-
  The Pragmatic Programmer is one
  of the most influential books
  in my professional career.
  With more than seven new years of experience
  since my first reading,
  I re-read the book to compare it to my journey
  as a software professional.
image: img/2017/prag-prog.jpeg
type: post
aliases:
 - /2017/pragmatic-programmer-revisited.html

---

*The Pragmatic Programmer* is an excellent book.
Top notch.

The book shaped how I think about writing software
and established a mental framework
for getting code developed
in an effective manner.
I recently decided to revisit the book
since seven years passed
from my initial read-through.
Now that I have much stronger feelings about software,
forged from my personal experience,
I was curious how the advice described
in the book
jived with my own thoughts.
I also wanted to see
how well the advice fit
into the software world
of 2017.

After so much time has passed,
does this book from 1999 still matter?
**Yes,
it does.**

The key to this continued relevance is a focus
on principles over specific practices.
There are specific practices and code samples sprinkled
throughout the text,
but they exist to support
a principle topic
instead of being the main focus.
The emphasis on principles creates a timelessness
to the material
in spite of the text being full
of references to older technology
like [CVS](https://en.wikipedia.org/wiki/Concurrent_Versions_System).
These principles cover a sprectrum
from generating code
to metaprogramming
to working with client expectations.

After so many years away
from the material,
my favorite principle continues to be the section entitled *Tracer Bullets*.
When I first read the book,
I was working for a large defense contractor.
The culture at work dictated a heavy process
with an emphasis
on a [waterfall methodology](https://en.wikipedia.org/wiki/Waterfall_model).
Tracer bullets made my brain explode
(not literally, thankfully)
when considering how software *could* be developed.
The section is best read to get a full appreciation
of the idea,
but the core concept is that
*software can be implemented
in an a way that generally points toward the client's goal
and honed in
until it strikes the target*.
This method is in contrast
to the meticulous planning and calculating
that would be required
to reach the goal on the first shot.
As someone who spent his time
considering the mission software
of satellite systems,
the idea of quick and cheap iteration was mind bending.
Maybe this idea is self-evident
for someone working in a web startup space,
but it was ground breaking
for a young guy steeped in a process heavy culture.

Where is the book lacking today?
In my mind,
the biggest difference is in the pace
of development.
For instance,
we encounter the suggestion to do *nightly* builds.
This was great advice for the time.
Integration was hard in older version control tools
and compilation could take much longer
than on today's hardware.
In modern development,
we use Continuous Integration services
like [Travis CI](https://travis-ci.org/)
to make sure our code is integrated far more than nightly.

I think I would also actively tell other developers
to be cautious with the appendix of resources.
There are definitely great suggestions in there
(like [Python](https://www.python.org/)).
On the other hand,
many suggestions are likely eclipsed
by more modern tools.
You might want use [Lua](https://www.lua.org/)
as an alternative to the book's suggestion
of [Tcl](https://www.tcl.tk/)
for an embedded programming language,
for example.

*The Pragmatic Programmer* isn't aging perfectly,
but it still does an amazing job
of showing developers a way
of thinking about development
that is,
well,
pragmatic.
It is a book that you should be sure to read.
*[Read it](https://pragprog.com/book/tpp/the-pragmatic-programmer).*
Seriously.
