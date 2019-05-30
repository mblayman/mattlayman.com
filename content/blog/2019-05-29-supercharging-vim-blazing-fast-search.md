---
title: "Supercharging Vim: Blazing fast search and global replace"
description: >-
  Vim has good built-in search features.
  We can turn them into great search features
  and supercharge our workflows
  with some plugins
  and settings changes.
  Learn how to make your searches lightning fast.
image: img/2017/vim.png
type: post
categories:
 - Guide
tags:
 - Vim
 - ripgrep
 - search
 - replace
 - quickfix-reflector

---

> What do you do when you need to search
in all the files
in your project?
Can you do it faster
than the default Vim configuration?
**Yes, absolutely.**

In the fourth article
of the Supercharging Vim series,
we're going to look at searching
and how to be effective
*and fast*
using search tools built
for a Vim workflow.

If you want to check out other articles
in the series,
you can follow any
of the links below.

{{< vim-series "search" >}}

## Searching Elsewhere

If you work with a web browser
or a different text editor,
then you may expect `Ctrl+f`
to bring up a search menu.
Since those other tools tend to be more graphical,
you might get some pop-up menu
with a dialog box
and a bunch of options.
That's not the Vim way of things.

Trying `Ctrl+f` will surprise you
with its behavior
(**pop quiz**: what *does* `Ctrl+f` do in Vim? Run `:help CTRL-F` for the answer OR try it out!)
If that's not the way to search
for stuff
in files,
what do you do?

## Default Vim Searching

Vim has two separate methods
to search
out-of-the-box: `:vimgrep` and `:grep`
(note: I'm using `:` to show
that these are editor commands
that you execute within Vim.
The goal is to help prevent confusion
since we're going to look at external tools
that share the same name).
I don't know the history
to explain why there are two,
but I'd guess it has to do
with the availability
of the `grep` program.

`grep` is an early Unix-era tool
that lets you search
through files
on the command line
(in fact, its name means "**g**lobally search a **r**egular **e**xpression and **p**rint").
The primary difference between `:vimgrep` and `:grep`
is whether Vim will call out
to the `grep` program or not.

`:vimgrep` is a Vim implementation
of grep functionality.
It uses Vim's internal features
to implement file searching.
In contrast,
`:grep` passes a search query
off to the `grep` program
to do the heavy lifting.

I think the differences in experience are minor.

1. `:vimgrep` has a slightly nicer user experience
    since it's native to Vim.
2. `:grep` is faster
    because developers have heavily optimized the `grep` program
    over the course
    of the last 44 years.

If I wanted to search for `Python`
in all of my project files,
the invocations for each would look like:

```vim
:vimgrep Python **
```

and

```vim
:grep -r Python *
```

With `:vimgrep`,
the command uses `**` to recurse
into all the directories
of my project.
When using `:grep`,
you must use `grep` flags
to get the right behavior.
That means that the command required `-r`
to do a recursive search.

The results from either method
of searching are put into the quickfix list.
The quickfix list is roughly like a scratch pad
in Vim.
When you run the search,
Vim will take you to the first result,
but the full list is available
for browsing.

To see that list of results,
you must show the quickfix list.
This is possible with `:cwindow`.
Running `:cwindow` opens
the quickfix list
in a new split.
You can navigate to the split
using something like `Ctrl+w j`
(`Ctrl+w` is the method
for getting to a variety of window commands.
Try `:help CTRL-W` for more details
within Vim).

One thing I love about the quickfix list is that it acts
like any other Vim buffer.
That means you can go to the quickfix list
and do slash (`/`) searches
on the search results!
I think this is a super handy method
of further refining searches.

The quickfix list also has the ability
to track which item you're on
in the list.
If you don't want to look
at the quickfix list directly,
you can go through each search match individually
by using `:cnext` to go to the next item
and `:cprev` to go to the previous one.

I hope you'll agree with me
that the built-in search features
of Vim
are already pretty awesome.
Now let's look at how we can make them even better.

## Supercharged Vim Searching

Don't get me wrong, `grep` is great.
You can depend on it being on nearly any Linux or macOS system,
and it will chew through data very quickly
to find what you're looking for.
With that said,
it's not the fastest game in town,
and it's missing some features
which are valuable to developers.

One big issue with `grep` is that
it is *not aware of version control systems
by default*.
This will be really obvious
if you've ever tried to grep
(yeah, developers use it as a verb)
through a JavaScript project
with a big `node_modules` directory.
Since `grep` doesn't pay attention
to version control systems,
it doesn't consider your `.gitignore` file
and will search in areas
that aren't your code,
like `node_modules`.
Unless you explicitly want to search
in a directory such as `node_modules`,
this is usually a waste of time
and adds a bunch of messy search results
that you don't need
in  your list.

To address issues like this,
developers made new search tools.

### ripgrep

Maybe you've heard about Rust.
If you haven't,
Rust is a new language
from Mozilla
that is akin to C,
but it has some excellent language features
that makes code written
in Rust
super fast.

{{< extlink "https://github.com/BurntSushi/ripgrep" "ripgrep" >}}
is a version of `grep`,
written in Rust.
I've actually mentioned ripgrep
in this series already.
In the [Navigate files instantly]({{< ref "/blog/2019-03-20-supercharging-vim-navigate-files-instantly.md" >}}) article,
we used ripgrep
as the engine
to power CtrlP,
the fuzzy file finder.

I may be repeating myself,
but it's worth discussing again:
**ripgrep is fast,
stupidly fast**.
Because I know you're probably a sucker
for benchmarks,
check out ripgrep's
{{< extlink "https://blog.burntsushi.net/ripgrep/" "performance benchmarks" >}}
for an very thorough read
of how ripgrep compares
to other similar tools.

If you don't have time to read through it all,
just remember:

> ripgrep is fast, stupidly fast.

It's time to get ripgrep
into Vim.
First, we must install ripgrep.
You can install with `brew install ripgrep`
if you're on macOS,
or check out the {{< extlink "https://blog.burntsushi.net/ripgrep/#installation" "ripgrep installation options" >}}
to see how to get it for your platform.
By the way, doing this has the very nice side effect
of adding `rg`
to your terminal PATH
so you can use ripgrep
for those times that you're outside of Vim too.

On the Vim side,
we're going to use {{< extlink "https://github.com/jremmen/vim-ripgrep" "vim-ripgrep" >}}.
Assuming that you're using [vim-plug]({{< ref "/blog/2017-11-22-supercharging-vim-using-plugins.md" >}}), add the plugin to your `vimrc` with:

```vim
Plug 'jremmen/vim-ripgrep'
```

Once the plugin is installed and available,
we have a new command at the ready, `:Rg`.
The earlier `grep` search of `:grep -r Python *`
boils down to:

```vim
:Rg Python
```

This is shorter to type
and will return results faster too!
**Double win!**
Another noteworthy call out is that `:Rg`
will automatically open the quickfix list
and put your cursor at the first line
on the list.
I think this behavior
is way more natural
than hiding the quickfix list
and switching your active buffer
to the first search result
as both `:vimgrep` and `:grep` do.

There is one configuration tweak that I like to make
to this plugin.
ripgrep is case sensitive by default,
but it has an excellent mode called "smart case"
which is very useful.
With smart case turned on,
if you do a search using all lowercase letters,
ripgrep will do a case insensitive search.
If you use any capital letters,
it assumes that you want that specific query
and will keep it case sensitive. Neat!

In most of my searches,
being lazy and using lowercase is easier
and usually does exactly what I want.
To get smart case,
we have to set `rg` command flags.
My full configuration
for this plugin looks like:

```vim
Plug 'jremmen/vim-ripgrep'
let g:rg_command = 'rg --vimgrep -S'
```

The `-S` is the flag to ripgrep
that enables smart case mode.

We've now supercharged our Vim searching.
What more can we do
to make searching
even more powerful?
Let's look at bulk updates.

## Bulk updates with quickfix-reflector

In certain circumstances,
you may want to do a big find and replace operation.
That operation may be something silly
like updating the copyright year
in all your source files.
Or perhaps you have a serious refactoring to do
that touches code that is all over the place.

For a long time,
I thought this was a weaker area in Vim.
As we saw above,
it's painless
to do a fast search,
but how do you edit those results?

The natural answer is to iterate through the quickfix list
and update each instance with your change.
Unfortunately, the weakness of this approach
is that you are editing one instance
at a time.
Surely there is a way to do bulk updates!

My old solution to bulk updates felt very *magical*.
It looked like this:

* Do a search to populate the quickfix list
    with the thing I wanted to change.
* Start recording a macro that would:
    1. Go to the next quickfix item.
    2. Make the change.
    3. Write the file.
    4. *Call the macro.*
* Stop recording the macro.
* Run the macro.
    The macro would then call itself continuously
    until there were no more items
    in the quickfix list.

While clever,
that's a lot of work for a find and replace.

At PyCon this year,
{{< extlink "https://twitter.com/mattboehm" "Matt Boehm" >}}
blew my mind
at a Vim open space
when he introduced the group
to {{< extlink "https://github.com/stefandtw/quickfix-reflector.vim" "quickfix-reflector" >}}.

quickfix-reflector works
by making the quickfix list editable.
If you try to edit something
in the quickfix list
without quickfix-reflector,
you'll get an error stating:

```
E21: Cannot make changes, 'modifiable' is off
```

This error is because the quickfix list
was not designed to handle edits.
The brilliant idea
of quickfix-reflector
is to change the list
to be editable.
When you write
to the quickfix list
with quickfix-reflector enabled,
it will **reflect** those changes
back to the files
that the quickfix list lines points to.

Knowing this,
what does a global find and replace look like
with quickfix-reflector on?
Let's say you have a project,
have fallen out of love with Python,
and want to express your undying devotion
to Ruby. [^1]
To change all occurrences of `Python` to `Ruby`,
you can:

[^1]: Hey, I didn't say this was going to be a realistic example! 😛

* `:Rg Python` - Search for every mention of `Python`.
* `VG` - Visually select all the lines in the quickfix list.
* `:s/Python/Ruby/g` - Substitute `Python` for `Ruby` globally.
* `:w` -
    Write the quickfix list to reflect those changes
    out to each individual file.

I think that is a very reasonable workflow.
It's essentially three steps:

1. Search for a pattern.
2. Change the pattern instances.
3. Save the changes.

That flow has none of the recursive shortcomings
of my previous "magical" method,
and it doesn't require me to edit matches one by one.

There's another feature
of quickfix-reflector worth highlighting:
**you can delete lines
from the quickfix list.**

This is a great addition
because you can search
for a rough pattern,
manually trim out some lines
that you didn't want,
then execute your find and replace
on the remaining lines
in the list.
I think this would be a lot faster
than trying to devise a perfect search regex
to get the exact quickfix list.

## Recap

This article is all about making your Vim search experience better.
We achieved this
with a one-two punch
from two different tools:

* ripgrep for blazing fast searching
* quickfix-reflector for blazing fast replacing

Equipped with these tools,
you can demolish tasks
that Vim might struggle with out-of-the-box.

If you liked this article
and learned something along the way,
would you do me a favor
and share it on Twitter
or your favorite social media
so that other have the chance to learn something too?
Also, please check out my other articles
in this series
for more strategies to supercharge your Vim editing.

{{< vim-series "search" >}}

**Thanks for reading!**
