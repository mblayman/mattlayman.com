---
title: "Get Out, Git! - Building SaaS #33"
description: >-
  In this episode,
  I removed the Git clone from the server.
  This is some of the final cleanup to streamline the deployment process.
type: video
image: img/2019/git.jpg
video: https://www.youtube.com/embed/LI1tejZkrQg
aliases:
 - /building-saas/33
categories:
 - Twitch
 - Python
 - Django
tags:
 - Python
 - Ansible
 - Git

---

In this episode,
I removed the Git clone from the server.
This is some of the final cleanup to streamline the deployment process.

Before we could remove the clone completely,
we had to decouple the final remaining connections
that still depended
on the repository clone.

The first thing to clean up was the
{{< extlink "https://letsencrypt.org/" "Let's Encrypt" >}}
certificate fetching process.
The load balancer's Ansible playbook had this task:

```yaml
- name: Create cert
  become: yes
  command: >
    /usr/bin/letsencrypt certonly --webroot
    --email "{{ secrets.conductor.email }}"
    --agree-tos
    --webroot-path "{{ client_root }}"
    -d "{{ root_domain }}"
    -d "{{ client_domain }}"
  when: deployment == "production" and certdir.stat.isdir is not defined
  notify:
    - Restart Nginx
```

The trouble was that this `client_root` pointed
at a directory
within the repository.
This was for historical reasons related
to hosting my long-since-gone Ember client app.
We changed the `client_root`,
but then had the challenge
of how to test the change.

My staging environment doesn't use actual Let's Encrypt certificates.
You can observe
in the Ansible task above
that the task only runs `when` the deployment is `"production"`.
To get some confidence
that the change would work,
I deployed,
the logged into the server
and ran the `letsencrypt` command above,
but used the `--dry-run` option
to test things out.

Along the way of making this `client_root` change,
I explained how Let's Encrypt works
to fetch TLS certificates
for your domain.
It's a really great service!

The other big change that I made centered
around getting the Git SHA of the master branch.
Since this process is removing the clone,
we needed a way to get the SHA
because that is used as the version
to pull the application
from S3.

Getting the SHA from a local clone
is a side effect
of using the Git module
in Ansible.
Without that clone,
I needed another command.
Ultimately,
I crafted this task:

```yaml
- name: Get the latest SHA from GitHub
  become: yes
  shell: "git ls-remote https://github.com/mblayman/conductor.git \
    refs/heads/master | cut -f1"
  register: gitsha
```

`ls-remote` lets you inspect the branches
of a remote repository.
The output include more information
than I needed,
but the trusty old `cut` command let me extract the SHA quickly.

With the Git clone removed,
I can remove the ssh deployment key
for my system
which will tighten up the security
of my deployment process.

On the next stream,
I'm thinking of using
{{< extlink "http://whitenoise.evans.io/en/stable/" "WhiteNoise" >}}
to make my static asset management
even simpler
and continue cleaning up deployment.
