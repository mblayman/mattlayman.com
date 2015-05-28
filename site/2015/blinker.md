%YAML 1.1
---
title: Connect Python objects to blinker signals
template: writing.j2
date: March 18, 2015
---
<img class='book' src='blinker.png'>

I started using [blinker][bl] for [handroll][hr].
Blinker is a signal generation library for broadcasting events.
The library lets signalers send messages
to connected receiver functions.
I will explain how I convinced Blinker to talk to objects
instead of pure Python functions.

[bl]: https://pythonhosted.org/blinker/
[hr]: http://handroll.github.io/

The example code is going to handle a "[frobnicated][frob]" signal.
Remember, the signal itself is not very important.

[frob]: http://dictionary.reference.com/browse/frobnicate

```python
import blinker

frobnicated = blinker.signal('frobnicated')
```

`frobnicated` is a named signal.
In a real project,
you might put all your signals in a single module.
[Pelican][pel] does this nicely.
Grouping all your signals in one place
gives signal consumers a clear view of what is available.

[pel]: https://github.com/getpelican/pelican/blob/master/pelican/signals.py

```python
class Receiver(object):

    def __init__(self):
        def handle_frobnicated(sender, **kwargs):
            self.on_frobnicated(sender, **kwargs)
        self.handle_frobnicated = handle_frobnicated
        frobnicated.connect(handle_frobnicated)

    def on_frobnicated(self, sender, **kwargs):
        print sender, kwargs['message']
```

The `__init__` method is where all the magic happens.
The first thing to notice is the use of an inner function,
`handle_frobnicated`.
The inner function uses the method signature
that the signal will invoke,
and delegates to `Receiver.on_frobnicated`.
Why?
This is necessary
because Blinker can't pass `self` to receiver functions.
`handle_frobnicated` acts as a [closure][cl] on `self`
which lets the signal call the instance method.

[cl]: http://en.wikipedia.org/wiki/Closure_%28computer_programming%29

```python
        self.handle_frobnicated = handle_frobnicated
```

That seems like a strange line,
doesn't it?
Blinker does some funny stuff with references.
Without storing the inner function,
Blinker will delete a weak function reference
and the inner function will no longer be among the signal's receivers.
I stared at the Blinker source code
for a long time
to figure that mystery out.

The last line in `__init__` connects the signal to the inner function.
The receiver is ready to handle `frobnicated` events.

```python
if __name__ == '__main__':
    receiver = Receiver()
    for i in range(10):
        frobnicated.send('Sender %s' % i, message='hello')
```

The code to fire the signal is fairly boring.
Notice that `frobnicated.send` has no need for `receiver`.
The publisher is disconnected from subscriber at this stage.
The final result looks like:

```bash
$ python blink_object.py
Sender 0 hello
Sender 1 hello
Sender 2 hello
Sender 3 hello
Sender 4 hello
Sender 5 hello
Sender 6 hello
Sender 7 hello
Sender 8 hello
Sender 9 hello
```

By connecting a signal to an object,
you get all the benefits that come along with classes.
Rather than making a monsterous function,
you could use various instance methods
within the handler.
This flexibility is a boon for unit testing.
The gain has similar advantages to using [class based views][cbv]
in Django
rather than function views.

[cbv]: https://docs.djangoproject.com/en/1.7/topics/class-based-views/intro/

You can [check out the full example in all its glory.](blink_object.py)
If you want to chat about this with me,
I'm [@mblayman][tw] on Twitter.

[tw]: https://twitter.com/mblayman
