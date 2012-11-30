Supplementary OpenGL Information
================================

This section is not required reading for doing 90% of the visualizer, but I have always felt it can be useful to know the background of a technology when making decisions in your coding.

What is OpenGL?
---------------

OpenGL stands for OPEN Graphics Library.  But let's be clear here.  OpenGL is neither open nor a graphics library in the general sense of either term. OpenGL is a tightly controlled standard set forth by The Khronos Group, which has people on its board from many major OS and graphics chipset providers. (e.g. Microsoft, Apple, NVidia, ATI, etc.)  

If you're not familiar with the concept of standards, then I'll explain here. A standard is a name brand associated with a specification.  To say that you are OpenGL compatible, or any other standard compatible, you must follow the strict set of specifications in the standard or potentially face legal implications. Typically there's some sort of integration test that the standard maker performs then deems the source code compatible or not.

So what OpenGL is, in a nutshell, is a set of rules that Graphics Card makers, software renderer developers, and the like must follow in their drivers to say that they run a certain version of OpenGL.

The only open implementation of OpenGL that I know of is `Mesa3D <http://www.mesa3d.org>`_.  It's a software renderer used primarily by GNU/Linux.

Retained Mode vs Immediate Mode
-------------------------------

There are two high-level approaches to rendering stuff: retained mode and immediate mode.  In retained mode, you send everything you want to draw to the graphics card once, then keep updating the stored information when you want to change something.  In immediate mode, you tell the graphics card exactly what to render every single frame.  Nothing is stored on the graphics card inbetween frames.  Retained mode is much faster, but can be more difficult to design a system around.  Pyglet thrives on retained mode as sending individual drawing calls ever frame is even slower when you're reliant on the speed of python.

Historically, OpenGL only supported immediate mode, using calls, glBegin() and glEnd().  Those calls are now deprecated and immediate mode is on its way out as The Khronos Group tries to streamline the API.  

Retained mode is managed using Display Lists (being deprecated) and Vertex Arrays through Vertex Buffer Objects.  Vertex arrays are lists of vertices that are stored in graphics memory along with colors, texture coordiates, fog coordinates, etc.  Then calling, glDrawArrays() or glMultiDrawArrays() tells OpenGL to use those verticies in memory to draw an object.  This becomes especially useful when you have a lot of reusable things in graphics memory.

