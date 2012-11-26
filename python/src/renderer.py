'''
The renderer is responsible for building the primitives, and complex objects
to be drawn by pyglet.  This module also contains various base classes for
primitives which can be modified on the fly.  
'''
from pyglet import graphics
from pyglet import gl
from pyglet import clock


class Primitive(object):
    vertex_lists = {}

    def draw(self):
        for i, j in zip(self.vertex_lists, self.modes):
            pass
            # self.renderer.frame.add(4, j, None, *i)


class Rectangle(Primitive):
    def __init__(self, renderer, x, y, width, height, texture=None,
            group=None, color=None):
        self.x = self._x = x
        self.y = self._y = y
        self.width = self._width = width
        self.height = self._height = height

        if not color:
            color = renderer.fg_color

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

        self.vertex_lists['rect'] = renderer.frame.add(4, gl.GL_POLYGONS, group,
                *data)


class Renderer(object):
    '''
    '''

    fg_color = (1, 0, 0, 1)
    bg_color = (0, 0, 1, 1)
    texture = None

    def __init__(self, application):
        '''
        '''
        self.app = application
        self.fps_display = clock.ClockDisplay()
        self.init_frame()
        self.frame = graphics.Batch()


    def init_frame(self):
        pass

    def draw_frame(self):
        self.frame.draw()
        self.fps_display.draw()

    def build_rect(self, x, y, width, height, group=None):
        '''
        '''

        return Rectangle(self, x, y, width, height, group)

