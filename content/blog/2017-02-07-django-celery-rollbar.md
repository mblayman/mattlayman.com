---
title: Rollbar monitoring of Celery in a Django app
description: >-
  Rollbar provides some excellent middleware
  that makes setup a snap for a Django application.
  But what if you're running Celery
  with your Django application too?
  There are a few bumps
  in the road
  that I'll explain how to resolve.
image: img/2017/rollbar.jpeg
type: post
aliases:
 - /2017/django-celery-rollbar.html

---

The last [Rollbar post](/2017/ember-rollbar.html)
that I made covered how to integrate Rollbar
into your Ember application.
As a reminder,
{{< extlink "https://rollbar.com/" "Rollbar" >}}
is a service
that let's you record your errors
*wherever* they happen.
In that original post,
I didn't cover how to include Rollbar
in a Django application
because the Rollbar team does a great job
of that
in {{< extlink "https://rollbar.com/docs/notifier/pyrollbar/" "their own documentation" >}}.
**But what happens when you want to do asynchronous task management
with {{< extlink "http://www.celeryproject.org/" "Celery" >}}
in your Django app?**
I encountered some gotchas
in making that work
so I'm going to describe what I learned here.

{{< extlink "https://www.collegeconductor.com/" "College Conductor" >}}
uses Celery
to make sure
that slow tasks
like sending email
do not happen
in the web request.
I still want the safety net
of error reporting
in my async tasks,
but I discovered that my Celery workers
were not sending errors to Rollbar.
This initally surprised me because I was using the Django middleware
in the Rollbar documentation.

When I looked closely
at the problem,
I realized that it made perfect sense
that Celery was not running Rollbar code.
The Celery worker reads the Django settings
to initialize its tasks,
but it does not execute the Django middleware.
Thus,
the Rollbar configuration is skipped.
After searching,
I found {{< extlink "https://github.com/rollbar/rollbar-celery-example" "Rollbar's example code" >}}
for configuring a Celery worker
and that is when I encountered my problem.
The sample code and the Django middleware
configure the `rollbar.BASE_DATA_HOOK` attribute,
but they use different Python functions
for the hook.
Both the Celery worker and the Django application
need access to the `Celery` app instance
so I had to resolve how to have two different `BASE_DATA_HOOK` functions.

The best solution I could devise
was to do Celery specific configuration
if a certain environment variable was set.

In my Django settings file, I have the necessary `ROLLBAR` dictionary:

```python
ROLLBAR = {
    'access_token': os.environ['ROLLBAR_ACCESS_TOKEN'],
    'environment': os.environ['ROLLBAR_ENVIRONMENT'],
    'root': BASE_DIR,
    'enabled': bool(os.environ.get('ROLLBAR_ENABLED', False)),
}
```

These settings, in combination with the Django middleware,
make the Django application report errors to Rollbar.
(Note: my Django app follows the
{{< extlink "https://12factor.net/" "twelve factor app" >}} design
so all of the environment specific stuff
like acccess tokens
are injected as environment variables.
It's a very powerful pattern.)

Over in my `celery.py` module, the code looks like:

```python hl_lines="13"
import os

from celery import Celery
from celery.signals import task_failure

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'conductor.settings.development')

app = Celery('conductor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if bool(os.environ.get('CELERY_WORKER_RUNNING', False)):
    from django.conf import settings
    import rollbar
    rollbar.init(**settings.ROLLBAR)

    def celery_base_data_hook(request, data):
        data['framework'] = 'celery'

    rollbar.BASE_DATA_HOOK = celery_base_data_hook

    @task_failure.connect
    def handle_task_failure(**kw):
        rollbar.report_exc_info(extra_data=kw)
```

The linchpin of this setup is the `CELERY_WORKER_RUNNING` environment variable.
All the code within the `if` statement will look very similar
to Rollbar's Celery example.
In my configuration management tool,
I add the `CELERY_WORKER_RUNNING` variable for the Celery worker
and exclude it for the Django app.
By doing this,
the system is able to get the proper `BASE_DATA_HOOK`
depending on the execution context.

Without too much extra work,
I managed to make my project send Django and Celery errors
to Rollbar
in a shared module.
I hope this setup can help anyone else struggling
to make the two contexts play nicely together.
