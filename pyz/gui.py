'''
The GUI (Graphical User Interface) is responsible for creating/showing buttons/sliders/other stuff the user can interact with/display info.
'''

import renderer
import pyglet
from input import Input

class Event(object):
    def __init__(self, name, **params):
        for key, value in params.iteritems():
            setattr(self, key, value)
        self.type = name


class InputComposite(renderer.Composite):
    '''
    This is the base class for any composite object that takes some form of
    user input.
    '''
    def __init__(self, renderer, input):
        super(InputComposite, self).__init__(renderer)
        self._input = input
        self._children = []

    def mouse_in_area(self, event):
        print event.x, event.y, self._x, self._y, self.width, self.height
        if event.x >= self._x and event.x < self._x + self.width:
            if event.y >= self._y and event.y < self._y + self.height:
                return True
        return False

    def handle_event(self, event):
        '''
        The input handler should be overridden by each subclass.  If a GUI object is a container object, then it should most likely call each of its children to see if they handle the input or not.  If `False` or `None` is returned, then its assumed that it did not use the input and the next logical place is checked.  The first widget that captures the input, should prevent all other widgets from trying to capture the input.
        '''
        return None


class GUI(Input):
    '''

    '''
    def __init__(self, app):
        super(GUI, self).__init__(app)
        self._renderer = app.renderer
        self._children = []

    def add_frame(self):
        frame = self.Frame(self._renderer, self)
        self._children += [frame]
        return frame

    def on_mouse_press(self, x, y, button, modifiers):
        evt = Event('mouse_press', x=x, y=y, button=button,
            modifiers=modifiers)
        self.handle_event(evt)

    def on_mouse_release(self, x, y, button, modifiers):
        evt = Event('mouse_release', x=x, y=y, button=button,
            modifiers=modifiers)
        self.handle_event(evt)

    def on_mouse_move(self, x, y, dx, dy):
        evt = Event('mouse_move', x=x, y=y, dx=dx, dy=dy)
        self.handle_event(evt)

    def handle_event(self, event):
        for child in self._children:
            if child.handle_event(event):
                return True
        return False

    class Frame(InputComposite):
        '''
        The frame object will be a GUI container that will be responsible for drawing/positioning all sub-objects.  When a frame moves, so should all its components.  The GUI should contain a list of all frames and nothing else.  When a mouse action occurs, it should only send events to the frames where the mouse event occurred, thus creating a hierarchy of event passing.::

            Frame
              > Window
                > Button
                > Button
                > Text
            Frame
              > Autohide bar
                > Slider
                > Button

        If a click occurs in the first frame, then a check will occur to see if it happened in the frame's window.  If it did, then a check will occur to see if the click occurred in the window's button, then the other button, and finally the text.  If nothing responded to the event, then the next frame will be checked.

        '''
        def __init__(self, renderer, input):
            super(GUI.Frame, self).__init__(renderer, input)

        def handle_event(self, event):
            '''
            A frame doesn't use input, so just check to see if the kids are OK.
            '''
            for child in self._children:
                if child.handle_event(event):
                    return True

            return False

        def add_child(self, child):
            self._children += [child]

    class Button(InputComposite):
        def __init__(self, renderer, input, x, y, width, height, text,
                color=None):
            super(GUI.Button, self).__init__(renderer, input)

            self._width, self._height = width, height
            self._text = text
            self._x, self._y = x, y

            down_offset = 0.2
            hover_offset = 0.05

            if not color:
                color = renderer.fg_color

            self.up_color = color
            self.down_color = [
                color[0] - down_offset,
                color[1] - down_offset,
                color[2] - down_offset,
                color[3]
            ]
            self.hover_color = [
                color[0] - hover_offset,
                color[1] - hover_offset,
                color[2] - hover_offset,
                color[3]
            ]

            self._color = self.up_color


            self.outline = renderer.Rectangle(0, 0, width, height,
                filled=False, color=renderer.bg_color, offset=(x, y))

            self.push_area = renderer.Rectangle(0, 0, width, height,
                filled=True, color=self.up_color, offset=(x, y))

            x = x + width / 2
            y = y + height / 2

            self.text = pyglet.text.Label(text, x=x, y=y, bold=True,
                anchor_x='center', anchor_y='center', batch=renderer.frame)

            self._state = 'up'
            self._hover = False
            self._active = False

        def handle_event(self, event):
            if self._state == 'up' and event.type == 'mouse_press':
                if self.mouse_in_area(event):
                    self._state = 'down'
                    self.push_area.color = self.down_color
            elif self._state == 'down' and event.type == 'mouse_release':
                self._state = 'up'
                if self.mouse_in_area(event):
                    self.push_area.color = self.hover_color
                else:
                    self.push_area.color = self.up_color
            elif event.type == 'mouse_move':
                if self._state == 'up':
                    if self.mouse_in_area(event):
                        self.push_area.color = self.hover_color
                    else:
                        self.push_area.color = self.up_color
            elif event.type == 'mouse_leave':
                self.push_area.color == self.up_color
                self._state = 'up'

        def transform(self, color=None, translate=None, scale=None):
            if color and color != self._color:
                self._color = color





