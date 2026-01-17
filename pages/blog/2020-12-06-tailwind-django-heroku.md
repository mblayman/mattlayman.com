---
title: "How To Set Up Tailwind CSS In Django On Heroku"
description: >-
    In this quick article,
    I showed how I set up Tailwind CSS
    for my Django app
    on Heroku.
image: /static/img/2019/heroku.png
date: 2020-12-06
slug: tailwind-django-heroku
categories:
  - Python
  - Django
tags:
  - Python
  - Django
  - Tailwind
  - Heroku

---

How can you set up
[Tailwind CSS](https://tailwindcss.com/)
for your Django app
on Heroku?
In this article,
we'll see how I did exactly that recently.

I have a side project
that uses Tailwind CSS.
To get started quickly,
I used the version
from a Content Delivery Network (CDN)
as Tailwind describes
in the [documentation](https://tailwindcss.com/docs/installation#using-tailwind-via-cdn).
This worked fine initially
while I got my project started,
but the CDN version is huge
(around 3MB).

I also deploy my app to Heroku,
so I didn't bother to take the time
to set up a customized build
of Tailwind.
If you follow Tailwind's more involved instructions,
you can reduce the size of your CSS file dramatically.
I set all of this up
and my CSS file went from the huge CDN size to 29kB.

Here are the high level steps
to set up Tailwind
for a Django app
on Heroku:

* Set up [Node.js](https://nodejs.org/en/).
* Install Tailwind.
* Create the Tailwind configuration file and your CSS file.
* Set the build command.
* Build the file locally for development.
* Hook the CSS file into your templates.
* Set up a buildpack for Heroku.

## Set Up Node.js

I use a Mac and [Homebrew](https://brew.sh/)
so installing the latest version
of Node.js looked like:

```bash
$ brew install node
```

If you're on a different platform,
the way to install Node.js is going to be different.
Check out the Node.js docs for install instructions.

## Install Tailwind

From within my repo,
I ran:

```bash
$ npm install tailwindcss
```

This created a `package.json` and `package-lock.json` file
in the root of my repository
that will list Tailwind
and its Node.js dependencies.

Installing Tailwind will also create a `node_modules` directory.
You definitely want to add this directory
to your `.gitignore` file.

## Create The Tailwind configuration

Tailwind uses a configuration file
for any customizations
that you want
to make.
I created an empty one with:

```bash
$ npx tailwindcss init
```

I moved the newly created `tailwind.config.js`
to a `frontend` directory
to help me keep things tidy.

Before I could get any benefit
from doing this work,
I had to make sure
that Tailwind knew where my templates were.
This is critical
because Tailwind will use PurgeCSS
to eliminate any extra CSS classes
that it can't find in my templates.
If you neglect this step,
the final version
that Tailwind will build will also be huge.

To set the proper purging,
I added this block to my Tailwind configuration file:

```js
  purge: [
    './templates/**/*.html',
  ],
```

In my project,
I keep all of my Django templates
in a `templates` directory
at the root
of my repository.

I also used Tailwind with PostCSS
so I needed a `postcss.config.js` file
in the root
of my repo as well.
Here's the content of the file:

```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  }
}
```

Finally, I needed my actual CSS file.
I added `frontend/site.css` with:

```css
@tailwind base;

@tailwind components;

@tailwind utilities;
```

## Set The Build Command

To pull it all together,
we need the build command.
Here's what I included in `package.json`
(with added formatting here for display purposes).

```json
{
  "scripts": {
    "build": "tailwindcss build frontend/site.css
                -c frontend/tailwind.config.js -o static/site.css"
  },
  ...
}
```

The build command instructs Tailwind on:

* The location of the input file
* Which configuration file to use
* Where to put the output file

## Build A Local CSS File

Now I can run `npm run build`
and a generated file named `site.css`
is stored in my `static` directory.
This is another file you'd want to add to your `.gitignore`
because you don't want to commit it to source control.

To test that everything was correct,
I ran my command using the production configuration
and tested it locally.
Tailwind showed in the build output
a significantly reduced file size.

```bash
$ NODE_ENV=production npm run build
```

If you do this, don't forget to run it again later
without the `production` value
or you'll be really confused
when your styles don't appear
as you develop new features
on your local machine!

## Hook The CSS File Into Templates

With the Tailwind toolchain in place,
I was ready to swap out my CDN version.
I went to my base template
and replaced the CDN line with:

```django
{% load static %}
  ...
  <link href="{% static "site.css" %}" rel="stylesheet">
```

By outputting the CSS file
into the `static` directory,
Django has no problem loading it
with its standard static files mechanism.

As an added bonus,
at deploy time,
Django will create a fingerprinted version
of the file that includes the hashed filename.
This means that my Tailwind CSS file will get the same long term caching benefits
that I got from the CDN version,
but at a massively smaller size!

## Set Up A New Heroku Buildpack

I had to tell Heroku
that I now want to run Node.js
as part of my app deployments.
We can do this by adding a new Heroku buildpack.
It's important that this come
before the Python buildpack
so that the Django `collectstatic` process
will find the generated file.
We can set the order
with the `index` option:

```bash
$ heroku buildpacks:add --index 1 heroku/nodejs
```

To tell Heroku
which version of Node.js
to use,
I added an `engines` section
to `package.json`:

```json
{
  "engines": {
    "node": "15.x"
  },
  ...
}
```

Now when I deploy my app
to Heroku,
Tailwind will build the production version CSS file
to serve to my users.
This happens because Heroku defaults
to setting `NODE_ENV` to `production`.

And that's how I did it!
The pages on my app are much snappier
after I made this change.
There is way less CSS
for the browser to process
on page load
by many orders of magnitude.

Thanks to the nudge
from [Will Vincent](https://x.com/wsv3000)
to get me to get off my lazy rear
and finally set up my JavaScript toolchain.

If you have questions
or enjoyed this article,
please feel free to message me on X
at [@mblayman](https://x.com/mblayman)
or share if you think others might be interested too.
