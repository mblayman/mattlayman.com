---
title: "Django Testing Toolbox"
description: >-
    In this article,
    I cover the tools that I reach for
    to do automated testing
    when building a Django application.
    You will also see some common techniques
    that I apply to every project.
image: img/2020/chemistry.jpg
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - testing

---

What are the tools
that I use to test a Django app?
Let's find out!

You might say I'm test obsessed.
I like having very high automated test coverage.
This is especially true
when I'm working on solo applications.
I want the best test safety net
that I can have to protect me from myself.

We're going to explore the testing packages
that I commonly use
on Django projects.
We'll also look at a few of the important techniques
that I apply to make my testing experience great.

## Must Have Testing Packages

### pytest-django

Forget fixtures.
Many people rave about {{< extlink "https://docs.pytest.org/en/stable/" "pytest" >}}
because of its fixture system
for setting up data.
The system is powerful,
but I don't really care for it.

That's not why I like pytest.

I like pytest for the super clean API
that it provides
for handling assertions.
It's `assert`.
That's it!

Having a test style
that revolves around a single keyword
and combined with standard comparison is fantastic.
Let's compare.

```python
import unittest

class TestWithUnittest(unittest.TestCase):
    def test_sample(self):
        none_variable = None

        self.assertEqual(3, 3)
        self.assertNotEqual(4, 5)
        self.assertTrue(True)
        self.assertNotIn(1, [2, 3, 4])
        self.assertIsNone(none_variable)

class TestWithPytest:
    def test_sample(self):
        none_variable = None

        assert 3 == 3
        assert 4 != 5
        assert True
        assert 1 not in [2, 3, 4]
        assert none_variable is None
```

For me,
it's a no brainer
that the `assert` style syntax is easier to read.
There is less API to learn.
The rest is applying Python comparison knowledge
that you probably already have.

You can hear me gush more about pytest
on my {{< extlink "https://www.youtube.com/watch?v=etosV2IWBF0" "Python Testing 101 with pytest" >}} presentation
that I gave to Python Frederick.

### factory_boy

Django uses a database.
I am definitely not a unit test purist.
It's totally ok
for unit tests
to use a database.
If you disagree
and think that's an integration test,
great,
I won't hold that against you. 😜

There is no better way
to make fake data
in your testing database
than to use {{< extlink "https://factoryboy.readthedocs.io/en/latest/" "factory_boy" >}}.
factory_boy has a single job:
create database rows
from your model definitions
that are real enough
to test with.

If you have a model,
you create a corresponding factory.
In your test,
you use the factory
to create a model instance.
*How is this better than* `MyModel.objects.create`?
It's better
because factory_boy handles required fields
in a default way.

Imagine you have a model
with 50 required fields.
You judge which is a better looking test.

```python
def test_crazy_model_with_factory():
    crazy = MyCrazyModelFactory()

    # Make assertion about the crazy instance.

def test_crazy_model_without_factory():
    crazy = MyCrazyModel.objects.create(
        a=1,
        b=2,
        c=3,
        d=4,
        e=5,
        f=6,
        g=7,
        h=8,
        i=9,
        j=10,
        # ... and 40 more required fields
    )

    # Make assertion about the crazy instance.
```

On top of basic fields types
like `CharField`,
factory_boy can handle relational fields
like `ForeignKey`
by using more factories linked together.

factory_boy is an amazing tool!

### django-test-plus

Django apps have some very common patterns
when testing.
You'll often want to check
on context data,
or the result
of an HTTP client request,
or if something is present
in a template.

With some clever mocking
and pulling in a variety
of Django tools,
it's possible to test all
of those kinds of common Django test scenarios.
Or you can switch to easy mode
by using {{< extlink "https://django-test-plus.readthedocs.io/en/latest/" "django-test-plus" >}}.

I find that django-test-plus makes the simple things simple
and the hard things doable.

Check this out:

```python
from test_plus.test import TestCase

class TestHome(TestCase):
    def test_ok(self):
        self.get_check_200('home')
```

**That's super!**
I didn't have to:

* Mess with `reverse` to get the URL for `home`.
* Use the test `Client` to make an HTTP request.
* Or even `assert` to check that the response was a `200 OK`!

django-test-plus is full of goodies like that
to simplify the amount of test code
that you need to write
to do the job.

This is the most recent addition to my testing toolbox,
and I've become a big fan.

## Super Useful Techniques

### TestCases Are Ok!

When people get into pytest,
they seemed to get sucked into some vortex
that says that tests need to be functions
instead of methods on a class.

I rarely use function-based tests.
**Why?**
Because {{< extlink "https://www.python.org/dev/peps/pep-0020/" "namespaces are one honking great idea" >}}!
A `TestCase` class gives you a namespace
to put related tests.

I despise going
into a test file
that is a gigantic bag
of function tests.
Where does anything go?
I can't easily figure it out.

With a `TestCase`,
you have a nice home
to place your tests.
You can test everything
about a view
or a model
in a single test class.
Is your test case class getting too big?
Maybe that's a code smell
that your view or model is too big
and doing too much!
I find that `TestCase` classes help me
discover these kind of problems sooner.

### Give Tests a Common Structure

Most tests have a common anatomy.
There are times
when you can deviate,
but having a common structure overall
will make your test suite easier to understand.
For my projects,
here is the unit test anatomy.

```python
from test_plus.test import TestCase

class TestPetDetailView(TestCase):
    """I try to pick a class name that is the thing I want to test,
    prefixed by `Test`.
    """

    def test_some_meaningful_name(self):
        """Use a docstring.

        Future you or your teammate will appreciate the written context.
        It's tempting to write only a long method name. In my experience,
        a missing docstring will bite you in the end.

        I like blank lines between Arrange/Act/Assert to have clear separation.
        """
        # Arrange - Set up your test state.
        pet = PetFactory(name='Fido')

        # Act - Run the code that you want to test.
        self.get('pet:detail', pk=pet.id)

        # Assert - Check the code that the test acted on.
        self.assertResponseContains('Fido')
```

### Use An In-Memory SQLite Database If You Can

You should probably have a separate settings file
for your testing configuration.
Here's {{< extlink "https://github.com/mblayman/homeschool/blob/ff59a73113b69a02aae3babaf200b2330593355b/project/testing_settings.py" "an example" >}}
from my
[Building SaaS]({{< ref "/building-saas/_index.md" >}}) project.

Unless you need specific functionality
from a certain database,
using an in-memory SQLite database can provide some very fast testing
with no cleanup fuss.
To make this work,
I set my `DATABASES` setting
in my test settings file to:

```python
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}
```

Others might point out that you're not testing
with what you'll deploy to your site.
They're right.
Maybe you're ok with that risk
like I am.
Maybe you test with the real database
in Continuous Integration.
Whatever helps you sleep at night, go for it.

### Disable Running Migrations While Testing

Migrations are slow.
And if you're working with a database
that needs the latest model state
to run tests,
what if you just work
with the final model state?

Well, you can!
This little settings snippet will cause Django
to skip migrations
when running the test suite.
It can be a *huge* speed boon.

```python
class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()
```

### Use A Faster Password Hasher

I joined a company years ago
that ran Django
in their tech stack.
In my first couple of weeks
on the job,
I was exploring
(because the job was awesome and gave me the space to learn).

I did some code profiling
on the team's test suite
and found that an absurd amount
of time was spent calculating password hashes.
On a real site,
this is behavior we want
because we want secure password hashes
and can tolerate the computation
that makes those hashes more secure.
On a test suite
that creates user records
in a test
and immediately clears the database
between tests,
this is extremely wasteful processing time.

The company's test suite created so many `User` instances
that,
when I switched out the password hasher,
the run time was more than cut in half!
I'm talking about going from 25 minute CI test runs
to a little over 10 minutes!

If you are creating lots of users
in your tests,
then this kind of change is a must.
The easiest option is to use one of Django's faster
(and less secure) hashers
like the `MD5PasswordHasher`.
Or, if you like even more speed,
you can use this dummy (insecure!) hasher.

```python
class SimplePasswordHasher(BasePasswordHasher):
    """A simple hasher inspired by django-plainpasswordhasher"""

    algorithm = "dumb"  # This attribute is needed by the base class.

    def salt(self):
        return ""

    def encode(self, password, salt):
        return "dumb$$%s" % password

    def verify(self, password, encoded):
        algorithm, hash = encoded.split("$$", 1)
        assert algorithm == "dumb"
        return password == hash

    def safe_summary(self, encoded):
        """This is a decidedly unsafe version.

        The password is returned in the clear.
        """
        return {"algorithm": "dumb", "hash": encoded.split("$", 2)[2]}


PASSWORD_HASHERS = ("project.testing_settings.SimplePasswordHasher",)
```

### Supercharge Your Text Editor

Do you know how to run a single Django test
from your text editor
with a single keyboard shortcut?
If you answered "No,"
then you owe it to yourself
to change that answer to "Yes."

Many editors have tools
or plugins
that can make running tests extremely natural.
For me in Vim,
I can run a test by pressing `<spacebar> t`
(you can learn how in this {{< extlink "https://www.mattlayman.com/blog/2017/supercharging-vim-instant-testing/" "Supercharging Vim" >}} article of mine).
The results from the test
will display right
in my editor
so that I can immediately jump back
to fixing whatever is broken.

Adding the ability
to run your test rapidly
will dramatically improve the feedback loop
when writing code.
You will find yourself more engaged
and able to write code better
if you can run your test
in the blink of an eye.

## In The End...

All of this is just, like, my opinion, man.
I hope you find some of it useful though.
Good luck testing!

If you have questions
or enjoyed this article,
please feel free to message me on X
at {{< extlink "https://x.com/mblayman" "@mblayman" >}}
or share if you think others might be interested too.

<iframe width="560" height="315" src="https://www.youtube.com/embed/1vBesOFURek" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

