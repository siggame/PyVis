Widgets
=======

This document will contain the list of possibly desired widgets for the UI. This will be used to discuss what we really, really want, what would be nice, and what could be postponed or even ignored indefinitely.

.. glossary::

    Windows 
        Contain groups of Widgets 

        Use Cases: Options Dialog, Debugging Window, Save/Open Window

    Buttons 
        Will trigger events to occur when released 

        Use Cases: Pause, Play, Skip, Open Options, Menus, changing modes, Places...

    Text Box 
        Will display text either as a label, description, or otherwise 

        Use Cases: Options Dialog, Tables

    Input Box 
        Allow user to modify a value

        Options dialog...,  Turn input

    Table 
        Shows data in an organized fashion

        Use cases: Debug window for a list of values, Bottom of screen for showing timeline tracks?

    Slider 
        Numeric number modifier 

        Use cases: Turn slider at bottom of screen, speed modifier, numeric options, scrolling up/down or left/right on a window.

    Radio Buttons 
        Could just use slider, I guess

    Toolbar Menu 
        Contains buttons which will allow the user to open new glogs, options, etc.

Things That Are a Must Have
---------------------------

* Open Glog Dialog or something similar

* Some way of intuitively controlling the timeline


Possible Short-Time Fixes
-------------------------

 * Leverage Tkinter for menus, open-file dialogs, and drag n' drop until a non-Tkinter approach is decided upon.  This may have to be the solution we continue to use for dialogs and drag n' drop since it is packaged with python and other solutions may be costly for us (time and packaging).  


