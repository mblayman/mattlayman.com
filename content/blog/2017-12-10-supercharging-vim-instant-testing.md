---
title: "Supercharging Vim: Instant testing"
description: >-
  Automated tests are extremely valuable
  when writing code.
  The faster you can get feedback
  that your code is correct,
  the quicker you’ll finish a task.
  In this post,
  learn how to run automated tests directly
  in your Vim editor
  and finish the job
  in record time.
image: img/2017/vim.png
type: post

---

> How do you know that your code works?

That's a surprisingly deep question
if you really dig into the meaning of "works,"
but from a practical level,
you can trust that code works
by verifying its behavior;
and a good way to verify is to write test code
that will assert
that the code behaves as expected.

In the second post
of this "Supercharging Vim" series,
we're going to explore how you can **run automated tests
within Vim**.
You'll feel like you have a new superpower
when you see test results appear
before you instantaneously.

If you dig this,
check out other posts
in the series.

1. [Using plugins](/2017/supercharging-vim-using-plugins.html)
2. Instant testing

## Not-so-instant testing

As a heavy user of Python,
a dynamic programming language
lacking some "guarantees"
that come with statically typed languages,
I write a lot of automated tests.

Automated tests give me the confidence
that my code is doing what I think it's doing.
For the times that the code is "misbehaving,"
my tests help me to narrow in
on the problem.

My process for writing code and test code used to look like this:

1. Write some test code.
2. Switch to a different terminal
   and run the test runner.
3. Switch back to Vim
   and write code that makes the test pass.
4. Repeat.

I would be in that process loop all day long.
Do you see the huge inefficiency
in that loop?
I was constantly *switching terminals*
between writing and running code.

Switching between writing and running code comes
with the territory of doing software development.
I learned early in my career
the benefit of running code frequently
as a technique
for catching errors.
My process problem was not the context switch itself,
but *how long* the switch took
because of the *terminal* switch.

Even aided by muscle memory for changing terminal tabs or windows,
I would have to find the right terminal,
get the test runner command from my shell's history,
and execute the runner.
To make things worse,
if I had to run a single test,
the result would be like:

```bash
$ nosetests myproject.tests.test_widget.TestWidget:test_feature
```

That's a lot of work to run some tests.
Shouldn't it be **easier** to run a single test
rather than harder?

As [Raymond Hettinger](https://twitter.com/raymondh) is prone to say:
*There must be a better way!*

## Testing *inside* Vim with `vim-test`

My former co-worker at Storybird,
[Ben Johnson](https://twitter.com/benjohnson),
introduced me to a Vim plugin called
[vim-test](https://github.com/janko-m/vim-test).
This plugin dramatically changed my relationship
with automated test tools.

If you followed the first post
and added [vim-plug](https://github.com/junegunn/vim-plug) to your `vimrc`,
then add vim-test
in your plugin section:

```vim
Plug 'janko-m/vim-test'
```

Run `:PlugInstall` to install vim-test.

Now you should be ready for some magic.
Open up a project,
navigate to a test file,
put your cursor inside a test method,
and run `:TestNearest`.

<div class="text-center">
<img src="https://media.giphy.com/media/EldfH1VJdbrwY/giphy.gif">
</div>

For those of you who aren't able to follow along,
Vim should have showed tests running
without having to switch terminals.
Even cooler than that,
vim-test figures out the exact test to run
so the results look similar to the
`myproject.tests.test_widget.TestWidget:test_feature`
command that I showed earlier.

After adding vim-test,
I experienced an immediate boost
in my productivity.
I discovered that the terminal switch not only took more time,
but it also negatively affected my mental flow.
With vim-test,
I could run a test,
see it pass,
and move on in the code
without feeling like I left my editor.
My brain got to stay focused on code,
and I think this is an extremely valuable benefit.

You can take vim-test a step further
by adding some custom key mappings
to quickly invoke longer commands
like `:TestNearest`,
`:TestFile`,
or `:TestSuite`.
I use the space bar as my `<Leader>` key
and give some mappings to
`<Leader>t`,
`<Leader>f`,
and `<Leader>s`.
These mappings let me run all kinds of tests
in two key strokes.
I think it really shows off Vim's power.

## Next time

vim-test is absolutely one
of the tools
that made my development flow faster.
In the next post,
we'll focus on another flow improvement tool
that does insanely fast file navigation
with fuzzy finding.

Next up: [ctrlp](http://ctrlpvim.github.io/ctrlp.vim/)
