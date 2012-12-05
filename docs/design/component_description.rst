Component Description
=====================

This document shall serve as a high-level overview of what each component of 
the visualizer architecture shall be responsible for.

.. image:: overview.svg
    :width: 450 px
    :align: center

UI
--
The UI contains :doc:`Widgets </design/widgets>` which are objects just like in the Timeline. Widgets contain a set of procedures expected in the UI.  The UI should draw all the objects it contains, and send appropriate inputs to the objects.  Individual objects should contain the logic to handle clicks, hovers, drags (not the queen-style), etc.  If no widget responds to the input, the UI should tell the input system it didn't know what to do.

Timeline
--------
The timeline is responsible for telling what to draw, when and under what state. This is the backbone of the visualizer and will be reponsible for presenting information in the most accurate way possible given the desired playback format. Playback formats shall be one of several possible modes:

* Unit Mode - This is a first class citizen of the timeline and should be the easiest to draw.  This should show units moving and performing actions one at a time and should have a properly ordered 1-1 correlation with the commands sent from each client.  Competitors should be spending about 10% of their time in this mode.

* Normal Mode - This mode is where competitors should be spending about 90% of their time in this mode.  While not entirely accurate, the information displayed in this mode should be as accurate as possible given that almost all units will be moving at once.  Objects that do not interact with each other in any way should perform their actions simulaneously.  Objects that interact with each other should be appropriately animated such that the displayed information shows the object state dependence on actions.  

* Condensed Mode - Condensed mode is similar to normal mode except that two turns are animated at the same time instead of just one in normal mode.  This will probably not be used much and should probably be an afterthought.  
  
* Liquid Mode - This is a theoretical mode between unit and normal mode where units begin their movement slightly lagging behind other units showing the order of actions, but not entirely blocking everything else. 

Renderer
--------
The renderer shall contain a set of procedures that Objects can call to get stuff drawn to the screen.  It will automatically look for resources based on the input texture name if it's not already loaded.  It should also deallocate resources it hasn't been using in a while.

Input
-----
This shall look for input events from the user and send them to the appropriate component.  In the initial implementation, this shall be the UI, then the Timeline, if no UI Widget has responded appropriately.

Inputs that should be sent are: 

* Down-button (For Drags)

* Up-button (left, right, and middle)

* Selections (If no down-button was responded too)

* Key presses

* Voice Commands :|

Controller
----------
This shall tell the timeline where it should currently be, and handle a few other general things in the system.  The config module should primarily be used by this.

Networking
----------
Shall support spectating.  More details to follow.

