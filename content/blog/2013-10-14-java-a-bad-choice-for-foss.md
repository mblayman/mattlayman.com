---
title: "Java: a bad choice for FOSS"
description: A description of the pain encountered with contributing to Java FOSS
image: img/2013/java.jpg
type: post

---
805MB. That's how much I had to download before I could even attempt to
contribute to an open source Java project.

Here's what I needed to get started: 197MB for Eclipse, 130MB for the JDK, 6MB
for Maven, 259MB for the dependencies (i.e. Maven's .m2 directory), and 213MB
for a bloated Git repo. Then I lost track when I started downloading additional
Eclipse plugins.

This. Is. Ridiculous.

I wish this was the only time I'd experienced such nonsense. Last year, I
fixed a bug in the Doxygen plugin for Jenkins. The bug was simple to fix, but
I had to go through the exact same silliness of downloading Eclipse, a JDK,
and a bunch of Maven stuff. It took me 10 minutes to write the unit test and
fix the problem. It took multiple hours of downloads on my fairly slow DSL
connection.

Clearly, if you already work with Java regularly and have Eclipse and a JDK,
then it may seem that I'm grumbling about nothing. However, *downloading
hundreds of megabytes just to make a simple fix is a **terrible** barrier to
entry*.

Healthy open source software lives on the contributions of individuals, but
the Java ecosystem makes it nearly impossible to get *quick* contributions
from people. Not everything can be a quick contribution, yet bite sized chunks
of work enable curious people to get involved. Because it took hours of setup
for the 805MB Java juggernaut, all my good will was spent. So when I hit some
issue with the Maven Checkstyle plugin not talking to the Eclipse Checkstyle
plugin, I declared defeat. I wanted to help, but my time is precious and I
don't feel like dealing with such friction.

My hat is off to those that tolerate such a bloated ecosystem and manage to
make progress for open source tools. I still love Jenkins. I just never want
to develop any of its code. Maybe I want the "F" in FOSS to stand for Fun.
