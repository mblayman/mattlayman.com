---
title: "Python alternative to Docker"
description: >-
  Are you using Python
  and thinking about containers
  to deploy your app?
  Before you jump to Docker,
  consider other package formats
  that may fit better.
  This article explores one such format
  from LinkedIn.
image: img/2019/docker.png
type: post
categories:
 - Python
tags:
 - Python
 - Docker
 - Shiv
 - containers

---

Deploying a Python app
to a server
is surprisingly hard.
Without blinking,
you'll be dealing
with virtual environments
and a host
of other complications.

The landscape
of deployment methods is huge.
What if I told you
that there is a way
to build your app
into a single file
and it *isn't a Docker container*?

In this article,
we're going to look at common ways
of deploying Python apps.
We'll explore the touted benefits
of Docker containers
to understand why containers are so popular
for web apps.
Finally, we'll look at an **alternative**
to Docker
that may be a lot simpler
for your Python web app
and compare and contrast this alternative against Docker.

## App deployment 101

The core goal of deploying a web application
on the internet
can be summarized
in a few words:

> Get your application code
to a server (machine)
where it can run
and be reached by people on the internet.

In that statement are many explicit and implicit requirements
for your web app.
Some of the big requirements look like:

1. You must have an app.
2. You must have a machine that can store the app.
3. You must have a mechanism to get the app to the machines.
4. You must have a web server that can run the app.
5. Your machine must be reachable at a domain on the internet.
6. Your machine must be secure
    (for some reasonable level of "secure"
    based on your business needs).

This article assumes you already have an application.
If you don't,
Python has a great set
of web frameworks
to help you build the app you want.
In my totally biased opinion,
{{< extlink "https://www.djangoproject.com/" "Django" >}}
is a great (if not the best) place to start.

###### Platform as a Service (PaaS) sidebar

At this stage,
I would do you a huge disservice
if I did not highlight the awesome value
of a Platform as a Service (PaaS).

If you're starting a new web application
and time-to-market is very important to you,
then (*PLEASE!*) consider trading money
for time
by using a PaaS.
I'm not sponsored
by any PaaS for telling you this,
but a PaaS
(like {{< extlink "https://www.heroku.com/" "Heroku" >}}
or {{< extlink "https://www.pythonanywhere.com/" "PythonAnywhere" >}})
will save you oodles
of time
for a bit more cash up-front.

{{< figure src="/img/2019/heroku.png" caption="Seriously, check it out." >}}

Since your time is **extremely** valuable
in an early stage business,
I'd suggest that a PaaS should be your go-to deployment target.
Your future self will thank you
as you're able to focus
on your problem
rather than deal
with servers.

End sidebar.

Still here?
Good.
I think this topic is still very interesting
as we dive into the guts.

### From app to server

Once you've created your Minimum Viable Product (MVP) application,
you need to be able to show it off
to the world.
We can do that
by getting access to a server
via a hosting service.

Hosting services include big players
like
{{< extlink "https://aws.amazon.com/" "Amazon Web Services (AWS)" >}},
{{< extlink "https://cloud.google.com/" "Google Cloud Platform (GCP)" >}},
or
{{< extlink "https://azure.microsoft.com/en-us/" "Microsoft Azure" >}}.
These large companies offer tons
of products
ranging from managed databases
to content delivery networks
to satellite ground station control
({{< extlink "https://aws.amazon.com/ground-station/" "I'm not kidding about that last one!" >}}).
The trade-off is having all these products is dealing
with lots of configuration options.

Other hosting services offer Virtual Private Servers (VPS)
with a smaller number
of extra services.
The services tend to have simpler offerings
aimed at smaller businesses.
Some popular players in this space are
{{< extlink "https://www.digitalocean.com/" "DigitalOcean (DO)" >}}
or
{{< extlink "https://www.linode.com/" "Linode" >}}.

After you select a hosting service
and have a machine to use
on their cloud,
there is a lot to configure.
This configuration is done
with software known as provisioning tools.
{{< extlink "https://www.ansible.com/" "Ansible" >}}
and
{{< extlink "https://www.saltstack.com/" "SaltStack" >}}
are commonly used in the Python space.

Provisioning tools can do virtually anything
on a server.
You can use them to:

* Install packages
    from the operating system's package manager.
* Run processes
    like load balancers
    and monitoring software.
* Add cron jobs
    to execute tasks on a schedule.
* Configure Python applications.

When we talk about doing a *deployment*,
we're generally referring
to running a provisioning tool
to make changes to your server infrastructure.

The challenge with these tools
is that they execute directly
on the environment
by default.
This means that if the provisioning tool fails and halts,
you can leave your server
in a weird, intermediate state.

The best strategy to increase reliability
of your provisioning tools
(and, thus, your deployment)
is to **do less**.

### How much is in your Python app?

For a Python application,
your server needs:

* The app code.
* The app's dependencies.
* A web server to run the app.

Seems simple, right? Hold on a second.

I'll outline one way to do that and you can see all that's involved.

* To get the app code,
    clone your git repository
    onto the server.
* To clone the repository,
    add an ssh deployment key
    to get access to the repo.
* To add an ssh deployment key,
    control it in an encrypted location
    that your provisioning tool can access.
* To add app dependencies,
    create a {{< extlink "https://docs.python.org/3/library/venv.html" "virtual environment" >}}.
* Use pip to install dependencies
    into the virtual environment.
* If any packages require C extensions
    (like lxml or PIL),
    use your package manager
    to install C development headers
    and libraries like libjpeg.
* Make sure a compiler is installed
    so it can compile the extensions.
* Install a web server.
* Configure the web server to use the app code.
* If you have static assets
    like CSS and JavaScript,
    install all the pre-processors
    and toolchains
    required to build and minify
    these static assets
    (this can be a HUGE task!).

Within that set of actions are many points
that can fail.
Can we get those steps out of the deployment process?

## Option A: Docker container

{{< extlink "https://www.docker.com/" "Docker" >}} is designed
to help with this problem.
The core idea with Docker
is that the steps outlined above
are done separately from the production server
and put inside of a *container*.

Using a special building process,
Docker will put all the output
like Python code,
dependencies,
compiled extensions,
and static assets
into the container.

The container is the interesting piece
in this equation.
**What is it?**

A container is single file called an image
that uses special filesystem structure
to store all of your app.
It's *not* a full operating system
like a virtual machine.
Instead,
a Docker daemon
(which is a background program)
interacts with the kernel
of the server's operating system
to run the image.

The image itself doesn't run.
It acts as a cookie cutter template.
The Docker daemon uses this template
to start a container *instance*.
The instance is the actual running process
that will execute your application's code.

**If this is starting to feel complicated,
then your software developer spidey sense is tingling correctly.**
Containers are a powerful technology
and used by large business enterprises
who need to scale to large amounts
of user load.

The benefit of a container
is that it is an interchangeable part
with a clear interface
that can be moved around easily.
In fact,
"container" is meant
to conjure the image
of a shipping container
which has similar properties.

The downside of containers
is that they introduce a lot
of additional overhead
to your system.
If you're running your own infrastructure
on a VPS,
then you must bear the burden
of managing the Docker daemon
and other pieces related to containers.

{{< figure src="/img/2019/container-boat.jpg" caption="Containers aren't always the best fit." >}}

Containers also bring overhead
to your software development process.
The developer tooling is getting better
like Microsoft's recent announcement of
{{< extlink "https://code.visualstudio.com/docs/remote/containers" "VS Code Container support" >}},
but not all editors support this kind
of interface.
That means that editing and debugging
in a container may be harder
than a flow on your local OS.

## Option B: Shiv, a bundled Python app

Instead of putting large chunks of an operating system
into a container,
what if you could bundle your Python app
into a single executable file?
That's exactly what {{< extlink "https://shiv.readthedocs.io/en/latest/" "Shiv" >}} does.
Shiv is a project from {{< extlink "https://www.linkedin.com/" "LinkedIn" >}}.

Shiv uses one of the more unknown corners
of the Python language, Python Zip Applications.
Zipapps are not a new feature in Python.
The zipapp PEP, {{< extlink "https://www.python.org/dev/peps/pep-0441/" "PEP 441" >}},
gained approval in 2015.
But *what is a zipapp*?

Zipapps are a way to execute Python code directly
from a Zip-formatted archive file.
Python will execute this file
by adding any packages within it
to the Python path,
and then running a `__main__.py` file
that is at the root
of the archive.
The benefit of this scheme is
that it is **ONE** executable file.
Being a single file makes it trivial
to track as a versioned "build artifact."

A build artifact refers to an output
from some build process.
Artifacts are often what deployments will install
on a server.
In a normal Python application,
you might consider your app code as a build artifact,
and each dependency as its own build artifact.
The more artifacts that a system has,
the higher the odds of failure
and more opportunity to have mismatches
between artifacts.

With a Shiv app,
all of your app code and dependencies are bundled together.
This produces a single unit that will either work
or fail.
If it fails,
**don't ship it!**
Having one artifact eliminates the possibility
of a bad interaction getting to your production system.

For instance,
let's consider a more traditional Python app.
Suppose that your app is tested in Continuous Integration (CI)
with package A at version 2.
If that app code is deployed to a server,
it's possible that package A is not updated
and the server has version 1.
Your application may begin to fail
because the two different pieces weren't tested together.

Now consider the Shiv app version
of this scenario.
A Shiv app is constructed in CI
and bundles your app code *with* package A at version 2.
When the tests pass,
that entire unit is deployed
and should work
because there is no opportunity
for you app code to interact
with package A at version 1.

I think this is a big win!

> By using a single build artifact,
we are removing the risk
of deploying broken code.
The risk moves
from the production system
that can affect customers
to the CI system
that cannot affect customers.

Let's look at how to get started
with Shiv
so you can get these benefits.

## Shiv in practice

The first step is to install Shiv.

```bash
$ pip install shiv
```

I like to keep all of my development toolchain tools
like Shiv
in a `requirements-dev.txt` file,
but do what works for you
whether that means using Pipenv
or some kind of requirements file.

Once you've install Shiv,
you'll have access to a `shiv` command line tool.

Before we can use Shiv,
we have to do some preparatory work
to our app.
Shiv wants to work with Python packages
so we need to package our app.

### Whirlwind packaging tutorial

Packaging is a large topic,
but I'll try to provide a reasonable example.
If you want to deep dive into packaging,
check out the {{< extlink "https://packaging.python.org/" "Python Packaging User Guide" >}}.

To make a package
for a standard Django app,
we minimally need:

1. A `setup.py` file to tell Python core metadata
    and where the code is.
2. A `MANIFEST.in` to tell Python
    where your data files (like templates) are.

Disclaimer:
There are loads of methods
for dealing with packaging.
If you're a packaging expert
and don't like the method I listed, sorry.

The `setup.py` file looks like:

```python
from setuptools import find_packages, setup

setup(
    name="myapp",
    version="1.0.0"
    packages=find_packages(),
    include_package_data=True,
)
```

The two things worth calling out are:

1. `find_packages` does all the heavy lifting
    of finding your Python code
    for your app.
2. `include_package_data=True` tells `setuptools`
    to use the `MANIFEST.in` file to get package data.

The `MANIFEST.in` file would look something like:

```txt
recursive-include myapp/templates *
```

This assumes that you have a Python package called `myapp`
that contains a `templates` directory
that has template files in it.
Because it uses `recursive-include`,
the packaging system will include *all* files
in the templates directory
even if they are nested within other directories.

That's enough to make a package
by running `python setup.py sdist`!

### Using `shiv` and your shiny new package

We want to put all of the packaged code
for the app and dependencies
into a single place.
This will give Shiv a clear spot
to bundle all the code together.
Now that you've got a package,
this process is done in a single command.

If you have all your dependencies
in a `requirements.txt` file,
you can run:

```bash
$ pip install . -r requirements.txt --target dist/
```

The dot (`.`) in the command instructs pip
to use install what it can find locally.
That means it will find your `setup.py` file
and install your app.

The `-r requirements.txt` is pip's method
for installing a list of packages
in a single swoop.
This is how all your dependencies are installed.

But where are we installing to?
That's what the `--target` flag does.
The target flag makes pip put all the code
into a location of your choosing
instead of the standard `site-packages` directory
where installed packages would normally go.

Once all the code is in the `dist` directory,
we're ready to build the Shiv app.
Let's look at the command to do that.

```bash
shiv --site-packages dist --compressed \
    -p '/usr/bin/env python3' \
    -o myapp.pyz \
    -e myapp.main:main
```

The `--site-packages` flag tells Shiv the location of the code.
`--compressed` instructs Shiv to use a compressed format
when building the zip archive.

The `-p` flag describes where Shiv should look
for Python
when it runs.
By using `/usr/bin/env`,
we can tell Shiv to look for whatever version
of Python
it can find on the path.
This is a useful trick because it could resolve to
different paths like `/usr/bin/python3`
or `/usr/local/bin/python3`
depending on how your OS installs Python.
This technique can avoid subtle breakage that would occur
if you specify a path to Python
that doesn't exist in a target environment.

The `-o` flag is the output file name.
When I use this in Continuous Integration,
I provide a name like `myapp-${CIRCLECI_SHA1}.pyz`
so I can uniquely identify the version
that CI generates.

Finally, the `-e` flag guides Shiv where to find the entry point
of your application.
In the example,
the portion before the colon is a module path
and the part after the colon is a function name.
That means that Shiv would try to execute a `main` function
that is located in a `myapp/main.py` file
in the project.

**Update:**
{{< extlink "https://twitter.com/LorenCarvalho" "@LorenCarvalho" >}},
author of Shiv,
messaged me
to say
that Shiv can pass its extra options to `pip`.
That means you can skip the `pip` command above
and replace the `pip` and `shiv` commands
with this single Shiv command:

```bash
shiv --compressed \
    -p '/usr/bin/env python3' \
    -o myapp.pyz \
    -e myapp.main:main \
    . -r requirements.txt
```

Thanks, Loren!

### What's in `main`?

To this point,
I've excluded what you put in your `main` function?
If you're running a webapp,
`main` should run the web server.

For my side project built on Django,
the `main` function looks a bit like:

```python
import sys
from gunicorn.app import wsgiapp

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")
    django.setup()

    sys.argv.append("conductor.wsgi:application")
    wsgiapp.run()
```

My project uses the popular
{{< extlink "https://gunicorn.org/" "Gunicorn" >}} web server.
The function includes enough information
that the app can load the WSGI entry point
without additional instruction.
The result is that I can start the application
without any additional flags.

```bash
$ ./conductor.pyz
[2019-09-17 02:50:06 +0000] [INFO] Starting gunicorn 19.9.0
[2019-09-17 02:50:06 +0000] [INFO] Listening at: http://127.0.0.1:8000 (85833)
[2019-09-17 02:50:06 +0000] [INFO] Using worker: sync
[2019-09-17 02:50:06 +0000] [INFO] Booting worker with pid: 85844
```

There are some really nice properties
of this approach
that I hope you noticed:

1. The code doesn't have to run in a virtual environment.
2. No external tool (namely, a web server) must be called.

### Hooking into deployment

With a functioning Shiv app in hand,
you can hook the app
into deployment.
Note that this doesn't mean eliminating your deployment tool.
If you're configuring your own environment
on a VPS,
then there are plenty of parts
in a fully functioning system.
A Shiv app doesn't eliminate those parts,
but it reduces the number of tasks related
to the Python app code.

To get an app into deployment,
you'll probably need a few pieces.

* A place to generate your latest Shiv app.
    Continuous Integration is your best bet here.
* Storage for the generated pyz app files.
    I've used AWS S3 for this.
    The possible number of alternatives is nearly endless
    so pick what you're comfortable with.
* Deployment tasks to pull the latest Shiv app
    from your storage location.
* Configuration to run the Shiv app
    from your service's process manager
    (e.g., Systemd or Supervisord).

That's Shiv app deployment
in a nutshell.
I haven't painted the complete picture,
but I hope you have enough
of an idea of how to run a single file Shiv app
as an alternative to a more traditional Python app deployment.

Next, let's compare Docker and Shiv.

## Docker vs Shiv

{{< figure src="/img/2019/fight.jpg" caption="Yeah, I know this is what you really came here to see." >}}

Let's be clear from the start:
*Docker and Shiv are both solid tools
that can work
for your project.*
As we compare these,
I'm not aiming to trash one
or the other.
If you can see the similarities
and differences,
you can judge
which would be a better fit
for your project.

First, Docker:

* Docker has a huge ecosystem.
    The tool is not language specific
    so a lot of energy is invested into it
    by a broad community.
* Docker wraps up many OS features and tools.
    If you pick a big enough container,
    you can run other commands beyond your web server.
* If your project isn't for Python,
    then Docker will be a much better fit
    than Shiv.
    Shiv is very narrowly focused
    on serving Python applications.
* Unless you're extremely careful,
    Docker images can get huge
    (it's not hard to have an image that reaches 2GB).
    The size becomes burdensome,
    especially if you don't have a great internet connection.
* Docker containers plug
    into big orchestration systems
    like Kubernetes.
    If your organization needs
    that level of coordination,
    you'll know.

What about Shiv?

* Shiv is tailor-made
    for Python.
    That narrow focus means you'll get a tool
    devoted to Python-specific needs
    like bundling your packages together.
* Shiv apps are simple to keep small.
    Because the app is the bundled Python code
    with an entry point,
    it's not pulling in extra stuff
    like compilers or development headers.
    For instance,
    my side project is only 23MB.
* Shiv behaves exactly like an executable.
    There's no extra daemon process
    that is needed to manage the execution
    (unlike the Docker image and container relationship).
* In a sense,
    Shiv is a much smaller ecosystem
    than the Docker ecosystem.
    There are not tools
    that exclusively focus
    on Shiv apps.
    On the bright side,
    Shiv apps are Python zipapps
    so the Shiv ecosystem ***is*** the Python ecosystem.

### When to reach for Docker

I would reach
for Docker
when I'm in a large organization
with tons of moving parts.
These organizations have scalability requirements
and ever evolving architectures
like a microservice model
that make containers appealing
due to container interchangeability.

For instance,
Docker is an extremely common choice
when working in a Kubernetes environment.
The container interface is well established.
This common interface means
that the management processes
within Kubernetes
can dynamically scale
and start new container instances
to react to increases and decreases
in web traffic.

*Importantly*,
Docker works well
when there is either:

* A dedicated DevOps/SRE team to support the infrastructure *OR*
* A managed service that works with containers
    like AWS Fargate or using Docker on Heroku.

Smaller organizations who do not have the resources
to support container infrastructure
may want to seek alternative architectures.

### When to reach for Shiv

I would reach
for Shiv
when I'm managing a more constrained infrastructure
and deploying a Python application.
Shiv avoids the overhead of container infrastructure
at the cost of flexibility.

Shiv works well when:

* A team has a Python application performing a specific task
    like a Django application running
    on Gunicorn.
* A team wants to deploy
    to virtual machines
    and wants to update those machines in-place
    as little as possible
    (i.e., non-destructive deploys).

To be clear,
I'm sure Shiv can work
in large organizations.
Remember: Shiv comes from LinkedIn
and LinkedIn is not a small organization.
My main point is that Shiv is an *excellent* fit
for smaller organizations
that are trying to operate
with minimal overhead.

## What fits for you?

For me,
as someone with a side project
and the experience
to run my own infrastructure,
Shiv is great.
The tool has helped me clean up deployments
so that they are quick and painless.

For you,
maybe Docker is still the best fit.
Or, perhaps,
the simplicity of Shiv piqued your interest
and you're ready to give it a try.

I hope that this article outlined enough
for you
so that you can make that call
and try creating your own Python executable app
if you want to.

If you have questions
or enjoyed this article,
please feel free to message me on Twitter
at {{< extlink "https://twitter.com/mblayman" "@mblayman" >}}
or share if others might be interested too.
