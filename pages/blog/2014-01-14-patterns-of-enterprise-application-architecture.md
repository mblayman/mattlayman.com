---
slug: patterns-of-enterprise-application-architecture
title: Patterns of Enterprise Application Architecture
date: 2014-01-14
description: A review of "Patterns of Enterprise Application Architecture"
image: img/2014/eaa.jpg
aliases:
 - /2014/patterns-of-enterprise-application-architecture.html
categories:
 - Book reviews
tags:
 - Patterns

---

*Active Record*. *Unit of Work*. You may have heard of these before. They are
software patterns adopted by popular projects like [Ruby on Rails](http://rubyonrails.org/)
or [SQLAlchemy](http://www.sqlalchemy.org/).
These popular patterns are described in Martin Fowler's *[Patterns of Enterprise Application Architecture](http://martinfowler.com/books/eaa.html)* book.

*Two-Step View*. *Table Module*. *Transform View*. There is a good chance
you've never heard of these software patterns, but they are also in Fowler's
book.

Good patterns and not-so-good patterns is my theme for this book.

*Patterns of Enterprise Application Architecture* lacks the same impact as
other patterns books that I have read (e.g.,
[GoF](http://en.wikipedia.org/wiki/Design_Patterns) or [XUnit Test Patterns](http://xunitpatterns.com/)).
Some of the patterns in the enterprise
book are meaningful, yet others feel very dated or are anti-patterns for
current development. The book was written in 2002, and it is clearly missing
developments on the web from the last decade. I grimaced a few times with some
of the patterns described in the web section. For instance, with all the big
data analysis of the modern web, it's unlikely that the extensive focus on
relational databases is as important now as it was then. Many of the patterns
had an implied view that relational databases would be used, but relational
databases are not the only storage systems in the current enterprise ecosystem.
I know Fowler indicated that he wasn't trying to tackle concurrency patterns
or asynchronous patterns, but that kind of development is critical to a lot of
systems today.

Now that more than a decade has passed, I think it is possible to identify
which patterns left a lasting impact on the software community and which
didn't. Look at the [list on Fowler's website](http://martinfowler.com/eaaCatalog/) and do some homework on them.
*Patterns of Enterprise Application Architecture* is a decent reference book,
but you can probably get better explanations on the web.
