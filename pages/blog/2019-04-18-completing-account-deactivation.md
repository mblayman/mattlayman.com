---
title: "Completing Account Deactivation on Building SaaS"
description: >-
   In the latest episode
   of Building SaaS with Python and Django,
   we completed the account deactivation workflow
   of the Django app.
image: img/python.png
slug: completing-account-deactivation
date: 2019-04-18
categories:
  - Python
  - Twitch
tags:
  - Python
  - Django
  - SaaS
---

In the latest episode
of Building SaaS with Python and Django,
we completed the account deactivation workflow
of the Django app.

This included:

* Canceling the subscription with Stripe.
* Marking the user as inactive.
* Sending the user to a friendly page
  to indicate that their account is deactivated.

<iframe width="560" height="315" src="https://www.youtube.com/embed/IRq_kJWEWDc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The recording is available on YouTube
and the full transcript is below.

<!--more-->

## Full Transcript

Hello. Welcome to Building SaaS with
Python and Django. I'm Matt Layman, and I'm
your streamer. I'm a software engineer
who does a lot of Python development and
we work on a Django app here.
I teach you things that I know about
building web applications.

The goal of
this is mostly about teaching so if you
have any questions shoot them over that
way in the chat. You can also follow me
on YouTube or Twitch or whatever. If you catch
this on YouTube in the future and you
want to catch me live you can follow me
on Twitch and I'll let you know when I'm
streaming up but it's typically on
Wednesday nights at 9 p.m. Eastern Time.

Tonight, we're going to be working on
an account deactivation flow for the app
that I build. We've been working on this
for a couple streams and we're getting
close to the end. There's just a few more
pieces that that are in play.

Last week's
stream we we worked on deactivating a
Stripe subscription so canceling the
subscription with the Stripe service
which is what I used to do recurring
billing. That piece is done and we're
going to be working from this GitHub
issue which I'm recording all of the
pieces that are needed to get the full
account deactivation flow. The two
remaining to do is a deactivated page
and then logging out the user when
they successfully deactivate and
handling what should happen after
they're done to make sure that they
can't get back into the service and get
it for free if if they try to attempt to
log in.

I thought today we could start
with the deactivated page just kind of
give an endpoint a finality to this and
then build out from that bastion.
We're going to jump over to our code and
I haven't committed since the last time
so there's still some from last week.
The last thing that we worked on
was the actual form saved so we have a
Django form. I guess one one call out
that I want to mention is at last week I
discussed handling internal errors so
"what happens if Stripe
errors?"

We don't want the site to blow up
in front of the user but at the same
time we want to be able to report a
problem so we did we threw a custom
exception. This conductor error that's
down here. If there's a problem with
Stripe, any problem at all, because it's
it's a problem that needs to be handled
and then we provide a message to the
user to say "Hey something went
wrong. Contact support to get it fixed."
Because you're trying to deactivate your
account, that's really that's not good
news. But the piece that was missing is I
didn't know how to still collect what
actually failed from Stripe and getting
it into my error reporting. I didn't
know the API at the time. I went up and
looked it up after the stream was
over and I'm a Rollbar user so it turns
out Rollbar makes this super easy.

If
you're in an exception block you can do
this report exec info which will
implicitly call `sys.exec_info` or
whatever the thing is to get to collect
the trace back information and that will
send it off to Rollbar so it should
transmit that information appropriately.
When you have an error though, the way
this was connected is I used Python
3's `from` exception feature.

Let's see
if I can back up to show you what I'm
talking about. Well let's go to the
actual code
so now there is in the forms
we go to our deactivate form.
No, it was in the Gateway. Alright, I'll
get there, I promise.

We have our canceled subscription and
we're catching the most generic Stripe
error that can be happening which is
this, and, in Python 3, a feature that was
added later in along and Python 3 that's
not part of light than 2. It's using the
`from` keyword here so that if you're
raising a new error from a different
error that that whole traceback is
aggregated together.

When I am
submitting information to Rollbar, it's
not terribly useful if all I did was
submit that over there was a Conductor
error. I really need the Stripe
information to tell me what was really
the problem. This `from` exception line
here or a rest of the line will be
critical to actually making the report
to prove are useful.

That's where we
ended last week and we need to get back
to the view and I've got a couple diffs
in here. The same kind of stuff that's in
GitHub but what right now we were hard
coding this to redirect to the dashboard
which is just wrong. I just needed a
place over to kind of indicate that
somewhere that would happen that's
different from the settings page on an
error state. What I really want to
have happen here is this needs to go to
a deactivated, if I spelled right, to
deactivated route and that doesn't exist
yet. But that is where we need to go so
I'm gonna leave us like that and then
we're going to go ahead and write a test
for this.

So `test_success`, we
already have that this is asserting
the location of the redirect so let's do
deactivated here. And that would be the
passing test, but right now this is gonna
fail because we don't have that view yet.
It's gonna say I looked up
`deactivated` and that URL does not exist.

You need to do something about that
so let's go to the URLs file and
except
the
activated page is going to be an
unauthenticated page because part of
this process of deactivation is logging
the user out so that they no longer have
access to their previous dashboard.
It can be a pretty dumb page in a lot
of ways.

We're gonna put it as a template
view and where should we put that so I
kind of have...
here we go... I guess I've got a
comment hint for myself here that this
is what we want marketing and not
authenticated views so these are sort of
grouped in a way that sign up these are
sort of related things that we need. And
this stops being true down around here
so I should probably do put a little
blank because these things are all
authenticated views.

The deactivate view that is the
action at the settings when we actually
click the button to deactivate that's
that's what it's calling this view and
that's not what we want. We want that
like past tense if you've already
done it.
Let's come up to the bottom here
of the non authenticated stuff and we'll
say
right here at the bottom and this is
just going to be deactivated.
I want to do a template view,
as view,
and the template name.

We could put
this in an accounts area. This is
related to accounts and that
accounts path so that seems fitting.
Where this view is coming from and we'll
call this deactivated HTML and
then I guess we need a name. The name is
"deactivated"
so I think I expect the test will still
fail.

I see. It was Black's formatting that
to this.
Here's Black will not try and
collapse us again.
We'll say authenticated views.
That's what was happening. It is still trying
to collapse it but that's fine at least
we now have a separator to know why. I
didn't actually know why those were
grouped together before, but Black is
auto-formatting that.
We have our deactivated page
that is gonna be a generic
template view that doesn't require any of the
authorization/authentication and that
should be enough.

Coming back to that
test I think this will still fail
because what's going to happen is the
template view is going to try and
instantiate and that deactivated
template doesn't exist yet. Oh No,
okay, maybe it's because it's not trying
to actually execute it. It's fine. so it's
just doing a redirect so that's
okay so maybe we need a test to prove
that you can get a 200 on that page.
Let's come back. Let's take this guy
and we're going to now do test
"deactivated" and our test is going to be
pretty dumb.
We're going to test that it's just okay
so we need a request
the requestfactory it doesn't need to be
authenticated
so a simple get request should do the
trick.

We can use the client. Do I
have a client? I don't know that I have a
client attached to this.
In that case, since we're doing we're
using the client which is a something
that Django has as a testing tool which
does kind of what it sounds like.
It's doing web requests basically and, in
fact, I need to do a get like that.
We're doing a get request and we are
going to do it on the deactivated page
like so.
It's going to give us a response and
we want to assert
that the response is a 200.
This doesn't test the content of the
deactivated page but it proves that the
page is at least wired properly.
This should fail right now because we
have not defined the template let's see
if we're right.

Yeah doesn't even get to the response
because it says the template doesn't
exist
so let's go to the templates area.
There's an accounts in here.
What I shouldn't what I want to copy it
from
don't really want to use this signup
template. I want something super basic
because the deactivated page the
message that I want to put on there is a
polite message. But essentially it's a
message telling people "sorry to see you
go. if you want to be reactivated you're
going to need to contact support to
reactivate your account" because I'm not
going to go through a flow right now of
letting people log in, access their some
version of their account, and sign
themselves back up.

I don't feel like
dealing with that at the moment because
I have low traffic so we need a pretty
simple page and trying to think of what
would be a good fit.
Let's take a look at the actual college
conductor site and see if I can find one
that I like let's look at the privacy
page.
A bit too legalesy. so I would probably
want sort of a box that says
here's what's going on.
Maybe something more like
the login page was just a box that was like this. But it
wasn't. Instead of a form, had kind of a
message that said "your account is
now deactivated."

That's probably
sufficient so let's see if we can find
that login page.
Which is a good put where did I put that.
There it is.
I'm going to yank all this information
pop yet come into accounts do
deactivated html to paste in here.
At the moment I don't care what the
content is. Run the test. It still
passes now which it wasn't doing before.
That's good news and then we're gonna
come over here and we're going to mess
around with the deactivated page.
We're happy with this
so I want to get off of
actual production site and jump over to
localhost.

This is a kind of view that we'll be
hiding in plain sight but it won't be
linked to anything so it's not like
Google is going to crawl this and find
this page so it's okay that's you know
if someone happened to come to my
deactivated page. It's not going to
bother me.
Let's go to the template
and the rest
of this is just sort of messing with the
template so we have
to change this to account
deactivated.
Refresh. That's the title of the top.
To the core of this thing
and we don't need this form error stuff
because there's not going to be a form.
We'll change the tag to say account
deactivated.

In my titling I'm trying to remember if
I do just the first word is
capitalized. I think that's the case so
maybe I should be consistent. Yes,
yeah be consistent with the styling of a
site I'm going to use a lowercase D and
we want to take out this stuff. Let's
just check it out.
so account
a little friendlier than this "account
deactivated" sounds very robotic>
We'll say "your account
is deactivated." We can use English. Why
not.
Oh maybe not not wide enough.
But
little bit wider.
Okay,
and then we want to give the prose.
I guess that tells them.

Two things that tells them, you know,
you're not going to get charged again.
Your subscription has been
canceled. Or "your subscription
to
conductor
was
cancelled
successfully."
Then
tell
that they're not gonna be charged you.
"You will not receive
any future charges."
Then we'll tell them
"if you wish to reactivate your account
please contact support."
you
and that this page down here but
we can send them that way so make it
super easy.
Although, do I care if someone
deactivated?
What is the probability that they're gonna
click a contact support page right at
that moment is like so low that I don't
think it's worth having a link? It's kind
of a saying like you're it almost feels
to me like saying you're really dumb. Why
did you do this? You need to do this
right now.
Leave it at that, and you
treat people like adults that if
they want to do it they can it's not
going to be a far fetch to see here's
context for it.
Here's contact.
I think that'll be okay.

Maybe you
will have one more thing of we are sorry
to see you go
and we'll give them a sense of time "your
account is now deactivated"
Okay, I think it's a simple enough
message. I the college connector rated
stage in in development is
a little traffic thing. It doesn't
have a lot of people trying so I think
that this is a kind of MVP approach to
account deactivation so I do want to
offer that because
there is a trial going on and I want to
give people the chance
to have something to see and not be like
offered this horrible experience so it's
kind of good enough now.

I think
with our
views file here, the way
you've got it successfully going to
deactivated
and as you could see from the way this
ran, well actually, let's confirm just for
clarity.
I'm now logged out but the deactivated
page is still available which is what we
want. Because logging out will be
part of this process so we have a
deactivated page and we're ready to move
on to these these other bits that are
along the way.

There are two other
things that needs to happen here.
We're doing this to do so that's done.
Back up to over the GitHub issue.
If you have any questions about the
deactivation workflow and the way I'm
approaching it at a meet at any time let
me know. I'm happy to go into my
thought process behind it. I wanted to
keep something fairly simple. I don't
think it's an overly complex flow but
there's still a lot of pieces in play so
it may not be super clear. We've got the
deactivated page and
we're going to log them out when it's
done.

I was looking as I'm using the
Django contrib auth system which is the
default authentication system. I knew
that this this logout option existed and
I didn't know its form. I didn't know if
I wanted to put the logout in the form
save or if I wanted to put it in the
view, but after seeing the API for this
this function takes an actual request
object. I thought it might take a user,
but it doesn't it take a request so
that tells me that rather than putting
it in the form save I really need to put
it in like guess right well right where
the to do is I need to call logout on
the request. According to my read
through the documentation, logout
doesn't throw any errors if there was a
problem so like this shouldn't be a
problem anyway because we're already
verifying that this person that's
authenticated but this should be a
pretty safe operation. I shouldn't need
to catch any real exceptions here so
trying to think
what kind of test we can do here so
going back to our file testing success
we're testing.
Mapped out Stripe
because it's going to call
form save that's fine
and in our success path we need another
assertion.

This view is passing in a request
object which has a user attached to it
and if logout is going to work on that
request object I would speculate that
the user attached to that request object
we can check is authenticated and down
here.
We should be able to. Let's do this.
So assert, and I don't usually like
putting assertions at the front
part of the test because I feel like it
muddies what the test is trying to do,
but let's check is authenticated
that's true.

Actually,
make sure that's a property is
authenticated
function that's not yeah as an attribute.
In older versions, this was a method.
That was a very important thing
because it used to used to trip people
up of it was it used to be a method so
methods in Python are always truthy so
because it was a method and some people
would treat it like a property or an
attribute it would return true even when
that was false so it was kind of
dangerous but they fixed up the API.

On
that there was an API work basically so
here I think my real thing that I want
to do is test that the user is no longer
authenticated. In other words, they're
logged out after this happens and this
let's get rid of that assert because we
know that's true beforehand so the
precondition is true and this will fail
on the other side because we haven't
called walk out again so we're gonna
come up to.
Okay that's at the off level so there's
login and logout
we're going to call
out actually are there any other log
outs in here.

Now we run a test
ah interesting
so this test expects a session I think I
can get away with that I added
- my requestfactory I think I called it
with session
so let's go over to the test case no
quest Factory
check on that.
Nope, I just call it `session`
not `with_session` but `session`.
Alright let's try it again.
That assertion
being false that we want to do. I'm
feeling now though but I probably by
calling logout here I might have broken
other tests in this test case. Oh no, I
didn't because this is the only one the
test the success path so it's the only
one that's going to require the session
because it's the only one getting all
the way through from the top to the
bottom.

That was really easy from
that perspective. I didn't know if that was
going to be harder or not but it turns
out not to be the case.
Now we're down to this last last bit
of what we have to do. I was reading
in advance of the session tonight to
figure out what Django is going to do by
default and so going coming back to the
Django contribute auth here we have. I
just searched for active and active only
appears in a few places so the user
model from Django control off has this
`is_active` flag and importantly let's do
a search for `is_active`. I think that was
the better one. Here it is so it says
the log-in required decorator does not
check `is_active` flag on either but this
is the important bit.

The default authentication back ends
which I'm using reject inactive users so
if I turn on if I set a user to not
active and log them out in the view at
the same time it should effectively lock
them out of the system. There'll be other
deactivated page so that they know that
if they try logging and again. That is
not going to work and they can contact
support that that should be evident but
I think these two things in tandem.
Should be enough to make sure that
someone can't get back into the
application after things are done so I
think the right place to do that to
actually set that users account to
inactive is on the form saving the
deactivate form.

We're going to leave the tests
and come in at the test forms and leave
the views file come into the forms file.
We're here. We have save and one
part about this form is that the user is
attached with the self attribute from
the window that your form is created so
we have access to the form to the user
in the form. We can
do a quick assertion that's assert true
that user is active
condition. To verify, you know, sanity
check, although most of the time I am
pretty confident that that's happened.
The case is true so the other
thing I want to do.
I'm going to update the docstring as
well so the user subscription gets
canceled and the user
it is marked inactive that's what we
care about. Let's change this to
false but we probably need to do a
`refresh_from_db`.

We have a failing test
coming into
the form save method and we're going to
take the user and set is active to false
and then save user.
Do I think that's all the code? I guess I
should preface let's run it
through some type check. All the type
checks are passing.
Things are looking pretty
good. I feel good about this so I
want to do a few things now so we're
getting close to the end of this feature.
If you're back from previous
sessions, this feature is behind a
feature flag so what is in the settings.
Let's get back to returning this stuff
on so we can see it all.

We put this whole feature behind a
feature flag so this deactivate
accounts section does not appear unless
a flag is activated so there's a
bunch of steps that I want to do a long
the way. I want to do a basic
verification that the deactivation
of flow works so we'll probably create a
user really quickly that we can login as
and try it allow and then we push it up
to production and we turn on the flag.
We see that it should be working
that's the hope so
to probably do this is on the staging
environment which has Stripe connected.

In order to do that I need to do a
deploy.
Let's look through the diff before we
commit this. We set our user to inactive
by changing the is active flag to false.
We tested the save and it cancels the
subscription and says these are to false.
So those are the two actions that
it takes. Our tests for the views are now
doing a deactivated page rather than
trying to redirect back to the dashboard.
That's good news. We test the failure
case of what happens when there's a
problem so that case is basically that
the exception is caught. It's reported to
rollbar which we've mocked out in this
test. It redirects back to the settings
and that there's a message that gets
sent to the user saying that there was a
problem. Then we did a quick sanity
check on the deactivated the activated
page to just assure that the the
template is there and that we can get a
200 response from that.

The views are
here where we took out all these TODOs
that were part of the deactivation
flow and we saved our form. We caught
errors. We reported problems. This is
essentially the other half of the test.
The actual production code and if
everything was valid. We log the user out
and then redirect them to the
deactivated page and then that should be
done. They should be done with this
system. We created a deactivated page to
actually give a place to go so that's
that's all that stuff.

Let's commit
this code and this time I'm gonna check
this and we're going to say that
complete the activation flow and this
fixes issue 372.
Fixes... there's a nice little shortcut
that you can put in GitHub that will
automatically close an issue if you
include that. There's some other I think
you can do "Closes." You can do some other
variants of that I don't remember what
they are but I use Fixes.
We commit that stuff and we push it
up to GitHub. I use some aliases so
that's what "gp" is git push.

Vagrant is still up but let's
confirm. Vagrant is where I do my staging
site
and it does either came up really
quickly or it already was up so let's do
a provision.
It should take a minute or two.
What's happening is the code that
we just pushed in GitHub is now
being deployed to this virtual machine.
We can go to the virtual machine. I
still have a test Stripe account that is
active
so if we go in there and
into the Stripe. Kill and
try and deactivate it.
Hopefully everything will go well.
That's running let me try and log
into straight

Here's the Stripe dashboard with
the test data
and
customers. See if we still have
this one but did I cancel the
subscription on it. I don't remember. I
did okay
Rats. We'll just create a new customer
but because this is test data it doesn't
really matter so I think what I must
have done is use this customer to cancel
the subscription in the last episode. I
forgot about that so we'll
create a Stripe test to customer and go
through the whole process to
verify that it is here in the
dashboard and once it's verified and
will actually go through the deactivate
flow and see if it behaves like we
wanted to.

If it does then I will do a
deployment to production and we'll go
into the flag - admin dashboard and go
turn it on and see how it looks and then
we'll probably wrap up for for the day.
We are done with the deployment
let's go to the conductor
test site.

I'm currently logged in.
That's
something I want to fix.
Give you an indicator of who is logged
in. I want to put that a username
somewhere you're logged in but maybe
next to dashboard or something like that.
Some kind of clue
that should be pretty easy one.
Because I think right now I'm
then as Stripe test.

The first thing I'm going to do
though is sign in as
admin because
pretty sure
don't have that flag turned on. Let's go
to the settings. There's no
deactivate turned on it's not on the
staging site so we're gonna go to the
admin and this can be the same process
that I'm going to use for the production
site as well so you'll see it twice.
Where I went to the place where feature
Flags are defined I'm using Django
Waffle and I'm gonna add a flag and the
flag name is `deactivate_flag` and I want
to turn it on for everyone.
Save that so now `deactivate_flag` is
on for everyone. You can go back to the
site go back to the dashboard, check the
settings, and there it is.
I've got my dummy email address in
here
and yeah everything's good.

Let's do a sign up we'll do Stripe
test two and
Stripe test to at nowhere dot com. Give it
a password
and a fake credit card which for Stripe
is just a bunch of 42s on repeat so you
can just keep typing for two for two for
two til you're done.
We'll create the free trial.
Alright, neat, so we have a refresh
there should be a straight test to
account our customer. I should say and
there is
okay so someone did that by accident
whatever and they want to get out of
here they look for how to deactivate.

The
most obvious place would be their
settings. Here's their deactivate account.
We give them this message that says if
you deactivate will halt your
subscription you won't be charged. It's
reassuring. We tell them in advance that
here's how you're going to reactivate if
you want to and we give a simple barrier
so people don't do this by accident.
But this is a copy-paste kind
of thing where we're just replacing
putting the email that is on file with
the account so here's the moment of
truth when we hit the activate does the
validation happen it goes to the save it
should cancel the subscription at Stripe.
Actually, I guess before we do that let's
come in here and make sure there is a
subscription.
Oh yeah, there's a subscription with
Stripe. It should logout the user dump
them to the deactivated page so this
dashboard and logout should go away and
it should become login and sign up again.
And that should be all the behavior.
let's click deactivate and see what
happens.

Great, we got to the deactivated page.
That's encouraging. It looks like we're
logged out because we're being prompted
to log in again and that's refresh
count page
there it is cancelled the
subscription so that seems like success
to me.
Since that is successful I'm going to go
ahead and deploy it.
It's the same kind of process. This
will take a little bit longer because
instead of connecting over localhost
it's now doing an actual ssh connection
to the remote server where college
conductor lives.

In a minute, to activate the flag I will
login. I'll be logged in with my admin
account at least. Go to the settings page
and see that that settings there I'm not
going to test it with my admin account
because I don't want to deactivate that
account on the production site. That
would be foolish.
I'm pretty confident that the
feature work which is exciting.
I guess while that's wrapping up with
the deploy we can talk through the set
of steps that we went through to do this
whole feature.

To start off with, I wanted
to start at the user experience level so
we actually started with that chunk of
dialog in the settings. This is not a
fancy form but it's not an inelegant
form either. In its simplicity, it
conveys what it needs to to get the
message across that here's what you're
about to do. It doesn't make it hard to
be deactivate but it doesn't make it so
that you can accidentally do it. But
those are all important things to me. I
didn't want people like clicking the
button by mistake and then calling me,
support, asking for help of "why
can't I get back into my accounts
something's gone wrong" So that was the
design of this form.

Then once we had the
form in place like we really didn't do
anything fancy of this form it was pure
HTML markup that didn't connect anything.
We then went into and created the view
that this thing would talk to. That view
was a post only view that was only
accessible to authenticated users so no
one else can randomly log you out. And on
top of that there's additional
protections that because you have to
supply the email you have to know the
email that's associated with that
account so some if I was logged in you
were logged in,
I couldn't log you out because my email
address is not going to match your email
address if we both had accounts on
College Conductor. There's some
safeguards against people logging each
other out deactivating other accounts if
someone was that nefarious which would
be ridiculous but possible I guess so at
least that protection is there so we
have the form that does that.

The form
process went through and canceled the
subscription at Stripe which it made a
Stripe API call.
In that process of doing the Stripe API
call we talked about custom error
handling and how to make sure that the
experience for the user in the event of
an error is, you know, nobody likes
getting errors and dealing with that but
at least they wouldn't get this page
that says "oh we messed up badly" and
don't know what to do. It's
essentially a guarded error that were
actually thought through and are making
sure that they're going to get taken
care of because not only are they told
to contact support so I would know
immediately but also the error message
was sent off to the error tracking
service. I'd be able to correlate the
failure and be able to say right off the
bat "oh yeah I'm so sorry I see it in the
the backend information that we have
that you know Stripe was some some part
of Stripe was down or there was a
network failure and I'm totally happy to
resolve at all." You know we can
get this result because I don't want
people walking away from account
deactivation with this really bad
terrible experience.

Once the Stripe
half of the equation was resolved then
we moved on to the College Conductor
half which is making sure the account
gets locked out that the user is marked
as inactive so they can no longer access
the service unless they specifically
request to get back in. That's the
entirety of the feature and our
deployment is done. Let's go over to the
website. I'm going to login
with my login credentials and going
to check over here and see there's no
deactivate section here yet because we
haven't created the flag so the thing to
do now is to go into the admin
and
`deactivate_flag`
to turn this on for everybody.

If I had a large user base, which
I don't, maybe I'd want to phase out how
are not phase out rollout do the phasing
of this flag in stages.
But I don't so we're just going to turn
on globally and then verify on site that
it is there. Great, it is.
That also covers the whole story of
feature flags except for one date. The
feature flags are useful for being able
to toggle this on and off like if I
wanted to, actually, let's just do it just
to show the benefit of this say I really
goofed and one of my users comes in and
says and deactivation is itself is
probably a bad idea but let's think
about a feature that is generally useful
but it's not going to cancel somebody's
account. They try out the feature and
notice a horrible bug that causes them a
really bad experience but I have other
users and I don't want to have more
people come in and using the feature
flag system. I could say "oh that's really
bad" Let's do this.
You know if we go backwards and turn the
feature off, now I'll come back to here
and the feature flag is off over here so
if we refresh the page, it goes away
so the feature that was maybe causing a
problem in production for other users
you can turn it off. You can then have
yourself or if you have engineers
working for you whatever your system is
go in and taking the data of what the
user experience was that caused a
failure, go in, and fix it and make sure
that it gets fixed properly and then
come back in and turn it on again. That
is the true value of flags.
They give you this ability to toggle
stuff which is super cool.

If you
didn't do that,
let's think about the process
if you weren't using a flag system. If
you weren't using a flag system you'd
roll out your feature
and the the pitfall of that of a flagless
system is what happens when your
user comes in and says hey this thing
doesn't work. Same scenario as just a
second ago. It doesn't work. Something is
wrong.
What can I do? You don't have the ability
to, in an instant, turn the feature off so
you might have other users encounter
that same error along the way. We're
going to pile on and maybe become
dissatisfied customers because you know
a customer that doesn't even know a
feature exists yet, like hasn't seen it,
hasn't used it, they're not going to feel
any animosity towards you. But a customer
who sees a new feature and tries it out
and it's broken is not going to be super
happy.

This gives you that control
there because in that scenario where you
don't have a flag system you have to
suddenly either scramble to fix it as
fast as possible and just apologize to
people as they start hitting this
problem or you have to have a rollback
strategy to roll your code back and if
you're in a complex enough system there
might be other things that have gone
into that release. Flags let you have
the finer granularity to roll things out
when they're ready this becomes even
more important as your team gets larger
and you're integrating a lot of code in
and you know you want to control when
things are seen to users.

That's the
whole benefit of a feature flag system
but to close the loop on a feature flag
there are plenty of flags that you might
want to leave in forever. Like maybe a
third party integration, like for example,
what's an obvious example.
Let's say you're trying a new third
party service like Mixpanel which is
tracking user actions on your site and
doing this sort of analytics and you're
not you're not sold on Mixpanel.
What you could do is put Mixpanel behind
a flag so that you can quickly toggle
the the service on or off
and having that ability to toggle that
gives you the flexibility of if you
decide to go for it, that it's good, or
maybe you have different environments
like a QA environment where you actually
don't want Mixpanel
on. Having the flagging system where you
can turn that off for Quality Assurance
purposes because that's that data would
just junk up your analytics.

You could
do that but enlarged flags or while
flags can be used for that purpose
like systems like this are more meant
for rolling out of features so when you
are satisfied with a flag you should go
through the process of cleaning it up.
Because if you look through the code...
let's do this. If we search for the
`deactivate_flag`, that's what we name this
flag. Now this is, thankfully, this one
it's only in one place. Let's close that.
It is an extra, essentially, it
looks like a conditional. It causes an
extra level of indentation and now we
have this flag thing. This seems fine
for now since it's just one flag, but
imagine you wanted to put another flag
inside of here like, you wanted to play
with the copy and you wanted to do like
an a/b test then you have another flag
in here and imagine you another flag
that's down here that's testing an
extra attribute on the form. You're
testing that out so feature flag systems
that are left around become a
cluttering and a nesting of conditional
type of logic.

I think what I
want to do to finish off the whole
feature and complete the life cycle of
this is to make the fairly
straightforward modification of "are we
done with this flag?" I'm going to delete
that and make it a permanent part of the
production code so, flag or no flag, this
will always be there.
Because this is not one of those those
features that needs to be selectively
controlled like a Mixpanel so
we removed the flag. Since we're not
using any sort of flag in here we can
now delete the `load` of `waffle_tags` which
makes flag available.
That's a small bit of cleanup that will
get the flag out of the system and that
is good enough to commit. I'm going to
add that to the stage and say remove
`deactivate_flag`.

That really closes out the
whole deactivate flow that's everything
we intended to do. There are little bits
that I might I'm not sure if I'm going
to do this on stream or not but I can
maybe show it off next time. I have a
part of my process that I mentioned in
the sign up. Let me show it in the sign
up. I indicate to anyone who signs up that
my SaaS app asks for a credit card up
front. I don't want
to do the freemium model and I don't
want to have a high load for people who
are trying it out who have no intention
of actually providing a credit card and
never paying for the service. By
having that bit of friction, it does reduce
dramatically the number of people who
come in to do a trial and I'm ok with
that
because the point is to get people who
are qualified enough that says "I'm
willing to try this and put a credit
card down knowing that I have a month to
try it out." And cancel is an important
aspect of that though is telling people
that the trial is
coming close to an end.

See at this
bottom paragraph that I tell people, you
know, three days before your trial is
about to be over,
I'll email you, letting you know, hey, we're
going to charge you soon if you have
enjoyed the service and want to continue
using it. If not, go over to the settings
page and you can deactivate your account.
I haven't actually hooked up that up
yet so I gotta make good on
that because I have an active trial
who's getting close to that window and I
don't want to be untruthful.
This was a minimum viable product. It was a
decent claim that I could make knowing
that I would honor that if I if I got
someone trialing so since I'm in a
position to do that I'm going to work
with the email service that I use, which
is Drip, and Drip connects to Stripe and
Stripe is connected and has the
subscription so I can go into Drip and
connect it to a Stripe event of when the
trial is ending.
I'm pretty sure that's configurable and
then send out the email that says "hey, go
to your account settings page if you
wish to deactivate otherwise we're going
to charge you when the
trial is over and get you know paying
for the service and getting value out of
it."

I may do that this week. I don't
remember how many days the the trial
that I have going has so if it's less
than the amount of time between now and
next week, I need to do that, but if it's
not, I might do this on stream and
will poke around at other aspects of a
SaaS.

It's not always just about
coding and Django and Python. There are
other services that you use that you
have to be comfortable with and get the
best value out of. I can show you at
least one of them. Drip is a really cool
tool. I think that's
probably about it so that will wrap us
up for tonight.

If this is something that if
you found this useful you can share it
out on X I will also post this to
YouTube like I do regularly so if you
want to refer back to anything that I
said, you are certainly welcome to do
that. If you found this useful, I'd
love to hear from you, find out
what you liked about it. I'm on X
as mblayman. I'm also on GitHub. I'm also
on a bunch of place in the places as mblayman
so look for me around. I
appreciate your feedback. Trying to think
if there's anything else that that needs
to be said. Probably not so that
brings us to a close for the night. I
appreciate you tuning in and we'll catch
you next week when we run more SaaS
development. Take care.
