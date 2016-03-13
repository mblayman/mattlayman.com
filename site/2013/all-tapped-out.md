%YAML 1.1
---
blog: True
title: When you're feeling all TAPped out
date: 2013-09-04T12:00:00Z
summary: An explanation of the Test Anything Protocol (TAP)
template: writing.j2

---
<img class='book' src='tap.png'>

Good software practices say you should do automated testing, but what do you do
when you work in an environment that can't get good test tools? Use a simple
testing protocol like TAP.

TAP is the *Test Anything Protocol*. The protocol is so simple that you could
probably write code to make TAP output in minutes. It is a line based protocol
which means that any language that has some sort of print method can generate
TAP. That's basically all software languages in common use.

I could provide the rules, but an example would be easier.

```tap
# This is a comment because it starts with a hash symbol.
ok 1 Something passed here.
not ok 2 Whoops, there was a failure.
When there is a line that TAP does not understand (like this one), it will skip it.
# TAP files should have a plan in the format of "1..<some number of tests>".
1..2
```

The key to the protocol is `ok` and `not ok`. When lines start with one of
these two phrases, TAP readers will interpret it as a pass or failure. Besides
the test number, everything else on the line is extra. Toss in how many tests
were run and you have fully functional TAP output. We can prove it with
Perl's aptly name `prove` tool.

```console
matt@eden:~$ prove sample.tap
sample.tap .. Failed 1/2 subtests

Test Summary Report
-------------------
sample.tap (Wstat: 0 Tests: 2 Failed: 1)
  Failed test:  2
Files=1, Tests=2,  0 wallclock secs ( 0.01 usr +  0.00 sys =  0.01 CPU)
Result: FAIL
```

Once you have some TAP results from your awesome homegrown test suite, you can
get them into a TAP reader like the [Jenkins
plugin](https://wiki.jenkins-ci.org/display/JENKINS/TAP+Plugin) or a specific
tool like [Tapper](http://tapper.github.io/Tapper/).

There are some additional features that I did not discuss here (like TODO
tracking). See the [TAP website](http://testanything.org/) for more details.
More adventurous individuals can check out the specifics by looking at the de
facto parser, [TAP::Parser](http://search.cpan.org/~ovid/Test-Harness-3.28/lib/TAP/Parser.pm), on Perl's CPAN.
