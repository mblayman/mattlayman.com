---
title: "From Concept To Live In Two Weeks With Django"
description: >-
    How can you build a fully functional web application
    for a customer
    in a short period of time?
    I share my experience building such a web app
    for a nonprofit organization
    while participating
    in a local virtual hackathon
    in Frederick, MD.
image: img/2020/growing.jpg
type: post
categories:
 - Python
 - Django
tags:
 - Python
 - Django
 - hackathon

---

My team had two weeks
to make a viable product.
We were a random group
of people
pulled together
with a desire
to help our local community
in Frederick, Maryland.
We were a student,
a web designer,
a former realtor turned IT support person,
and a software developer.

Our mission,
which was put forth
by the virtual hackathon
that brought us together,
was to try to make a tool
to help the local homeless.

We were assigned to a sponsor,
the director of the
{{< extlink "https://shipfrederick.com/" "Student Homelessness Initiative Partnership (SHIP)" >}}.
The goal of SHIP is a noble one.
The partnership seeks to help the homeless
in our county
that are young.
These homeless youth face many challenges related
to their health,
education,
and basic needs
like food and shelter.

The director outlined his plan
for helping some of these youth.
Knowing that many are equipped with mobile phone
in our modern world,
he wanted to create an app
that gives these youth all the information they need
to find support services.
My team's job was to build that app.

## Our Plan

The virtual hackathon was a two week event
where teams worked on nights and weekends
to build a project.
Since we only had two weeks
to pull something together,
we had to make decisions about what was possible.

Our sponsor provided the goal posts
and specified what he wanted
in the final project.
We needed:

* The ability to display a local service
    (like a food pantry)
    and show the address to get directions
    or a phone number to make a call
    or a variety of other useful facts
    about the service.
* A way to categorize the different kinds
    of services
    into some logical groups
    for easier navigation.
* A method to get immediate assistance
    to a person
    with a pressing need.
* A way to let local people stay connected
    with announcements.

Given our team composition
(i.e., we weren't all grizzled software developers)
and the time constraints,
we ruled out making native mobile applications.
We didn't have the experience to build native apps
in Android and iOS,
nor did we have the time
to get through app store review and approval processes.

Because of our constraints,
we decided to make a mobile web app.
As the software developer
on the team,
we relied on my past experience
to pick the right technology.
I'm a big proponent
of reaching for pre-built tools
if possible.
We considered if we could build the site
with something like Squarespace or Wix.
We also considered the 900 lb gorilla
of WordPress.
After thinking through the options,
the team ultimately decided
that those tools weren't going to have the flexibility
that we needed
from someone else's pre-built layouts and templates.

Knowing that we wanted something custom
and knowing that I was the guy
who needed to write the bulk
of the code,
we picked Django,
my old friend.

## Bringing The App To Life

Having a realtor
on your team
is great
for working well
with a customer.
My teammate was able
to work very closely
with our sponsor
to figure out what was really desired.
We initially received a brief
from the hackathon organizers
of what we were expected to build.
After some chats
with the sponsor,
what we found is that
he was really looking for something like
the {{< extlink "https://www.ourchildrenla.org/win-app-web/" "What I Need (WIN)" >}}
app built by a group
in Los Angeles, CA.

With his affinity for making social connections,
my teammate hustled
to do interviews
with the people behind the WIN app
and another group
in New Jersey
that the also deployed the app.
From that research,
we were in a fantastic position
to build what the sponsor wanted.

One of my personal observations
from this experience
is that a very diverse team
with wildly different skills
can produce great results.
Had the team been composed
of people with no interest
in making these connections
and doing proper customer research,
I think we would have delivered something far inferior.

We knew that our sponsor essentially wanted a clone
of the WIN app.
With that in mind,
that's exactly what I built
for version 1
of the application.

## Building The App

I made a few technical choices
that I think permitted the team
to make rapid progress
building the application.
We picked the following technology:

* {{< extlink "https://www.djangoproject.com/" "Django" >}} -
    The web framework provided all the tools that were required
    to build a database-backed web app
    that could display the information we needed.
* {{< extlink "https://tailwindcss.com/" "Tailwind CSS" >}} -
    This CSS framework is an extremely flexible toolbox
    that gave us the ability to iterate
    on the look of the application very quickly.
* {{< extlink "https://www.heroku.com/" "Heroku" >}} -
    Using Heroku as the hosting platform dramatically simplified deployment
    of the app down to a single command:
    `git push heroku master`

Since we already devoted multiple days
to customer research
and product investigation,
I only had a couple
of days
to build an application
if we wanted
to demonstrate the app
to the sponsor
at the end
of the first week.

Thankfully,
Django does most
of the heavy lifting
for starting a new project.
Coupled with my past knowledge
of the framework
and the tools in the ecosystem,
I developed a WIN clone.
The Django models for the application were a bit rushed,
but I assembled enough pieces
to be able to display categories and services
that a user would need to see.

I didn't know what data our sponsor wanted
for Frederick
so I copied the categories
that I saw from the WIN app
and used Tailwind to mock up a similar UI.
(Pro tip: I needed each
of the categories
to show as a different color,
but I didn't build that
into the initial model.
By using the `cycle` template tag,
I was able to show a unique color
for every category.
It was a good hack
for achieving visual interest
without complicating the data model initially.)

At the end of the week,
we did a demonstration
to the sponsor.
For the demo,
I ran the application locally
on my computer
with `./manage.py runserver`.
Then I connected
to {{< extlink "https://ngrok.com/" "ngrok" >}}
and shared the URL
via email
so that each of us could view the site
on our own mobile devices.
ngrok is a great tool
to share your localhost quickly
with other people.

Our sponsor was really pleased
with our progress.
More importantly than the pat
on the back,
he added hugely valuable feedback
about features that we missed
that we still needed to build.
He observed data that the app missed
and the lack
of a notification feature
for users.

With one week to go,
we needed to:

* Get the site up on Heroku
* Evolve the cloned UI from the WIN app into something better
    for our own application
* Add the features requested by the sponsor

My first priority was Heroku.
I didn't want the application
to be something that could only run
on a local development web server.
Even though Heroku is great
and Django works well on it,
there is some setup work to do.
I needed to update various configuration
for static files
and reading settings
from environment variables
before the app was ready to go.
{{< extlink "http://whitenoise.evans.io/en/stable/" "WhiteNoise" >}}
and {{< extlink "https://django-environ.readthedocs.io/en/latest/" "django-environ" >}}
are two tools
that make getting Django apps
onto Heroku much easier.

Once the Heroku setup was finished,
I added a bunch of great user interface work done
by the web designer
on our team.
Tailwind made this process much easier
than might otherwise be possible.
The new design really refined the UI
and add the level of polish
that my initial mockup lacked.

Since we used Tailwind,
integrating the design mostly involved
updating some Django templates
and little else.
Because Tailwind is so focused on HTML,
I didn't have to line up HTML
to a certain structure
that matched class or id ordering
in a CSS file.

Our final feature
to add
was a user notification feature.
For this resource app,
we didn't want users
to have a login
with a username and password.
Dealing with user management
for a community
of homeless youth
would be a large maintenance burden
for the nonprofit organization.
Instead,
we opted to use a mailing list.

The simplest solution we would devise
for building a notification system
was to use someone else's system.
A mailing list is a well known channel
for communicating
and most people
on the internet
get an email address
at some point.
By using a mailing list,
we were able to skip
handling of user accounts
and scheduling background jobs
that run outside of the normal web browsing experience.

To make the mailing list convenient
for our sponsor,
I used Django's
{{< extlink "https://docs.djangoproject.com/en/3.1/ref/contrib/syndication/" "syndication feed framework" >}}
to create an RSS feed
for the announcement model
that we built into the app.
Since we had an RSS feed,
we could connect that
to a {{< extlink "https://mailchimp.com/" "Mailchimp" >}} automation.
Mailchimp will manage the user list
and automatically send out emails
whenever the announcements RSS feed is updated.
From our sponsor's point of view,
all he needs to do is create an announcement
within the Django admin site.

That brings us to the end of the hackathon.
At the end of the second week,
we did a final presentation
where the sponsors
and hackathon judges could assess the final product.

*We won!*
I got a nice t-shirt
and my name in the {{< extlink "https://techfrederick.org/techfrederick-hackathon-teams-create-software-solutions-for-local-non-profits/" "local tech news" >}}.

## Post Hackathon Activity

After the hackathon was over,
we needed to do some final work
to make the site real
for the nonprofit organization.

Our final demo happened
on an auto-generated domain name
on Heroku.
I worked with the sponsor
and did some DNS configuration
to get the new tool
at a proper subdomain.
We also needed to make the app available all the time
and get it off of the Heroku free tier
which will cause the app to "sleep"
when not in use.
A sleeping app has a poor user experience
since it takes quite a bit of time
to start up again
when someone visits the site.
Thankfully,
the app is so small
and has so little data,
that the nonprofit can use the Hobby tier
for a tiny bill of $7/month.

The site is live today
and you can check it out.
Remember,
it's optimized
for mobile devices,
but it looks decent
in a full browser too
(thanks to the design work
and Tailwind).
We named the app "SHIP Haven"
and it's viewable at
{{< extlink "https://haven.shipfrederick.com/" "https://haven.shipfrederick.com/" >}}.

Additionally,
you can view the code!
We did all the work
in the {{< extlink "https://github.com/TechFrederick" "TechFrederick GitHub organization" >}}
in the {{< extlink "https://github.com/TechFrederick/ship" "ship repository" >}}.

I had a really good time putting this project together.
The time pressure and working with a team of people
that I didn't know
was a fun experience,
and I'm very pleased
that we were able to produce something
that our community can use.
If you have the opportunity
to participate
in a local hackathon
in your community,
I highly recommend it!
I hope you learned a bit from our experience.

If you have questions
or enjoyed this article,
please feel free to message me on X
at {{< extlink "https://x.com/mblayman" "@mblayman" >}}
or share if you think others might be interested too.
