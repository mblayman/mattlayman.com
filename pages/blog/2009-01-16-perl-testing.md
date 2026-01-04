---
slug: perl-testing
title: "Perl Testing: A Developer’s Notebook"
date: 2009-01-16
description: >-
  How can you get better at testing in Perl?
  This post reviews a book
  that focuses on automated testing in Perl.
image: img/2009/perl-testing.jpg
categories:
 - Book reviews
tags:
 - Perl
 - Testing

---

I just finished reading [Perl Testing: A Developer’s Notebook](http://oreilly.com/catalog/9780596100926/)
by Ian Langworth and chromatic
(yes, one of the authors identifies himself/herself as “chromatic,”
presumably for privacy concerns).

All in all, the book was eye opening in understanding the world of testing in Perl.
I develop Perl code at work in a culture that does not focus on unit testing,
but, equipped with the things that I learned from this book,
I am now even more adamant that I will be creating unit tests for all of my future Perl code.

Unlike Python’s core testing library, `unittest`,
which is focused on objects and test methods,
Perl’s core testing libraries, `Test::Simple` and `Test::More`,
are focused on procedural style testing.
As a consequence of being procedural,
Perl test code has a style that reads very differently from a Python test case,
and it is this style that was so eye opening about the Perl Testing book.
The style difference isn’t a bad thing, it just requires some mental adjustment shifting.

Perl Testing is written in a no-nonsense manner that jumps straight to a solution
for how to solve some hard problems when testing Perl.
Personally, I think that the book’s style makes the material such a useful resource
when considering how to test a problem.
The Perl community likes to say TIMTOWTDI,
which means “There is more than one way to do it,”
but sometimes there are too many ways to do something.
Langworth and chromatic provide lots of solid examples
of how to test things so that you,
as a future Perl test code author,
will not have to recreate the logic necessary to test some really challenging code.

The book isn’t perfect,
but the overall quality of the material,
and the incredibly helpful libraries that it introduces,
makes *Perl Testing: A Developer’s Notebook*
a valuable resource for any Perl developer
who wants to test his code (which should be every Perl developer).
