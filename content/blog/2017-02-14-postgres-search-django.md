---
title: PostgreSQL text search in Django
description: >-
  In order to add search functionality
  on a budget
  for College Conductor,
  I incorporated the text searching capabilities
  of the PostgreSQL module
  available to Django 1.10.
  This post covers features
  and limitations
  of PostgreSQL search.
image: img/2017/postgresql.png
type: post
aliases:
 - /2017/postgres-search-django.html

---

[College Conductor](https://www.collegeconductor.com/)
gives educational consultants and counselors
access to the information
of thousands of U.S. colleges and universities.
The most natural method
to find these schools
is through search.
Since College Conductor keeps up
with the latest versions
of [Django](https://www.djangoproject.com/),
I was able to add search
by using PostgreSQL's
[full text search](https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/search/)
that is exposed to the Django ORM.
The search features are not perfect,
but they provide results quickly
and avoid bringing in a more targeted tool
like Elasticsearch.
This post will cover some of the advantages and disadvantages
of using these Django features.

The search ability
of College Conductor
centers around searching
for university names.
That means that the data has a couple
of interesting characteristics:

1. All search results will be on *phrases*
   like *University of Virginia*
   or *Johns Hopkins University*.
2. A large percentage of the terms
   are practically useless
   to search for (e.g., *University*, *College*).

When I reviewed the search options
that Django exposes in PostgreSQL,
I found two reasonable approaches:
**full text search**
and
**trigram similarity**.

Let's look at the one that I *didn't* choose first.

## Trigram similarity

Trigram similarity operates
by chunking up data
into three letter groups.
Using some computation,
PosgreSQL can compare the trigrams
and attempt to deduce
what the result should be.
This technique is great
for resolving typos
(which is sometimes called "fuzzy matching").
For instance,
if you're searching for fruit
and type `appel`,
a trigram search would find
the expected result of `apple`.

Unfortunately,
I found that trigrams failed spectacularly
for long phrases.
I liked the idea of fuzzy matching
so I started with the trigram option.
When I tested out the functionality,
it didn't work at all.
Not only would `Vriginia`
fail to find `University of Virginia`,
but searching for `Virginia`
would **also** fail to find the school.
I believe this failure occurred
because so much of the school's full name was missing.
Who wants to type out
`Massachustets College of Pharmacy and Health Sciences`
to benefit from spelling Massachusetts incorrectly?
Answer: no one.

Let's try option two.

## Full text search

Getting a reasonable solution working
for full text search was tricky.
Again,
phrases proved to be troublesome.
For any level of success,
I had to break up a search query
into its parts
and join them together
with an OR operator.
By taking this approach,
I could avoid the granularity problem
that was unavoidable
with the trigram version.

Here's the code to build the queryset:

```python
# `search` is the user's provided search string.
terms = [SearchQuery(term) for term in search.split()]
# `name` is where the name of the school is stored in the model.
vector = SearchVector('name')
query = functools.reduce(operator.or_, terms)
queryset = queryset.annotate(
    rank=SearchRank(vector, query)).order_by('-rank')
queryset = queryset.filter(rank__gte=0.04)
```

Using this join strategy with an OR operator
had one additional snag.
There was a level of junk results
that would appear
that had nothing to do
with the search phrase.

The result include a rank annotation
that measure of how good the match is
for the query.
Inspecting the rank
showed that all the junk was below a numeric threshold.
Because the list of U.S. schools changes
extremely infrequently,
I decided to cut off anything below the threshold
(which happened to be close to `0.04`).
If the data set changed frequently,
I wouldn't trust this magic number;
but I get to benefit from the unchanging nature
of my data set.

There are still problems with this method of searching
that I'm not crazy about:

1. Because trigrams are not part of the search,
   no results will appear unless a term is spelled correctly.
   That's annoying.
2. A partial search is equally invalid.
   For example,
   a search for `Virg` will not find any results.
   Also annoying.

In the long term,
I don't think PostgreSQL full text search
will remain for College Conductor.
In the short term,
however,
it is a great choice
for getting decent search functionality cheaply.
