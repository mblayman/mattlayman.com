---
slug: ember-segment
title: Using Segment with Ember.js
date: 2016-12-20
description: >-
  Ember CLI makes using Segment a snap.
  Learn about the core features of ember-cli-segment.
images: img/2016/segment.png
aliases:
 - /2016/ember-segment.html
categories:
 - Guide
tags:
 - JavaScript
 - Ember
 - Segment

---

I've been working on
[College Conductor](https://www.collegeconductor.com/)
to help serve Independent Educational Consultants
(like [this one](https://laymancollegeconsulting.com/) :)
and high school guidance counselors.
To find product market fit,
I'm using [Segment](https://segment.com/)
which gets the data I need
to decide how to improve the service.
In this post,
**I'll describe how I connected Segment
to College Conductor's
[Ember.js](http://emberjs.com/) frontend.**

Working with Segment in Ember can be done with
[ember-cli-segment](https://github.com/josemarluedke/ember-cli-segment),
an Ember addon that provides an Ember
[service](https://guides.emberjs.com/v2.1.0/applications/services/)
to communicate with Segment.
The first thing I did was install the addon with:

```bash
$ ember install ember-cli-segment
```

`ember-cli-segment` has a solid README on their GitHub page
that instructs users what to do at a very detailed level.
Before getting buried in details,
I had two initial goals with this addon.

1. Connect to Segment to record basic analytics.
2. Utilize the [identify](https://segment.com/docs/sources/server/http/#identify)
   API to connect users to their actions.

Once these two goals were completed,
I could monitor enough behavior
to make data based decisions
about what to improve
in the product.

## Connect to Segment

Connecting the Ember app to Segment involved adding my Segment write key
to the app's configuration. The result
in my `environment.js` file
was something like:

```javascript
ENV['segment'] = {
  WRITE_KEY: 'my_segment_write_key'
}
```

With that much configuration,
data started flowing from College Conductor to Segment.
Exciting!

## Identifying users

My second goal of identifying users
was done with an application route hook.
If you create a method named `identifyUser`
in your application route,
then `ember-cli-segment` will make the `identify` API call
on your behalf.

I had to supply a user ID
and whatever other information I wanted.
At this stage in my product development,
including the account username
is all the extra data I want.

My code in `app/application/route.js` looks like:

```javascript
identifyUser() {
  const user = this.get('currentUser.user');
  if (user) {
    this.get('segment').identifyUser(
      user.get('id'), {username: user.get('username')});
  }
}
```

This code grabs the authenticated user
from the `currentUser` service
that I created
and identifies that user with Segment.

## Thankful

By the time I finished
with this work,
I was very grateful for `ember-cli-segment`.
The addon made my job much easier.
This is one of the things that I really like
about the Ember community.
Ember CLI addons can take out some
of the very heavy development work.
That means I can spend more time
on College Conductor
and less time on the nuts and bolts
of service integration.
