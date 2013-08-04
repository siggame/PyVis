'''
The renderer is responsible for building the primitives, and complex objects to be drawn by pyglet.  This module also contains various base classes for primitives which can be modified on the fly.
'''
from copy import copy

from pyglet import clock
from pyglet import gl
from pyglet import graphics
import math

class Drawable(object):
    x = property(
        lambda self: self._x,
        lambda self, x: self.transform(translate=(x, self._y)))

    y = property(
        lambda self: self._y,
        lambda self, y: self.transform(translate=(self._x, y)))

    width = property(
        lambda self: self._width,
        lambda self, width: self.transform(scale=(width, self._height))
        )

    height = property(
        lambda self: self._height,
        lambda self, height: self.transform(scale=(self._width, height))
        )

    color = property(
        lambda self: self._color,
        lambda self, color: self.transform(color=color)
        )


class Primitive(Drawable):
    '''
    This is the base class for any primitive to draw to the screen. To be used most effectively, all library-provided primitives should be declared within :class:`renderer.Renderer`.

    :param renderer: renderer instance to add this primitive to.
    :type renderer: :class:`renderer.Renderer`

    :raises: AttributeError if renderer is not passed to constructor and not instantiated from an instance of a renderer
    '''
    def __init__(self, renderer=None, offset=(0, 0)):
        self.off_x, self.off_y = offset
        self.vertex_list = None
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

class Composite(Drawable):
    '''
    This is the base class for any object that uses one or more primitives to function.
    '''
    def __init__(self, renderer):
        self.primitives = []
        self._renderer = renderer

    def transform(self, translate=None, scale=None, rotate=None):
        if scale:
            raise Exception('This needs to be overridden by the composite you'
                'wish to scale.')

        for p in self.primitives:
            p.transform(translate=translate, rotate=rotate)

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

    fg_color = (1, 0.5, 0.5, 1)
    bg_color = (1, 1, 1, 1)
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

    class Arc(Primitive):
        '''
        This class creates an arc primitive for which circles and pies (yum!) can be created.

        :param x: The x offset (from the left side of the screen) to the arc center
        :type x: float

        :param y: The y offset (from the bottom of the screen) to the arc center
        :type y: float

        :param radius: The radius of the arc
        :type radius: float

        :param points: The number of vertices to make up the arc
        :type points: int

        :param start: The starting position of the pie in degrees
        :type start: float

        :param end: The ending position of the pie in degrees
        :type end: float

        :param filled: The arc appears as a pie because it will be filled with color
        :type filled: bool

        :param loop: If not filled, this will set whether the first and last points join at the middle or just an arc is created.
        :type loop: bool

        '''

        def __init__(self, x, y, radius, points=20, texture=None, group=None, color=None,
            filled=True, loop=True, start=0, end=360, **kwargs):
            super(Renderer.Arc, self).__init__(**kwargs)

            self._x, self._y = x, y
            self._radius = radius
            self._points = points
            self._start, self._end = start, end
            self._filled = filled
            self._loop = loop

            if not color:
                color = self.renderer.fg_color

            data = [
                ('v2f', (0,) * points * 2),
                ('c4f', (color) * points)
            ]

            if texture:
                raise Exception('Not Yet Implemented')
            '''
                data += [
                    ('t2f',
                        (0, 0,
                         1, 0,
                         1, 1,
                         0, 1))
                ]
                group = graphics.TextureGroup(texture, parent=group)
            '''

            indices = []
            if filled:
                # TODO: Change this to gl.GL_TRIANGLE_FAN when pyglet has fixed its
                # allocator issues around TRIANGLE_FANs and LINE_LOOPs

                mode = gl.GL_TRIANGLES

                for p in range(points - 1):
                    indices += [0, p, p + 1]
            else:

                for p in range(points - 1):
                    indices += [p, p + 1]

                if loop:
                    indices = [0, 1] + indices + [points - 1, 0]

                mode = gl.GL_LINES


            self.vertex_list = self.renderer.frame.add_indexed(points, mode,
                group, indices, *data)

            self.transform()

        def transform(self, translate=None, scale=None, rotate=None,
                start=None, end=None):
            '''
            This transform method actually modifies the vertex lists to update the positions of the polygons.  This is most efficient when in unit-mode where only one unit is moving at a time.

            This is because at this point very few objects are moving per frame. So all objects that have not moved take up zero cpu time.

            This may not be as efficient when applied to normal, condensed, or liquid mode because far more polygons will be moving at the same time.  It may be better to draw each vertex list separately after having gone through a matrix transformation.

            As a final note, it may be best to move these primitives into a class built in cython so that python doesn't have to deal with all this bullshit processing.

            As an addendum to my final note, it may be sufficient to move this processing to another python process (see multiprocessing), instead of using cython.

            Or just use both.

            :param translate: The new position.
            :type translate: 2-tuple of float or int

            :param scale: The new scale.
            :type scale: 2-tuple of float or int
            '''
            if translate:
                self._x, self._y = translate
            if scale:
                self._radius = scale

            if start:
                self._start = start

            if end:
                self._end = end

            start = math.radians(self._start)
            end = math.radians(self._end)

            if self._filled or self._loop:
                point_count = self._points - 1
            else:
                point_count = self._points

            interval = (end - start) / (point_count - 1)

            points = []

            t = start
            for p in range(point_count):
                x = (self._x + self.off_x) + self._radius * math.cos(t)
                y = (self._y + self.off_y) + self._radius * math.sin(t)
                points += [x, y]
                t += interval

            if self._filled or self._loop:

                if not self._filled and self._start % 360 == self._end % 360:
                    points = points[0:2] + points
                else:
                    points = [self._x + self.off_x, self._y + self.off_y] + points

            self.vertex_list.vertices[:] = points

        radius = property(
            lambda self: self._radius,
            lambda self, radius: self.transform(radius=radius)
            )

        start = property(
            lambda self: self._start,
            lambda self, start: self.transform(start=start)
            )

        end = property(
            lambda self: self._end,
            lambda self, end: self.transform(end=end)
            )


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
        :type filled: bool
        '''
        def __init__(self, x, y, width, height, texture=None,
                group=None, color=None, filled=True, **kwargs):


            super(Renderer.Rectangle, self).__init__(**kwargs)

            self._x, self._y = x, y
            self._width, self._height = width, height

            if not color:
                self._color = self.renderer.fg_color
            else:
                self._color = color

            data = [
                ('v2f', (0,) * 8),
                ('c4f', (self._color) * 4)
            ]

            if texture:
                data += [
                    ('t2f',
                        (0, 0,
                         1, 0,
                         1, 1,
                         0, 1))
                ]
                group = graphics.TextureGroup(texture, parent=group)

            if filled:
                # TODO: Change this to gl.GL_TRIANGLE_FAN when pyglet has fixed its
                # allocator issues around TRIANGLE_FANs and LINE_LOOPs
                mode = gl.GL_TRIANGLES
                indices = [0, 1, 2, 0, 2, 3]
            else:
                mode = gl.GL_LINES
                indices = [0, 1, 1, 2, 2, 3, 3, 0]

            self.vertex_list = self.renderer.frame.add_indexed(4, mode, group,
                indices, *data)

            self.transform()

        def transform(self, translate=None, scale=None, rotate=None, color=None):
            '''
            This transform method actually modifies the vertex lists to update the positions of the polygons.  This is most efficient when in unit-mode where only one unit is moving at a time.

            This is because at this point very few objects are moving per frame. So all objects that have not moved take up zero cpu time.

            This may not be as efficient when applied to normal, condensed, or liquid mode because far more polygons will be moving at the same time.  It may be better to draw each vertex list separately after having gone through a matrix transformation.

            As a final note, it may be best to move these primitives into a class built in cython so that python doesn't have to deal with all this bullshit processing.

            :param translate: The new position.
            :type translate: 2-tuple of float or int

            :param scale: The new scale.
            :type scale: 2-tuple of float or int
            '''

            if color and color != self._color:
                self._color = color
                self.vertex_list.colors[:] = (color) * 4

            if translate:
                self._x, self._y = translate
            if scale:
                self._width, self._height = scale

            x = self._x + self.off_x
            y = self._y + self.off_y
            self.vertex_list.vertices[:] = [
                x, y,
                x + self._width, y,
                x + self._width, y + self._height,
                x, y + self._height
            ]
