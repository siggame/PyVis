Visualizer Nomenclature
=======================

This document shall have precedence over ANY other document in referring to various elements of the visualizer.  If there is a name-conflict with this document, then it shall be fixed to be in accordance with this document or a motion to have this document amended shall occur. 

Gameplay Modes
--------------

.. glossary::

    Unit-Mode
        This has in the past also been referred to as unit-by-unit mode.  This mode appears in the visualizer as movement occurring from a single object at a time, in the order that commands were sent to the server.  This is useful for debugging unit logic based on the exact state of the game.

    Normal-Mode
        This has in the past also been referred to as turn-by-turn mode.  This mode appears in the visualizer as all objects in a turn moving simultaneously (intelligently or not).  This is useful for showing the flow of an AI on a turn-by-turn basis.

    Condensed-Mode
        This has in the past also been referred to as two-turn-mode.  This mode appears in the visualizer as all objects for two (or more) turns moving simultaneously, having the appearance of a real-time game. This is useful for entertainment purposes and showing the flow of a game to some extent.

    Liquid-Mode
        This mode is a theoretical mode that is a mixture of Unit-Mode and Normal-Mode.  Object movement is lagged to some extent based on when commands occurred, but there is still a fair amount of simultaneous moves occurring.  This mode may be useful for quick debugging by inspection, but still showing the overall flow of the game.
