'''
The renderer is responsible for building the primitives, and complex objects to be drawn by pyglet.  This module also contains various base classes for primitives which can be modified on the fly.  
'''
from copy import copy

from pyglet import clock
from pyglet import gl
from pyglet import graphics


class Primitive(object):
    '''
    This is the base class for any primitive to draw to the screen. To be used most effectively, all library-provided primitives should be declared within :class:`renderer.Renderer`.

    :param renderer: renderer instance to add this primitive to.
    :type renderer: :class:`renderer.Renderer`

    :raises: AttributeError if renderer is not passed to constructor and not instantiated from an instance of a renderer
    '''
    vertex_lists = {}
    def __init__(self, renderer=None):
        if not renderer:
            try:
                renderer = self.renderer
            except AttributeError as e:
                print(
                '''You must either pass in renderer argument to '''
                '''the primitive or use renderer.Primitive()''')
                raise e

        else:
            self.renderer = renderer

class Renderer(object):
    '''
    This class allows access to the primitives (the basic drawing building blocks) to draw just about anything.  Widgets should use these to draw themselves::

        class Button(RectWidget):
            def __init__(self, renderer, x, y, width, height, text):
                btn_base = renderer.Rectangle(x, y, width, height, 
                    color=(0.2, 0.3, 0.2))
                btn_text = renderer.Text(x, y, width, height, text)
                # etc. 
                # etc.

    primitives should be called through the Renderer instance instead of through the class (i.e.)::
        
        renderer = Renderer()
        renderer.Rectangle()

    instead of::
        
        renderer = Renderer()
        Renderer.Rectangle(renderer=renderer)

    There is special python magic to make that work.  See `__init__()` for that.
    '''

    fg_color = (1, 0, 0, 1)
    bg_color = (0, 0, 1, 1)
    texture = None

    def __init__(self):
        self.fps_display = clock.ClockDisplay()
        self.init_frame()
        self.frame = graphics.Batch()

        # -*- WARNING -*-
        # -*- Python magic -*-
        # Luckily this only has to be called once per renderer 
        # and per program there is on average 1.0 renderer
        # (Actually it might be useful to have two of these...)
        # Finds all classes in Renderer that inherit Primitive
        # at some point, and for each, creates a copy for this 
        # instance and sets the renderer attribute for each 
        # to this instance.

        # This is just so we can do stuff like renderer.Rectangle()
        # without having to pass in the renderer because that doesn't
        # make any sense.
        # -*- Python magic -*-
        # -*- WARNING -*-

        for name in dir(self):
            cls = getattr(self, name)
            if hasattr(cls, '__mro__') and Primitive in cls.__mro__:
                setattr(self, name, type(name, (cls,), dict(renderer=self)))


    def init_frame(self):
        '''
        This method should be called at the beginning of every game loop.  
        It does the pre-loop set up, if any.

        :rtype: None
        '''
        pass

    def draw_frame(self):
        '''
        This method should be called at (or near) the end of every game loop after all the objects have been updated and are ready to draw to the screen.

        This will draw the batch associated with the renderer.

        :rtype: None
        '''
        self.frame.draw()
        self.fps_display.draw()


    class Rectangle(Primitive):
        '''
        This class creates a rectangle primitive.  

        :param x: the x offset (from the left side of the screen) to draw the rectangle.
        :type x: float

        :param y: is the y offset (from the bottom of the screen) to draw the rectangle.
        :type y: float

        :param width: is the width of the rectangle
        :type width: float

        :param height: is the height of the rectangle
        :type height: float

        :param texture: is the texture to paint the rectangle with 
        :type texture: 

        :param group: is the group, if any, that the rectangle should be associated with.  Using texture will automatically make this a part of the appropriate TextureGroup and make *group* its parent.
        :type group: Group

        :param color: is the color to paint the rectangle.  If not specified, the renderer's default `fg_color` will be used instead.
        :type color: 3-tuple or 4-tuple of floats from 0 to 1 

        :param filled: specified whether to draw this as a filled-in rectangle or rectangle outline.
        :type filled: boolean
        '''
        def __init__(self, x, y, width, height, texture=None,
                group=None, color=None, filled=True, **kwargs):

            
            super(Renderer.Rectangle, self).__init__(**kwargs)
            
            self.x = self._x = x
            self.y = self._y = y
            self.width = self._width = width
            self.height = self._height = height

            if not color:
                color = self.renderer.fg_color

            data = [('v2f', (x, y, x + width, y,
                     x + width, y + height,
                     x, y + height)),
                ('c4f',
                    (color) * 4)]

            if texture:
                data += [
                    ('t2f',
                        (0, 0,
                         1, 0,
                         1, 1,
                         0, 1))]
                group = graphics.TextureGroup(texture, parent=group)

            if filled:
                # TODO: Change this to gl.GL_TRIANGLE_FAN when pyglet has fixed its
                # allocator issues around TRIANGLE_FANs and LINE_LOOPs
                mode = gl.GL_QUADS
            else:
                mode = gl.GL_LINE_LOOP

            self.vertex_lists['rect'] = self.renderer.frame.add(4, 
                    gl.GL_QUADS, group, *data)


