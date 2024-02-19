---
title: "Fun With Scrapy Link Validation on CI"
description: >-
  How can you make sure, automatically,
  that all the links
  to other internal pages within a site
  continue to work?
  In this article,
  we look at how to use Scrapy, a web scraping tool,
  and GitHub Actions,
  a Continuous Integration system,
  to accomplish this goal.
image: img/2024/scrapy-github-actions.png
type: post
categories:
 - Python
tags:
 - Python
 - Scrapy
 - GitHub Actions
 - CI

---

Here's my scenario:
I have a static site generator
that is building HTML pages
for a community project
that I'm working on.
**How can I make sure, automatically,
that all the links
to other internal pages within the site
continue to work?**
In this article,
I'll show you how I managed to do that
using Scrapy, a web scraping tool,
and GitHub Actions,
the project's Continuous Integration system.

To solve this problem,
I decided to use a web scraper.
Specifically,
I used a spider.
A web spider is software that is specifically design
to visit a page,
scan for links,
and visit any discovered link
(while also avoiding re-visiting already covered pages).

A spider ensures that any accessible link
on the site from a user's perspective
are still working since,
by definition,
the spider uses the links to complete its mission.
The spider is great at navigating the working links,
but we need to do a bit of work
to make it report on the links that *don't* work.

Ultimately,
the solution looks roughly like:

1. Start a local web server.
2. Start the spider and tell it to crawl the local website.
3. Check the results to make sure nothing was broken.

There's a wrinkle in this plan though.
We want to run this on Continuous Integration service
(namely, GitHub Actions),
and that service likes to run processes one at a time.
**How will we run the server and the spider together?**
For that,
we'll use a process manager
that can manage executing these two processes at the same time
as sub-processes.
For our process manager,
we will use
{{< extlink "https://pypi.org/project/honcho/" "honcho" >}}.

Let's address the pieces,
then pull everything together with honcho at the end.

## Local web server

For this article,
I don't need to go into how I'm actually statically building the HTML pages.
You can take it as a given that when we run `make build`,
we get an `out` directory that's full of static files like HTML, CSS, images,
and all that good stuff.

For validation purposes,
we don't need a fancy web server,
so we'll lean on the built-in web server in Python to help us out.
Our command to get this running on port 8000 look like:

```bash
$ python -m http.server --directory out 8000
```

Now we'll have the website served on `http://localhost:8000`.

## The Spider

As I mentioned earlier,
we're going to use
{{< extlink "https://scrapy.org/" "Scrapy" >}}.
Scrapy has a ton of great web scraping tool
and pre-built spiders that we can use and extend.

After installing Scrapy with `pip install scrapy`,
you'll get a `scrapy` command line tool to issue more commands.
I needed a new project and a spider skeleton to start.
Here's how to get bootstrapped:

```bash
$ scapy startproject checker .
$ scrapy genspider -t crawl crawler http://localhost:8000
```

That `.` at the end of the `startproject` command was important.
By doing that, we can skip an extra directory layer that Scrapy wanted to add.
Instead, we've got a `scrapy.cfg` file in the root
as well as the `checker` directory
that contains the Scrapy project code.

Now I'm going to throw the spider code at you to digest.
The important bits will be highlighted after the code.

```python
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Spider(CrawlSpider):
    name = "crawler"
    allowed_domains = ["localhost"]
    start_urls = ["http://localhost:8000"]
    # Opt-in to 404 errors
    handle_httpstatus_list = [404]

    rules = [Rule(LinkExtractor(), callback="parse", follow=True)]

    def parse(self, response):
        if response.status == 404:
            yield {"url": response.url}
```

Time for the highlights.

* `name` - The name of the spider must be unique, and it couldn't be the same
    as the Scrapy project name.
* `allowed_domains` - From the template, the originally looked like `localhost:8000`,
    but when I ran the spider, it complained about port numbers.
    Once I removed the port number, the spider was happy.
* `start_urls` - This tells where the spider where to start (ok!).
* `handle_httpstatus_list` - This class attribute was the most important one
    for this task and was not included with the spider template.
    Essentially, spiders want to send only valid responses for parsing by default.
    But in this scenario, our *goal* is to find the bad ones!
    Therefore, we need to tell Scrapy to give us the 404 results too.
* That line with `rules` is a fancy way of saying "process all the links
    on the allow domain" and send the results to the `parse` method.
    If you want more specific filtering, link extractors are the docs
    that you want to dig into.

In a Scrapy parse method, you have to return (or yield) one of a few different types:
an "item", a Scrapy request, or `None`.

* `None` is probably permitted for the implicit return when the method ends.
    I'm not sure if it signals anything else.
* A Scrapy request (i.e., `scrapy.Request`) is a signal to the Scrapy engine
    that another link should be scraped. Because we're using the `CrawlSpider`,
    we didn't need that.
* A Scrapy item is either a dictionary or special Scrapy class instance.
    You can see in this spider that we are yielding a dictionary
    with a URL if the status was a 404. **These are our broken links.**

When we yield items out of parse,
Scrapy will capture these results and send them to our output format
(which they call a "feed export").
With the default settings,
this looks like lines of JSON blobs.
To run the spider and collect our results,
we can run:

```bash
$ scrapy crawl --overwrite-output checker.jsonl --nolog crawler
```

In this command, we're calling the spider directly
because I named it `crawler`.
With this spider,
if we have any lines in `checker.jsonl`,
then we know that there were 404s in the crawl,
and we have a handy report of what those 404s were!

## Piece It Together

honcho, our process manager,
works from a `Procfile` format
to specify which commands to run.
Since this project already uses the default `Procfile`
for managing local development,
I create a new `Procfile.checker` that contains:

```text
web: python -m http.server --directory out 8000
checkers: scrapy crawl --overwrite-output checker.jsonl --nolog crawler
```

When we run `honcho -f Procfile.checker start`,
honcho will start two subprocesses,
one for each line in the file.
The web server will listen for local requests,
and Scrapy will crawl that web server looking for broken links.
When the spider is done,
its process will end.
This will trigger honcho to shut down
because honcho expects every process to continue running
and shuts down automatically when one of its subprocesses exits.

This is cool, but we need to be able to verify the results
without manual inspection of the `checker.jsonl` file.
For that part,
we can use some command line tools.
I packaged the set of commands into a `Makefile` target.

```make
test-ci:
	honcho -f Procfile.checker start
	cat checker.jsonl
	test ! -s checker.jsonl
```

The `test` line is the important one for automated validation.
The `-s` flag checks that a file exists and has a non-zero length
(i.e., there are bytes in the file).
By using `!`,
we negate the expression.
In other words,
the `test` command succeeds when the file is empty
and fails when there is data in there.
This is exactly what we want
since an empty file means no 404 errors.

The `cat` command is included
so that any output in the file will be reported in the CI log.

## On GitHub Actions

To complete the whole flow,
we need to put something into the GitHub Action configuration file.
We've already done all the hard work and packaged this whole thing up neatly
in a Makefile target!

This project has a single job.
All that was needed in the configuration file was to execute our Makefile target
as a step in the job after building the static files output.

```yaml
      - name: Test internal links
        run: make test-ci
```

Now,
whenever CI runs,
Scrapy and the web server will fire up,
crawl all internal links on the static website,
and pass if there are no 404 errors.
Success!

The project that I'm working on
is for my local community in Frederick.
The code for the project is only a couple of weeks old
and, by adding this spider,
we already found **three broken links**.
It's paying off already! Sweet.

If you want to check out the code for this project, you can.
The code is all open source on GitHub
at {{< extlink "https://github.com/TechFrederick/community" "TechFrederick/community" >}}.
I hope this little exploration was a fun way to get into spiders for you.
I know that I certainly learned a bunch in this process of building it out.
