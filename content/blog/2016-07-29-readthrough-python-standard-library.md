---
title: Reading through the Python standard library
description: >-
  What I learned about the Python standard library
  and how you can apply those learnings to your own study.
image: img/2016/library.jpg
type: post
aliases:
 - /2016/readthrough-python-standard-library.html

---
A couple of years ago I decided to read the entire Python standard library.
A few months back, I finished.

What I learned is this:
**while there is some interesting "hidden" stuff in there,
you don't need to do this to become proficient.**

Did you know that nearly all the HTTP status codes are in the standard library?
Judging by all the Python packages that defined their own status codes,
I assumed that the codes weren't in there.
I was {{< extlink "https://docs.python.org/2/library/httplib.html" "wrong" >}}.
And they got {{< extlink "https://docs.python.org/3/library/http.html#http-status-codes" "better in 3.5" >}}.
Reading through the library revealed many "easter eggs" like that.

Even though learning about those hidden corners
of the standard library is fun,
there's a really large problem with reading through the whole library.

### It's a lack of context.

One challenge of reading through everything is that you may be unaware
of what parts are excellent (like `os.path`)
and what parts are not (I won't name names here).
Occasionally,
the reader is given a warning about the dragons ahead.
You might find a tip to use {{< extlink "https://docs.python.org/3/library/urllib.request.html" "requests" >}}.
I think those kinds of suggestions are rare.

Maybe you're asking:

### "*So if the library doesn't provide much direction, what do I do?*"

Part of getting good with the standard library is experiential.
The best ways to gain that experience is through practice and exposure.
This is where I point you to the community.

Your local Python user group (hi, {{< extlink "https://www.meetup.com/python-frederick/" "Python Frederick" >}}!),
online Python communities like on IRC,
and open source Python projects
are excellent places to get exposure.
You'll encounter people who can provide pointers
and read code from those who are a bit farther on this journey than you are.

If it's tough for you to get into those social groups,
maybe {{< extlink "http://docs.python-guide.org/en/latest/" "The Hitchhiker's Guide to Python" >}}
will work for you.
For folks that have a programming background,
I can also recommend {{< extlink "http://www.diveintopython3.net/" "Dive Into Python 3" >}}.
I got my start with the Python 2 version
and can attest that it's a good resource.

If you're tempted to read through the standard library like I was,
**cool! Best of luck!**
Please don't forget that there are people around you
that can help provide that missing context.

*Photo credit to
{{< extlink "https://www.flickr.com/photos/loughboroughuniversitylibrary/6333984637" "Loughborough University" >}}.*
