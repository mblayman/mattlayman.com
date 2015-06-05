%YAML 1.1
---
title: Oh, my shell? Oh My Zsh
template: writing.j2
date: May 28, 2015
---
<img class='book' src='omz.png'>

Do you ever think about what program is running your terminal?
For a long time,
I knew the answer for most Linux / OS X systems was [bash][bash],
a [shell][sh] program.
*But what else is available?*

Aside from the occasional script,
I didn't pay much attention to bash.
bash helped me get around my computer
and autocomplete stuff,
and that felt like enough.
This was **profoundly** shortsighted.

[bash]: http://www.gnu.org/software/bash/
[sh]: http://en.wikipedia.org/wiki/Shell_%28computing%29

Heavy command line users should think about their shell.
I finally devoted time to shell research,
and I became a [Zsh][zsh] convert.

[zsh]: http://www.zsh.org/

Zsh is the power user's weapon of choice.
It has an amazing [set of features][slides] that go far beyond bash.
For example, `cd ~/p/h` followed by a tab
will quickly expand to `cd ~/projects/handroll/`
on my computer.
Zsh is smart enough to determine what you mean
when you want to change directories
so you can type fewer characters.

[slides]: http://www.slideshare.net/jaguardesignstudio/why-zsh-is-cooler-than-your-shell-16194692

On top of Zsh being awesome, it also has some great tools
to extend its awesomeness.
One popular tool for the shell is [Oh My Zsh][omz].
OMZ offers many plugins and themes that make Zsh excel even more.
I've added the `git` and `virtualenvwrapper` plugins to my setup,
and they've already been a huge boon.
There are hundreds more.

[omz]: http://ohmyz.sh/

Want to try out Zsh? Go for it with these commands:

```bash
$ sudo apt-get install zsh
$ chsh -s /bin/zsh # Change shell to zsh.
$ curl -L \
    https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
```
