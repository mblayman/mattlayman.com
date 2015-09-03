%YAML 1.1
---
blog: True
title: Highlighting new file formats with Pygments
date: 2015-09-02T08:00:00Z
summary: Creating syntax highlighting for a new filetype using Pygments
template: writing.j2

---
<img class='book' src='pygments.png'>

I want pretty documentation for my [tappy][tappy] project and
syntax highlighting code samples helps make software documentation pretty.
For tappy,
code samples can include Python or
[Test Anything Protocol (TAP)][tap] output.
Unfortunately, the syntax highlighter for tappy's documentation, Pygments,
did not know how to highlight TAP.
That smelled like a fun project to me.

[tappy]: http://tappy.readthedocs.org/en/latest/
[tap]: http://testanything.org/

If you read the [Pygments documentation][pygments],
eventually you'll learn that adding a new filetype
means writing a new [*lexer*][lexer].

[pygments]: http://pygments.org/docs/
[lexer]: http://pygments.org/docs/lexerdevelopment/

A lexer's job is to parse and recognize data and
break it into tokens.
Tokens are the abstract objects that you might expect
in a programming language.
Some examples within Pygments include a `Comment`, `Number`, or `Operator`.
Once a lexer breaks data into tokens,
those tokens can be passed to a formatter
for stylizing output.
For instance,
a formatter might color every `Keyword` token green.
