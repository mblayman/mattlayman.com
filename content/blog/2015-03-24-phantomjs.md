---
title: Inject JavaScript with PhantomJS to inspect websites
description: >-
  What if you could interact with the JavaScript
  of another website
  by adding your code
  to the page?
  PhantomJS,
  a "headless" web browser,
  has the ability to do exactly that.
  In this post,
  you will learn how to extract data from the web via PhantomJS scripts.
image: img/2015/phantomjs.png
type: post
aliases:
 - /2015/phantomjs.html
categories:
 - Software
tags:
 - JavaScript
 - PhantomJS

---
How can you inspect the source of a website with a script?
You can download the page,
parse it with a library like {{< extlink "http://lxml.de/" "lxml" >}},
and extract what you're looking for.
*But what if the page is mostly made from JavaScript?*
There may not be much HTML to parse.
Most of the page might be generated on the DOM dynamically.
If this is the kind of page
that you want to scan,
a tool like lxml will not help much.

Another option is {{< extlink "http://phantomjs.org/" "PhantomJS" >}}.
PhantomJS is a "headless" web browser.
That means that it is a browser that has no GUI.
PhantomJS is exactly the kind of tool that you want
for exploring very dynamic webpages
from a script.

Let's look at an example.

```javascript
var page = require('webpage').create();
page.open('http://www.mattlayman.com', function(status) {
  if page.injectJs('scan.js') {
    var results = page.evaluate(function() {
        return getResults();
    });
    // Do something with the results from scan.js.
    phantom.exit();
  }
}
```

This little script opens `http://www.mattlayman.com`.
When the page is loaded,
the script injects a file named `scan.js`.
This file contains whatever code you want.
Maybe it is a bunch of {{< extlink "https://jquery.com/" "jQuery" >}} to process the DOM.
`scan.js` exists in the context of the page
so it can access whatever data is needed.
Then the script calls `evaluate` to invoke `getResults`.
`getResults` is an imaginary method
in `scan.js`.
Data is transferred
from the context of the website
to the context of the PhantomJS script.
With the scanning code done,
you can do anything with the results.

PhantomJS makes it painless to get into a website,
inspect the content of the site
by looking at the DOM,
and process the data
to your heart's content.
This is a brief introduction,
but I hope it gives you a flavor
of what a headless browser like PhantomJS can do.
