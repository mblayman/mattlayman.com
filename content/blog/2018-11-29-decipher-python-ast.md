---
title: "Deciphering Python: How to use Abstract Syntax Trees (AST) to understand code"
description: >-
  How does the Python program run your code?
  How can you understand how your code runs?
  This post explores Abstract Syntax Trees (AST),
  a vital part of how Python evaluates code
  before running it.
  We'll use an AST
  in a practical example
  to show you how to learn more about your code
  for your benefit.
image: img/python.png
type: post
categories:
 - Python
tags:
 - AST
 - analysis
 - Python

---

Let's get a little "meta" about programming.

How does the Python program
(better know as the interpreter)
"know" how to run your code?
If you're new to programming,
it may seem like magic.
In fact,
it still seems like magic to me
after being a professional
for more than a decade.

The Python interpreter is not magic
(sorry to disappoint you).
It follows a predictable set of steps
to translate your code
into instructions that a machine can run.

At a fairly high level,
here's what happens to your code:

1. The code is *parsed* (i.e., split up) into a list of pieces usually called *tokens*.
   These tokens are based on a set of rules
   for things that should be treated differently.
   For instance,
   the keyword `if` is a different token than a numeric value like `42`.
2. The raw list of tokens is transformed
   to build an Abstract Syntax Tree, AST,
   which is the subject we will explore more in this post.
   An AST is a collection nodes
   which are linked together
   based on the grammar
   of the Python language.
   Don't worry if that made no sense now
   since we'll shine more light on it momentarily.
3. From an abstract syntax tree,
   the interpreter can produce a lower level form
   of instructions
   called bytecode.
   These instructions are things like `BINARY_ADD`
   and are meant to be very generic
   so that a computer can run them.
4. With the bytecode instructions available,
   the interpreter can finally run your code.
   The bytecode is used to call functions
   in your operating system
   which will ultimately interact with a CPU and memory
   to run the program.

Many more details could fit into that description,
but that's the rough sketch of how typed characters
are executed by computer CPUs.

## ASTs as analysis tools

By the time your source code is turned into bytecode,
it's too late to gain much understanding
about what *you* wrote.
Bytecode is very primitive
and very tuned to making the interpreter fast.
In other words,
bytecode is designed for computers over people.

On the other hand,
abstract syntax trees have enough structured information
within them
to make them useful
for learning about your code.
ASTs still aren't very people friendly,
but they are more sensible than the bytecode representation.

Because Python is a "batteries included" language,
the tools you need to use ASTs are built into the standard library.

The primary tool to work with ASTs is the `ast` module.
Let's look at an example to see how this works.

## `ast` by example

Below is {{< extlink "/2018/ast_example.py" "the example Python script" >}} that we'll use.
This script answers the question of
"what modules were imported?"

{{% code file="/static/2018/ast_example.py" language="py" %}}

This code does a couple of major things:

1. Transforms a Python file's text
   (in this case, the example code itself)
   into an abstract syntax tree.
2. Analyzes the AST to extract some information out of it.

You can run this code as:

```bash
$ python3 ast_example.py
{'from': ['pprint'], 'import': ['ast']}
```

### Transform to AST

```python
with open("ast_example.py", "r") as source:
    tree = ast.parse(source.read())
```

In two lines of code,
we read a file and create an AST named `tree`.
The `ast.parse` function makes this a snap!
There is a ton happening under the hood of that function
that we can blissfully ignore.

With one function call,
Python processed all the tokens,
followed all the rules of the language,
and built a data structure (i.e., a tree)
containing all the relevant information
to run the code.

Before moving on,
let's take a moment to consider what a tree is.
Trees are a very deep topic
in software development
so consider this a primer
rather than an exhaustive explanation.

> A tree is a way to hold data
as a set of "nodes" connected by "edges."

```text
         +-----+
         |  A  |
         +-----+
        /       \
       /         \
+-----+           +-----+
|  B  |           |  C  |
+-----+           +-----+
```

In this diagram,
A, B, and C are all nodes
and there are edges connecting A to B and A to C.

One way to represent this tree in code could be:

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

tree = Node('A')
tree.children.append(Node('B'))
tree.children.append(Node('C'))
```

Notice that the `tree` is actually a node!
When we work with a tree,
we're really dealing with a collection of nodes,
and the tree variable is a reference to the "root" node
(e.g., node A).
By having this kind of structure,
we can check each node in the tree
and take action.
We do that by visiting each node
in the tree
and processing its data.

```python
def print_node_value(value):
    print(value)

def visit(node, handle_node):
    handle_node(node.value)
    for child in node.children:
        visit(child, handle_node)

# tree is from the previous example.
visit(tree, print_node_value)
# This should print:
# A
# B
# C
```

Now that we have an idea of what a tree is,
we can consider what the next section
of the example script does.
The tree structure
of the Python abstract syntax tree
is more involved
because of the count of its nodes
and the type of data stored,
yet the core idea of nodes and edges is the same.

### Analyze the AST

Once we have the tree,
the `Analyzer` follows the visitor pattern
that I showed above
to extract information out of the tree.

I noted that a Python AST is more complex
than my basic `Node` design.
One difference is that it tracks various *types* of nodes.
This is where `ast.NodeVisitor` is useful.

A `NodeVisitor` can respond to any type of node
in the Python AST.
To visit a particular type of node,
we must implement a method
that looks like `visit_<node type>`.

My example code is trying to find out
about imports.
To learn about imports,
the code pulls from the `Import` and `ImportFrom` node types.

```python
def visit_Import(self, node):
    for alias in node.names:
        self.stats["import"].append(alias.name)
    self.generic_visit(node)

def visit_ImportFrom(self, node):
    for alias in node.names:
        self.stats["from"].append(alias.name)
    self.generic_visit(node)
```

This code takes the name of the module
and stores it
in a list of statistics.
While the code is not fancy,
it shows you how to interact
with AST nodes.

With the `NodeVisitor` class defined,
we can use it to analyze the tree.

```python
analyzer = Analyzer()
analyzer.visit(tree)
```

The `visit` method will delegate to your `visit_<node type>` method
whenever that type of node is encountered
while traversing through the tree structure.

So, what kinds of node types are there?
You can find the full list in the
{{< extlink "https://docs.python.org/3/library/ast.html#abstract-grammar" "Abstract Grammar" >}} section
of the `ast` module documentation.
Truthfully,
I find that documentation a little hard to absorb.
You may have more success
by referring to a more exhaustive guide like the
{{< extlink "https://greentreesnakes.readthedocs.io/en/latest/nodes.html" "Green Tree Snakes" >}} Nodes guide.

## Wrapping up

By now,
you hopefully understand how to:

1. Build an AST from Python source code.
2. Do analysis on the AST using a `NodeVisitor`.

I think you can answer many interesting questions
about your code
by using abstract syntax trees.
Questions like:

* How many variables did I use?
* What are the most common function calls in my code?
* Are my modules tightly coupled to each other?
* Which third party libraries show up frequently
  in different packages?

The `ast` module is probably not a tool
that you will reach for very often.
In those times that you **do** need `ast`,
its minimal API is quite memorable
and you can analyze code quickly.

If you found this useful,
would you mind sharing this on Twitter
or your favorite social media site?
I like chatting with people
about these kinds of topics
so feel free to tweet me at
{{< extlink "https://twitter.com/mblayman" "@mblayman" >}}.
