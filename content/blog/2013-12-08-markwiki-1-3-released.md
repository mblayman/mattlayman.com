---
title: MarkWiki 1.3 released
description: MarkWiki 1.3 release announcement
image: img/2013/allthethings.jpg
type: post
aliases:
 - /2013/markwiki-1-3-released.html

---
MarkWiki 1.3 is now packaged and uploaded to
[PyPI](https://pypi.python.org/pypi/MarkWiki). This release includes two
notable features.

1. MarkWiki now has a built-in search engine. All wiki pages are indexed by
   the search engine whenever pages are added, modified, or deleted. This
   should be a big boon to finding relevant information. The new search engine
   is powered by [Whoosh](http://whoosh.readthedocs.org/en/latest/intro.html),
   a pure Python search tool, so there is no need to install search tools from
   other languages.
2. New users can self-register on a MarkWiki installation that uses
   authentication. MarkWiki 1.2 required an administrator to create new
   accounts. That restriction worked, but it was not scalable for larger
   instances.

You can install this version with:

```console
$ pip install MarkWiki
```

The user documentation is available at
[pythonhosted.org](http://pythonhosted.org/MarkWiki/). The developer
documentation is at [Read the
Docs](http://markwiki.readthedocs.org/en/latest/). You can also track the
source code directly on [GitHub](https://github.com/mblayman/markwiki).

Thanks to Lukas Michelbacher for pointing out that the 1.2 release had broken
packaging (and sorry to anyone that affected). I've taken steps to help avoid
situations like that by using continuous integration for MarkWiki via [Travis
CI](https://travis-ci.org/mblayman/markwiki). I hope this helps future
releases maintain high quality.

Have fun!
