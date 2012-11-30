How Rendering In Pyglet Works
=============================

Understanding how pyglet draws stuff to the screen may help you determine what and how you should send stuff to pyglet, so here is how pyglet works.

There are several objects in pyglet and they form a drawing hierarchy. 

The Batch
---------
At the tippy top, the most abstracted object is the batch.  The batch contains absolutely zero information pertaining to how to draw things.  The batch consists of a list of groups in an order that is dictated by OrderedGroups and time of insertion (although you should not rely on the latter).

The Group
---------
The group is similar to a batch, except that there is OpenGL state information attached to it.  When you tell a group to draw, it sets its state, tells everything attached to it to draw, then un-sets the state.  Groups can have parents and children so you can have a state-setting hierarchy::

    Batch
     - OrderedGroup(0)
       - TexturedGroup('wooly_willy.png')
         - Wooly Stuff 
       - FoggyGroup
         - TexturedGroup('kittens.png')
           - Textured Stuff
         - NonTextured Stuff
        

So when the 'kittens.png' group is being draw, the OrderedGroup state is set, although probably nothing, the FoggyGroup state is set (which will make all polygons under it appear foggy), and the TexturedGroup state is set (which will apply that texture to all the polygons.  The stuff that groups draw are VertexDomains.

The VertexDomain
----------------
This is an abstraction for an OpenGL Vertex Array. This is the lowest level of the hierarchy as it contains the raw data associated with drawing vertices along with texture coordinates, fog coords, colors, etc. Everything in a VertexDomain must have the same
`OpenGL Drawing Mode <http://www.opengl.org/sdk/docs/man3/xhtml/glDrawArrays.xml>`_ (GL_LINES, GL_POINTS, GL_TRIANGLES, etc.)  This object has zero knowledge of the VertexLists associated with it.

See the :doc:`Supplementary OpenGL Section </opengl/index>` for more info, if you're interested.

The VertexList
--------------
This is not really apart of the hierarchy.  This is a helper class that points to the raw data in the VertexDomain.

A vertex domain may contain several primitives in its vertex array::

    ...AAAABBBBCCCCDDDD...
           ^  ^
           |  |
           ____
            |
    b_vertex_array points to the start and stop of the associated VertexDomain, vertex array.
