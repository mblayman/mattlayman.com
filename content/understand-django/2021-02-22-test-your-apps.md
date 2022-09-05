---
title: "Test Your Apps"
description: >-
    How do you confirm that your website works?
    You could click around
    and check things out yourself,
    or you can write code to verify the site.
    I'll show you why you should prefer the latter.
    In this Understand Django article,
    we'll study automated tests
    to verify the correctness of your site.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - tests
series: "Understand Django"

---

In the previous
[Understand Django]({{< ref "/understand-django/_index.md" >}})
article,
we saw how static files
like CSS, JavaScript, and images
can be incorporated
into your site.
Now we're going to focus
on how to verify
that your website works
and continues to work
by writing automated tests
that check your pages
and your code logic.

{{< understand-django-series "tests" >}}

## Why Write Tests

I'm going to assume
that if you're reading this,
then you've either got a Django project
or are considering working
with Django
to build a project.
If that's true,
think about your project
and how you would make sure it works.

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

For starting out,
manually checking out your site is fine.
What happens, though,
when your create more pages?
How do you continue to confirm
that all your pages are functional?
You could open up the local site
and start clicking around,
but the time spent confirming
that everything works begins to grow.
Maybe your verification effort takes 3 minutes, 5 minutes, or perhaps much more.
If you're not careful,
your creation may start to feel
like the mythical multi-headed Hydra,
and what once was a fun project
to work on
devolves into a chore
of tedious page verification.

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

Let's look at a test
for a hypothetical `add` function
which functions
like the `+` operator.
This should give us a feel
for what an automated test is like
if you've never encountered tests before.

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

This automated test would take virtually no time to run
if you compared it to running the function
in a Python REPL
to inspect the result manually.

Seeing a silly example
of an `add` function doesn't really help you much
with how you should test your Django project.
Next,
we'll look at some types
of tests
for Django.
If you add these kinds of tests
to your project,
you'll be able to make changes
to your website
with more confidence
that you're not breaking things.

## Useful Types Of Django Tests

When we explored the anatomy
of a Django application,
I noted that I *always* delete the `tests.py` file
that comes with the `startapp` command.
The reason I do this is
because there are different kinds
of tests,
and I want those different kinds
to live in separate files.
My apps have those separate files
in a `tests` package
within the app
instead of a `tests.py` module.

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

This structure hints
at the kinds
of tests
that you'd write
for your application,
but I'll touch on specifics more a bit later.
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

When we have tests
that runs many parts
of your application
that are *integrated* together,
we call these tests *integration tests*.
Integration tests are good at surfacing issues related
to the *connections between code*.
For instance,
if you called a method
and passed in the wrong arguments,
an integration test is likely
to discover that problem.

On the other end of the spectrum
are tests that run very little code.
The `add` test from above is a good example.
These kinds of tests check individual units
of code
(e.g., a Django model).
For that reason,
we call these *unit tests*.
Unit tests are good at *checking a piece
of code
in isolation*
to confirm its behavior.

Unit tests have downsides too.
These tests execute
without a lot of context
from the rest
of an application.
This can help you confirm the behavior
of the piece,
but it might not be the behavior
that the larger application requires.

In this explanation,
the lesson is that both kinds
of tests are good,
yet have tradeoffs.
Beware of anyone who tells you
that you should only write one kind
of test
or the other.

> A good set of automated tests will include both **unit** and **integration** tests
to check behavior
of the individual units
and the interconnections
between parts.

We have to consider another aspect
to this discussion:
what is the "right" amount
of code for a unit test?
*There's no absolutely correct answer here.*
In fact,
this topic is hotly debated
among testers.

Some people will assert
that a unit test should only run the code
for that unit.
If you have a class
that implements some pure logic
and doesn't need other code,
then you're in the ideal case.
But what happens if you're testing
a method that you added to a Django model
that needs to interact
with a database?
Even if the only thing you're testing is the individual model method,
a unit test purist would highlight
that the test is actually an integration test
if it interacts with a database.

**I usually find this kind of discussion counterproductive.**
In my experience,
this sort of philosophical debate
about what is a unit test doesn't typically help
with testing your web app
to verify its correctness.
I brought all of this up because,
if you're going to learn more about testing
after this article,
I caution you
to avoid getting sucked
into this definition trap.

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

As we get into some examples,
I need to introduce a couple
of tools
that I use
on all of my Django projects.
I'll describe these tools
in more depth
in a later section,
but they need a brief introduction here
or my examples won't make much sense.
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

Again,
I'll focus on these two packages later on
to cover more of their features,
but you'll see them used immediately
in the examples.

#### Model Tests

In Django projects,
we use models
to hold data
about our app,
so it's very natural
to add methods
to the models
to interact
with the data.
How do we write a test
that checks that the method
does what we expect?

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

We can imagine a project
that includes an ecommerce system.
A big part
of handling orders is tracking status.
We could manually set the status field
throughout the app,
but changing status
within a method gives us the chance
to do other things.
For instance,
maybe the `ship` method also triggers sending an email.

In the test above,
we're checking the state transition
from `PENDING` to `SHIPPED`.
The test acts on the `ship` method,
then refreshes the model instance
from the database
to ensure that the `SHIPPED` status persisted.

What are some good qualities
about this test?

The test includes a docstring.
Trust me, you *will* benefit from docstrings
on your tests.
There is a strong temptation to leave things
at `test_shipped`,
but future you may not have enough context.

Many developers opt for long test names instead.
While I have no problem with long descriptive test names,
docstrings are helpful too.
Whitespace is a *good* thing
and, in my opinion, it's easier to read
"The widget updates the game state when pushed."
than `test_widget_updates_game_state_when_pushed`.

The test checks one action.
A test that checks a single action can fit
in your head.
There's no question about interaction
with other parts.
There's also no question about what is actually being tested.
The simplicity of testing a single action makes each unit test
tell a unique story.

Conversely,
you'll likely encounter tests
in projects
that do a lot of initial arrangement,
then alternate between act and assert lines
in a single test.
These kinds of tests are brittle
(i.e., the term to indicate that the test can break
and fail easily)
and are difficult to understand
when there is a failure.

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

Notice that I'm bending the AAA rules a bit
for this test.
Part of the Django convention
for forms
is that the form is valid
before calling the `save` method.
If that convention is not followed,
then `cleaned_data` won't be populated correctly
and most `save` methods depend on `cleaned_data`.
Even though `is_valid` is an action,
I view it as a setup step
for form tests.

When we work with forms,
a lot of what we care about is cleaning the data
to make sure
that junk is not getting
into your app's database.
Let's write a test
for an invalid form.

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

This test shows how to check an invalid form,
but I'm less likely to write this particular test
in a real project.
Why?
Because the test is checking functionality
from Django's `EmailField`
which has the validation logic
to know what is a real email or not.

Generally,
I don't think it's valuable
to test features
from the framework itself.
A good open source project
like Django
is already testing those features
for you.
When you write form tests,
you should check on custom `clean_*` and `clean` methods
as well as any custom `save` method
that you might add.

The patterns for both happy path and error cases are what I use
for virtually all
of my Django form tests.
Let's move on
to the integration tests
to see what it look like
to test more code
at once.

### Integration Tests

In my opinion,
a good integration test won't look very different
from a good unit test.
An integration test can still follow the AAA pattern
like other automated tests.
The parts that change are the tools you'll use
and the assertions you will write.

My definition of an integration test
in Django
is a test
that uses Django's test `Client`.
In previous articles,
I've only mentioned what a client is in passing.
In the context
of a web application,
a client is anything that consumes the output
of a web app
to display it to a user.

The most obvious client for web app
is a web browser,
but there are plenty
of other client types out there.
Some examples that could use output
from a web application:

* A native mobile application
* A command line interface
* A programming library like Python's `requests` package
    that can handle HTTP requests and responses

The Django test `Client` is like these other clients
in that it can interact
with your Django project
to receive data from requests
that it creates.
The nice part about the test client is that the output
is returned in a convenient way
that we can assert against.
The client returns the `HttpResponse` object directly!

With that context,
here's an integration test
that we can discuss.

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

That's a lot of code to execute
in a single test!
The goal of the test is
to check that all the major pieces hang together.

Now let's observe what the test is not doing.
Even though the test runs a ton of code,
there aren't a huge number of `assert` statements.
In other words,
our goal with an integration isn't
to check every tiny little thing
that could happen in the whole flow.
Hopefully, we have unit tests
that cover those little parts
of the system.

When I write an integration test,
I'm mostly trying to answer the question:
**does the *system* hold together without breaking?**

Now that we've covered unit tests
and integration tests,
what are some tools that will help you make testing easier?

## Tools To Help

When testing your application,
you have access to so many packages
to help
that it can be fairly overwhelming.
If you're testing
for the first time,
you may be struggling
with applying the AAA pattern
and knowing what to test.
We want to minimize the extra stuff
that you have to know.

We're going to revisit the tools
that I listed earlier, `pytest-django` and `factory_boy`,
to get you started.
Consider these your Django testing survival kit.
As you develop your testing skills,
you can add more tools
to your toolbox,
but these two tools are a fantastic start.

### `pytest-django`

{{< extlink "https://docs.pytest.org/en/stable/" "pytest" >}} is a "test runner."
The tool's job is to run automated tests.
If you read {{< extlink "https://docs.djangoproject.com/en/4.1/topics/testing/overview/" "Writing and running tests" >}}
in the Django documentation,
you'll discover
that Django *also* includes a test runner
with `./manage.py test`.
What gives?
Why am I suggesting that you use `pytest`?

I'm going to make a bold assertion:
**pytest is better**.
(Did I just go meta there? Yes, I did. 😆)

I like a lot about Django's built-in test runner,
but I keep coming back to pytest
for one primary reason:
I can use `assert` in tests.
As you've seen
in these test examples,
the `assert` keyword makes for clear reading.
We can use all of Python's normal comparison tests
(e.g., `==`, `!=`, `in`)
to check the output
of tests.

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

Using `assert` from pytest means
that you get all the benefits
of the `assert*` methods,
but you only need to remember a single keyword.
If that wasn't enough,
let's compare the readability:

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

For the same reason
that Python developers prefer `property` methods
instead of getters and setters
(e.g. `obj.value = 42` instead of `obj.set_value(42)`),
I think the `assert` style syntax is far simpler
to visually process.

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

As you build up your Django project,
you will have more models
that help to describe the domain
that your website addresses.
Generating model data
for your tests is a capability
that is immensely valuable.

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

We can imagine an app
that shows information about movies.
The `Movie` model could have a variety
of foreign key relationships
like director, producer, studio,
and so on.
I'll use a few in the example,
but imagine what would happen
as the number of foreign key relationships increases.

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

On the surface,
the test isn't *too* bad.
I think that's mostly because I kept the modeling simple.
What if `Director`, `Producer`, or `Studio` also had required foreign keys?
We'd spend most
of our effort
on the Arrangement section
of the test.
Also,
as we inspect the test,
we get bogged down with unnecessary details.
Did we need to know the names
of the director, producer, and studio?
No, we didn't need that for this test.
Now,
let's look at the factory_boy equivalent.

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

This factory definition is very declarative.
We declare what we want,
and factory_boy figures out how to put it together.
This quality leads to factories
that you can reason about
because you can focus
on the what
and not the how
of model construction.

The other noteworthy aspect is that the factories compose together.
When we call `MovieFactory()`,
factory_boy is missing data
about everything
so it must build all of that data.
The challenge is that the `MovieFactory` doesn't know
how to build a `Director`
or any of the movie's foreign key relationships.
Instead,
the factory will delegate
to *other* factories
using the `SubFactory` attribute.
By delegating to other factories,
factory_boy can build the model
and its entire tree
of relationships
with a single call.

When we want to override the behavior
of some of the generated data,
we pass in the extra argument
as I did in the second example
by providing "Sci-Fi"
as the `genre`.
You can pass in other model instances
to your factories too.

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

In this article,
we explored tests
with Django projects.
We focused on:

* Why would anyone want to write automated tests
* What kinds of tests are useful
    to a Django app
* What tools can you use to make testing easier

Next time,
we will dig into deployment.
Deployment is getting your project
into the environment
where you will share your application
for use.
This might be the internet
or it might be a private network
for your company.
Wherever you're putting your app,
you'll want to know about:

* Deploying your application with a Python web application server
    (i.e., `./manage.py runserver` isn't meant for deployed apps)
* Deployment preconditions
    for managing settings, migrations, and static files
* A checklist to confirm that your settings are configured
    with the proper security guards
* Monitoring your application for errors

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
