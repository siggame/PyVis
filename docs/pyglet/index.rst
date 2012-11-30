Pyglet, A Perhaps Useful Guide
==============================

Other Pages
-----------

 * :doc:`The Pyglet Drawing Hierarchy </pyglet/pyglet-drawing>`

Pyglet is a pure-python library that accesses the native OpenGL calls on your OS.  It actually does a lot of other cool stuff.  But from a graphics perspective, this is important.  Using a tool called gengl.py, it automatically generates all the python hooks to access everything you could want to access in OpenGL including extensions and other stuff.  It also does all the set up for you.

If you take a look at :doc:`Pyglet Drawing </pyglet/pyglet-drawing>`, it will show you how pyglet organizes things so as to provide very efficient and fast rendering. 

The main thing to take away from that is that pyglet is very fast when it keeps rendering the same things.  If you create an environment where pyglet has to keep adding new things, then it will be very slow.  This includes clearing and re-adding already existing items.  

The most efficient way to use pyglet is to essentially create diffs between frames.  If nothing has changed for an element, then the diff is nothing. 

A paused game should be hyper fast because the diff should be empty.

When making something hidden, it is faster to set its alpha to zero or set all the vertices in the object to (0, 0).
