---
title: "User Interaction With Forms"
description: >-
    How do users provide data
    to your website
    so you can interact
    with them?
    We can answer that question
    by exploring Django's form system,
    and the tools that Django provides
    to simplify your site
    as you engage
    with your users.
image: /static/img/django.png
slug: user-interaction-forms
date: 2020-05-05
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - forms

---

{{< web >}}
In the previous
[Understand Django](/blog/understand-django)
article,
we saw how Django templates work
to produce a user interface.
That's fine
if you only need to display a user interface,
but what do you do
{{< /web >}}
if you need your site
to interact with users?
You use Django's form system!
{{< web >}}
In this article,
{{< /web >}}
we'll focus
on how to work with web forms
using the Django form system.

1. [From Browser To Django](/understand-django/browser-to-django)
2. [URLs Lead The Way](/understand-django/urls-lead-way)
3. [Views On Views](/understand-django/views-on-views)
4. [Templates For User Interfaces](/understand-django/templates-user-interfaces)
5. User Interaction With Forms
6. [Store Data With Models](/understand-django/store-data-with-models)
7. [Administer All The Things](/understand-django/administer-all-the-things)
8. [Anatomy Of An Application](/understand-django/anatomy-of-an-application)
9. [User Authentication](/understand-django/user-authentication)
10. [Middleware Do You Go?](/understand-django/middleware-do-you-go)
11. [Serving Static Files](/understand-django/serving-static-files)
12. [Test Your Apps](/understand-django/test-your-apps)
13. [Deploy A Site Live](/understand-django/deploy-site-live)
14. [Per-visitor Data With Sessions](/understand-django/sessions)
15. [Making Sense Of Settings](/understand-django/settings)
16. [User File Use](/understand-django/media-files)
17. [Command Your App](/understand-django/command-apps)
18. [Go Fast With Django](/understand-django/go-fast)
19. [Security And Django](/understand-django/secure-apps)
20. [Debugging Tips And Techniques](/understand-django/debugging-tips-techniques)

## Web Forms 101

Before we can dive into how Django handles forms,
we need to have an understanding of HTML forms
in general.
Django's form functionality builds upon web forms
so this topic won't make sense
without a baseline knowledge
of the topic.

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

`action` would be better named as "destination" or "url."
Alas, we are stuck with `action`.
This attribute of the `form` tag is where user data should be sent to.
It's also useful to know that leaving out `action`
or using `action=""` will send any form data
as an HTTP request to the same URL
that the user's browser is on.

The `method` attribute dictates which HTTP method to use
and can have a value of `GET` or `POST`.
When paired with `action`,
the browser knows how to send a properly formatted HTTP request.

Let's say we have this example.

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
For instance,
you could give your application some search functionality
with a URL like `/search/?q=thing+to+search`.
These links could be bookmarked easily
and are a natural fit
for that kind of function.

The `POST` method of sending form data is for data
that we want to be secure or saved
within an application.
With a GET request,
form data in the querystring is exposed
in a number of places
(see [more information](https://owasp.org/www-community/vulnerabilities/Information_exposure_through_query_strings_in_url)
from the Open Web Application Security Project (OWASP)).
On the other hand,
POST sends the data in the body
of the HTTP request.
This means that if your site is secure
(i.e., using HTTPS),
then data is encrypted
while traveling
from a browser to a server.

If you ever login to a website
and submit a password
in a form,
you can be nearly certain
that the form is sent
with the POST method option
(and if it's not, run away!).

We've seen that `form` is the container
that guides how to send form data.
`input` and `select` are the tags
that let us display a meaningful form
to the user.

The more prevalent tag is `input`.
With the `input` tag,
form authors will set `type` and `name` primarily.
The `type` attribute tells the browser
which kind of input to display.

* Do we need a checkbox? `type="checkbox"`
* Do we need a password field that hides characters? `type="password"`
* How about a classic text box? `type="text"`

You can see a full list of types
on the [MDN input documentation](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input) page.

The other attribute, `name`, is the identifier
that the form will pair with the user data.
The server uses the identifier
so it can distinguish
between the pieces of data
that a form submission may include.

Another tag that your forms may use is the `select` tag.
This kind of tag is less frequent
than the `input` tag.
The `select` tag lets users make a choice
from a list of options.
The default browser user interface
for this tag is a dropdown menu.

With these core elements
of HTML forms,
we are equipped
to understand Django's form capabilities.
Let's dive in!

## Django Forms

Django's form features act as a bridge
between HTML forms
and Python classes and data types.
When presenting a form
to a user via a view,
the form system is able
to display the proper HTML form tags
and structure.
When receiving this form data
from a user's submission,
the form system can translate the browser's raw form data
into native Python data that we can use.

We can begin
with the `Form` class.
A form class acts as the data declaration
of what data we need
from the user.
Here's an example that we can examine.

```python
# application/forms.py

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100
    )
    email = forms.EmailField()
    message = forms.CharField(
        max_length=1000
    )
```

* User-defined Django forms should subclass the `Form` class.
    This class adds a lot of powerful functionality
    that will aid us
    as we explore more.
* The data that we want to collect is listed
    as class level attributes.
    Each field of the form is a certain field type
    that has its own characteristics
    to help translate raw form data
    into the data types
    that we want to work with in views.

If we take this form
and add it to a view's context as `form`,
then we can render it in a template.
The default rendering of the form uses an HTML table,
but we can render the fields in a simpler format
with the `as_p` method.
This method will use paragraph tags instead
for the form elements.
If the template looks like:

{{< web >}}
```django
{{ form.as_p }}
```
{{< /web >}}

Then Django will render:

{{< web >}}
```html
<p><label for="id_name">Name:</label>
  <input type="text" name="name" maxlength="100" required id="id_name"></p>
<p><label for="id_email">Email:</label>
  <input type="email" name="email" required id="id_email"></p>
<p><label for="id_message">Message:</label>
  <input type="text" name="message" maxlength="1000" required id="id_message">
</p>
```
{{< /web >}}

To make it possible to submit the form,
we need to wrap this rendered output
with a `form` tag
and include a submit button
and a CSRF token.

Huh? *CSRF token?*
Sadly,
the world is full of nefarious people
who would love to hack your application
to steal data
from others.
A CSRF token is a security measure
that Django includes to make it harder
for malicious actors
to tamper with your form's data.
We'll talk more about security
{{< web >}}
in a future article.
{{< /web >}}
For now,
sprinkle the token into your forms
with Django's built-in template tag
and everything should work.

{{< web >}}
```django
<form action="{% url "some-form-url" %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <p><input
        type="submit"
        value="Send the form!"></p>
</form>
```
{{< /web >}}

That's how a form gets displayed.
Now let's look at a view that handles the form properly.
When working with form views,
we will often use a view
that is able to handle
both `GET` and `POST` HTTP requests.
Here's a full view
that we can break down piece by piece.
The example uses a function view
for simplicity,
but you could do something similar
with a class-based view.

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
            # Do something with the form data
            # like send an email.
            return HttpResponseRedirect(
                reverse('some-form-success-url')
            )
    else:
        form = ContactForm()

    return render(
        request,
        'contact_form.html',
        {'form': form}
    )
```

If we start
by thinking about the `else` branch,
we can see how little this view does
on a `GET` request.
When the HTTP method is a `GET`,
it creates an empty form
with no data passed to the constructor
and renders a template
with the `form`
in the context.

`contact_form.html` contains the Django template above
to display the HTML form
to the user.
When the user clicks "Send the form!",
another request comes
to the same view,
but this time the method is an HTTP `POST`
and contains the submitted data.

The `POST` request creates a `form`,
but there is a difference
in how it is constructed.
The form submission data is stored
in `request.POST`,
which is a dictionary-like object
that we first encountered
{{< web >}}
in the views article.
{{< /web >}}
By passing `request.POST`
to the form's constructor,
we create a form with data.
In the Django documentation,
you will see this called a *bound form*
because data is *bound* to the form.

With the form ready,
the view checks if the data is valid.
We'll talk about form validation
in detail later
{{< web >}}
in this article.
{{< /web >}}
In this instance,
you can see that `is_valid` could return `False`
if the form data contained "I am not an email address"
in the `email` field, for instance.

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
from django.urls import reverse

from .forms import ContactForm

class ContactUs(FormView):
    form_class = ContactForm
    template_name = 'contact_form.html'

    def get_success_url(self):
        return reverse(
            'some-form-success-view'
        )

    def form_valid(self, form):
        # Do something with the form data
        # like send an email.
        return super().form_valid(form)
```

The `FormView` expects a form class and template name
and provides some methods to override
for the common places
where your own application logic should live.

## Form Fields

With the basics of form handling done,
we can turn our attention
to the kinds
of fields
that forms can use.
The extensive list of fields is
in [the Django documentation](https://docs.djangoproject.com/en/4.1/ref/forms/fields/),
and we will look at a few
of the most common ones
{{< web >}}
in this article.
{{< /web >}}

The first thing to remember about Django form fields is
that they convert HTML form data
into native Python data types.
If you examine the data
of a form submission,
you'll discover
that each value is essentially a string
by default.
If Django did nothing for you,
then you would constantly have to convert
to the data types that you want.
By working with form fields,
that data conversion is automatically handled
for you.
For instance,
if you choose a `BooleanField`,
after the Django form is validated,
that field value will be either `True` or `False`.

Another important item to know about fields is
that they are associated
with particular Django widgets.
Widgets are the way
to control what Django renders
when you render a form.
Each form field has a default widget type.
Sticking with `BooleanField`,
its default widget is a `CheckboxInput`
which will render an `input` tag
with a type of `checkbox`
(i.e., your standard form checkbox).

Fields are the critical intersection
between the world of the browser and HTML
and the Python world
with all of its robust data types.

What fields are you most likely
to reach for?
And what do you need to set on those fields?

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
    comment = forms.CharField(
        widget=forms.Textarea
    )
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
[a variety of string formats](https://docs.djangoproject.com/en/4.1/ref/settings/#datetime-input-formats)
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
    MEALS = [
        ("b", "Breakfast"),
        ("l", "Lunch"),
        ("d", "Dinner")
    ]
    favorite_meal = forms.ChoiceField(
        choices=MEALS
    )
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

This handful of fields will deal
with most form needs.
Be sure to explore the full list
of what is available
to equip yourself
with other beneficial types.

Form fields share some common attributes
for things that each field needs.

The `required` attribute is a boolean
that specifies whether a field must have a value or not.
For instance,
it wouldn't make much sense
if your site had a support form
that you planned to use to contact people via email,
and an `email` field
on the form
was optional.

`label` sets what text is used
for the `label` tag
that is rendered
with a form `input`.
In the meal example,
we could use the `label` attribute to change "Favorite meal"
into "What is your favorite meal?"
That would make a much better survey experience.

Sometimes forms may not be clear
and users need help.
You can add a `help_text` attribute
that will render additional text
by your form field wrapped in a `span` tag
with a `helptext` class
if you want to style it with CSS.

Because forms are one of the main ways
that users will provide information
to your application,
the forms system is rich with features.
You can learn a lot about Django
by diving deeply
into that portion
of the documentation.

Let's shift our focus
to form validation
since I've mentioned it a few times
in passing now.

## Validating Forms

In the view example,
I showed a form
that calls the `is_valid` method.
At a high level,
we can understand
what that method is doing;
it's determining whether the form is valid or not.

But what is `is_valid` actually doing?
It does a lot!

The method handles each of the fields.
As we saw,
fields can have a final data type
(like with `BooleanField`)
or an expected structure
(like with `EmailField`).
This process of converting data types
and validating the field data is called cleaning.
In fact,
each field must have a `clean` method
that the form will call
when `is_valid` is called.

When `is_valid` is `True`,
the form's data will be
in a dictionary named `cleaned_data`
with keys
that match the field names
declared by the form.
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
    create_support_ticket(
        email,
        comment
    )
    return HttpReponseRedirect(
        reverse('feedback-received')
    )
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

Once again,
Django is doing a lot of heavy lifting
for you
to make working with forms easier.
The system *also* permits developers
to add custom validation logic.

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
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if 'bob' not in email:
            raise forms.ValidationError(
                'Sorry, you are not a Bob.'
            )
        return email
```

There are a few important points about this:

* `clean_email` will only try to clean the `email` field.
* If validation fails,
    your code should raise a `ValidationError`.
    Django will handle that and put the error
    in the right format
    in the `errors` attribute
    of the form.
* If everything is good,
    be sure to return the cleaned data.
    That is part of the interface
    that Django expects for clean methods.

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
        if (
            date_of_birth and
            date_of_death and
            date_of_birth > date_of_death
        ):
            raise forms.ValidationError(
                'Birth date must be before death date.'
            )
        return cleaned_data
```

This method is similar to `clean_<field name>`,
but we must be more careful.
Individual field validations run first,
but they may have failed!
When clean methods fail,
the form field is removed from `cleaned_data`
so we can't do a direct key access.
The clean method checks if the two dates are truthy and each has a value,
then does the comparison between them.

Custom validation is a great feature to improve the quality
of the data you collect
from users of your application.

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

Now that we know how to collect data
from users,
how can we make the application hold onto that data
for them?
{{< web >}}
In the next article,
{{< /web >}}
we will begin to store data
in a database.
We'll work with:

* How to set up a database for your project.
* How Django uses special classes called models to keep data.
* Running the commands that will prepare a database
    for the models you want to use.
* Saving new information into the database.
* Asking the database for information that we stored.

{{< web >}}
If you have questions,
you can reach me online
on X
where I am
[@mblayman](https://x.com/mblayman).
{{< /web >}}
&nbsp;
