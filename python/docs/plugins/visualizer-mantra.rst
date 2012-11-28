Vizualizer Mantra
=================

This work shall act as a set of guidelines for plugin design decisions.  It shall also give guidance in the visualizer core on what should be improved such that plugins may more easily achieve the goals set forth by this document.

Purpose of the Visualizer
-------------------------

There are several purposes that could be said that the visualizer holds, but above all the purpose of the visualizer is to convey as much artificial intelligence information in the most accurate, succinct way possible.  Only when this goal is met, should other features and fluff be worked on.  


Other purposes of the visualizer include (but are not limited to):

 * PR fluff for attracting new competitors

 * Tournament bracket visualization

 * Human client for certain games

Should the visualizer be attractive?
------------------------------------

I'll go into this more a little later, but the answer is emphatically, yes!  In order to properly convey information, your visualizer has to have as few distractions as possible.  An ugly visualizer is a distracting visualizer and takes away from giving competitors the ability to easily debug issues with their AI.  Likewise, too many visuals can make the visualizer more attractive, but can also distract the competitor, so a balance between beauty and minimalism must be achieved.


Visualizing Everything
----------------------

Every action that a competitor can issue in their AI through the client must have a visual analogue.  Everything from movements and attacks to talking and additional debugging information, if available.  In almost every game, all of this information, if conveyed at once, would present information overload for the competitor or there simply isn't enough screen real-estate to display it all at once.  What you want to do, then is prioritize each of these things and maybe assign a time percentage associated with it, which approximates how much time you think a competitor will look at this information for a competition.

 ================= ========== ============================
 Attribute/Event   Time Chunk Reasoning
 ================= ========== ============================
 Move                 95%     For this game pathfinding is 
                              pivotal and issues with 
                              pathing is always critical
 ----------------- ---------- ----------------------------
 Attack               90%     Attacks are the secondary
                              mechanic of this game
 ----------------- ---------- ----------------------------
 Talk                 60%     Competitors will probably
                              only display talk 
                              information when crucial.
                              However, they may not always
                              be looking for this info.
 ----------------- ---------- ----------------------------
 Per-unit money       20%     Not overly useful to know
                              individual unit moniez 
                              constantly.  
 ----------------- ---------- ----------------------------
 Total money          80%     Crucial to end-game winnar
 ----------------- ---------- ----------------------------
 Score                80%     Same as above, except
                              includes number of bots
 ----------------- ---------- ----------------------------
 Territory Control    20%     Can be easily seen by just
                              looking at the map, but 
                              takes so little space, no 
                              reason to not show it.
 ----------------- ---------- ----------------------------
 Health                80%    Crucial to determine unit
                              deaths.
 ================= ========== ============================

The above table tells us that we should almost constantly show, in order, moves, attacks, score/total money, and health.  Talk is pretty important but could perhaps be toggle-able.  Territory control is not hugely important, but takes up minimal screen real-estate.  Per-unit money should not be a priority to show on the screen, but should be easily available  when needed.  Maybe we could make it visible when a unit is selected, or perhaps when it's being hovered over.

How To Convey Information
-------------------------

There's a lot of ways we can show information.  You'll have to rely on creativity for a lot of this, but some of the common ways are:

.. glossary::

    A texture 
        For example if there's 4 unit types, you might have 4 textures to differentiate between them easily.  

    A changing bar
        The most common example of this is health.  If a unit's health is depleting, the bar decreases in size.  But that's not the only way.  If there's only one unit type in the game, and such granularity is not needed for health, you could have 4 textures which depict different states of disrepair for the unit.  With that, you've effectively saved some real-estate on a unit that can be used for something else.  You could also depict a falling timer or perhaps a score ceiling with two racing bars.

    Plain text
        Scores are most easily displayed with this, especially if there is no ceiling which competitors are racing to achieve.  Debugging information, units talking, and anything else that would only be confusing if it was depicted in a graphical format. Never use plain text for something that occurs all over the screen and is important.  Health would appear awful as numbers.

    Animations
        Animations should be used for a couple of reasons.  When you're trying to depict the flow of information from one state to another or when you want to draw the competitors eyes to a certain portion of the screen.  If the state of an object is changing and it's not crucial information, it shouldn't be animated.  If you have a game which goes from one game mode to another, then an animation should be used to let the user know that the game mode is changing.  The most obvious and pertinent usage of animation is, of course, objects moving from one position to another.  

    Color
        When you're trying to differentiate between objects (like units between teams) color is especially effective.  If you're trying to save screen real estate, you can use color as a depiction of flow from one state to another.  While not a way to accurately determine an object's state, it can give a general feeling of its state.  A bright color could also appear if a competitor's eyes should be drawn somewhere.

    Particle Systems 
        Can be used to show an important objects state.  An injured mothership might spark bright electricity which will let the competitor easily know that the ship is about to blow.  A subtle particle system can be used to show the interaction between two objects.

 
Inspection is Better Than Inspecting
------------------------------------

Visual inspection is priority. 

What this means is that if there is something important that a competitor can only see by a click or series of clicks, then you need to redesign.  If you have to sacrifice beauty to achieve this, then you should.  The visualizer is a tool, not an emotionally driven experience for the competitor.  All information that a competitor would want to see more than 60% of the time should be displayed in some way (perhaps even notifying them that something has changed, but no specifics, unless further inspection occurs).
