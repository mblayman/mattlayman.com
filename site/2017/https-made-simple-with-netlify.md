%YAML 1.1
---
blog: True
title: HTTPS made simple with Netlify
date: 2017-08-02T12:00:00Z
summary: >-
  Serving webpages securely
  with HTTPS
  offers numerous benefits.
  This post explores those benefits
  and shows how to set up HTTPS
  in no time using Netlify.
image: netlify.jpg
template: writing.j2

---
<img class='book' src='netlify.jpg'>

For an extremely long time,
adding encryption to a website
was inconvenient
and costly.
To get that precious green lock
in the URL bar
(which only appears when a website is served
with *secure* HTTP, a.k.a. HTTPS),
a developer had to perform
a series
of arcane steps.
These steps include
digital certificates,
signing requests,
and all manner
of terminology
that are *yet another thing*
to learn.
This procedure was *manual*
and *painful*.

Thanks to the amazing work
of [Let's Encrypt](https://letsencrypt.org/),
a certificate authority (CA)
managed by a non-profit
with large corporate backing,
**most of the difficulty
with adding HTTPS
is disappearing.**
Let's Encrypt makes it possible
for services
like [Netlify](https://www.netlify.com/)
to add HTTPS
to a website,
trivially.

Before discussing how this feat is done
and what Netlify does,
let's see why HTTPS is valuable.

## Benefits of HTTPS

> "Why would I want HTTPS on my website?"
>
> &mdash;You, just now ;)

Hopefully,
the most obvious reason is that HTTPS makes your website **secure**.
This means that the connection
between the website's servers
and the client's browser can't be tampered with or observed.
As a website creator,
you avoid sleazy Internet Service Providers (ISPs)
attempting to add their own advertising
to your content.
Or,
if you live in a country
with a government
with a strong censorship policy,
you, as a website visitor,
maintain a level
of privacy that's not possible over regular HTTP.
A secure connection is a boon
to content producers and consumers.

Another benefit of HTTPS is speed.
HTTPS is a requirement
before a browser can use HTTP/2,
the next version of HTTP.
HTTP/2 is faster than the first version
of HTTP
for a variety of reasons
that I won't be covering
in this post
(try searching for "https faster than http"
if you want to learn why it's faster).
A faster page load makes users happy!

A final benefit
from HTTPS
stems from Google's preference
for secure sites.
Back in 2014,
Google documented
that [it would use HTTPS as a ranking signal](https://webmasters.googleblog.com/2014/08/https-as-ranking-signal.html).
I knew that this was true,
but I didn't realize the weight
of this signal
until I added HTTPS to this site.
With a secure URL,
I saw a massive jump
in my website ranking.
Website creators are missing some low hanging SEO
if they stick with HTTP.

## Enabling HTTPS with Netlify

[Netlify](https://www.netlify.com/)
is a web service
that can host content.
They have a strong focus
on serving static content
with dynamic content coming
from various APIs.
The company calls this style of architecture
a [JAMstack](https://jamstack.org/)
for JavaScript, APIs, and prebuilt Markup.

If you run a statically generated website,
Netlify is a great fit.
Whether you use
[Jekyll](https://jekyllrb.com/),
[Hugo](https://gohugo.io/),
or some obscure tool (like I do with [handroll](http://handroll.readthedocs.io/en/latest/)),
Netlify's build process can accommodate your tool of choice.

> How does Netlify provide HTTPS support?

All it took for me to enable HTTPS was a couple of button clicks.
Before enabling HTTPS,
I had to connect my domain name.
This was a process I needed to do anyway,
and the [Netlify documentation](https://www.netlify.com/docs/custom-domains/) was very solid.
With my domain name connected to my Netlify deployment,
I clicked a button prompting me
to enable HTTP,
and I was done.

Behind the scenes,
Netlify contacted Let's Encrypt
using one of the CA's automated processes.
The automated process leads to an exchange
that generates a [TLS certificate](https://en.wikipedia.org/wiki/Transport_Layer_Security).
The certificate is what makes it possible to use HTTPS.
The beautiful part
about the process
is that the details don't matter
to the website creator.
This is a huge divergence
from the past
and a welcome relief.

I'm a relatively new user
of Netlify's services,
but I've become a big fan.
If you try them out,
I think that you'll find a friendly product
which makes it easy to make the web a more secure (and faster!) place.
