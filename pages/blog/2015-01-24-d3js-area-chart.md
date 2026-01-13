---
slug: d3js-area-chart
title: A "simple" D3.js area chart
date: 2015-01-24
description: >-
  A step-by-step walkthrough of a D3.js area chart.
  This post covers each piece needed to create an area chart
  from a list of JavaScript data.
image: img/2015/d3js-area-chart.jpg
aliases:
 - /2015/d3js-area-chart.html
categories:
 - Guide
tags:
 - JavaScript
 - D3js

---

<style>
svg.demo { border: 1px solid #dedede; }

.axis path, .axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.area { fill: #4ca3bd; }
</style>

Let's take:

<table>
  <thead>
    <tr><th>X</th><th>Y</th></tr>
  </thead>
  <tbody>
    <tr><td>0</td><td>10</td></tr>
    <tr><td>1</td><td>15</td></tr>
    <tr><td>2</td><td>35</td></tr>
    <tr><td>3</td><td>20</td></tr>
  </tbody>
</table>

And make:

<svg class="demo" id="area" />

D3.js is mindbending, and I find the examples on the D3.js wiki to be too
little explanation with too much going on. In this example, I will show
you how to make the simplest area chart I could devise. If you want to
jump straight to "the answer," see [the complete JavaScript](/2015/area.js).

D3.js is not a chart library. It is a chart *parts* library. The library feels
like a mashup of SVG and data manipulation with some sugar sprinkled on top.
While immensely flexible, the flexibility comes at the cost of complexity.
Let's dive in.

To build the chart, we need: data, an SVG container, margins, an X axis, a Y
axis, the area shape itself, and some CSS to make it look pretty.

#### Data

We're not going to mess with TSV or CSV loaders or any of the callback stuff.
Here is the data, plain and simple.

```javascript
var data = [
    { x: 0, y: 10, },
    { x: 1, y: 15, },
    { x: 2, y: 35, },
    { x: 3, y: 20, },
];
```

#### SVG

D3 uses SVG (Scalable Vector Graphics) to draw its shapes. It's possible to
create a new `<svg>` tag on the fly, but I added the following to the HTML
source code.

```html
<svg id="area" />
```

#### Margins

Charts in D3 have no margins, but the primary D3 author frequently talks about
defining [conventional margins](http://bl.ocks.org/mbostock/3019563). The idea
is to make some margins and define an SVG group (i.e. the `g` tag) that is
set to those margin boundaries. The code only considers the group tag as the
drawable area.

```javascript
var margin = {top: 20, right: 20, bottom: 40, left: 50},
    width = 575 - margin.left - margin.right,
    height = 350 - margin.top - margin.bottom;
```

#### Axes

To draw data in a scalable way, D3 needs to be able to map the data (e.g.,
x=0, y=10) to a pixel position. We must take the X data and set it on the
axis so that the maximum X value (i.e. 3) matches the pixel width of the
chart area. Because D3 is so flexible, it means that X and Y must be
defined independently.

In math class, you were probably taught that X is for the domain
and Y is for the range. Unfortunately, D3 uses domain/range terms to apply to
axes too. We have to think about the X data (0 - 3) as the domain, and the
chart horizontal dimension (0 - `width`) as the range. The same kind of
thinking has to be applied for the Y axis as well (0 - 35 applied to the
chart vertical dimension).

You can think of the `x` and `y` variables as translator functions that take
a domain value and convert it to a pixel size. `xAxis` and `yAxis` are
indicating where the axes should go.

```javascript
var x = d3.scale.linear()
    .domain([0, d3.max(data, function(d) { return d.x; })])
    .range([0, width]);

var y = d3.scale.linear()
    .domain([0, d3.max(data, function(d) { return d.y; })])
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");
```

#### Area

The area function transforms each data point like (2, 35) into information
that describes the shape. Each corresponds to an x position, an upper y
position, `y1`, and a lower y position, `y0`. The odd thing here is that `y0`
is set to the constant of `height`. This makes sense when you know that SVGs
are positioned relative to the upper left corner of the graphic. Any distance
"down" is a positive number, so a positive `height` means the bottom of the
graphic.

```javascript
var area = d3.svg.area()
    .x(function(d) { return x(d.x); })
    .y0(height)
    .y1(function(d) { return y(d.y); });
```

#### Putting it all together

So far, we have not done anything except define some data and functions.
Now we need to put those functions to work.

```javascript
var svg = d3.select("svg#area")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.append("path")
    .datum(data)
    .attr("class", "area")
    .attr("d", area);

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);
```

The variable definition of `svg` grabs the `svg` tag with ID `area` and
adds a group tag, `g`, to define the margins within the SVG. All the
drawing will happen inside this `g` tag.

The next section adds a `path`. This is where the data and the area function
meet. *It is the keystone of this entire example.* D3 uses each data
point and passes it to the `area` function. The `area` function translates
the data into positions on the path in the SVG. It will result in:

```html
<path class="area" d="M0,214.28571428571428L168.33333333333331,
171.42857142857142L336.66666666666663,0L505,128.57142857142858L505,
300L336.66666666666663,300L168.33333333333331,300L0,300Z"/>
```

The last two sections adds the axes to the SVG. There isn't much to say
about them.

#### Make it pretty

In "Putting it all together", I ignored the `.attr("class", "area")`
explanations. D3 can add any tag attributes with `attr()`. I added some
`class` attributes so that the graph can be styled. SVG uses different
properties than standard HTML tags, but the styling below gave
the graph its simple look.

```css
svg { border: 1px solid #dedede; }

.axis path, .axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.area { fill: #4ca3bd; }
```

#### Other charts

In this post, I covered the basics of making an area chart. In future posts,
I will explain how to use other types of data and how to make stacked
area charts. Stay tuned!

<script src="https://d3js.org/d3.v3.min.js" charset="utf-8"></script>
<script src='/static/2015/area.js'></script>
