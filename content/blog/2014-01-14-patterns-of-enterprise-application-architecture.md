---
title: Patterns of Enterprise Application Architecture
description: A review of "Patterns of Enterprise Application Architecture"
image: img/2014/eaa.jpg
type: post
aliases:
 - /2014/patterns-of-enterprise-application-architecture.html
categories:
 - Book reviews
tags:
 - Patterns

---
*Active Record*. *Unit of Work*. You may have heard of these before. They are
software patterns adopted by popular projects like {{< extlink "http://rubyonrails.org/" "Ruby on Rails" >}}
or {{< extlink "http://www.sqlalchemy.org/" "SQLAlchemy" >}}.
These popular patterns are described in Martin Fowler's *{{< extlink "http://martinfowler.com/books/eaa.html" "Patterns of Enterprise Application Architecture" >}}* book.

*Two-Step View*. *Table Module*. *Transform View*. There is a good chance
you've never heard of these software patterns, but they are also in Fowler's
book.

Good patterns and not-so-good patterns is my theme for this book.

*Patterns of Enterprise Application Architecture* lacks the same impact as
other patterns books that I have read (e.g.,
{{< extlink "http://en.wikipedia.org/wiki/Design_Patterns" "GoF" >}} or {{< extlink "http://xunitpatterns.com/" "XUnit Test Patterns" >}}).
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
didn't. Look at the {{< extlink "http://martinfowler.com/eaaCatalog/" "list on Fowler's website" >}} and do some homework on them.
*Patterns of Enterprise Application Architecture* is a decent reference book,
but you can probably get better explanations on the web.
