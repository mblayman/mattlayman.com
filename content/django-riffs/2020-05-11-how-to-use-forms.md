---
title: "Episode 5 - How To Use Forms"
aliases:
 - /django-riffs/5
 - /djangoriffs/5
 - /django-riffs/5.
 - /djangoriffs/5.
description: >-
    On this episode,
    we will learn about HTML forms
    and Django's form system
    to use when collecting input
    from users.
image: img/django-riffs-banner.png
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - forms

---

On this episode,
we will learn about HTML forms
and Django's form system
to use when collecting input
from users.

Listen at {{< extlink "https://open.spotify.com/episode/1tW4cgRVvbi67BQ39rOXLH" "Spotify" >}}.

## Last Episode

On the previous episode,
we looked at templates,
the primary tool
that Django provides
to build user interfaces
in your Django app.

## Web Forms 101

HTML can describe the type
of data
that you may want your users
to send to your site.
Collecting this data is done
with a handful of tags.
The primary HTML tags to consider are `form`, `input`, and `select`.

A `form` tag is the container
for all the data
that you want a user to send
to your application.
The tag has two critical attributes
that tell the browser how to send data: `action` and `method`.

```html
<form method="GET" action="/some/form/">
    <input type="text" name="message">
    <button type="submit">Send me!</button>
</form>
```

When the form's method is `GET`,
the form data will be sent as part
of the URL
in a querystring.
The GET request sent to the server will look
like `/some/form/?message=Hello`.
This type of form submission is most useful
when we don't need to save data
and are trying to do some kind of query.

The `POST` method of sending form data is for data
that we want to be secure or saved
within an application.

We've seen that `form` is the container
that guides how to send form data.
`input` and `select` are the tags
that let us display a meaningful form
to the user.

You can see a full list of types
on the {{< extlink "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input" "MDN input documentation" >}} page.

The other attribute, `name`, is the identifier
that the form will pair with the user data.
The server uses the identifier
so it can distinguish
between the pieces of data
that a form submission may include.

## Django Forms

Django's form features act as a bridge
between HTML forms
and Python classes and data types.
When presenting a form
to a user in view,
the form system is able
to display the proper HTML form tags
and structure.
When receiving this form data
from a user's submission,
the form system can translate the browser's raw form data
into native Python data that we can use.

```python
# application/forms.py

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)
```

1. Django forms are sub-classes
    of the `Form` class.
2. The data that we want to collect is listed
    as class level attributes.

If the template looks like:

```django
{{ form.as_p }}
```

Then Django will render:

```html
<p><label for="id_name">Name:</label>
  <input type="text" name="name" maxlength="100" required id="id_name"></p>
<p><label for="id_email">Email:</label>
  <input type="email" name="email" required id="id_email"></p>
<p><label for="id_message">Message:</label>
  <input type="text" name="message" maxlength="1000" required id="id_message">
</p>
```

To make it possible submit the form,
we need to wrap this rendered output
with a `form` tag
and include a submit button
and a CSRF token.

```django
<form action="{% url "some-form-view" %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <p><input type="submit" value="Send the form!"></p>
</form>
```

```python
# application/views.py

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import ContactForm

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Do something with the form data like send an email.
            return HttpResponseRedirect(reverse('some-form-success-view'))
    else:
        form = ContactForm()

    return render(request, 'contact_form.html', {'form': form})
```

* When the form is valid,
    the view does the extra work represented
    by the comment
    and redirects to a new view
    that can show some kind of success message.
* When the form is invalid,
    the view goes out of the `if` clause
    and calls `render`.
    Since the data is bound to the `form`,
    the contact form has enough information
    to show which form fields
    caused the errors
    that made the form invalid.

That's the core of form handling!
The presented view is a common pattern
for handling form views
in Django.
In fact, this view pattern is so common
that Django provides a built-in view
to implement what is done in the example
named `FormView`.

```python
# application/views.py

from django.views.generic import FormView

from .forms import ContactForm

class ContactUs(FormView):
    form = ContactForm
    template = 'contact_form.html'

    def get_success_url(self):
        return reverse('some-form-success-view')

    def form_valid(self, form):
        # Do something with the form data like send an email.
        return super().form_valid(form)
```

## Form Fields

With the basics of form handling done,
we can turn our attention
to the kinds
of fields
that forms can use.
The extensive list of fields is
in {{< extlink "https://docs.djangoproject.com/en/3.0/ref/forms/fields/" "the Django documentation" >}},
and we will look at a few
of the most common ones
in this article.

Fields are the critical intersection
between the world of the browser and HTML
and the Python world
with all of its robust data types.

### CharField

`CharField` is a real workhorse
for Django forms.
The `CharField` captures text input
and uses a standard `input` tag
with a type of `text`.
If you want to collect more text,
like in a feedback form,
you can switch
from the default `TextInput` widget
to a `Textarea` widget.
This will make your form render a `textarea` tag
that will give far more space
for any input.

```python
# application/forms.py

from django import forms

class FeedbackForm(forms.Form):
    email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea)
```

### EmailField

The `EmailField` is like a specialized version
of the `CharField`.
The field uses an `input` tag
with a type of `email`.
Many modern browsers can help
to check that valid email addresses are provided.
Also, when this field is validated within the framework,
Django will attempt to validate the email address too
in case the browser wasn't able to do it.

### DateField

A `DateField` is another field
that is mostly like a `CharField`.
The field even uses the `input` type of `text`
when rendered.
The difference with this field comes
from the data type that the form will provide
after it is validated.
A `DateField` will convert
{{< extlink "https://docs.djangoproject.com/en/3.0/ref/settings/#datetime-input-formats" "a variety of string formats" >}}
into a Python `datetime.date` object.

### ChoiceField

A `ChoiceField` is useful
when you want a user to make a choice
from a list of options.
For this field type,
we must provide a list of choices
that the user can pick from.
Imagine that we want to ask users
what their favorite meal of the day is.
Here's a form that can do that.

```python
# application/forms.py

from django import forms

class SurveyForm(forms.Form):
    MEALS = [("b", "Breakfast"), ("l", "Lunch"), ("d", "Dinner")]
    favorite_meal = forms.ChoiceField(choices=MEALS)
```

This will contain a form
with a `select` tag
that looks like:

```html
<p>
  <label for="id_favorite_meal">Favorite meal:</label>
  <select name="favorite_meal" id="id_favorite_meal">
    <option value="b">Breakfast</option>
    <option value="l">Lunch</option>
    <option value="d">Dinner</option>
  </select>
</p>
```

## Validating Forms

What is `is_valid` actually doing?
It does a lot!

When `is_valid` is `True`,
the form's data will be
in a dictionary named `cleaned_data`
with keys
that match the field names
declared by the forms.
With the validated data,
you access `cleaned_data` to do your work.
For instance,
if we had some kind of integration
with a support ticket system,
perhaps our `FeedbackForm` above is handled
in the view like:

```python
if form.is_valid():
    email = form.cleaned_data['email']
    comment = form.cleaned_data['comment']
    create_support_ticket(email, comment)
    return HttpReponseRedirect(reverse('feedback-received'))
```

When `is_valid` is `False`,
Django will store the errors it found
in an `errors` attribute.
This attribute will be used
when the form is re-rendered
on the page
(because, if you recall from the view example,
the form view pattern sends a bound form
back through a `render` call
in the failure case).

If you have a form field,
you can add customization
by writing a method on the form class.
The format of the method must match with the field name
and prepend `clean_`.
Let's imagine that we want a website
for Bobs.
In order to sign up for the website,
your email address must have "bob"
in it.
We can write a clean method
to check for that.

```python
# application/forms.py

from django import forms

class SignUpForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if 'bob' not in email:
            raise forms.ValidationError('Sorry, you are not a Bob.')
        return email
```

These `clean_<field name>` methods are hooks
that let you include extra checking.
This hook system gives you the perfect place
to put validation logic for data
that is specific
to your application.
But what about validating multiple pieces
of data?
This might happen when data has some kind
of interrelationship.
For instance,
if you're putting together a genealogy website,
you may have a form that records birth and death dates.
You might want to check those dates.

```python
# application/forms.py

from django import forms

class HistoricalPersonForm(forms.Form):
    name = forms.CharField()
    date_of_birth = forms.DateField()
    date_of_death = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        date_of_death = cleaned_data.get('date_of_death')
        if date_of_birth and date_of_death and date_of_birth > date_of_death:
            raise forms.ValidationError('Birth date must be before death date.')
        return cleaned_data
```

## Summary

That's how forms make it possible
to collect data
from your users
so your site can interact with them.
We've seen:

* Web forms and the `form` HTML tag
* The `Form` class that Django uses to handle form data in Python
* How forms are rendered to users by Django
* Controlling what fields are in forms
* How to do form validation

## Next Time

In the next episode,
we're going to talk about storing data
in a database.
Django gives us the ability
to do this storage
with models.
Models are a way to represent your application's data
and make your website very dynamic.

You can follow the show
on {{< extlink "https://open.spotify.com/show/1RtdveQIz5m5MqLKPWbhnD" "Spotify" >}}.
Or follow me or the show
on X
at
{{< extlink "https://x.com/mblayman" "@mblayman" >}}
or
{{< extlink "https://x.com/djangoriffs" "@djangoriffs" >}}.

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
