---
title: "Episode 12 - Success With Static Files"
aliases:
 - /django-riffs/12
 - /djangoriffs/12
 - /django-riffs/12.
 - /djangoriffs/12.
description: >-
    On this episode, our focus will be on static files.
    Static files are vital to your application,
    but they have little to do with Python code.
    We'll see what they are and what they do.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - static
nofluidvids: true

---

On this episode,
our focus will be on static files.
Static files are vital
to your application,
but they have little to do with Python code.
We'll see what they are
and what they do.

Listen at {{< extlink "https://open.spotify.com/episode/1Tn41YfkWh3ffvBpZB8c49" "Spotify" >}}.

## Last Episode

On the last episode,
we looked at Django middleware.
We discussed why middleware is useful
and how you can work with it.

## What Are Static Files?

Static files are files
that don't change
when your application is running.

These files do a lot to improve your application,
but they aren't dynamically generated
by your Python web server.
In a typical web application,
your most common static files will be the following types:

* Cascading Style Sheets, CSS
* JavaScript
* Images

Static files are crucial
to your Django project
because the modern web requires more than dynamically generated HTML markup.
Do you visit any website
that has *zero* styling
of its HTML?
These kinds of sites exist
and can be awesome
for making a quick tool,
but most users expect websites
to be aesthetically pleasing.
For us,
that means that we should be prepared
to include some CSS styling
at a minimum.

## Configuration

To use static files
in your project,
you need the `django.contrib.staticfiles` app
in your project's `INSTALLED_APPS` list.
This is another one
of the default Django applications
that Django will include
if you start from the `startproject` command.

The `staticfiles` app has a handful
of {{< extlink "https://docs.djangoproject.com/en/3.1/ref/settings/#settings-staticfiles" "settings" >}}
that we need to consider to start.

```python
# project/settings.py

...

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
```

Next,
we can define the URL path prefix
that Django will use
when it serves a static file.
Let's says you have `site.css`
in the root
of your project's `static` directory.
You probably wouldn't want the file
to be accessible as `mysite.com/site.css`.
To do so would mean that static files could conflict
with URL paths
that your app might need to direct
to a view.
The `STATIC_URL` setting lets us namespace our static files
and, as the {{< extlink "https://www.python.org/dev/peps/pep-0020/" "Zen of Python" >}} says:

> Namespaces are one honking great idea -- let's do more of those!

```python
# project/settings.py

...

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = '/static/'
```

With `STATIC_URL` set,
we can access `site.css`
from `mysite.com/static/site.css`.

There's one more crucial setting
that we need to set,
and it is called `STATIC_ROOT`.
When we deploy our Django project,
Django wants to find all static files
from a single directory.
The reason for this is for efficiency.
It's possible for Django
to search through all the app `static` directories
and any directories set
in `STATICFILES_DIRS`
whenever it searches for a file
to serve,
but that would be slow.

Once we set `STATIC_ROOT`,
Django will have the desired output location
for static files.
If you set the path somewhere
in your repository,
don't forget to put that path
in your `.gitignore`
if you're using version control
with {{< extlink "https://git-scm.com/" "Git" >}}
(and I highly recommend that you do!).
I happen to set my `STATIC_ROOT`
to a `staticfiles` directory.

```python
# project/settings.py

...

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = '/static/'
```

## Working With Static Files

The primary way
of working with static files
is with a template tag.
The `static` template tag will help render the proper URL
for a static file for your site.

```django
{% load static %}
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" type="text/css" href="{% static "css/site.css" %}">
</head>
<body>
  <h1>Example of static template tag!</h1>
</body>
</html>
```

Since we know that `STATIC_URL` is `/static/`
from the configuration section,
why don't I hardcode the link tag path
to `/static/css/site.css`?
You could,
and that might work,
but you'll probably run into some long term problems.

* What if you ever wanted to change `STATIC_URL`?
  Maybe you want to change it to something shorter like `/s/`.
  If you hardcode the name,
  now you have more than one place to change.
* Using some extra features,
  Django may change the name
  of a file to something unique
  by adding a hash to the file name.
  With a hardcoded path of `/static/css/site.css`,
  this may lead to a 404 response
  if Django expects the unique name instead.
  We'll see what the unique name is for
  in the next section.

We should remember
to use the `static` tag
in the same way
that we use the `url` tag
when we want to resolve a Django URL path.
Both of these tags help avoid harcoding paths
that can change.

```python
# application/views.py

from django.http import JsonResponse
from django.templatetags.static import static

def get_css(request):
    return JsonResponse({'css': static('css/site.css')})
```

## Deployment Considerations

When you deploy your application
to a server,
one crucial setting
to disable
is the `DEBUG` setting.
If `DEBUG` is on,
all kinds of secret data can leak
from your application,
so the Django developers *expect* `DEBUG` to be `False`
for your live site.
Because of this expectation,
certain parts of Django behave differently
when `DEBUG` changes,
and the `staticfiles` app is one such part.

When `DEBUG` is `True`
and you are using the `runserver` command
to run the development web server,
Django will search for files
using a set of "finders"
whenever a user requests a static file.
These finders are defined
by the `STATICFILES_FINDERS` setting,
which defaults to:

```python
[
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
```

As you might guess,
the `FileSystemFinder` looks for any static files
found in the file system directory
that we listed in `STATICFILES_DIRS`.
The `AppDirectoriesFinder` looks for static files
in the `static` directory
of each Django application
that you have.
You can see how this gets slow
when you realize
that Django will walk
through `len(STATICFILES_DIRS) + len(INSTALLED_APPS)`
before giving up
to find a single file.

`collectstatic` will copy all the files it discovers
from iterating through each finder
and collecting files
from what a finder lists.
In my example below,
my Django project directory is `myproject`,
and I set `STATIC_ROOT` to `staticfiles`.

```bash
$ ./manage.py collectstatic

42 static files copied to '/Users/matt/myproject/staticfiles'.
```

When deploying your application
to your server,
you would run `collectstatic`
before starting the web server.
By doing that,
you ensure that the web server
can access any static files
that the Django app might request.

### Optimizing Performance In Django

The last setting we'll consider is the `STATICFILES_STORAGE` setting.
This setting controls how static files are stored and accessed
by Django.
We may want to change `STATICFILES_STORAGE`
to improve the efficiency
of the application.
The biggest boost we can get from this setting
will provide file caching.

In an ideal world,
your application would only have to serve a static file exactly *one* time
to a user's browser.
In that scenario,
if an application needed to use the file again,
then the browser would reuse the *cached* file
that it already retrieved.
The challenge that we have is that static files (ironically?)
change over time.

The "trick" is to serve a "fingerprinted" version
of the file.
As a part of the deployment process,
we would like to uniquely identify each file
with some kind of version information.
An easy way for a computer to do this is
to take the file's content
and calculate a hash value.
We can have code take `site.css`,
calculate the hash,
and generate a file with the same content,
but with a different filename
like `site.abcd1234.css`
if `abcd1234` was the generated hash value.

The next part of the process is
to make the template rendering use the `site.abcd1234.css` name.
Remember how we used the `static` template tag
instead of hardcoding `/static/css/site.css`?
This example is a great reason why we did that.
By using the `static` tag,
Django can render the filename
that includes the hash
instead of only using `site.css`.

The final bit that brings this scheme together is
to tell the browser
to cache `site.abcd1234.css`
for a very long time
by sending back a certain caching header
in the HTTP response.

* If the user fetches `site.abcd1234.css`,
    their browser will keep it
    for a long time
    and never need to download it again.
    This can reused every time the user visits a page
    in your app.
* If we ever change `site.css`,
    then the deployment process can generate a new file
    like `site.ef567890.css`.
    When the user makes a request,
    the HTML will include the new version,
    their browser won't have it in the cache,
    and the browser will download the new version
    with your new changes.

Great!
How do we get this
and how much work is it going to require?
The answer comes back
to the `STATICFILES_STORAGE` setting
and a tool called
{{< extlink "http://whitenoise.evans.io/en/stable/" "WhiteNoise" >}}
(get it!? "white noise" *is* "static." har har).

WhiteNoise is a pretty awesome piece of software.
The library will handle
that *entire* caching scheme
that I described above.

To set up WhiteNoise,
you install it with `pip install whitenoise`.
Then,
you need to change your `MIDDLEWARE` list
and `STATICFILES_STORAGE` settings.

```python
# project/settings.py

...

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
  # ...
]

STATICFILES_STORAGE = \
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

When your application runs,
the WhiteNoise middleware will handle which files
to serve.
Because files are static
and don't require dynamic processing,
we include the middleware high
on the list
to skip a lot of needless extra Python processing.
In my configuration example,
I left the `SecurityMiddleware` above WhiteNoise
so the app can still benefit
from certain security protections.

The scheme that I described is not the only way
to handle static files.
In fact,
there are some tradeoffs
to think about:

1. Building with WhiteNoise means
    that we only need to deploy a single app
    and let Python handle all
    of the processing.
2. Python, for all its benefits,
    is not the fastest programming language out there.
    Leaving Python to serve your static requests will run slower
    than some other methods.
    Additionally,
    your web server's processes must spend time serving the static files
    rather than being fully devoted to dynamic requests.

### Optimizing Performance With A Reverse Proxy

An alternative approach
to using Django
to serve static files
is to use another program
as a *reverse proxy*.
This setup is more complex,
but it can offer better performance
if you need it.
A reverse proxy is software
that sits between your users
and your Django application server.
CloudFlare has a
{{< extlink "https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/" "good article" >}}
if you want to understand why "reverse" is in the name.

If you set up a reverse proxy,
you can instruct it
to handle many things,
including URL paths
coming to your site's domain.
This is where `STATIC_ROOT` and `collectstatic` are useful outside of Django.
You can set a reverse proxy
to serve all the files
that Django collects
into `STATIC_ROOT`.

The process is roughly:

1. Run `collectstatic`
    to put files into `STATIC_ROOT`.
2. Configure the reverse proxy
    to handle any URL pattern
    that starts with `STATIC_URL`
    (recall `/static/` as an example)
    and pass those requests
    to the directory structure
    of `STATIC_ROOT`.
3. Anything that doesn't look
    like a static file (e.g., `/accounts/login/`)
    is delegated
    to the app server running Django.

In this setup,
the Django app never has to worry
about serving static files
because the reverse proxy
takes care of those requests
before reaching the app server.
The performance boost comes
from the reverse proxy itself.
Most reverse proxies are designed
in very high performance languages
like C
because they are designed
to handle a specific problem:
routing requests.
This flow lets Django handle the dynamic requests
that it needs to
and prevents the slower Python processes
from doing work
that reverse proxies are built for.

If this kind of setup appeals
to you,
one such reverse proxy
that you can consider is
{{< extlink "https://www.nginx.com/" "Nginx" >}}.
The configuration of Nginx is beyond the scope
of this series,
but there are plenty
of solid tutorials
that will show how to configure a Django app
with Nginx.

## Summary

In this episode,
we covered static files.

We looked at:

* How to configure static files
* The way to work with static files
* How to handle static files
    when deploying your site
    to the internet

## Next Time

On the next episode,
we're going to talk about testing your app.
We'll see how automated tests can provide you the peace of mind
that your application works as you expect.

You can follow the show
on {{< extlink "https://open.spotify.com/show/1RtdveQIz5m5MqLKPWbhnD" "Spotify" >}}.
Or follow me or the show
on X
at
{{< extlink "https://x.com/mblayman" "@mblayman" >}}
or
{{< extlink "https://x.com/djangoriffs" "@djangoriffs" >}}.

Please rate or review
on Apple Podcasts, Spotify,
or from wherever you listen to podcasts.
Your rating will help others discover the podcast,
and I would be very grateful.

Django Riffs is supported by listeners like *you*.
If you can contribute financially
to cover hosting and production costs,
please check out my {{< extlink "https://www.patreon.com/mblayman" "Patreon page" >}}
to see how you can help out.
