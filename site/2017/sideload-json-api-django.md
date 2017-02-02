%YAML 1.1
---
blog: True
title: Sideload JSON API resources in Django
date: 2017-01-10T12:00:00Z
summary: >-
  If you use Django REST Framework
  and the DRF JSON API extension,
  you may want to learn
  how to sideload extra resources
  to save on network requests
  of commonly paired models.
  We will explore the extra settings required
  to make that happen.
image: jsonapi.png
template: writing.j2

---
<img class='book' src='jsonapi.png'>

I'm a big proponent
of using a framework
to reduce the time required
to make something useful.
Occasionally,
using a framework means that developers must *explore*
to understand what is possible.
This truth is even more evident
when there are layers of extensions
to achieve a desired result.
For instance,
[College Conductor](https://www.collegeconductor.com/) is driving an
[EmberJS](http://emberjs.com/) app
with a [JSON API](http://jsonapi.org/)
powered by [Django](https://www.djangoproject.com/).
The API uses the excellent
[Django REST Framework](http://www.django-rest-framework.org/)
and the [DRF JSON API](http://django-rest-framework-json-api.readthedocs.io/en/stable/)
extension.
DRF JSON API translates from vanilla DRF API serialized output
to JSON API flavored output.
In this post,
**I'll cover my exploration
of the DRF JSON API source code
to find out how to load extra model resources
in a single API request.**

The JSON API specification describes
how to include extra resources
using a
[Compound Document](http://jsonapi.org/format/#document-compound-documents).
Compound Documents are the mechanism
to serialize extra resources
*in a single request*.
The benefit of doing this
is saving at least one HTTP request
(with all of its associated delay)
and possibly more
if the client app is inefficient
with resource requests.
Unfortunately,
DRF JSON API does not explain
how to make a Compound Document
(a fact I hope to correct with this
[Pull Request](https://github.com/django-json-api/django-rest-framework-json-api/pull/308)).
For now,
that means that users must scour the source.
What follows is an example
that can save you from source code spelunking.

Let's suppose that you would like to make a quest game.
In your game,
you have a quest
and you send a knight
on your quest.
There is a very small amount
of information
about your knight
so it would be great
to send that data
along with the quest.

We can begin
with the non-sideloaded versions
of the two serializers.

```python
from rest_framework_json_api import serializers

from game.models import Knight, Quest


class KnightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Knight
        fields = (
            'id',
            'name',
            'strength',
            'dexterity',
            'charisma',
        )


class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = (
            'id',
            'title',
            'reward',
            'knight',
        )
```

Let's assume that the `Quest.knight` is a foreign key
to a `Knight`.
In this version
of our `QuestSerializer`,
DRF JSON API will serialize the associated knight's ID
without the data
that we want.

Now,
we can transform the `QuestSerializer`
in a couple of ways.
First, the code:

```python
class QuestSerializer(serializers.ModelSerializer):
    included_serializers = {
        'knight': KnightSerializer,
    }

    class Meta:
        model = Quest
        fields = (
            'id',
            'title',
            'reward',
            'knight',
        )

    class JSONAPIMeta:
        included_resources = ['knight']
```

Hopefully,
the two changes are hard to miss.
This new serializer informs DRF JSON API
of *what* we want the API to include
via the `included_resources` meta attribute.
We must also tell the serializer *how* to serialize the `knight`.
The *how* is accomplished by the `included_serializers` dictionary.
These settings are enough to make DRF JSON API
include both the quest and knight data
in a single request. Neat!

Before we part,
I must sadly note that this is how this should work
*in theory*.
There is currently a bug ([#291](https://github.com/django-json-api/django-rest-framework-json-api/issues/291))
that is fixed by [Pull Request #307](https://github.com/django-json-api/django-rest-framework-json-api/pull/307).
When that is merged and released,
you'll be able to use sideloaded resources
in your Django based JSON API.
