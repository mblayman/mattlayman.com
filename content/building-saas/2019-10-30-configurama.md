---
title: "Configurama - Building SaaS #36"
description: >-
  In this episode, we turned our attention to handling settings and configuration.
  We discussed different techniques for handling settings,
  looked at available tools, and started integrating one of the tools into the project.
type: video
image: img/python-django.png
video: https://www.youtube.com/embed/LoNdFiMwH8M
aliases:
 - /building-saas/36
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Django
 - Configuration
 - Goodconf

---

In this episode, we turned our attention to handling settings and configuration.
We discussed different techniques for handling settings,
looked at available tools, and started integrating one of the tools into the project.

The initial discussion
in the stream
focused on different ways of doing settings.
I talked about what I view as a difference
between configuration (mostly static stuff)
and settings (dynamic parts of the app).

I also discussed where to get settings from.
We talked about the {{< extlink "https://12factor.net" "12 Factor App" >}} style
with environment variables,
and secret management tools like {{< extlink "https://www.vaultproject.io/" "HashiCorp Vault" >}}
and {{< extlink "https://aws.amazon.com/kms/" "AWS KMS" >}}.
Ironically, I blanked out on {{< extlink "https://aws.amazon.com/secrets-manager/" "AWS Secrets Manager" >}}
as an option.
Additionally,
we considered the alternative
of reading settings
from a file
instead of environment variables
and the security implications
of environment variables.

After digging into strategies,
I showed the documentation
of popular tools
in the Django space.
We found some
of these tools listed
on the new {{< extlink "https://forum.djangoproject.com/t/top-5-3rd-party-packages/391" "Django Forum" >}}!

{{< extlink "https://django-environ.readthedocs.io/en/latest/" "django-environ" >}}
was the first tool
that we looked into.
The package supports the 12 Factor pattern
and is designed to work
with environment variables.
It also has the ability to use an `.env` file
for reading from a file
if desired.
One nice thing about this tool is
that it can translate some conventional environment variables
into standard Django settings patterns.
For instance,
by defining `DATABASE_URL`,
the tool can produce the entire dictionary
of database settings
by calling `env.db()`.
That's pretty neat.

The next tool was {{< extlink "https://django-configurations.readthedocs.io/en/stable/" "django-configurations" >}}.
django-configurations seemed more about handling different environment types
using an inheritence scheme.
The idea is interesting.

Lastly,
we looked at {{< extlink "https://github.com/lincolnloop/goodconf" "Goodconf" >}}.
Goodconf lets you define a configuration class
that describes all the dynamic settings.
From that definition,
Goodconf can read from a settings file defined
in JSON or YAML format,
or it can read from environment variables.
I like a lot of aspects about Goodconf.
The package lets us define help text
to go with the setting.
For large projects,
this is super useful
so that anyone can inspect what a setting is for.
Conveniently,
a Goodconf config instance can generate the settings file
which can then be updated
or act as a template.

After evaluating these tools,
I concluded that Goodconf was the best fit
for College Conductor.
We spent the remainder
of the stream
integrating the tool
into the project.

On the next stream,
we will flesh out the rest
of the configuration
and test out the changes
on different environments.
