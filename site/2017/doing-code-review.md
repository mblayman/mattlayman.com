%YAML 1.1
---
blog: True
title: Doing code review
date: 2017-12-23T12:00:00Z
summary: >-
  How can you start code reviews
  on your team?
  Your team might have questions
  similar to ones I recently received.
  I shared my thoughts
  as someone who has done regular code reviews
  for years.
image: code-review.png
template: writing.j2

---

<img class='book mv20' src='code-review.png'>

> How do you do code reviews?

This question was recently presented to me
from someone considering adding code reviews
to his team's process.

This post lists his questions
and my answers (lightly edited)
for the benefit
of other teams looking
for advice about starting code reviews.

## How exactly do you review code?

### When is a reviewer being pedantic vs being helpful?

I think this is the best place for automated linting tools
for style guides and other static analysis.
In my experience,
having those tools in place removes 99% of pedantic debates.
People are shockingly comfortable
with obeying linting tools
if that's the team policy.
Once those checks are in place,
I've found that the conversation is generally elevated above
pedantic commentary.

Beyond that,
a cordial tone in writing review comments is critical.
Asking questions instead of speaking in absolutes
often changes review conversation dramatically.
The key is that the team remembers
that reviewers should be seen less as gatekeepers
and more as collaborators
with the intention of improving the code.

### When is it good to push back on code?

I push back on code when there is a clear defect that will cause problems.
Otherwise, my policy is to leave my comments and approve the code review,
trusting that my teammate will consider the advice
and apply any appropriate changes.
The combo of "here are some things that I think could be better"
plus "I approve this" acts as a signal of trust.

### If someone pushes in code that does the job, but there are ways to future-proof for possible customer changes that might come down, do I send it back or just accept it?

At Storybird,
we're extremely wary of future proofing because the future is so uncertain.
There is some appropriate place between a hack and gold plating.
We usually accept something and improve the code in a future branch.
Again, static analysis may save your bacon here.
Adding checking for cyclomatic complexity and the like sets the bar
in case someone tries to commit something truly awful.

### If I see a change that could or should be made, do I just paste the code into the review, or does that hurt the learning process? Or is my asking this question betraying my lack of understanding of code reviews?

Code talks.
I think developers still learn tremendously when code snippets are given.
I will often put in code chunks as a sketch of the real thing.
The core bits might be there,
but I don't try to compile the code
and I might do something like add `# Do the rest of the stuff` comments
to laser focus on the code that really matters for discussion.

### Do you just do it online in a code repo (gerrit, in our case) or can/should you do it in person (I realize you wouldn't do them in person, per se, but do you do them with the developer realtime)?

I've done both styles and *online versions are vastly superior*.
The async nature of a code review respects the developer's time.
Our profession is so focused on getting into flow.
If you have to show up to an in-person code review (physical or phone calls),
it really ruins those chances to get into flow in a day.
This would be especially true
if you end up having multiple reviews per day.
I think you'll have much easier buy-in from developers
if you go with the online version.

## How does the team develop in a code-review environment?

### Is there a good strategy for breaking up commits, or do you just live with huge commits in those cases?

My rule of thumb is a **500 line diff max**.
Too much beyond that and even the best reviewer's eyes start to glaze over.
This favors delivering small features or clear chunks in a feature.
Since we deploy often,
we merge large features behind feature flags.

There are some occasions where we'll review large branches.
We try to make this rare enough that a developer feels slightly guilty
for making a huge branch.
I don't suggest that this guilt is for shaming.
It's more of a "shoot, I made my teammate's work way harder
by giving them tons to review."

### If you make one commit and push it for review, what do you do while you're waiting for that to be reviewed?

We usually have code reviews (GitHub Pull Requests) scoped to a feature level.
By scoping to a feature instead of a single commit,
it's a natural transition point to move onto some other task
while waiting for a review.

On the occasion that I'm working a really large feature,
I might start from a feature branch (branch A)
and put up a pull request when a decent chunk of work is done
(like a sub-feature in the overall picture).
Then I'll branch from A to create branch B
and continue working while A is under review.
This allows branch B to use stuff that it might need from branch A.
When A is done and merged back to master,
I'll merge master back into branch B.
Doing this makes the PR for branch B only show the content for branch B.

## Summary

I hope some these answers can help a team
that is thinking
of starting code reviews.
If there are other questions
that aren't answered here,
feel free to reach out,
and I can try to answer.
