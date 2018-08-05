---
title: handroll, sitemaps, and robots.txt
description: >-
  Make a sitemap that Google can find
  using new features available in handroll 3.1.
  In a few steps,
  you can improve the visiblity
  of your website
  to search engine crawlers.
image: img/2016/robot.jpeg
type: post
aliases:
 - /2016/handroll-sitemaps-robots.html
categories:
 - Python
 - Open source
tags:
 - handroll
 - sitemaps
 - robots.txt

---
Google {{< extlink "https://www.google.com/webmasters/" "webmaster tools" >}} provide suggestions
to improve your site ranking.
The suggestions generally involve making it easier
for their crawlers
to find your content.
One such suggestion is adding a
{{< extlink "https://www.sitemaps.org/index.html" "sitemap" >}}.
*Adding a sitemap
can increase your visibility
on the internet.*

A sitemap is a listing
of pages
within your site.
Web crawlers often work
by starting at the root
of your website
(like [https://example.com/](#)),
and then navigating
to each of the links
on that page.
The crawler will repeat the process
until it can't find any more links.
For a well-linked site,
this process works well.
Unfortunately,
if you have a page that is not linked
to other pages,
the crawler will not know that it exists.
The benefit of a sitemap
is that you can inform the crawler
about all your pages,
whether they are linked well to other pages
or not.

handroll 3.1 includes a sitemap extension
that will generate a sitemap for you automatically.
To use it, add the following to your `handroll.conf`.

```ini
[site]
with_sitemap = True
```

That's it!
From now on,
any of your HTML files will be included
in a `sitemap.txt` file.
Once you have a sitemap,
you should inform web crawlers
of its location.

Conventionally, websites "communicate"
with web crawlers
via a `robots.txt` file.
This file gives instructions
of what a crawler should
or should not crawl.
It also happens to be the place
where you can specify the location
of a sitemap file.

`robots.txt` wants the full URL
to the sitemap file
so I used handroll's new Jinja 2 template composer
to generate my file
without hardcoding my domain.

The whole file,
named `robots.txt.j2`,
looks like:

```j2
User-agent: *
Disallow:
Sitemap: {{ config.domain }}/sitemap.txt
```

With one additional line
in my configuration file
and three lines
in a template file,
I made it easier
for web crawlers
to find everything I care about
on my website.
