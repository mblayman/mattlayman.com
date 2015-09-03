%YAML 1.1
---
blog: True
title: Highlighting new file formats with Pygments
date: 2015-09-03T04:00:00Z
summary: Creating syntax highlighting for a new filetype using Pygments
template: writing.j2

---
<img class='book' src='pygments.png'>

I want pretty documentation for my [tappy][tappy] project
and syntax highlighting code samples helps make software documentation pretty.
For tappy,
code samples can include Python
or [Test Anything Protocol (TAP)][tap] output.
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
you define a series of [regular expressions][regex]
and map them to tokens.
Here is an example for TAP comments:

[regex]: https://en.wikipedia.org/wiki/Regular_expression

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
by providing a [stack][stack].
When a regular expression matches a certain pattern,
it can trigger a context change
and push onto the stack.
In the new context,
the lexer moves to a different set of regex patterns
that makes sense for that context.
When the context ends,
the stack is popped
and the lexer goes back to working with the original regex patterns.

[stack]: https://en.wikipedia.org/wiki/Stack_%28abstract_data_type%29

If you're trying to absorb how this all works,
I think you should take a look at the [full source][taplexer]
of the `TAPLexer`.
I took care to document it well,
and you can see the context shifts
as the lexer moves from `root` to `plan`
or `root` to `test`.

[taplexer]: https://github.com/mblayman/tappy/blob/master/tap/lexer.py

Now that you're equipped,
go forth and make a new lexer of your own!
Also, you can check out the [huge array of lexers][lexers]
already defined in the Pygments project
if you want to study the work of others.

[lexers]: http://pygments.org/docs/lexers/
