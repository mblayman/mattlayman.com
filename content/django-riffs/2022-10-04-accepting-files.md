---
title: "Episode 17 - Accepting Files"
aliases:
 - /django-riffs/17
 - /djangoriffs/17
 - /django-riffs/17.
 - /djangoriffs/17.
description: >-
    Maybe your app needs to handle files
    from users
    like profile pictures.
    Accepting files from others is tricky
    to do safely.
    On this episode,
    we'll see the tools
    that Django provides
    to manage files safely.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - files
nofluidvids: true

---

On this episode,
we're going to dig into file management.
Unlike the static files
that you create for the app yourself,
you may want your app to accept files
from your users.
Profile pictures are a good example
of user files.
You'll see how Django handles those kinds
of files
and how to deal with them safely.

Listen at {{< extlink "https://djangoriffs.com/episodes/accepting-files" "djangoriffs.com" >}}
or with the player below.

<div class="h-48">
<iframe height="200px" width="100%" frameborder="no" scrolling="no" seamless src="https://player.simplecast.com/7c13d5d7-312b-4179-8415-f9a0ce465bfc?dark=false"></iframe>
</div>

## Last Episode

On the last episode,
we looked at how to manage settings
on your Django site.
What are the common techniques
to make this easier to handle?
That's what we explored.

## Files In Django Models

While it *is* possible to store file data directly
in a database,
you won't see that happen often.
The reason is that storing the data in the database
usually affects the performance
of the database,
especially with a large number of files.

Instead,
a common pattern
in database usage
is to store files separately
from the database itself.
Within the database,
a column would store some kind of *reference*
to the stored file
like a path
if files are stored on a filesystem.
**This is the approach
that Django takes
with files.**

Now that you know that Django takes this approach,
you can remember:

1. Django models hold the *reference* to a file (e.g., a file path)
2. The file *data* (i.e., the file itself) is stored somewhere else.

The "somewhere else" is called the "file storage,"
and we'll discuss storage
in more depth
in the next section.

Django includes two fields
that help with file management:

* `FileField`
* `ImageField`

### `FileField`

```python
# application/models.py

from django.db import models

class Profile(models.Model):
    picture = models.FileField()
    # Other fields like a OneToOneKey to User ...
```

This is the most basic version of using file fields.
We can use this model very directly
with a Django shell
to illustrate file management.

```python
$ ./manage.py shell
>>> from django.core.files import File
>>> from application.models import Profile
>>> f = open('/Users/matt/path/to/image.png')
>>> profile = Profile()
>>> profile.picture.save('my-image.png', File(f))
```

* The `File` class is an important wrapper
    that Django uses
    to make Python file objects (i.e., the value returned from `open`) work
    with the storage system.
* The name `image.png` and `my-image.png` do not have to match.
    Django can store the content of `image.png`
    and use `my-image.png`
    as the name to reference
    within the storage system.
* Saving the picture will automatically save the parent model instance
    by default.

The current model example raises questions.

* Where does that data go?
* What if we have a name conflict between two files like "`my-image.png`"?
* What happens if we try to save something that isn't an image?

If we make no changes to the current setup,
the data will go into the root
of the media file storage.
This will lead to a mess if you're trying to track many file fields,
but we can fix this with the `upload_to` field keyword argument.
The simplest version of `upload_to` can take a string
that storage will use as a directory prefix
to scope content
into a different area.

```python
# application/models.py

import uuid
from pathlib import Path
from django.db import models

def profile_pic_path(instance, filename):
    path = Path(filename)
    return "profile_pics/{}{}".format(uuid.uuid4(), path.suffix)

class Profile(models.Model):
    picture = models.FileField(upload_to=profile_pic_path)
    # Other fields like a OneToOneKey to User ...
```

There's one more problem to fix
in this example.
How do we know that a user provided a valid image file?
This is important to check,
because we want to avoid storing malicious files
that bad actors might upload
to our apps.

This is where the `ImageField` has value.
This field type contains extra validation logic
that can check the *content* of the file
to check that the file is, in fact, an image.
To use `ImageField`,
you'll need to install the
{{< extlink "https://pillow.readthedocs.io/en/latest/" "Pillow" >}} library.
Pillow is a package
that let's Python work with image data.

```python
# application/models.py

import uuid
from pathlib import Path
from django.db import models

def profile_pic_path(instance, filename):
    path = Path(filename)
    return "profile_pics/{}{}".format(uuid.uuid4(), path.suffix)

class Profile(models.Model):
    picture = models.ImageField(upload_to=profile_pic_path)
    # Other fields like a OneToOneKey to User ...
```

## Files Under The Hood

The setting to control which type
of file storage Django uses is `DEFAULT_FILE_STORAGE`.
This setting is a Python module path string
to the specific class.

So, what's the default?
The default is a storage class
that will store files locally
on the server
that runs the app.
This is found at `django.core.files.storage.FileSystemStorage`.
The storage class uses a couple
of important settings:
`MEDIA_ROOT` and `MEDIA_URL`.

The `MEDIA_ROOT` setting defines
where Django should look for files in the filesystem.

```python
MEDIA_ROOT = BASE_DIR / "media"
```

The other setting important to `FileSystemStorage` is `MEDIA_URL`.
This settings will determine how files are accessed
by browsers
when Django is running.
Let's say `MEDIA_URL` is:

```python
MEDIA_URL = "/media/"
```

Our profile picture would have a URL like:

```python
>>> from application.models import Profile
>>> profile = Profile.objects.last()
>>> profile.picture.url
'/media/profile_pics/76ee4ae4-8659-4b50-a04f-e222df9a656a.jpg'
```

This is the path that we can reference
in templates.
An image tag template fragment would like:

```django
<img src="{{ profile.picture.url }}">
```

The Django documentation shows how file storage is a specific interface.
`FileSystemStorage` happens to be included
with Django and implements this interface
for the simplest storage mechanism,
the file system
of your server's operating system.

## Recommended Package

What is a problem
that can arise
if you use the built-in `FileSystemStorage`
to store files
for your application?
There are actually many possible problems!
Here are a few:

* The web server can have too many files and run out of disk space.
* Users may upload malicious files
    to attempt to gain control
    of your server.
* Users can upload large files
    that can cause a Denial of Service (DOS) attack
    and make your site inaccessible.

The most popular storage package
to reach for is
{{< extlink "https://django-storages.readthedocs.io/en/latest/" "django-storages" >}}.
django-storages includes a set of storage classes
that can connect
to a variety
of cloud services.
These cloud services are able to store an arbitrary number of files.
With django-storages,
your application can connect to services like:

* Amazon Simple Storage Service (S3)
* Google Cloud Storage
* Digital Ocean Spaces
* Or services you run separately like an SFTP server

Why use django-storages?

* You will never need to worry about disk space.
    The cloud services offer effectively unlimited storage space
    if you're willing to pay for it.
* The files will be separated from your Django web server.
    This can eliminate some categories of security problems
    like a malicious file trying to execute arbitrary code
    on the web server.
* Cloud storage can offer some caching benefits
    and be connected to Content Delivery Networks easily
    to optimize how files are served to your app's users.

As with all software choices,
we have tradeoffs to consider
when using different storage classes.
On its face,
django-storages seems to be nearly all positives.
The benefits come with some setup complexity cost.

For instance,
I like to use Amazon S3
for file storage.
You can see from the
{{< extlink "https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html" "Amazon S3 setup" >}} documentation
that there is a fair amount of work to do
beyond setting a different `DEFAULT_FILE_STORAGE` class.
This setup includes setting AWS private keys,
access controls,
regions,
buckets,
and a handful of other important settings.

django-storages is a pretty fantastic package,
so if your project has a lot of files to manage,
you should definitely consider using it
as an alternative to the `FileSystemStorage`.

## Summary

In this episode,
you learned about Django file management.
We covered:

* How Django models maintain references to files
* How the files are managed in Django
* A Python package that can store files in various cloud services

## Next Time

In the next episode,
let's explore commands.
Commands are the code
that you can run with `./manage.py`.

You can follow the show
on {{< extlink "https://djangoriffs.com" "djangoriffs.com" >}}.
Or follow me or the show
on Twitter
at
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}
or
{{< extlink "https://twitter.com/djangoriffs" "@djangoriffs" >}}.

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
