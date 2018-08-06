---
title: Semantic UI in Ember
description: >-
  Semantic UI is a popular styling framework
  for websites.
  I integrated Semantic UI
  in my Ember app
  and had an interesting experience
  with the process.
  I explain a bit of what I learned
  from that experience.
image: img/2017/ember.png
type: post
aliases:
 - /2017/semantic-ui-ember.html
categories:
 - Software
tags:
 - CSS
 - Semantic UI
 - Ember

---

For my SaaS app,
{{< extlink "https://www.collegeconductor.com/" "College Conductor" >}},
I made the choice to use
{{< extlink "http://emberjs.com/" "Ember" >}}
to power the frontend web client.
I also decided to use
{{< extlink "https://semantic-ui.com/" "Semantic UI" >}}
as the UI toolkit
to build the look and feel
of the site.
Integrating the two projects
into a single product
proved to be harder than I anticipated.
Let's look at why that happened.

My first decision when evaluating Semantic UI
led me to consider
if a viable Ember add-on existed.
The official Semantic UI project
points to
{{< extlink "http://semantic-org.github.io/Semantic-UI-Ember/#/modules" "Semantic-UI-Ember" >}}
as the default answer
for working with Semantic
in Ember.
Ultimately,
I concluded that the add-on wasn't right
for me.
Semantic-UI-Ember wraps many of Semantic's elements and views
into Ember components.
While I appreciate what they are trying to do,
I didn't really like that my project would always lag
behind the latest Semantic UI releases,
and that there was a whole extra layer of API
to learn.
The thought of bouncing between two different sets
of documentation
for my UI toolkit
did not appeal to me
at all.

After I ruled out Semantic-UI-Ember,
I decided to integrate the toolkit myself.
Semantic has packages that are available
via {{< extlink "https://www.npmjs.com/" "npm" >}}
in a variety of flavors.
Semantic is built with the
{{< extlink "http://lesscss.org/" "Less" >}} CSS preprocessor.
My goal was to make sure
that I could work with the Less-based files
and integrate into Ember's toolchain.
Because of that goal,
I chose the `semantic-ui-less` package.
This package offers all of the Semantic files
without its normal
{{< extlink "http://gulpjs.com/" "Gulp" >}} build process.
My logic was that Ember's Less integration
could build my Semantic theme
and be a seamless part
of my development workflow.
*Reality was not so kind.*

The biggest problem that I experienced
with `semantic-ui-less`
related to the project's expectations
about file locations.
The Less files from the package were stored
in the `node_modules` directory of my project.
Ember's tooling could handle this location,
but Semantic itself did not fare well.
I had a devilish time trying to convince Semantic
of the location of my theme.
Even when it did find the theme,
the paths weren't quite right
for Semantic to use its overriding mechanism properly.
The fallout of that
was that I had to directly modify the theme
to get the styling that I wanted.
I felt stuck with a mediocre integration.
To make matters worse,
the Ember development server would sometimes throw errors
when I changed a Less file.
I'd have to restart the development server
and lose the benefit of having it integrated.

I finally decided to keep my use of Semantic separate
from my Ember toolchain.
By switching to the `semantic-ui` package,
I could get the Gulp toolchain
that the project expects.
My Semantic files get stored
in my app's `vendor` directory
and I set the Ember configuration
to pull in Semantic's built version.
Making this switch resulted
in a less integrated experience,
but it dramatically simplified working with the two projects.

My lesson with this process
is to be wary of immediately trying to integrate two technologies,
especially when you're not experienced with *either*
when you start.
By keeping the projects separated,
I now have additional complexity
in my deployment process.
Thankfully, my Ansible scripts can readily handle that
so I'm ok with the tradeoff.
This whole experience is an example
of where I failed to follow some sage advice,
*{{< extlink "http://wiki.c2.com/?DoTheSimplestThingThatCouldPossiblyWork" "do the simplest thing that could possibly work" >}}*.
