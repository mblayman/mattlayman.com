---
title: "Episode 13 - Does My Site Work?"
aliases:
 - /django-riffs/13
 - /djangoriffs/13
 - /django-riffs/13.
 - /djangoriffs/13.
description: >-
    On this episode,
    we will discuss how you can verify
    that your site works
    and continues to work.
    We're digging into automated testing
    and how to write tests
    for your Django apps.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - testing
nofluidvids: true

---

On this episode,
we will discuss how you can verify
that your site works
and continues to work.
We're digging into automated testing
and how to write tests
for your Django apps.

Listen at {{< extlink "https://djangoriffs.com/episodes/automated-tests" "djangoriffs.com" >}}
or with the player below.

<div class="h-48">
<iframe height="200px" width="100%" frameborder="no" scrolling="no" seamless src="https://player.simplecast.com/65d9efe2-dd0c-41c5-87f2-6e91e51ef86c?dark=false"></iframe>
</div>

## Last Episode

On the last episode,
our focus was on static files.
Static files are vital
to your application,
but they have little to do with Python code.
We saw what they are
and what they do.

## Why Write Tests

When you start out with a project,
whether for a tutorial
or for something real
that you plan to grow,
the fledgling site has very little functionality.
To check that the site is working,
you can start up the local web server,
open your browser,
navigate to the `localhost` URL,
and confirm that the site is functional.
How long does that take?
5 seconds?
15 seconds?
30 seconds?

You can't eliminate the fact
that a larger project means
that there is more to check.
What you *can* do is change the name
of the game.
You can change your page checking
from something manual
that may take 15 seconds to verify a page
to something that a computer can do
in *milliseconds*.

This is where automated tests come
into the picture.
Automated tests let computers do what computers do best:
run repetitive tasks repeatedly, consistently,
and quickly.
When we write tests,
our goal is to confirm some logic or behavior
in a deterministic way.

```python
def test_does_it_add():
    assert add(40, 2) == 42
```

The test works by running the code
and comparing the result
to whatever we expect that result to be.
The test *asserts* that the equality statement is true.
If the equality is false,
then the assertion raises an exception
and the test fails.

## Useful Types Of Django Tests

My `tests` package will often mirror the structure
of the application itself.
The program which executes tests,
which is called a "test runner,"
typically expects to find tests
in files that start with `test_`.
The package often includes:

* `test_forms.py`
* `test_models.py`
* `test_views.py`
* etc.

Broadly,
when we write automated tests,
there is an important dimension
to consider:
how much application code should my test run?

The answer to that question influences the behavior
of tests.
If we write a test
that runs a lot of code,
then we benefit
by checking a lot of a system
at once; however,
there are some downsides:

* Running a lot of code means more things can happen
    and there is a higher chance
    of your test breaking
    in unexpected ways.
    A test that often breaks
    in unexpected ways is called a "brittle" test.
* Running a lot of code means that there is a lot
    of code to run.
    That's axiomatic,
    but the implication is that a test
    with more code to execute will take longer
    to run.
    Big automated tests are still very likely
    to be much faster
    than the same test executed manually,
    so running time is relative.

> A good set of automated tests will include both **unit** and **integration** tests
to check behavior
of the individual units
and the interconnections
between parts.

Here are my working definitions
of unit and integration tests
in Django.
These definition are imperfect
(as are *any* definitions),
but they should help frame the discussion
in this article.

* **Unit tests** - Tests that check individual units
    within a Django project like a model method
    or a form.
* **Integration test** - Tests that check a group of units
    and their interactions
    like checking if a view renders the expected output.

Now that we have some core notion
of what tests are about,
let's get into the details.

### Unit Tests

My two "must have" packages are:

* `pytest-django`
* `factory-boy`

`pytest-django` is a package
that makes it possible
to run Django tests
through the `pytest` program.
pytest is an extremely popular Python testing tool
with a huge ecosystem
of extensions.
In fact,
`pytest-django` is one
of those extensions.

My biggest reason
for using `pytest-django` is
that it let's me use the `assert` keyword
in all of my tests.
In the Python standard library's `unittest` module
and, by extension,
Django's built-in test tools
which subclasses `unitttest` classes,
checking values requires methods
like `assertEqual`
and `assertTrue`.
As we'll see,
using the `assert` keyword exclusively is a very natural way
to write tests.

The other vital tool
in my tool belt is `factory-boy`.
factory_boy is a tool
for building test database data.
The library has fantastic Django integration
and gives us the ability
to generate model data
with ease.

#### Model Tests

I'm going to give you a mental framework
for *any* of your tests,
not only unit tests.
This framework should help you reason
through any tests
that you encounter
when reading and writing code.
The framework is the *AAA pattern*.
The AAA patterns stands for:

* **Arrange** - This is the part of the test
    that sets up your data
    and any necessary preconditions
    for your test.
* **Act** - This stage is when your test runs the application code
    that you want to test.
* **Assert** - The last part checks
    that your action is what you expected.

For a model test,
this looks like:

```python
# application/tests/test_models.py

from application.models import Order
from application.tests.factories import OrderFactory

class TestOrder:
    def test_shipped(self):
        """After shipping an order, the status is shipped."""
        order = OrderFactory(status=Order.Status.PENDING)

        order.ship()

        order.refresh_from_db()
        assert order.status == Order.Status.SHIPPED
```

What are some good qualities
about this test?

The test includes a docstring.
Trust me, you *will* benefit from docstrings
on your tests.
There is a strong temptation to leave things
at `test_shipped`,
but future you may not have enough context.

The test checks one action.
A test that checks a single action can fit
in your head.
There's no question about interaction
with other parts.
There's also no question about what is actually being tested.
The simplicity of testing a single action makes each unit test
tell a unique story.

The qualities in this test translate
to lots of different test types.
I think that's the beauty
of having a solid mental model
for testing.
Once you see the way
that tests:

1. Set up the inputs.
2. Take action.
3. Check the outputs.

Then automated testing becomes a lot less scary
and more valuable to you.
Now let's see how this same pattern plays out
in forms.

#### Form Tests

When writing tests,
we often want to write a "happy path" test.
This kind of test is when everything works exactly
as you hope.
This is a happy path form test.

```python
# application/tests/test_forms.py

from application.forms import SupportForm
from application.models import SupportRequest

class TestSupportForm:
    def test_request_created(self):
        """A submission to the support form creates a support request."""
        email = "hello@notreal.com"
        data = {
            "email": email, "message": "I'm having trouble with your product."
        }
        form = SupportForm(data=data)
        form.is_valid()

        form.save()

        assert SupportRequest.objects.filter(email=email).count() == 1
```

With this test,
we are synthesizing a POST request.
The test:

* Builds the POST data as `data`
* Creates a bound form (i.e., connects `data=data` in the constructor)
* Validates the form
* Saves the form
* Asserts that a new record was created

```python
# application/tests/test_forms.py

from application.forms import SupportForm
from application.models import SupportRequest

class TestSupportForm:
    # ... def test_request_created ...

    def test_bad_email(self):
        """An malformed email address is invalid."""
        data = {"email": "bogus", "message": "Whatever"}
        form = SupportForm(data=data)

        is_valid = form.is_valid()

        assert not is_valid
        assert 'email' in form.errors
```

The test shows the mechanics
for checking an invalid form.
The key elements are:

* Set up the bad form data
* Check the validity with `is_valid`
* Inspect the output state in `form.errors`

### Integration Tests

In my opinion,
a good integration test won't look very different
from a good unit test.
An integration test can still follow the AAA pattern
like other automated tests.
The parts that change are the tools you'll use
and the assertions you will write.

```python
# application/tests/test_views.py

from django.test import Client
from django.urls import reverse

from application.tests.factories import UserFactory

class TestProfileView:
    def test_shows_name(self):
        """The profile view shows the user's name."""
        client = Client()
        user = UserFactory()

        response = client.get(reverse("profile"))

        assert response.status_code == 200
        assert user.first_name in response.content.decode()
```

What is this test doing?
Also, what is this test *not* doing?

By using the Django test client,
the test runs a lot of Django code.
This goes through:

* URL routing
* View execution (which will likely fetch from the database)
* Template rendering

When I write an integration test,
I'm mostly trying to answer the question:
**does the *system* hold together without breaking?**

## Tools To Help

### `pytest-django`

{{< extlink "https://docs.pytest.org/en/stable/" "pytest" >}} is a "test runner."
The tool's job is to run automated tests.
If you read {{< extlink "https://docs.djangoproject.com/en/3.1/topics/testing/overview/" "Writing and running tests" >}}
in the Django documentation,
you'll discover
that Django *also* includes a test runner
with `./manage.py test`.
What gives?
Why am I suggesting that you use `pytest`?

I'm going to make a bold assertion:
**pytest is better**.

Django's test runner builds off the test tools
that are included
with Python
in the `unittest` module.
With those test tools,
developers must make test classes
that subclass `unittest.TestCase`.
The downside of `TestCase` classes is
that you must use a set of `assert*` methods
to check your code.

The list of `assert*` methods are included
in the {{< extlink "https://docs.python.org/3/library/unittest.html#assert-methods" "unittest" >}} documentation.
You can be very successful
with these methods,
but I think it requires remembering an API
that includes a large number
of methods.
Consider this.
Would you rather:

1. Use `assert`? OR
2. Use `assertEqual`,
    `assertNotEqual`,
    `assertTrue`,
    `assertFalse`,
    `assertIs`,
    `assertIsNot`,
    `assertIsNone`,
    `assertIsNotNone`,
    `assertIn`,
    `assertNotIn`,
    `assertIsInstance`,
    and `assertNotIsInstance`?

```python
self.assertEqual(my_value, 42)
assert my_value == 42

self.assertNotEqual(my_value, 42)
assert my_value != 42

self.assertIsNotNone(my_value)
assert my_value is not None

self.assertTrue(my_value)
assert my_value
```

Outside of the awesome handling of `assert`,
{{< extlink "https://pytest-django.readthedocs.io/en/latest/" "pytest-django" >}}
includes a lot of other features
that you might find interesting
when writing automated tests.

### `factory_boy`

The other test package
that I think every developer should use
in their Django projects is
{{< extlink "https://factoryboy.readthedocs.io/en/stable/" "factory_boy" >}}.

> factory_boy helps you build model data for your tests.

You *could* use your model manager's `create` method
to create a database entry
for your test,
but you're going to run into some limits very fast.

The biggest challenge with using `create` comes
from database constraints like foreign keys.
What do you do if you want to build a record
that requires a large number
of non-nullable foreign key relationships?
Your only choice is to create those foreign key records.

```python
def test_detail_view_show_genre(client):
    """The genre is on the detail page."""
    director = Director.objects.create(name="Steven Spielberg")
    producer = Producer.objects.create(name="George Lucas")
    studio = Studio.objects.create(name='Paramount')
    movie = Movie.objects.create(
        genre='Sci-Fi', director=director, producer=producer, studio=studio
    )

    response = client.get(reverse('movie:detail', args=[movie.id]))

    assert response.status_code == 200
    assert 'Sci-Fi' in response.content.decode()
```

```python
def test_detail_view_show_genre(client):
    """The genre is on the detail page."""
    movie = MovieFactory(genre='Sci-Fi')

    response = client.get(reverse('movie:detail', args=[movie.id]))

    assert response.status_code == 200
    assert 'Sci-Fi' in response.content.decode()
```

`MovieFactory` seems like magic.
Our test got to ignore all the other details.
Now the test could focus entirely
on the genre.

Factories simplify the construction of database records.
Instead of wiring the models together
in the test,
we move that wiring to the factory definition.
The benefit is that our tests can use the plain style
that we see in the second example.
If we need to add a new foreign key
to the model,
only the factory has to be updated,
not all your other tests
that use that model.

What might this `Movie` factory look like?
The factory might be:

```python
# application/tests/factories.py

import factory

from application.models import Movie

# Other factories defined here...

class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    director = factory.SubFactory(DirectorFactory)
    producer = factory.SubFactory(ProducerFactory)
    studio = factory.SubFactory(StudioFactory)
    genre = 'Action'
```

factory_boy makes testing
with database records a joy.
In my experience,
most of my Django tests require some amount
of database data
so I use factories very heavily.
I think you will find
that factory_boy is a worthy addition
to your test tools.

## Summary

In this episode,
we explored tests
with Django projects.
We focused on:

* Why would anyone want to write automated tests
* What kinds of tests are useful
    to a Django app
* What tools can you use to make testing easier

## Next Time

On the next episode,
we're get into the important things you should consider
when making your site live on the internet.
This is the topic of deployment,
and we'll see the details next time.

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
