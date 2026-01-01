---
slug: test-driven-development-woes
title: "Test Driven Development woes"
date: 2008-04-01
description: >-
  This post reviews Test Driven Development: By Example.
  I struggled with using the material
  in the context
  of a complex legacy system without tests.
image: img/2008/tdd.jpg
categories:
 - Book reviews
tags:
 - TDD

---


I just finished reading Kent Beck’s *Test-Driven Development: By Example*, and,
while I enjoyed the examples in the first half of the book,
I’m disappointed about the lack of discussion on dealing with “legacy” code.

In my short amount of time using Test-Driven Development (TDD),
I have seen that it can be a great, confidence building tool;
and it has enabled the Entertainer devs to iron out some major issues in the code base
(e.g., video thumbnailing was done entirely by Paul by following the TDD principles).
However, I have struggled with retroactively applying TDD and unit testing to preexisting code.

I have literally lost sleep thinking about how to isolate tests
and break coupling of existing classes.
My hope was that Beck’s book would provide some answers.
Instead, I got “There is a whole book (or books) to be written about switching to TDD
when you have lots of code.
What follows is necessarily only a teaser.”
His “teaser” basically stated that there is a Catch-22
of “refactoring would result in errors because there aren’t tests,
and tests can’t be written because the code isn’t refactored for it” (paraphrased).
And his advice is essentially to try your best to break it.
The entire subject gets about a page in the book.

Would I recommend reading Beck’s Test-Driven Development? Sure.
It’s a good introductory read to understanding the core principles
of “test-first” unit testing.
The first half of the book offers some great,
relatively simple examples that most developers should have no trouble following.
The second half does disappoint, however,
as it seems more like half-baked refactoring advice instead
of tackling really challenging problems that could be addressed
(like what to do with preexisting code or GUIs).

I’ll be reading Fowler and Beck’s *Refactoring: Improving the Design of Existing Code* next
to see if I can get some answers to the questions that I desperately want;
even if that advice is set outside of the unit testing/TDD mentality.
