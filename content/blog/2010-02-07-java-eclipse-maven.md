---
title: "Java, Eclipse, and Maven altogether"
description: >-
  This post focuses on my experience
  of setting up Java projects
  using the most popular tools available.
image: img/2010/java.png
type: post
categories:
 - Guide
tags:
 - Java
 - Eclipse
 - Maven

---

I’ve never really spent time with Java.
My experience with the language was limited to examining Java code
in books on design patterns.
I am now taking a class at Johns Hopkins University that uses Java,
so it was time for me to learn how to work with the language.
This post describes my initial experience with the Java environment
and points a new user to some good tools that are used by “enterprise” Java developers.

My employer produces a lot of Java code for its customers.
I have many co-workers who use Java regularly, and,
in my conversations with them,
I’ve heard of some popular tools that make Java development easier.
The two primary tools seem to be:

* {{< extlink "http://www.eclipse.org/" "Eclipse" >}}, an Integrated Development Environment (IDE),
* and {{< extlink "http://maven.apache.org/" "Maven" >}}, a project management/build tool.

Also, {{< extlink "http://m2eclipse.sonatype.org/" "M2Eclipse" >}}, which integrates Maven and Eclipse, comes highly recommended by my peers.

With these tools, I set up a “Hello World!” application on Ubuntu 9.10.
Some of the steps turned out to be easy,
while others were surprisingly annoying and tedious.
Hopefully, this post can help a new Java developer avoid those stumbling blocks.

First, install Eclipse and Maven: `sudo apt-get install eclipse maven2`.

Second, install the M2Eclipse plugin.
The free M2Eclipse PDF book gives instructions about how to install the plugin
from inside Eclipse’s software manager.
One gotcha that I ran into was needing a JDK (Java Development Kit)
for Eclipse to use when installing M2Eclipse.
Ultimately, I just needed to install openjdk (`sudo apt-get install openjdk-6-jdk`).
Eclipse switched to the JDK because the act of installing openjdk changed the symlink
that `/usr/bin/java` pointed to.
To check which Java is being used, execute `sudo update-alternatives --config java`
(note: that’s two dashes before config).

Once the JDK is installed,
use the Eclipse software manager under “Help -> Install New Software…”
to install the dependencies listed in the M2Eclipse book.
This stage was pretty annoying because Eclipse can’t resolve dependencies, but it had to be done.

Next, create a project within Eclipse using Maven.
To do this, select “File -> New -> Project…” and go to the new Maven section.
Select “Maven Project” and move through the wizard until Maven asks about archetypes.
What are archetypes?
Archetypes are basically project templates with certain conventions for consistency
in Maven projects.
Select the archetype with ArtifactId `maven-archetype-quickstart` to create a basic project.

Now right click the package in the Package tree,
and select a Maven action (a.k.a. goal) from the “Run As” menu.
“Maven package” will create a jar in the target directory.
However, if you try to run that with `java -jar <your-jar-name-here>`,
it will fail because the jar can’t find the `main()` method.
To fix that problem, follow {{< extlink "http://jean-francois.im/2008/02/why-maven-2-rocks.html" "Jean François’ instructions" >}}
(look for the section about build plugins).

This was a condensed walk-through for making a project in Eclipse with Maven.
Virtually everything listed here can be found in the documentation listed
at each tool’s respective site.
If you have questions,
leave a comment and I’ll try my best to answer.
The benefits of using Maven and Eclipse are numerous,
but suffices to say it should now be possible to handle Java dependencies well
in a robust IDE.
