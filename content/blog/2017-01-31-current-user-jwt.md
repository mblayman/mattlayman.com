---
title: A currentUser service for Ember with JWT
description: >-
  As a user of Ember Simple Auth
  and Ember Simple Auth Token,
  I needed to show an authenticated user
  for College Conductor.
  By making a currentUser service,
  my application could access the user.
  Since College Conductor uses JWT,
  making the service required some extra thought.
  Check out how it works!
image: img/2017/jwt.svg
type: post
aliases:
 - /2017/current-user-jwt.html
categories:
 - Guide
tags:
 - Ember
 - JWT
 - authn

---

Any Software as a Service will likely need
the capability to authenticate a user
and show information
about that user.
As an interesting design choice,
{{< extlink "http://emberjs.com/" "Ember" >}} does **not**
include authentication
as a core feature.
Instead,
Ember developers must turn to the addon ecosystem.
After some research,
I chose
{{< extlink "http://ember-simple-auth.com/" "Ember Simple Auth" >}}
with
{{< extlink "https://github.com/jpadilla/ember-simple-auth-token" "Ember Simple Auth Token" >}}
to use
JSON Web Tokens ({{< extlink "https://jwt.io/" "JWT" >}})
for {{< extlink "https://www.collegeconductor.com" "College Conductor" >}}.
JSON Web Tokens are an emerging standard
that make secure exchanges (like authentication) possible.
To provide user information
throughout the application,
I had to do some extra work
to create an Ember
{{< extlink "https://guides.emberjs.com/v2.11.0/applications/services/" "service" >}}.
I'm going to cover what I learned
in the process.

Thankfully for me (and you),
Ember Simple Auth has good documentation
to cover a wide variety
of uses.
As a template,
I used the
{{< extlink "https://github.com/simplabs/ember-simple-auth/blob/master/guides/managing-current-user.md" "Managing a Current User" >}}
guide
to direct the service
that I needed.
This guide lays out the structure required
to extract information
from the `session` service provided
by Ember Simple Auth.

Generating a service to start is one command away:

```bash
$ ember generate service current-user
```

We can begin by looking
at the code
in the Ember Simple Auth guide.

```javascript
import Ember from 'ember';

const { inject: { service }, isEmpty, RSVP } = Ember;

export default Ember.Service.extend({
  session: service('session'),
  store: service(),

  load() {
    let userId = this.get('session.data.authenticated.user_id');
    if (!isEmpty(userId)) {
      return this.get('store').findRecord('user', userId).then(
        (user) => {
          this.set('user', user);
        });
    } else {
      return Ember.RSVP.resolve();
    }
  }
});
```

This service is almost exactly what we need
but there is a problem.
When using JWT,
the data stored in the session is an encoded token.
The service needs to get the user ID
and it's not easily accessible.
That leads to code like:

```javascript hl_lines="12 21 22 23 24"
import Ember from 'ember';

const { inject: { service }, isEmpty, RSVP } = Ember;

export default Ember.Service.extend({
  session: service(),
  store: service(),

  load() {
    const token = this.get('session.data.authenticated.token');
    if (!isEmpty(token)) {
      const userId = this.getUserIdFromToken(token);
      return this.get('store').find('user', userId).then((user) => {
        this.set('user', user);
      });
    } else {
      return RSVP.resolve();
    }
  },

  getUserIdFromToken(token) {
    // What goes here?
    return 42;
  }
});
```

As I explored the source code,
I discovered that the session did not store the decoded token data.
I had to find a way to decode the token
so I could extract the `user_id`
that my API provided.
The JWT authenticator
in Ember Simple Auth Token
included what I needed.
Ember Simple Auth does not expose
a method to get the authenticator
(please prove me wrong!)
so I opted to create an instance myself
and invoke its `getTokenData` method.

The result looks like:

```javascript
import JWT from 'ember-simple-auth-token/authenticators/jwt';

<snip>

  getUserIdFromToken(token) {
    const jwt = new JWT();
    const tokenData = jwt.getTokenData(token);
    return tokenData['user_id'];
  }
```

If I reflect on what I had to do,
I think it is safe to state
that the final change was not too difficult.
The part that I find interesting is
that I had to be comfortable digging through the source code
of Ember Simple Auth Token.

> Reading other source code is a needed developer skill.

Last week,
I wrote about
{{< extlink "/2017/necessity-of-software-abstraction.html" "software abstractions" >}}
and the benefits of boundaries.
The boundaries provided by abstractions are extremely useful,
but we should be comfortable breaking through them
when it seems like there are no options.
Reading the source code
of third party addons, extensions, plugins,
and the like
is a useful tool
that can often make quick work
of a tricky problem.
