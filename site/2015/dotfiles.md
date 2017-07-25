%YAML 1.1
---
blog: True
title: 'dotfiles: Hone your software tools'
date: 2015-10-22T12:00:00Z
summary: >-
  Carpenters, painters, illustrators, and many other craftspeople
  collect tools
  over the years
  as their experience
  and skills grow.
  These tools help produce better work.
  Similarly,
  developers can create their own personal toolbox
  to perfect their craft.
  In this post,
  you can learn ways to manage your toolbox.
image: axe.jpg
template: writing.j2

---
<img class='book' src='axe.jpg'>

My dad taught me
that if I took care of my tools,
they would serve me well
and last a lifetime.
**Software tools are no different.**
If you give them attention,
they will serve you well.

Our primary tools as software craftspeople are
text editors,
shells,
and version control systems.
These tools are refined
via *dotfiles*.
dotfiles are those files and directories
on your computer
that often begin with a `.`
and hold configuration settings
for softare.
`.bashrc` is a well known dotfile
that stores settings for `bash`
like a custom `PATH`
or short aliases for frequently used commands.

Careful attention to your dotfiles
unleashes the full power of your tools.
With my dotfiles and two keystrokes,
I can run a full test suite
or a single unit test
or search my entire project
in a split second.
By studying these configuration files,
you learn all the options
that are available to you.

*How do I start taking advantage of these files?*,
you might ask.
Look at how others do it.
[http://dotfiles.github.io/](http://dotfiles.github.io/)
is a great resource to start.
This site contains plenty of example user repositories
and a collection of tools to control dotfiles
to get you going.
If you use Vim, Zsh, or Git,
you can take a peek at what I've done
to [my dotfiles](https://github.com/mblayman/dotfiles)
(you may also learn something even if you **don't** use those tools).

Don't chop down your next software project
with a dull axe.
*Hone your software tools.*
