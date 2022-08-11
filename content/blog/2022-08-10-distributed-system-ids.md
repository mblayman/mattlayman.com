---
title: "Distributed System IDs"
description: >-
    Somtimes it feels like everything is harder
    with a distributed system.
    This article looks at identifiers
    and how even your IDs might need some special design consideration
    for a distributed system.
image: img/2022/brain.jpg
type: post
categories:
 - Software
tags:
 - brain dump
 - identity

---

Which one of these is an ID for an account?

* `acct_UwHaw7hBQAcXKofSdJhhfPlw`
* `UwHaw7hBQAcXKofSdJhhfPlw`

There's not a right answer to this question.
Either of these IDs could be linked to an account
in a given system.
Between the two,
which do you think would be *more likely*
to be an account ID?
The first one,
with its `acct_` prefix,
feels a lot more likely
to be an account ID.

I've been thinking about distributed system identifiers recently
and trying to shore up my preferences.
There are many ways to do identifiers
that have different tradeoffs.
Here are a few different types
of IDs that you might encounter.

* Random strings
* Random strings with prefixes
* Integers
* UUIDs
* KSUIDs
* URNs

As you assess these identifier types,
you can find many strings and weaknesses in different approaches.
Integers might be crazy simple
because of auto-incrementing tables,
but you open a system up to the possibility
of an enumeration attack.
UUIDs should satisfy uniqueness concerns,
but it's impossible to infer what an ID refers to.
I could go through the list
and highlight the strengths and weaknesses
of each approach.

What's a good approach for a service oriented architecture?
That is the current area that I'm wrestling with.
In a service oriented architecture,
different services will likely need to store IDs
to model concepts in other services
to be able to reference that data in the future.
Knowing that a service will likely store an ID
from any other service as a reference,
what style should you bias toward?

I think it might help to go through some philosophical considerations
with IDs.
Here's an important question to consider:
*should IDs be transparent or opaque?*

To me,
a URN is an example of a transparent identifier.
The spec for a URN defines a very clear structure
for an identifier.
In other words,
a URN adds semantic qualities
to the ID.
Since these structural semantics exist,
it's possible for code to use an ID itself
to make logical decisions.

This is an example URN: `urn:ietf:rfc:2648`.
Because the structural semantics are present,
a service could perform validation
on this identifier.
Maybe a service only works
with IETF standards,
so the service rejects `urn:ietf:rfc`
because it wants `urn:ietf:std`.
A transparent identifier means
that the service can inspect the ID
and see into it.
This power is potentially interesting,
but I wonder if there is a strong temptation
to abuse this transparency
and overload the semantic structure of the ID.

Another option is an opaque identifier.
With this design philosophy,
a service should assume that the ID is a black box.
The service should make no assumptions about the structure.
With this style,
the validation that I mentioned
with transparent IDs is not possible.
Why might we want this style?

An opaque identifier can allow the service that *owns* the ID
to make changes
without affecting other services that hold the ID.
When the non-owning service knows nothing about the ID,
it can blindly store whatever is given to it.
I'm not sure if there's a strong benefit with this,
but I know that information hiding is a powerful feature,
so I have a gut feeling that there's something here
that I can't articulate well.

While I think that there's something interesting
with having an identifier be opaque
to the software service
that stores another service's ID,
there is certainly power in having an ID be transparent
to a *person*.
Stripe is always the first service that comes to mind
in this regard.
All of Stripe's IDs include prefixes like `acct_` or `card_`.
I have no idea if Stripe treats these as opaque among their internal services,
but these prefixes are massively useful
to disambiguate what kind of ID something is.
If you ever pass the wrong kind of ID
to a field,
a quick inspection should make it obvious what the problem is.

Returning to my original hypothetical question,
that's why I felt that the ID
with an `acct_` prefix was the more natural fit.
Adding that small amount of semantic information makes Stripe IDs
so much more valuable
than a raw integer, hash, or UUID.

Whether I ultimately land in favor of transparent or opaque ID
as my preference,
having a transparent ID for humans is an obvious win to me.
When a distributed system is passing around many different types of IDs,
this level of semantic data can likely reduce data mismatch errors very rapidly.

To my personal taste,
this simple prefix style is preferable
to the URN style.
When used in an internal system,
a URN's top level namespace of `urn:mycompany` would be a big waste
of storage.
Storage is relatively cheap now,
but why store that extra data
that would be meaningless?
If `urn:mycompany` is 13 bytes multiplied by *every ID in a large distributed system,
replicated to many services,*
then I think that could start to add up.
I'm also curious if there would be performance impacts
on a database index,
but I don't know enough about how the different SQL databases build their indices
to know if there would be a material impact.

The other layer that I am thinking of when considering this is how to migrate
to a different ID style.
Changing IDs is not a trivial undertaking
since identity is the core to referencing many models.
A change in this design could have far reaching consequences
like causing breaking changes to REST APIs
or anything that previously referenced one of these IDs.
My guess is that there aren't many companies
that consider their ID design
at the very outset of their company journey.

Migration is almost certainly a normal undertaking
when teams are looking for a "more robust" ID format.
Switching IDs will undoubtedly have effects
on any service that needs to reference a different service.
These effect might cause non-trivial updates.
For instance,
if you formerly used an integer ID type
and switched a string,
then a different service will need to do a data migration
to translate from one ID format to another.

I might caution teams to give some consideration
to their IDs when they start modeling.
Do you want your services to introspect on an ID
that is transparent?
Do you want to have a service treat an ID
as a foreign blob
that it stores in a generic way?

Isn't it funny how even the most seemingly basic design choices can be full
of hidden complexity?
