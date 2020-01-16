---
title: "User Accounts With django-allauth - Building SaaS #41"
description: >-
    In this episode, we added django-allauth to create accounts
    that default to email instead of using usernames.
    We added the package, configured some templates, and created tests.
type: video
image: img/2020/django-allauth.png
video: https://www.youtube.com/embed/makqrv3SgzU
aliases:
 - /building-saas/41
categories:
 - Twitch
 - Python
 - Django
tags:
 - Django
 - django-allauth
 - users

---

In this episode, we added django-allauth to create accounts
that default to email instead of using usernames.
We added the package, configured some templates, and created tests.

We continued to look at Will Vincent's
{{< extlink "https://wsvincent.com/django-login-with-email-not-username/" "django-allauth post" >}}
on creating user accounts
with email and passwords.

django-allauth let's us swap out username and email
so that users won't need to create a username,
which is the behavior that I want
for this service.

In `requirements.in`,
I installed django-allauth:

```txt
django-allauth==0.41.0
```

Then ran `pip-compile`
to create the new `requirements.txt`
and `pip` to install the actual package.

```bash
(venv) $ pip-compile --output-file=requirements.txt requirements.in
(venv) $ pip install -r requirements.txt
```

After that,
we needed to put django-allauth
into `INSTALLED_APPS`.

```python
# project/settings.py
INSTALL_APPS = [
    ...
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    ...
]
```

Then I added the settings that Will outlines.
These are settings that django-allauth needs
to set things up for email-based accounts.

```python
# project/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
```

Finally,
we created some place for the django-allauth views
to reside.

```python
# project/urls.py
urlpatterns = [
    path("office/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]
```

This gave us enough configuration
to see the views in action
on the local site.

After that,
we created an area for templates
at the root of the project.
We have to tell Django
where the templates directory is.

```python
# project/settings.py
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        ...
    }
]
```

Following template configuration,
we added some custom templates
for `login.html` and `signup.html`.

With templates in place,
I needed to make a place for user's to land
after they logged in.
I created a view named `app`
and pointed the settings at that view.

```python
# homeschool/schools/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def app(request):
    context = {}
    return render(request, "schools/app.html", context)
```

```python
# project/settings.py
LOGIN_REDIRECT_URL = "app"
ACCOUNT_LOGOUT_REDIRECT_URL = "app"
```

To finish off the night,
I wrote some tests
to verify the behavior
of my new view.

```python
# homeschool/schools/tests/test_views.py
from django.test import Client, TestCase
from django.urls import reverse

from homeschool.users.tests.factories import UserFactory


class TestApp(TestCase):
    def test_ok(self):
        """The app returns 200 OK for a user."""
        client = Client()
        user = UserFactory()
        client.force_login(user)

        response = client.get(reverse("app"))

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_access(self):
        """Unauthenticated users are redirected to the login page."""
        client = Client()

        response = client.get(reverse("app"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response.get("Location"))
```

These tests prove that an authenticated user can access the site
and an unauthenticated user get redirected
to the login page.

Next time,
we will move on
to some of the core models
of the project.
