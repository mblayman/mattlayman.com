---
title: Feature flags and waffles
description: >-
  Modern software development has a strong focus
  on continuously delivering new code,
  and many businesses do not have the luxury
  to ship code
  on an infrequent schedule.
  How can an engineering team manage this speed
  of development
  and produce a quality product?
  One invaluable tool to achieve this goal
  is feature flags.
  Learn more about what feature flags are
  and how they work.
image: img/2017/waffles.jpg
type: post
aliases:
 - /2017/feature-flags-and-waffles.html
categories:
 - Python
tags:
 - Django
 - feature flags

---

You're on a team
that wants to ship a Super Cool New Feature™.

The feature will cause changes all over your web app.
Instead of releasing the work in pieces,
the marketing team wants to have a big reveal
to create a buzz.
*How do you manage this challenge?*

One option is to keep all the work in a separate code branch.
When everything is done,
merge the code back into your main branch,
ship it,
and reveal it to the world.
**Whoa, hold on, that sounds risky.**

What could *possibly* go wrong? Well, how about:

1. Other changes continued on your main branch
   and now your long lived feature branch is **full of conflicts**
   with your main branch.
2. Your feature code was only tested
   by developers
   and is **full of bugs**
   that destroy the usability
   of your Super Cool New Feature.

That sounds... **terrible**.

How can we *continuously deliver* the feature
without killing the marketing buzz?
We can use **feature flags.**

## Feature flags

> Feature flags are a tool
that give development teams the ability
to expose a feature
in a controlled manner.

You might come across feature flags
as *{{< extlink "https://martinfowler.com/articles/feature-toggles.html" "feature toggles" >}}*
or *feature flippers*.
Even though the names are different,
the intent is the same.
With feature flags,
a team controls which features are active
**and** which people see those active features.

A feature flag functions as a configurable point
in a system
that a team can enable or disable.
In code,
a feature flag looks a little like:

```python
if feature_flag_is_active:
    return super_cool_new_feature()
else:
    return old_behavior()
```

What makes `feature_flag_is_active` true or not can depend
on who the user is.
This extra level
of control
is useful
to gate the release.

We could enable our Super Cool New Feature
for the marketing team (or QA)
in advance.
This gives them time to review,
provide feedback,
and let's us address bugs.

I can tell you
from personal experience
that mastery
over the feature timeline
is a huge boon
for {{< extlink "https://storybird.com/" "Storybird" >}}.
The team at Storybird can polish features
before sharing them
with hundreds of thousands
of teachers and students.

Now that you're equipped
with the knowledge
of what feature flags are,
let's explore one library
that implements them.
Go get the syrup
because we're going to be talking about waffles,
er,
`django-waffle`.

## Are you waffling?

> **waffle**: verb - EQUIVOCATE, VACILLATE
>
> {{< extlink "https://www.merriam-webster.com/dictionary/waffle" "Merriam-Webster" >}}

{{< extlink "http://waffle.readthedocs.io/en/latest/index.html" "Django Waffle" >}}
is a feature flag library
that can enable or disable code,
as described previously,
and is quick
to add to any Django project.

Waffle includes
{{< extlink "http://waffle.readthedocs.io/en/latest/types/index.html" "a few types of feature control" >}}.
For our purposes,
I'm going to focus
on flags
as they are the most interesting
and powerful type.

`waffle.flag_is_active` is the critical method
for the Waffle flags API.

Suppose part of our Super Cool New Feature is a new template design
for our product page.
If the original product view looked like:

```python
class ProductView(View):
    def get(self, request, *args, **kwargs):
        # Do work to build template context...
        return render(request, 'old_design.html', context)
```

Then our new code that adds a Waffle flag would look like:

```python
class ProductView(View):
    def get(self, request, *args, **kwargs):
        # Do work to build template context...
        if waffle.flag_is_active(request, 'super_cool_new_feature'):
            return render(request, 'new_design.html', context)
        else:
            return render(request, 'old_design.html', context)
```

Let's break down how this works.

Waffle stores flag settings
in a database table.
A team controls the available flags
via the {{< extlink "https://docs.djangoproject.com/en/1.11/ref/contrib/admin/" "Django admin" >}}.
From the admin site,
a developer can set a flag's name,
enabled/disabled status,
and some filters
for more specific control
like superuser, staff, or specific group access.

When the view executes,
`flag_is_active` inspects `request.user`
against the settings decribed
in the `super_cool_new_feature` database row.
If the user meets the criteria,
the function evaluates to `True`
and your new code will run.

For the Super Cool New Feature,
Waffle can be called in every place
that needs to be changed
using the same feature flag name.
This introduces a way to turn the feature on (or off!)
with a quick edit in the Django admin.

## Wrapping up

Maybe you've come this far
and a question has percolated up
through your mind.

> Isn't this more complicated?

**Yes, it is.**
Like every engineering choice,
feature flags have trade-offs.

By adding a feature flag directly to the code,
we create clean up work
when the feature flag is no longer needed.
This clean up work takes time,
but it is better than the alternative.
*A long lived feature branch
almost always causes trouble.*

> *Feature flags divorce the shipping of features
from the revelation of features.*

This flexibility is great
for teams that need to move fast.
And there are amazing side benefits
like creating a work culture
that delivers code constantly.
Constant delivery ***builds trust***
between an engineering team
and other teams
because of a tight feedback loop.
If you're looking
for a way to move your team faster
and improve your workplace,
give feature flags a shot!
