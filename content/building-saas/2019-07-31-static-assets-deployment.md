---
title: "Add Static Assets to Deployment - Building SaaS #29"
description: >-
  In this episode,
  we pushed CI built static files to S3,
  then pulled those files into the Ansible deployment.
  This is part of the ongoing effort to simplify deployment by moving work to CI.
type: video
image: img/2019/circleci.png
video: https://www.youtube.com/embed/tUUeQEIVBT8
aliases:
 - /building-saas/29
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Circle CI
 - Ansible

---

In this episode,
we pushed CI built static files to S3,
then pulled those files into the Ansible deployment.
This is part of the ongoing effort to simplify deployment by moving work to CI.

Last time,
we processed static files
like JavaScript, CSS, and images
using {{< extlink "https://webpack.js.org/" "webpack" >}}
on {{< extlink "https://circleci.com/" "Circle CI" >}}.
Once the files were processed,
I used the `tar` command to create a tarball
(i.e., a `.tar.gz` file)
that contains all the static assets.

The first task from this episode was the upload
the generated tarball to {{< extlink "https://aws.amazon.com/s3/" "AWS S3" >}}.
I created an S3 bucket
where the asset tarballs can live.
We then used the {{< extlink "https://circleci.com/orbs/registry/orb/circleci/aws-s3" "Circle CI AWS S3 orb" >}}
to push the generated tarball to the new S3 bucket.

With the tarball on S3,
we were finally ready to move to deployment.
I created {{< extlink "https://www.ansible.com/" "Ansible" >}} tasks to:

1. Create a directory for asset tarballs to live on the server.
2. Pull a tarball from S3 and store it in the directory.
3. Extract the tarball files into the static root directory
    where {{< extlink "https://www.nginx.com/" "Nginx" >}}
    can serve the files to users.

I didn't quite finish it all
because some file permission issues popped
that we still need to resolve.
Next time we will fix those issues,
then do the fun stuff
of ripping out the old deployment steps.
