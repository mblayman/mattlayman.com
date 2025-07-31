---
title: "User Authentication"
description: >-
    Our focus in this Understand Django article
    is how to manage users
    in your Django application.
    We'll study Django's built-in user authentication system.
image: img/django.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - authentication
 - authorization
series: "Understand Django"

---

{{< web >}}
In the previous
[Understand Django]({{< ref "/understand-django/_index.md" >}})
article,
we learned about the structure
of a Django *application*
and how apps are the core components
of a Django project.
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
we're going to dig into Django's built-in user authentication system.
We'll see how Django makes your life easier
by giving you tools
to help your web application interact
with the users
of your site.

{{< understand-django-series "auth" >}}

## Authentication And Authorization

We need to start with some terms
before we begin our study.
When your project interacts
with users,
there are two primary aspects tightly coupled
to users
that we must consider.

*Authentication*:
When a user tries to prove
that they are who they say they are,
that is authentication.
A user will typically authenticate
with your site
via some login form
or using a social provider
like Google
to verify their identity.

> Authentication can only prove
that {{< extlink "https://en.wikipedia.org/wiki/The_Important_Book" "you are you" >}}.

*Authorization*:
What is a user allowed to do?
Authorization answers that question.
We use authorization
to determine what permissions or groups a user belongs to,
so that we can scope what a user can do
on the site.

> Authorization determines what you can do.

The Django auth system covers both of these topics.
Sometimes the software industry will shorten authentication
to "authn"
and authorization to "authz,"
but I think those labels are fairly silly
and confusing.
I will call out topics by their full name
and refer to the entire Django system as "auth."

## Setup

If you used the `startproject` command
to begin your project,
then, congratulations,
you're done
and can move on!

The auth features
in Django require a couple
of built-in Django applications
and a couple
of middleware classes.

The Django apps are:

* `django.contrib.auth` and
* `django.contrib.contenttypes` (which the `auth` app depends on)

The middleware classes are:

* `SessionMiddleware` to store data about a user in a session
* `AuthenticationMiddleware` to associate users with requests

Middleware and sessions are both future topics
so consider them internal details
that you can ignore for now.

The Django docs provide additional context
about these prerequisites
so check out the
{{< extlink "https://docs.djangoproject.com/en/4.1/topics/auth/#installation" "auth topic installation section" >}}
for more details.

## Who Authenticates?

If your site is going to have any level
of personalization
for anyone
who uses it,
then we need some way
to track identity.

In the Django auth system,
identity is tracked
with a `User` model.
This model stores information
that you'd likely want
to associate
with anyone who uses your site.
The model includes:

* name fields,
* email address,
* datetime fields
    for when a user joins
    or logs in to your site,
* boolean fields
    for some coarse permissions
    that are very commonly needed,
* and password data.

The `User` model is a critically important model
in many systems.
Unless you're creating a website
that is entirely public data
and has no need
to factor in identity,
then you will probably use the `User` model heavily.

Even if you *don't* expect your site's visitors
to identify
in some fashion,
you'll still probably benefit
from the `User` model
because it is integrated
with the Django admin site.
I mentioned
{{< web >}}
in [Administer All The Things]({{< ref "/understand-django/2020-08-26-administer-all-the-things.md" >}})
{{< /web >}}
{{< book >}}
in the Administer All The Things chapter
{{< /book >}}
that we needed a user
with certain permissions
to access the admin,
but we glossed over the details
of what that meant.

The admin will only permit users
with the `is_staff` attribute set
to `True`.
`is_staff` is one of the boolean fields
that I listed
as included
in the default `User` model implementation.

Now we have an understanding
that the `User` model is a very important model
in a Django site.
At minimum,
the model is important as you use the Django admin,
but it can also be very important
for the people
that come to your site.

Next,
let's look a bit deeper
at authentication
and how that works
in conjunction
with the `User` model.

## Authenticating With Passwords

Like many other websites
that you've used,
Django's built-in auth system
authenticates users
with passwords.

When a user wants to authenticate,
the user must log in
to the site.
Django includes a `LoginView` class-based view
that can handle the appropriate steps.
The `LoginView` is a form view that:

* Collects the `username` and `password`
    from the user
* Calls the `django.contrib.auth.authenticate` function
    with the `username` and `password`
    to confirm that the user is who they claim to be
* Redirects to either a path that is set
    as the value of the `next` parameter
    in the URL's querystring
    or `settings.LOGIN_REDIRECT_URL`
    if the `next` parameter isn't set
* Or, if authentication failed,
    re-renders the form page
    with appropriate error messages

How does the `authenticate` function work?
The `authenticate` function delegates the responsibility
of deciding
if the user's credentials are valid
to an *authentication backend*.

Like we have seen
with templates
and with databases,
the auth system has swappable backends.
With different backend options,
you can have multiple ways
of authenticating.
The `authenticate` function will loop through any auth backends
that are set
in the `AUTHENTICATION_BACKENDS` list setting.
Each backend can do one of three things:

* Authenticate correctly with the user and return a `User` instance.
* Not authenticate and return `None`.
    In this case, the next backend is tried.
* Not authenticate and raise a `PermissionDenied` exception.
    In this case, no other backends are tried.

You could add a backend
to that setting
that lets people authenticate
with their social media accounts
({{< extlink "https://django-allauth.readthedocs.io/en/latest/" "django-allauth" >}}
is a great option to do exactly that).
You might be in a corporate setting
and need Single Sign-On (SSO)
for your company.
There are backend options
that enable that too.

Although there are many options,
we'll focus
on the built-in backend
included with the auth system.
The default backend is called the `ModelBackend`
and it is in the `django.contrib.auth.backends` module.

The `ModelBackend` is named as it is
because it uses the `User` model
to authenticate.
Given a `username` and `password`
from the user,
the backend compares the provided data
to any existing `User` records.

The `authenticate` function calls the `authenticate` *method*
that exists on the `ModelBackend`.
The backend does a lookup
of a `User` record
based on the given `username` passed to the method
by the `authenticate` function.
If the user record exists,
the backend calls `user.check_password(password)`
where `password` is the actual password
that is supplied
by the person
who submitted the POST
to the `LoginView`.

Django doesn't store actual passwords.
To do so would be a major weakness
in the framework
because any leak
of the database would leak all users' passwords.
And that's totally not cool.
Instead,
the `password` field
on the `User` model
stores a *hash*
of the password.

Maybe you've never encountered hashing before.
A hash is a computed value
that is generated
by running input data through a special function.
The details of the computation is a very deep topic,
especially when considering security,
but the important thing
to know about hashes is that you can't reverse the computation.

In other words,
if you generated a hash
from `mysekretpassword`,
then you wouldn't be able
to take the hash value
and figure out that the original input was `myseckretpassword`.

Why is this useful?
By computing hashes,
Django can safely store
that computed value
without compromising a user's password.
When a user wants to authenticate
with a site,
the user submits a password,
Django computes the hash
on that submitted value
and *compares it to the hash stored
in the database.*
If the hashes match,
then the site can conclude
that the user sent the correct password.
Only the password's hash
would match the hash stored
in the `User` model.

Hashing is a fascinating subject.
If you want to learn more about the guts
of how Django manages hashes,
I would suggest reading the
{{< extlink "https://docs.djangoproject.com/en/4.1/topics/auth/passwords/" "Password management in Django" >}}
docs
to see the details.

## Authentication Views

That's a lot of stuff
to do for authentication!

Is Django going to expect you to call the `authenticate` function
and wire together all the views yourself?
No!

I mentioned the `LoginView` earlier,
but that's not the only view
that Django provides
to make authentication manageable.
You can add the set of views
with a single `include`:

```python
# project/urls.py

from django.urls import include, path

urlpatterns = [
    ...
    path(
        "accounts/",
        include("django.contrib.auth.urls")
    ),
]
```

This set includes a variety of features.

* A login view
* A logout view
* Views to change a password
* Views to reset a password

If you choose to add this set,
your job is to override the built-in templates
to match the styling
of your site.
For example,
to customize the logout view,
you would create a file named `registration/logged_out.html`
in your templates directory.
The {{< extlink "https://docs.djangoproject.com/en/4.1/topics/auth/default/#all-authentication-views" "All authentication views" >}}
documentation provides information
about each view
and the name of each template
to override.
Note that you *must* provide a template for the login view
as the framework does not supply a default template for that view.

If you have more complex needs
for your site,
you might want to consider some external Django applications
that exist in the ecosystem.
I personally like {{< extlink "https://django-allauth.readthedocs.io/en/latest/" "django-allauth" >}}.
The project is very customizable
and provides a path
to add social authentication
to sign up with your social media platform
of choice.
I also like django-allauth
because it includes sign up flows
that you don't have to build yourself.
The application is definitely worth checking out.

We've now seen how Django authenticates users
to a website
with the `User` model,
the `authenticate` function,
and the built-in authentication backend, `ModelBackend`.
We've also seen how Django provides views
to assist
with login, logout, and password management.

Once a user is authenticated,
what is that user allowed to do?
We'll see that next as we explore authorization
in Django.

## What's Allowed?

### Authorization From User Attributes

Django has multiple ways
to let you control what a user is allowed
to do
on your site.

The simplest form
of checking
on a user
is to check
if the site has identified the user or not.
Before a user is authenticated
by logging in,
that user is anonymous.
In fact,
the Django auth system has a special class
to represent this kind
of anonymous user.
Sticking to the principle
of least surprise,
the class is called `AnonymousUser`.

The `User` model includes an `is_authenticated` attribute.
Predictably,
users that have authenticated will return `True`
for `is_authenticated`
while `AnonymousUser` instances return `False`
for the same attribute.

Django provides a `login_required` decorator
that can use this `is_authenticated` information.
The decorator will gate any view
that needs a user to be authenticated.

This may be the appropriate level
of authorization check
if you have an application
that restricts who is allowed
to log in.
For instance,
if you're running a Software as a Service (SaaS) application
that requires users
to pay a subscription
to use the product,
then you may have sufficient authorization checking
by checking `is_authenticated`.
In that scenario,
if your application only permits users
with an active subscription
(or a trial subscription)
to log in,
`login_required` will guard against any non-paying users
from using your product.

There are other boolean values
on the `User` model
that you can use for authorization checking.

* `is_staff` is a boolean to decide
    whether a user is a staff member or not.
    By default,
    this boolean is `False`.
    Only staff-level users are allowed
    to use the built-in Django admin site.
    You can also use the `staff_member_required` decorator
    if you have views that should only be used
    by members of your team
    with that permission.
* `is_superuser` is a special flag
    to indicate a user
    that should have access to everything.
    This "superuser" concept is very similar
    to the superuser that is present
    in Linux permission systems.
    There's no special decorator
    for this boolean,
    but you could use the `user_passes_test` decorator
    if you had very private views
    that you needed to protect.

```python
from django.contrib.admin.views.decorators import (
    staff_member_required
)
from django.contrib.auth.decorators import (
    user_passes_test
)
from django.http import HttpResponse

@staff_member_required
def a_staff_view(request):
    return HttpResponse(
        "You are a user with staff level permission."
    )

def check_superuser(user):
    return user.is_superuser

@user_passes_test(check_superuser)
def special_view(request):
    return HttpResponse(
        "Super special response"
    )
```

The `user_passes_test` decorator behaves much
like `login_required`,
but it accepts a callable
that receives a user object
and returns a boolean.
If the boolean value is `True`,
the request is permitted
and the user gets the response.
If the boolean value is `False`,
the user will be redirected
to the login page.

### Authorization From Permissions And Groups

The first set of checks
that we looked at is data
that is stored
with a `User` model record.
While that works well
for some cases
that apply to many sites,
what about authorization
that depends
on what your application does?

Django comes with a flexible permission system
that can let your application control
who can see what.
The permission system includes some convenient auto-created permissions
as well as the ability to make custom permission
for whatever purpose.
These permission records are `Permission` model instances
from `django.contrib.auth.models`.

Any time you create a new model,
Django will create an additional set of permissions.
These auto-created permissions map
to the Create, Read, Update, and Delete (CRUD) operations
that you can expect to use
in the Django admin.
For instance,
if you have a `pizzas` app
and create a `Topping` model,
Django would create the following permissions:

* `pizzas.add_topping` for Create
* `pizzas.view_topping` for Read
* `pizzas.change_topping` for Update
* `pizzas.delete_topping` for Delete

A big reason to create these permissions is to aid your development
*and* add control to the Django admin.
Staff-level users (i.e., `user.is_staff == True`)
in your application have no permissions
to start with.
This is a safe default
so that any new staff member cannot access all
of the data
in your system
unless you grant them more permissions
as you gain trust
in them.

When a staff user logs into the Django admin,
they will initially see very little.
As permissions are granted
to the user's account,
the Django admin will reveal additional information corresponding
to the selected permissions.
Although permissions are often granted
through the `User` admin page,
you can add permissions
to a user
through code.
The `User` model has a `ManyToManyField`
called `user_permissions`
that associates user instances
to particular permissions.

Continuing with the pizza application example,
perhaps you work with a chef
for your pizza app.
Your chef may need the ability
to control any new toppings
that should be available to customers,
but you probably don't want the chef
to be able to delete orders
from the application's history.

For the chef,
you'd grant the `pizzas.add_topping`,
`pizzas.view_topping`,
and
`pizzas.change_topping` permissions,
but you'd leave out `orders.delete_order`.

```python
from django.contrib.auth.models import (
    Permission, User
)
from django.contrib.contenttypes.models import (
    ContentType
)
from pizzas.models import Topping

content_type = ContentType.objects.get_for_model(
    Topping
)
permission = Permission.objects.get(
    content_type=content_type,
    codename="add_topping"
)
chef_id = 42
chef = User.objects.get(id=42)
chef.user_permissions.add(permission)
```

We haven't covered the `contenttypes` app
so this code may look unusual
to you,
but the auth system uses content types
as a way
to reference models generically
when handling permissions.
You can learn more about content types
and their uses
at {{< extlink "https://docs.djangoproject.com/en/4.1/ref/contrib/contenttypes/" "the contenttypes framework" >}}
documentation.
The important point
to observe from the example
is that permissions behave
like any other Django model.

Adding permissions to individual users is a nice feature
for a small team,
but if your team grows,
it could devolve
into a nightmare.

Let's suppose that your application is wildly successful,
and you need to hire a large support staff
to help
with customer issues.
If your support team needs
to view certain models
in your system,
it would be a total pain
if you had to manage that
per staff member.

Django has an ability to create groups
to alleviate this problem.
The `Group` model is the intersection
between a set of permissions
and a set of users.
Thus,
you could create a group
like "Support Team,"
assign all the permissions
that such a team should have,
and include all your support staff
on that team.
Now,
any time that the support staff members require a new permission,
it can be added once
to the group.

A user's groups are tracked
with another `ManyToManyField`
called `groups`.

```python
from django.contrib.auth.models import (
    Group, User
)

support_team = Group.objects.get(
    name="Support Team"
)
support_sally = User.objects.get(
    username="sally"
)
support_sally.groups.add(support_team)
```

In addition to the built-in permissions
that Django creates
and the group management system,
you can create additional permissions
for your own purposes.

Let's give our chef permission
to bake pizzas
in our imaginary app.

```python
from django.contrib.auth.models import (
    Permission, User
)
from django.contrib.contenttypes.models import (
    ContentType
)
from pizzas.models import Pizza

content_type = ContentType.objects.get_for_model(
    Pizza
)
permission = Permission.objects.create(
    codename="can_bake",
    name="Can Bake Pizza",
    content_type=content_type,
)
chef_id = 42
chef = User.objects.get(id=42)
chef.user_permissions.add(permission)
```

To check on the permission in our code,
you can use the `has_perm` method
on the `User` model.
`has_perm` expects an application label
and the permission codename
joined together
by a period.

```python
>>> chef = User.objects.get(id=42)
>>> chef.has_perm('pizzas.can_bake')
True
```

You can also use a decorator
on a view
to check a permission as well.
The decorator will check the `request.user`
for the proper permission.

```python
# pizzas/views.py

from django.contrib.auth.decorators import permission_required

@permission_required('pizzas.can_bake')
def bake_pizza(request):
    # Time to bake the pizza
    # if you're allowed.
    ...
```

## Working With Users In Views And Templates

Now we've discussed how to authenticate users
and how to check their authorization.
How do we *interact* with users
in your application code?

The first way is inside of views.
Part of configuring the auth system is to include the `AuthenticationMiddleware`
in `django.contrib.auth.middleware`.

This middleware has one job
in request processing:
add a `user` attribute to the `request`
that the view will receive.
This middleware gives us very clean
and convenient access
to the user record.

```python
# application/views.py

from django.http import HttpResponse

def my_view(request):
    if request.user.is_authenticated:
        return HttpResponse(
            'You are logged in.'
        )
    else:
        return HttpResponse(
            'Hello guest!'
        )
```

The `AuthenticationMiddleware` is what makes it possible
for the decorators
{{< web >}}
that I've described in this article
{{< /web >}}
{{< book >}}
that I've described in this chapter
{{< /book >}}
(i.e., `login_required`, `user_passes_test`, and `permission_required`)
to work.
Each of the decorators finds the `user` record
as an attribute attached to the `request`.

How about templates?
If you had to add a user
to a view's context
for every view,
that would be tedious.

Thankfully,
there is a context processor
named `auth`
that lets you avoid that pain
(the processor is in `django.contrib.auth.context_processors`).
The context processor will add a `user`
to the context
of every view
when processing a request.

Recall that a context processor is a function
that receives a `request` object
and returns a dictionary
that will be merged
into the context.
Knowing that,
can you guess how this context processor works?

If you guessed `AuthenticationMiddleware`,
{{< web >}}
you get a cookie! 🍪
{{< /web >}}
{{< book >}}
you get a cookie!
{{< /book >}}
Since the middleware adds the `user`
to the `request`,
the context processor has the very trivial job
of creating a dictionary
like `{'user': request.user}`.
There's a bit more to the actual implementation,
and you can check out the
{{< extlink "https://github.com/django/django/blob/4.1/django/contrib/auth/context_processors.py#L49" "Django source code" >}}
if you want to see those details.

What does this look like in practice?
We've actually seen this already!
One of the examples from the explanation
of templates used the `user` context variable.
Here's the example again so you don't need to jump back.

{{< web >}}
```django
{% if user.is_authenticated %}
    <h1>Welcome, {{ user.username }}</h1>
{% endif %}
```
{{< /web >}}
{{< book >}}
```djangotemplate
{% if user.is_authenticated %}
    <h1>Welcome, {{ user.username }}</h1>
{% endif %}
```
{{< /book >}}

If you decide to use Django's permissions,
you can also take advantage of the `perms` context variable
in your templates.
This variable is supplied
by the `auth` context processor as well
and gives your template access to the permissions
of the `user` in a concise manner.
The {{< extlink "https://docs.djangoproject.com/en/4.1/topics/auth/default/#permissions" "Django docs" >}} include some good examples
of how the `perms` variable can be used.

Now you've seen how Django leverages the auth middleware
to make users easily accessible
to your views and templates.

## Summary

{{< web >}}
In this article,
{{< /web >}}
{{< book >}}
In this chapter,
{{< /book >}}
we got into Django's built-in user auth system.

We learned about:

* How auth is set up
* What the `User` model is
* How authentication works
* Django's built-in views for making a login system
* What levels of authorization are available
* How to access users in views and templates

{{< web >}}
Next time we'll study middleware
{{< /web >}}
{{< book >}}
In the next chapter, we'll study middleware
{{< /book >}}
in Django.
As the name implies,
middleware is some code
that exists
in the "middle"
of the request and response process.
We will learn about:

* The mental model for considering middleware
* How to write your own middleware
* Some of the middleware classes that come with Django

{{< web >}}
If you have questions,
you can reach me online
on X
where I am
{{< extlink "https://x.com/mblayman" "@mblayman" >}}.
{{< /web >}}
&nbsp;
