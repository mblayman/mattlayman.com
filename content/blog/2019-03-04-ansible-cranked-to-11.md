---
title: "Ansible Cranked to 11"
description: >-
  On last week's Twitch stream,
  I added Mitogen
  to my Ansible deploy,
  and it dramatically improved how fast
  I could deploy to my site.
image: img/python.png
type: post
categories:
 - Python
 - Twitch
tags:
 - Python
 - Ansible
 - Mitogen

---

On the {{< extlink "https://www.twitch.tv/mblayman" "Building SaaS with Python and Django" >}} Twitch stream,
I tried out a new tool
to see if it would improve my deploy time.
We configured Ansible to use {{< extlink "https://mitogen.readthedocs.io/en/latest/ansible.html" "Mitogen" >}}
and it was an incredible success.

**With Mitogen, the Ansible deploy was 4.5X faster!**
Check out the YouTube video
to watch how quickly we could get Mitogen going.

<iframe width="560" height="315" src="https://www.youtube.com/embed/iZy4qC9ToAw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<!--more-->
