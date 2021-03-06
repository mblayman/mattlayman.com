---
title: Toying with Statsd and Graphite
description: >-
  In this post,
  I describe my experience
  with setting up Statsd and Graphite.
  Statsd and Graphite work together
  to make custom monitoring
  of your web services
  a snap to get going.
image: img/2015/graph.png
type: post
aliases:
 - /2015/statsd-graphite.html
categories:
 - Guide
tags:
 - Statsd
 - Graphite

---
The graphing bug bit me.

I am currently enjoying the backlog of the {{< extlink "http://giantrobots.fm/" "Giant Robots podcast" >}}.
One of the subjects that Giant
Robots often covers is measuring user behavior. You can only know what
your users want if you a) talk to them or b) observe them. There are
many services for observing users like {{< extlink "http://newrelic.com/" "New Relic" >}},
{{< extlink "http://www.google.com/analytics/" "Google Analytics" >}},
or {{< extlink "https://mixpanel.com/" "Mixpanel" >}} that offer a lot of value, but this post is about
going your own way with Statsd and Graphite.

When I did some hunting for how to measure behavior on your own, I ran
into {{< extlink "https://github.com/etsy/statsd/" "Statsd" >}} from Etsy. Statsd is a minimal server that listens
for data input over a UDP port. Because UDP is a connectionless protocol
(it's a fire and forget model of messaging), UDP messages are very fast
to send. Applications use a Statsd client and send messages about
various measures. For instance, an application could
increment a counter for each request received to figure out the amount
of traffic.

Statsd is good at aggregating metric data, but it is not intended to
store or display the data. Enter {{< extlink "http://graphite.readthedocs.org/en/latest/" "Graphite" >}}. Graphite is a web
application that can display time based graphs (exactly the kind of
data Statsd spits out) and store time based data in a specialized
database. Statsd and Graphite make an excellent pair.

I explored these tools by following some of the advice in a
{{< extlink "https://www.digitalocean.com/community/tutorials/an-introduction-to-tracking-statistics-with-graphite-statsd-and-collectd" "DigitalOcean tutorial" >}}.
First, I set up Vagrant to use a virtual machine for Graphite. The VM uses Ubuntu 14.04.

```console
$ vagrant init ubuntu/trusty64
```

The `Vagrantfile` only needs a couple of changes to forward
ports from the guest to the host.

```ruby
  config.vm.network "forwarded_port", guest: 2003, host: 2003
  config.vm.network "forwarded_port", guest: 8000, host: 8000
```

In the VM, I followed the tutorial directions to configure Graphite.
Since I was only testing out these tools, I did not bother to set
up Apache. Graphite's web application is a Django app so the
`graphite-manage` command line tool that comes with the Ubuntu
package is really a renamed Django `manage.py` file. It was easy
to test with the built in Django development server. Note: it
is important to use `0.0.0.0` as the address instead of `localhost`
or else the host VM will not be able to access the web app.

```console
$ sudo graphite-manage syncdb
$ sudo graphite-manage runserver 0.0.0.0:8000
```

In a browser on the host, I could visit `http://localhost:8000` to
access the web app (because of the port forwarding from the Vagrant
setup). Now the VM was listening on port 2003 for incoming data and
able to display the results in the web app. Awesome.

Next, I set up Statsd. I already had NodeJS installed on my host
machine (which also happens to be an Ubuntu 14.04 OS) so I did not
bother to configure another VM. To set up Statsd, you clone the
GitHub repository, set some configuration settings, and fire up
NodeJS.

```console
$ git clone git@github.com:etsy/statsd.git
```

Here was my configuration file.

```javascript
{
  graphitePort: 2003,
  graphiteHost: "localhost",
  port: 8125,
  backends: [ "./backends/graphite" ],
  graphite: {
    legacyNamespace: false
  }
}
```

Finally, to start Statsd:

```console
$ node stats.js exampleConfig.js
```

After all that configuration, I could execute a basic command to create
a metric in Graphite. The protocol is specific to Statsd, but there are
plenty of language specific clients that help abstract away the details.
{{< extlink "http://statsd.readthedocs.org/en/latest/" "Python statsd" >}} looks like the front runner for my language of
choice.

```console
$ echo "sample.gauge:14|g" | nc -u -w0 127.0.0.1 8125
```

That was a lot of work to see a `y = 14` graph in Graphite, but it's not
a lot of work if you consider what can be done with this pipeline on
a production website. The UDP nature of Statsd means that any layer
in a large site (e.g., application servers, caching servers) can
collect data with very minimal overhead. Graphite provides a very
powerful set of graphing tools to display and analyze that data. I
think that the tag team of Statsd and Graphite makes a great toolbox
for monitoring a web system. I bet Etsy agrees.
