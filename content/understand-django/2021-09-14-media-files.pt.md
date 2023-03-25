---
title: "User File Use"
description: >-
    Maybe your app needs to handle files
    from users
    like profile pictures.
    Accepting files from others is tricky
    to do safely.
    In this article,
    we'll see the tools
    that Django provides
    to manage files safely.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - files
series: "Understand Django"

---

In the last
{{< web >}}
[Understand Django]({{< ref "/understand-django/_index.md" >}})
article,
{{< /web >}}
{{< book >}}
chapter,
{{< /book >}}
you learned about Django settings
and how to manage the configuration
of your application.
We also looked at tools
to help you
define settings
effectively.

{{< web >}}
With this article,
{{< /web >}}
{{< book >}}
With this chapter,
{{< /book >}}
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

{{< understand-django-series "files" >}}

## Files In Django Models

{{< web >}}
As we saw in the models article,
{{< /web >}}
{{< book >}}
As we saw in the models chapter,
{{< /book >}}
model fields in a Django model map
to a column in a database table.
When you want to access the *data*
for a model instance,
Django will pull the data
from a database row.

Dealing with files in models is a bit different.
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
This is the approach
that Django takes
with files.

Now that you know that Django takes this approach,
you can remember:

1. Django models hold the *reference* to a file (e.g., a file path)
2. The file *data* (i.e., the file itself) is stored somewhere else.

The "somewhere else" is called the "file storage,"
and we'll discuss storage
in more depth
in the next section.

Let's focus on the first item.
What do you use to reference the files?
Like all other model data,
we'll use a field!
Django includes two fields
that help with file management:

* `FileField`
* `ImageField`

### `FileField`

What if you want to store a profile picture?
You might do something like this:

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
>>> profile.picture.save(
...     'my-image.png',
...     File(f)
... )
```

In this example,
I'm creating a profile instance manually.
There are a few interesting notes:

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

More often than not,
you won't need to use these interfaces directly
because Django has form fields
and other tools
that manage much of this for you.

The current model example raises questions.

* Where does that data go?
* What if we have a name conflict between two files like "`my-image.png`"?
* What happens if we try to save something that isn't an image?

If we make no changes to the current setup,
the data will go into the root
of the media file storage.
Media file storage is a topic that will be covered later.
For the moment,
recognize that putting all the files into a single place (i.e., the root)
will be a mess.
This mess will be pronounced if you're trying to track many file fields,
but we can fix this with the `upload_to` field keyword argument.
The simplest version of `upload_to` can take a string
that the storage logic will use as a directory prefix
to scope content
into a different area.

We're still left with potentially conflicting filenames.
Thankfully,
`upload_to` can also accept a callable
that gives us a chance to fix that issue.
Let's rework the example.

```python
# application/models.py

import uuid
from pathlib import Path
from django.db import models

def profile_pic_path(
        instance,
        filename
    ):
    path = Path(filename)
    return "profile_pics/{}{}".format(
        uuid.uuid4(),
        path.suffix
    )

class Profile(models.Model):
    picture = models.FileField(
        upload_to=profile_pic_path
    )
    # Other fields like a OneToOneKey to User ...
```

With this new version
of the profile model,
all of the images will be stored
in a `profile_pics` path
within the file storage.

This version also solves the duplicate filename problem.
`profile_pic_path` ignores most
of the original filename provided.
If two users both happen to upload `profile-pic.jpg`,
`profile_pic_path` will assign those images random IDs
and ignore the `profile-pic` part
of the filename.

You can see that the function calls `uuid4()`.
These are effectively random IDs called
{{< extlink "https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)" "Universally Unique Identifiers (UUID)" >}}.
UUIDs are likely something that you've seen before
if you've worked with computers long enough,
even if you didn't know their name.
An example UUID would be `76ee4ae4-8659-4b50-a04f-e222df9a656a`.
In the storage area,
you might find a file stored as:

```text
profile_pics/76ee4ae4-8659-4b50-a04f-e222df9a656a.jpg
```

Each call to `uuid4()` is nearly certain
to generate a unique value.
Because of this feature,
we can avoid filename conflicts
by storing profile pictures
with a unique name.
As an aside,
UUIDs are not very friendly for users,
so if you plan to let your users download these files,
you might wish to explore alternative naming techniques.

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
that lets Python work with image data.

Our final example looks like:

```python
# application/models.py

import uuid
from pathlib import Path
from django.db import models

def profile_pic_path(
        instance,
        filename
    ):
    path = Path(filename)
    return "profile_pics/{}{}".format(
        uuid.uuid4(),
        path.suffix
    )

class Profile(models.Model):
    picture = models.ImageField(
        upload_to=profile_pic_path
    )
    # Other fields like a OneToOneKey to User ...
```

Now that we've seen how Django will track files and images
in your models,
let's go deeper
and try to understand the file storage features.

## Files Under The Hood

We now know that models store references to files
and not the files themselves.
The file storage task is delegated
to a special Python class
in the system.

This Python class must implement
{{< extlink "https://docs.djangoproject.com/en/4.1/ref/files/storage/" "a specific API" >}}.
Why?
Like so many other parts of Django,
the storage class can be swapped out
for a different class.
We've seen this swappable pattern already
with templates, databases, authentication, static files, and sessions.

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

On my computer,
with the above setting
and the `Profile` class example
from earlier,
Django would store a file somewhere like:

```text
# This path is split to be easier to read.
/Users/matt/example-app/ \
    media/profile_pics/ \
    76ee4ae4-8659-4b50-a04f-e222df9a656a.jpg
```

The other setting important to `FileSystemStorage` is `MEDIA_URL`.
This setting will determine how files are accessed
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
An image tag template fragment would look like:

{{< web >}}
```django
<img src="{{ profile.picture.url }}">
```
{{< /web >}}
{{< book >}}
```djangotemplate
<img src="{{ profile.picture.url }}">
```
{{< /book >}}

The Django documentation shows how file storage is a specific interface.
`FileSystemStorage` happens to be included
with Django and implements this interface
for the simplest storage mechanism,
the file system
of your server's operating system.

We can also store files separately
from the web server,
and there are often really good reasons to do that.
Up next,
we'll look at another option
for file storage aside from the provided default.

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

If you conclude that `FileSystemStorage` will not work
for your app,
is there another good option?
Absolutely!

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
* Services you run separately like an SFTP server

These services would have additional cost
beyond the cost of running your web server
in the cloud,
but the services usually have shockingly low rates
and some offer a generous free tier
for lower levels of data storage.

Why use django-storages?

* You will never need to worry about disk space.
    The cloud services offer effectively unlimited storage space
    if you're willing to pay for it.
* The files will be separated from your Django web server.
    This can eliminate some categories of security problems
    like a malicious file trying to execute arbitrary code
    on the web server.
* Cloud storage can offer some caching benefits
    and be easily connected to Content Delivery Networks
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

While the setup cost exists,
you'll usually pay that cost at the beginning
of a project
and be mostly hands off after that.

django-storages is a pretty fantastic package,
so if your project has a lot of files to manage,
you should definitely consider using it
as an alternative to the `FileSystemStorage`.

## Summary

{{< web >}}
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
you learned about Django file management.
We covered:

* How Django models maintain references to files
* How the files are managed in Django
* A Python package that can store files in various cloud services

{{< web >}}
In the next article,
{{< /web >}}
{{< book >}}
In the next chapter,
{{< /book >}}
let's explore commands.
Commands are the code
that you can run with `./manage.py`.
You'll learn about:

* Built-in commands provided by Django
* How to build custom commands
* Extra commands from the community that are useful extensions for apps

{{< web >}}
If you'd like to follow along
with the series,
please feel free to sign up
for my newsletter
where I announce all of my new content.
If you have other questions,
you can reach me online
on Twitter
where I am
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;
