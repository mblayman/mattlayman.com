---
title: Open Graph, Twitter cards, and plugins... Oh My!
description: >-
  Social media is a huge part of how people share news
  with each other
  on the internet.
  This post looks into how to make your content appear richer
  on sites like Facebook and Twitter.
image: img/2017/og.png
type: post
aliases:
 - /2017/open-graph-twitter-plugins.html

---

Facebook recently reported having 1.86 billion monthly active users.
Twitter clocks in at 313 million montly active users.
Like them or not,
social media sites are extremely popular channels
for people to learn about the world around them.
This means that making your content ready
for social media
is a great way to improve people's perception
of your work.

To make your content social media ready,
you need to include some metadata markup
in your HTML
that these sites can discover
when scanning your pages.
Facebook's metadata format is called
[Open Graph](http://ogp.me/)
and Twitter describes their metadata as
[cards](https://dev.twitter.com/cards/overview).
**This post will cover Open Graph and Twitter cards
and how I incorporated them
into this site.**
My interest in this subject is as a blogger,
but this metadata can capture a wide variety of content types.

## Open Graph

The most relevant Open Graph type
for a blog post is an `article`.
Let's look at the metadata for this post
and break it down.

```html
<meta property="og:type"
  content="article" />
<meta property="og:url"
  content="http://www.mattlayman.com/2017/open-graph-twitter-plugins.html" />
<meta property="og:image"
  content="http://www.mattlayman.com/2017/og.png" />
<meta property="og:title"
  content="Open Graph, Twitter cards, and plugins... Oh My!" />
<meta property="og:description"
  content="Social media is a huge part of how people share news with each
           other on the internet. This post looks into how to make your
           content appear richer on sites like Facebook and Twitter." />
```

All of these meta tags are added to the `head` portion
of the HTML document.
Open Graph defines tags that must be set on any type
of Open Graph content.
Those are `og:type`, `og:url`, `og:image`, and `og:title`.
I chose to add the optional `og:description`
because each of my posts include a summary
that naturally fit in the description field.
An article can include additional information,
but this minimum amount will provide a full looking styling
when your content shows
on Facebook.

## Twitter cards

Twitter cards aren't nearly so granular
as Open Graph content.
For a Twitter card,
the `summary` type is a good fit
for a blog post.

```html
<meta name="twitter:card"
  content="summary" />
<meta name="twitter:site"
  content="@mblayman" />
<meta name="twitter:image"
  content="http://www.mattlayman.com/2017/og.png" />
<meta name="twitter:title"
  content="Open Graph, Twitter cards, and plugins... Oh My!" />
<meta name="twitter:description"
  content="Social media is a huge part of how people share news with each
           other on the internet. This post looks into how to make your
           content appear richer on sites like Facebook and Twitter." />
```

Like its Open Graph brethren,
Twitter card meta tags are placed
in the `head` section.
You can see immediately
there is a striking similarity
between Open Graph and Twitter cards
when you have content
like a blog post.
The only noticable differences are
the absence of a `url` for Twitter cards
and a `twitter:site` property
in its place.

## Plugins

Neither of these types of metadata
are difficult to add to a page,
especially if you're writing HTML by hand.
But I'm not writing my HTML by hand.
Instead,
I use
[handroll](http://handroll.readthedocs.io/en/latest/),
a static site generator
that I developed
because I wanted to see if I could.

handroll reads my posts
from Markdown files
and generates HTML with templates.
I don't have the opportunity
to fiddle directly with the tags that appear
in the `head` section.

One of my goals with handroll
was to include a robust plugin system
that would permit me to extend my site
with functionality that I wanted
while avoiding functionality
that I had no need for.
This system enabled me
to integrate Open Graph and Twitter cards.

handroll [extensions](http://handroll.readthedocs.io/en/latest/extensions.html)
operate on well defined signals
that are invoked
at various stages
of producing the output
of the site.
Knowing that these extension points exist,
I was able to write two plugins.
These plugins work by reacting
to any blog post that changes.
When a post changes,
the plugin processes
[frontmatter](http://handroll.readthedocs.io/en/latest/configuration.html#front-matter),
scans for attributes that can populate the meta tags,
and injects the tags
into context
that is used
during template rendering.
In my base template,
my only addition was the following:

```jinja2
  {{ open_graph_metadata }}
  {{ twitter_metadata }}
```

I quite enjoyed this process for a couple of reasons:

1. It feels great to make my content richer
   so that it is easier to share
   and presents better when shared.
2. I was very satisfied
   with how quickly I could develop the extensions.
   Having well defined interfaces
   that behave consistently
   can make quick work of a task.

You can see an example of one of the extensions
by checking out the Open Graph
[code](https://github.com/handroll/handroll/blob/master/handroll/extensions/og.py)
on GitHub.
