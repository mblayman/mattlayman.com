---
slug: pygments-lexer
title: Highlighting new file formats with Pygments
date: 2015-09-03
description: >-
  How do text editors and other tools make code look pleasant
  with colors?
  We'll explore ways to colorize code
  by looking at Pygments,
  a "syntax highlighter,"
  and how the tool does its job.
image: img/2015/pygments.png
aliases:
 - /2015/pygments-lexer.html
categories:
 - Python
tags:
 - Pygments
 - syntax highlighters

---

I want pretty documentation for my [tappy](http://tappy.readthedocs.org/en/latest/) project,
and syntax highlighting code samples helps make software documentation pretty.
For tappy,
code samples can include Python
or [Test Anything Protocol (TAP)](http://testanything.org/) output.
Unfortunately, the syntax highlighter for tappy's documentation, Pygments,
did not know how to highlight TAP.
That smelled like a fun project to me.

If you read the [Pygments documentation](http://pygments.org/docs/),
eventually you'll learn that adding a new filetype
means writing a new *[lexer](http://pygments.org/docs/lexerdevelopment/)*.

A lexer's job is to parse data
and break it into tokens.
Tokens are the abstract objects that you might expect
in a programming language.
Some examples within Pygments include a `Comment`, `Number`, or `Operator`.
Once a lexer breaks data into tokens,
those tokens can be passed to a formatter
for stylizing output.
For instance,
a formatter might color every `Keyword` token green.

Pygments' primary tool for creating new lexers
is to use its `RegexLexer` and subclass it.
With this lexer,
you define a series of [regular expressions](https://en.wikipedia.org/wiki/Regular_expression)
and map them to tokens.
Here is an example for TAP comments:

```python
(r'^#.*\n', Comment),
```

TAP comments are lines that start with a hash character, `#`.
The regular expression matches that pattern
and pairs matching content to a `Comment` token.

That's the core concept for the lexer,
but there is more fun to have!
There is another layer within this parsing process.
If everything could be matched with a set of regular expressions,
then the job would be over,
but languages often have context
that change the meaning of the source data.
A contrived example would be the `if` characters.
In one context, `if` should be a `Keyword` token.
In another context, `if` may be part of a `String` token like
"*if* I exercise, then I can stay healthy."

The `RegexLexer` allows developers to handle these context changes
by providing a [stack](https://en.wikipedia.org/wiki/Stack_%28abstract_data_type%29).
When a regular expression matches a certain pattern,
it can trigger a context change
and push onto the stack.
In the new context,
the lexer moves to a different set of regex patterns
that makes sense for that context.
When the context ends,
the stack is popped
and the lexer goes back to working with the original regex patterns.

If you're trying to absorb how this all works,
I think you should take a look at the [full source](https://bitbucket.org/birkenfeld/pygments-main/src/7941677dc77d4f2bf0bbd6140ade85a9454b8b80/pygments/lexers/testing.py?at=default&fileviewer=file-view-default)
of the `TAPLexer`
*(Update: this lexer was merged
into Pygments
so the code now lives
in the Pygments code
instead of tappy)*.
I took care to document it well,
and you can see the context shifts
as the lexer moves from `root` to `plan`
or `root` to `test`.

Now that you're equipped,
go forth and make a new lexer of your own!
Also, you can check out the [huge array of lexers](http://pygments.org/docs/lexers/)
already defined in the Pygments project
if you want to study the work of others.
