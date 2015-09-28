%YAML 1.1
---
blog: False
title: 'dotfiles: Hone your software tools'
date: 2015-06-13T12:00:00Z
summary: Why I am refining my development tools and why you should too
template: writing.j2

---
<img class='book' src='axe.jpg'>

Something my dad taught me as a kid was to **use the right tool for the job**.

To use the right tool,
you need to *have* the right tool.
For a craft like carpentry,
collecting the right tools can be an expensive proposition.
For a software craftsman,
collecting the right tools is a matter of research and time.
Once you've found the best tool for a job,
how can you add it to your toolbox?
For that matter,
*what is the toolbox of a software craftsman?*

If a software craftsman's text editor,
shell,
and version control system
are the tools,
then **dotfiles** are the toolbox.
dotfiles are those files and directories
on your computer
that often begin with a `.` (clever name, eh?).
A dotfile holds configuration settings
for a piece of softare.
`.bashrc` is a well known dotfile
that stores settings for `bash`
like a custom `PATH`
or short aliases for frequently used commands.

To make dotfiles a useful and reusable toolbox,
I think you need to put them into a version control system
like Git.
The benefit of putting these files under version control
is that you can apply them anywhere
and be comfortable and efficient
on whatever computer you use.

For many years, I resisted this notion.
I reasoned that if I could know a system's defaults,
then I could be fast anywhere.
There are at least two fallacies in that thinking:

1.  Operating systems don't have the same defaults.
    Ubuntu is different from Fedora.
    Linux is different from OS X.
    Windows is different from everything.
2.  The tool authors did not write software
    specifically for the way I think.
    The fastest way I would do something
    may not be the fastest way they would do something.
