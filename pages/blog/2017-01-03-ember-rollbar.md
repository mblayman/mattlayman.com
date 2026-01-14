---
slug: ember-rollbar
title: Monitor Ember app errors with Rollbar
date: 2017-01-03
description: >-
  Using Rollbar in your Ember application
  can give you eyes on the same errors
  that your users encounter.
  Learn how you can add Rollbar
  into your application.
image: img/2017/rollbar.jpeg
aliases:
 - /2017/ember-rollbar.html
categories:
 - Guide
tags:
 - JavaScript
 - Ember
 - Rollbar

---

One fact that I've come to accept
as an experienced developer
is that errors *will* happen.
Guaranteed.
The reasons for this situation
are vast.
Perhaps there are quirks
in a browser you didn't test.
Or perhaps the user did something
that you didn't plan for.
You can't anticipate every situation.
Knowing that errors will happen means you have two choices.
You can ignore this fact
and let your users suffer
(at the risk of losing them).
Or,
**you can record these errors
and fix them
to improve your application.**
I recently set up Rollbar
for [College Conductor](https://www.collegeconductor.com/)
and wanted to share my experience.

[Rollbar](https://rollbar.com/)
is a service
that let's you record your errors
*wherever* they happen.
Error information is stored
with your Rollbar account
so you can examine a problem
and decide how to fix it.

If you're developing an Ember application,
you can quickly integrate your app
with Rollbar. Let's see how.
Begin by installing an Ember CLI addon
for Rollbar:

```bash
$ ember install ember-cli-rollbar
```

Once the addon is installed,
it needs to be configured
to communicate
with Rollbar.
In your `config/environment.js` file,
add a section like this:

```javascript
var ENV = {
  rollbar: {
    accessToken: 'your post_client_item token'
  }
};
```

Rollbar has a few different tokens
available on your access tokens settings page.
The correct one to use with Ember
is the `post_client_item` token.

With that configuration done,
you're ready to go!
When the Ember app is not in `development` mode,
errors will be reported to Rollbar.

Good luck with your app.
I hope this information helps you improve
your project
for your users.
In a few mere weeks of use,
Rollbar has already helped me
track down a number of problems.
I'm sure it can do the same for you.
