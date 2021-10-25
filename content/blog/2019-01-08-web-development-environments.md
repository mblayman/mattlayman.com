---
title: "Local web development vs Vagrant vs Docker: What’s right for you?"
description: >-
  Web development is full of tools
  that claim to help you develop
  your perfect application.
  What's the right tool?
  Let's explore options
  like Docker,
  Vagrant,
  and honcho
  to see which tool can work
  for you on your next (or current) web app.
image: img/2019/vagrantdocker.png
type: post
categories:
 - Python
 - opinion
tags:
 - Python
 - Django
 - honcho
 - Vagrant
 - Docker

---

What tools do you use to build your web applications?
Your choice matters a lot
because you'll spend a lot of time
working in that environment.

If you make a poor choice,
you'll be stuck
with something suboptimal
that can slow you down massively
and make your project grind to a halt.

If you make a harmonious choice,
your tool will aide you
on your development journey
and let you crank out features
to delight your customers.

This topic deserves your consideration
because time is one of our most precious resources,
and a bad tool choice will eat your time.

> Don't waste **your** time on tools that are bad fits for your project!

The best way to save your time is to know the landscape of tools.
Knowing the landscape will let you choose a tool
that will be a great fit *for you*.

**We're going to explore different modes
of doing web development
and the tools for each mode
so you can get an idea of the styles
and decide which one will fit you best.**

For my examples,
I'm going to assume that you're building a
{{< extlink "https://www.djangoproject.com/" "Django" >}}
web application.
This is a great choice,
but I certainly won't fault you
if you make other choices.
My use of Django is to illustrate patterns
that are common in many web frameworks
and simultaneously give you some real code to look at.

## Humble beginnings

You started your amazing project yesterday.
You have grand visions
of becoming The Hot New Thing&trade;.

This isn't your first rodeo with Python
so you knew to:

1. Start with a virtual environment.

    ```bash
    $ python3 -m venv venv && source venv/bin/activate
    ```

2. Install the web framework.

    ```bash
    (venv)$ pip install Django
    ```

3. Generate boilerplate to get started.

    ```bash
    (venv)$ django-admin startproject new_hot_thing && cd new_hot_thing
    (venv)$ ./manage.py startapp awesome
    # Run more Django stuff
    ```

4. Run the development server.

    ```bash
    (venv)$ ./manage.py runserver
    ```

This is a pattern that you'll find
in many of the Python web frameworks.
Once you make a place for code to live,
generate some code
from starter templates,
and run the code with a local web server,
you can make serious headway!

### The Good

What can we say is *good* about this setup?

1. This is about as minimal as you can get.
   The low barrier to entry means
   that web development can be accessible to many people.
2. Every web framework worth its salt will explain how to do this.
   The tutorials want to get developers to success
   to hook them into joining that ecosystem.
   This means that you'll find lots of support
   when getting this far.
3. It feels pretty amazing
   to see the success page
   from the development web server
   after five minutes worth of work
   (*Dopamiiiine!!*).
4. When you start writing tests,
   those tests should be fast
   because they will run directly
   from your local operating system.

### The Bad

What's *not* great with this setup?

1. Getting this running on another machine will become a pain.
   Since you installed Django directly
   with `pip`,
   it's a step that you'll have to remember
   when running this somewhere else.
   <br><br>
   This will be a problem when you want to go live
   and share your creation
   with the world
   because running your software
   from your laptop is not going to go well.
2. Your local operating system is not going to match
   with the operating system of your live website.
   <br><br>
   *Statistically, you run Windows.*
   Maybe you're a macOS person like me,
   but the data shows that Windows still dominates.
   Most websites run on
   {{< extlink "https://aws.amazon.com/" "AWS" >}},
   {{< extlink "https://cloud.google.com/" "GCP" >}},
   {{< extlink "https://azure.microsoft.com/en-us/" "Azure" >}},
   or on a Virtual Private Server
   like
   {{< extlink "https://www.digitalocean.com/" "Digital Ocean" >}} or
   {{< extlink "https://www.linode.com/" "Linode" >}},
   and most things running on these services are Linux.
   <br><br>
   The bad news is that the differences
   between operating systems will bite you.
   Windows and Linux are different beasts.
   <br><br>
   I am acutely aware of this fact
   from writing a cross platform Perl application
   waaaay back in the day
   (the filesystem `/` and `\` differences alone were the bane
   of my existence).
3. The development web server will only take you so far.
   Those tools are designed
   for local development
   and can be light on features.
   Want to test out HTTPS support
   with the dev server?
   **Tough luck.**

## Emerging from primordial web app goo

Weeks or months have ticked by.
Version 1.0 of The Hot New Thing is nearly ready,
and your site is growing.

By this point,
your workflow is getting out of control.
You're still running the development web server,
but you also started to run Celery
for handling background tasks.
You found a use for caching
so Redis is in the mix too.
On top of all that,
The Hot New Thing needs some JavaScript
to power its slick UI
which means that you're pulling along webpack
for the ride.

Management of this system is nutty
because you have four different terminals open
to start all the different processes
to check your site.

This level of pain is a common step
on the path to growing.
Now is a good time to introduce `Procfile`
and process management tools.

{{< extlink "http://blog.daviddollar.org/2011/05/06/introducing-foreman.html" "Years ago" >}},
the Ruby community created a tool called
{{< extlink "http://ddollar.github.io/foreman/" "foreman" >}}.
foreman manages running multiple processes in a single command.
Each process is given a label (like `web`)
and all logging is funneled
to a single terminal window.

You define the processes to run in a `Procfile`
with something that could look like:

```text
web: ./manage.py runserver
worker: celery worker --app new_hot_thing:celeryapp --loglevel info
frontend: webpack --watch
```

This model of working makes it very quick
to start (and stop!) your development system.
The `Procfile` model is also used
by {{< extlink "https://www.heroku.com/" "Heroku" >}}
as the way to specify your system
for their Platform as a Service.
That's *very* convenient if you want to go live quickly
without the hassle of managing cloud infrastructure.

foreman is a great tool
if you're running a Ruby on Rails or Sinatra app
because the tool is based on Ruby
and you already have a Ruby runtime available.

**But we're working on a Django app!**

Thankfully,
there is a Python clone
of foreman
called {{< extlink "https://honcho.readthedocs.io/en/latest/" "honcho" >}}.
honcho gives you the same benefits
without needing Ruby.

Now you can start up like this:

```bash
(venv)$ honcho start
23:02:53 system     | web.1 started (pid=25464)
23:02:53 system     | worker.1 started (pid=25465)
23:02:53 system     | frontend.1 started (pid=25466)
23:02:53 frontend.1 | some logging
23:02:53 web.1      | some more logging
23:02:54 worker.1   | even more logging
```

### The Good

Okay, what's good in this model?

1. You can wrangle complexity into a single tool.
   If you're working with a small team
   with different expertise
   (like backend Python developers
   and frontend JavaScript developers),
   everyone can start the system
   by interfacing with `honcho`.
   <br><br>
   Frontend devs can hone their magical `webpack` incantations,
   and backend folk can swap `runserver`
   with a more featureful server like `gunicorn` or `uwsgi`.
2. This system can still run as fast as your operating system will permit.
   There are no extra layers since honcho will start native OS processes.
3. All your logging in a single place on the terminal is excellent.
   You don't have to jump between terminal tabs
   or `tail` multiple log files.

### The Bad

And the bad aspects?

1. This complexity comes at the cost of setup.
   For instance, if you're running Celery locally,
   then maybe that means you need RabbitMQ running.
   You have to install all the extra tools
   that your system will need
   onto your laptop.
   That can get hairy.
2. If you've developed automation tools
   to deploy to your live site,
   you easily create a rift
   between what you need
   for your local setup
   versus what the cloud servers need.

## Inception level 2

If The New Hot Thing gets too big
with too many moving parts
(or you're a consultant supporting multiple clients
which would cause conflicting machine configurations),
running on your local operating system loses its appeal.

You may also be bothered
that you're running a different operating system
than what your live site runs.

> Now we get virtual.

The only way to stay directly
on your local laptop
*and* use the same operating system
as your live site would be
to switch the operating system
that your laptop runs.
This isn't practical
for most developers.

Instead,
you can run your code in a virtual machine (VM).
A virtual machine is a fully functioning operating system
that lives *within* your local OS.
The local operating system is called the "host" OS.

To run a virtual machine,
you'll use a **hypervisor**
(e.g., {{< extlink "https://www.virtualbox.org/" "VirtualBox" >}}).
The hypervisor's job is to pretend
to be a physical machine.
By acting as a physical machine
to the virtual machine,
the virtual machine runs
as if it was installed directly
on the hardware.

The most popular tool
for running a development environment
within a VM is with
{{< extlink "https://www.vagrantup.com/" "Vagrant" >}}.
Vagrant is designed
to make it seamless
when interacting with a hypervisor.

To run your virtual machine, run:

```bash
$ vagrant up
```

Vagrant will download the operating system
if it doesn't have it yet.
Then it will start it up
and configure it with a user account.
This makes it very quick to get into your VM.
To run commands on the VM,
you connect to it
as if it were a remote machine.
Vagrant installs some development security certificates
which means you can ssh
into the VM with:

```bash
$ vagrant ssh
```

Once you're connected to the VM,
it will behave like any other operating system
that you've worked with before.

While the foreman/honcho setup depended
on the `Procfile`,
Vagrant depends on the `Vagrantfile`.
This configuration file provides the specifics
for your virtual machine. The file can:

1. Instruct Vagrant which operating system image
   it should base the virtual machine on.
2. Configure a mapping
   from a host directory
   to a directory on the VM.
   This is useful to access your project code quickly
   inside the VM.
3. Run "provisioning" scripts
   to set up the virtual machine
   to run your web server, background task worker,
   or anything else that your site must run with.

### The Good

This version of development adds a very large layer
into your process
so why would you want to include it?

1. Your development environment will run the same operating system
    as your live site.
    Any problems you catch and fix
    on the development site
    will be problems that you solved
    for your live site.
2. You won't litter your host operating system
    with development software
    that you may not want regularly.
    This means it will be safer and easier
    to run multiple projects
    on your machine
    without worrying about conflict.
3. Fewer differences
    in the operating system
    means that your development configuration
    can be closer to your live site
    and should be less to maintain.
4. Easier to share with a team.
    Since you have to use automated scripts
    to get your VM going
    with all the right dependencies,
    it is easier to get teammates
    in a similar configuration.

### The Bad

It isn't all sunshine and roses.

1. This mode is slower.
    Running a virtual machine requires running
    through the virtual OS *and* the host OS.
    You can expect a 10-20% performance overhead
    for running this way.
2. *Mo' layers, mo' problems*.
    Adding complexity at any point
    in your stack
    increases the odds
    of new problems.

    For instance,
    I've found myself fighting
    with hypervisor drivers
    when my VM and host OS wouldn't play nicely together.
    This is a problem that couldn't exist
    with local development
    because local development doesn't even *use* a hypervisor!
3. Dependent on provisioning tools.
    I've run up against scenarios
    where the automated scripts
    for the VM
    get so complicated
    that no one wants to touch it anymore.
    That's not a good place to be.

You can get **extremely** far
with a virtual machine-centric development mode.
I've been at businesses
with millions of users
that exclusively use virtual machines
for development.
It's a solid choice for teams
for a long time.

What can you do when things start getting big?
Like, *really* big?

## It's over 9000!![^1]

[^1]: {{< extlink "https://www.youtube.com/watch?v=SiMHTK15Pik" "My inner teenager wants to come out." >}}

Another popular mode of development uses a design
that bundles dependencies
and a web app
into a single unit.
This unit is a *container*.

Containers became popular a few years ago
when {{< extlink "https://www.docker.com/" "Docker" >}} solidified.
Since that time,
the software industry is abuzz
with discussion about containers.

> Why? Why would you reach for containers for your app?

When you use containers,
you're trying to address the mismatch
between development
and your live site.
The industry term
for a live website
is "production,"
so you might hear
about this problem
as the dev/prod (development/production) parity problem.

We've already encountered this problem a couple of times
in this article.
If an environment has differences
between how it was developed
and how it's used live,
problems from those differences can affect projects.

Let's think back to our local development example.
In the most primitive case,
the parts that you install to make your website run
with `runserver`
will not be the same
as your live site.
If you're in that statistical group
of Windows on the desktop
and Linux in the cloud,
you immediately have differences
at the OS
and foundational pieces
like virtual environments
(i.e., `venv` *not* VMs).

What if, for instance, The New Hot Thing is a replacement
for Instagram?
In that case,
you'll be manipulating images.
Image code libraries are tricky beasts
with lots of weird dependencies
(hi, {{< extlink "https://pillow.readthedocs.io/en/5.3.x/installation.html" "PIL" >}}!).
It's very likely that your local setup would be different
than production.

> **Ready for some bad news?**
Inter-dependency and environment problems get harder
as your site grows
and the complexity
of your software system increases.

Container technology like Docker tries to fix this problem.
And that's why mature teams
with complex systems
reach for containers.

### Obligatory shipping container analogy

The fundamental analogy that is used
for containers
is that a container is akin
to a shipping container.

A shipping container is successful for transporting goods
because it has a standard size
and interface
that make it easy to work with.
If you've seen one shipping container,
you've seen them all.

By using standards
around sizes,
the shipping industry is able
to produce tools
that can ship all sorts of goods.
A container could hold cars
or be full of stuffed teddy bears.
In either case,
the tools that move the container
from dock to ship to dock to truck
are the same.
This produces massive efficiencies
in the transport of goods
around the globe.

Docker and friends attempt to do something similar
for software.
If you can shove all your code
and dependencies
into a container
(i.e., a thing with a common interface),
then moving that thing around
from one environment to another
should be easier.

### Containers in practice

*That's the theory.*
How well do containers work in practice
and who should attempt this?

That depends on how much staff you have,
how much control you want,
and maybe even what language you're using
to build your web app.

After you're able to produce a container
(technically, a container *image*,
but let's not sweat that detail for now),
you can move that container around
and plug it into a system
that *manages* containers.

Here's where the staff size comes in.
There are services that exclusively manage containers
like {{< extlink "https://aws.amazon.com/fargate/" "AWS Fargate" >}}.
A service like Fargate trades staff time for money.
With Fargate,
Amazon will run your containers
on their infrastructure
without forcing you to manage machines.
Considering the cost
of developer time,
this could be an insanely good deal for you.
Aside from cost,
one downside of this approach is less control.

If you need more control
for your container environment,
{{< extlink "https://kubernetes.io/" "Kubernetes" >}}
is probably where you will end up.
Kubernetes (often abbreviated as k8s)
is a "container orchestration" tool.
The tool is designed to run huge distributed infrastructure.
This makes perfect sense when you learn
that Google is the original source
of the project.

When you use Kubernetes,
you have to start thinking about your container/project
as a service
that must be flexible enough to move around
to different machines
in an ever-changing infrastructure.
There is an entire world of tools
and services
that emerged to support this development model.
If that sounds terrifying
(and it's ***totally*** reasonable for that to sound terrifying),
then your project probably doesn't need to go there.

The big cloud vendors like Google offer Kubernetes
on their infrastructure.
It's extremely challenging to convert a large project to use k8s.
You can expect a DevOps team working on it full time
to take months to complete such a transformation.

### Developing with containers<br><br>

> **You know what's crazy!?
We haven't even talked about
how to develop software
in a container world!**

I think this is a common problem
for this subject
of containers.
It doesn't take much
to get sucked
into this whirlwind
of operational concerns
about managing dev/prod parity.
You can forget
that someone still has to produce a product
to make users happy.

If the dev/prod parity problem is killing your team
and you've decided to move to containers
and bear the cost of that transition,
let's look at what this will mean
for developers
on a day-to-day basis.

Step 1 of working with containers is to build a container image.
Because Docker is the most popular container technology,
we'll use that for our Django example.
To build a container,
your project will need a `Dockerfile`.

> **Sidebar**: `Procfile`. `Vagrantfile`. `Dockerfile`.
At least the industry has some kind of consistency.

A `Dockerfile` is an unusual format
that is a series of commands
which describe how to produce your project's image.

Here's a sample.
I wouldn't rely on it as best practices.
You can use it more to give you an idea
for what goes into a `Dockerfile`.

```Dockerfile
FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
    python-pip

ADD ./requirements.txt /srv/new_hot_thing/requirements.txt
RUN pip install -r /srv/new_hot_thing/requirements.txt

WORKDIR /srv/new_hot_thing
ADD . /srv/new_hot_thing

EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]
```

This file starts from a base image `ubuntu:xenial`,
installs some Python packages,
and tells Docker what command to run
to execute the container (i.e. `uwsgi`).

From the directory where your `Dockerfile` is located,
you build the image.

```bash
$ docker build -t new-hot-thing:1234 .
```

This image does nothing by itself.
It's an artifact.
You can think of it as a blueprint
for a process that could run
in the future.
When you run a container image,
it starts a container *instance*.
This is the living process that will actually execute code.
Docker has a {{< extlink "https://docs.docker.com/engine/reference/run/" "run" >}} command
to vivify an image.

```bash
$ docker run new-hot-thing:1234
```

In a container universe,
the developer lifecycle looks like:

1. Write some code.
2. Build an image.
3. Run the image as a container instance.

Running the instance may be the only way
that you can run your unit tests.
Since the container is the place where dependencies are stored,
your workflow will start to revolve around Docker.
This could mean wrapper scripts to interact
with the code.
For instance, PyPI is built with {{< extlink "https://github.com/pypa/warehouse" "Warehouse" >}}.
The project uses a {{< extlink "https://github.com/pypa/warehouse/blob/1fbb4ac752e68b5840b9e09b68e44a165569bfa6/Makefile" "Makefile" >}}
to run common Docker operations
like `make tests`.

### Developing with multiple containers (without k8s)

Observant readers might have noticed
that this container only runs the web server.
What happened to Celery, Redis, and webpack?
If you guessed "make more container images,"
then you get a prize!
Here's an internet high five! 🎉✋🎉

To get back to the same level of productivity as honcho
for local development,
you need to run multiple containers
in tandem.
For those starting out with Docker,
{{< extlink "https://docs.docker.com/compose/overview/" "Docker Compose" >}} is your tool.
Docker Compose gives you a tool set
to link Docker images together
to produce a system
on your local host.

If you want to use Docker Compose,
you'll need another YAML file.
This one is called `docker-compose.yml`.
We can use Warehouse again
since that project has an extensive
{{< extlink "https://github.com/pypa/warehouse/blob/9cdf355be864330cce55614f5285bb96ceb89368/docker-compose.yml" "docker-compose.yml" >}} file.

The Docker Compose file breaks down the system
into "services."
These services are very similar to what we saw
in the `Procfile` format.
In fact,
Warehouse uses some of the same names
as our example like `web` and `worker`.
Through this configuration file,
we can build out all the containers we require
to run our system.

Here's a sample service (trimmed a bit for clarity):

```yaml
  worker:
    build:
      context: .
      args:
        DEVEL: "yes"
    command: hupper -m celery -A warehouse worker -B -l info
    volumes:
      - ./warehouse:/opt/warehouse/src/warehouse:z
    env_file: dev/environment
    links:
      - db
      - redis
```

To get the show going:

```bash
$ docker-compose up
```

### Developing with multiple containers (with k8s)

Nearly every DevOps person
that I speak with about Kubernetes will get almost giddy
about it.
This strange glee does not carry over
to most developers I know.
I attribute a large part of that feeling in developers
to a lack of knowledge
about how to develop well
in this world.

> We've seen the massive amount
of complexity that containers introduce.
Kubernetes layers on even more.
How does a developer survive this?

Because Kubernetes is a different kind
of animal
with its own lingo
like Pods, Namespaces, and Nodes,
running as a developer
in this world is different.

In contrast to Docker Compose,
Kubernetes has a more fluid topology
than Compose.
At the core,
containers run inside a cluster.
The cluster is a set of nodes (a.k.a. machines)
that act together
and are orchestrated
by k8s software
in a dynamically changing configuration.

We work in Kubernetes
by taking a container definition
and putting it into a {{< extlink "https://kubernetes.io/docs/concepts/workloads/pods/pod/" "Pod" >}}.
A container defines the application level needs
like language runtime and dependencies,
while a Pod defines the cluster level needs
like required memory and CPU usage.
The Pod tells Kubernetes how to allocate the application
to some amount of nodes in the cluster.

If you want to develop
in Kubernetes,
you need a cluster.
As your team gets started,
you can probably use {{< extlink "https://kubernetes.io/docs/setup/minikube/" "minikube" >}}
for each developer.
minikube is a 1 node cluster
that contains all the core k8s components
inside a single virtual machine.

> **minikube is Kubernetes-in-a-box**.

In the cluster's default state,
it won't have any of your application's services
in it.
We can deploy these services
to minikube
or any other cluster
using `kubectl`
or some other tool like {{< extlink "https://helm.sh/" "Helm" >}}.
Since we've descended down the rabbit hole
for quite a while,
let's gloss over the details
around this level of provisioning.

I want to skip the subject
of provisioning tools
because it's a huge topic
that can't fit
into this (already long) article.
In any of the development modes
that we've looked at,
provisioning tools are needed
to automate some or all portions
of deployment.
You can do local or VM development
with Ansible, Puppet, or Chef as your tool.
Or you can work with containers
and find tools like Helm.
In any modality,
you'll need tooling to help.
We can look more at provisioning tools
and their benefits
in a future article.

One of the unfortunate side effects
of working with containers
is the constant need to make container images
to run the code.
This issue is so problematic
that Microsoft and Google created tools
to work around this limitation.

Microsoft released a tool called
{{< extlink "https://draft.sh/" "Draft" >}}.
Google's tool is named
{{< extlink "https://skaffold.dev/" "Skaffold" >}}.
Both tools serve to make Kubernetes *development* easier.

Each tool takes a slightly different approach,
but I think I could sum up their primary function as:
**run a process that will watch code files for changes
and build and deploy to a Kubernetes cluster
when changes are detected**.

For Draft, the process to run is:

```bash
$ draft up
```

For Skaffold, the equivalent command is:

```bash
$ skaffold dev
```

Both tools will do roughly the same thing.

1. Watch for code changes.
2. Build a new container image.
3. Push the image to a container repository
    if you're working on a remote cluster
    (a minikube setup will skip this *slow* step).
4. Deploy the container image
    to your development cluster
    with whatever provisioning tools
    that you've configured.

Check out the features
of each tool for yourself
to decide if one is a better fit
than the other.
From my own analysis,
I think **Skaffold is a stronger offering**
because of its support for multiple provisioners
and having more flexibility around how you build your container.

That was a lot to say to cover the containers mode of development.
Now we can get an idea of the good and the bad.

### The Good

What makes containers good?

1. Containers give you confidence
    that what you make in development
    will work nearly identically
    as what you put on your live site.
2. The number of moving parts
    in an individual container is fewer
    than in a large monolithic system.
    This can make individual containers easier to reason about.
3. Containers push system design toward a service-oriented architecture.
    We might debate if this is a good architecture,
    but it does provide clear boundaries
    between different parts of the system
    which is a boon for very large teams.

### The Bad

Containers have definite downsides.

1. Using containers adds more layers
    and increases the complexity of the system a lot.
2. Building container images takes time
    and introduces some friction
    in the development flow.
3. Containers require a lot of effort
    to make a development environment.
    As the number of containers/services increases,
    the effort required also increases
    because of coordination and communication costs.

## Recap

In this article,
we've looked at three modes of development.

1. Local development -
    Starting and working with your project directly
    on your host operating system
2. Virtual machine development -
    Running your project and all its dependencies
    inside of a virtual machine (guest operating system)
    on your computer
3. Container development -
    Building container images
    that integrate
    with industrial strength
    cluster management tools
    like Kubernetes

### Bottom line pros and cons

If you're racing to the end
of this article
and are looking for the "answer,"
then I'm afraid you're out of luck.
Each mode of development is right depending
on your project or team's context.

> When should you consider a particular mode of development?

For local development,

* **Pro:**
    It's great when speed is paramount
    or if you're prototyping
    or exploring a problem space.
* **Con:**
    The differences between your development environment
    and your live site's environment may cause issues.

For virtual machine development,

* **Pro:**
    Virtual machines replicate most of the qualities
    of your live site so you'll get a lot of stability
    from using them.
* **Con:**
    Running an entire operating system
    on your computer
    is slower
    and the extra layer of operating systems
    can create trouble.

For container development,

* **Pro:**
    Containers will help large teams scale up their large systems
    using patterns established
    by the big dogs
    like Google.
* **Con:**
    The complexity of container management
    will make most developers feel like mortals
    who don't really understand how their code works
    inside the system.

## Opinionated take

Here's my unsolicited advice
for choosing a development mode:

> Stick with local development
for as long as you can tolerate its warts.

Early or small projects need to move quickly
to determine if a project is worthwhile.
If you're starting a business
or trying to prove out the viability
of an idea,
the last thing you want is all the decisions associated
with writing code
in a container-centric world.

Virtual machines will also slow you down
as you have to think
about bridging between the virtual operating system
and your actual computer.

If you really need speed,
use a Platform as a Service (PaaS)
like Heroku.
Considering the **cost of your time**
and the benefit of getting to market quickly,
this option may be far cheaper
than you think.

**Don't let complexity kill your project prematurely!**

If your project or idea has legs,
you'll know when to move up
to a more complex workflow.
Unless you're moving straight to a service-oriented architecture
(and why would you do that?),
I believe that virtual machines are a better choice
than containers.

A successful project is likely a project
that has a certain amount of complexity.
The complexity that was manageable
on a local machine setup
can start to overwhelm your team.
A virtual machine is able
to wrap up that complexity.
This will smooth out the differences
between developer environments
so you can collaborate
with other developers easier.

Finally,
if your system ever accelerates to huge growth,
you can move to containers.

> Remember: Your Hot New Thing is not Google.
You likely do not (and will not) have Google-sized problems.
The benefit is that you don't need Google-sized solutions.

I hope you found this article helpful
to understand different modes
for developing software.

If you found this useful,
please share it with others
on Twitter or whatever social media you enjoy
so they can benefit too.

I'd love to read your thoughts
or try to answer your questions.
You can follow me on Twitter
or tweet at me at
{{< extlink "https://twitter.com/mblayman" "mblayman" >}}.
