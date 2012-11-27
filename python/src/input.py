'''
input
'''
import pyglet

class Input(object):
    '''
    input
    '''
    def __init__(self, application):
        self.app = application

        win = self.app.window

        # Get events
        @win.event
        def on_key_press(symbol, modifiers):
            self.on_key_press(symbol, modifiers)

        @win.event
        def on_key_release(symbol, modifiers):
            self.on_key_release(symbol, modifiers)

        @win.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            self.on_mouse_move(x, y, dx, dy)

        @win.event
        def on_mouse_motion(x, y, dx, dy):
            self.on_mouse_move(x, y, dx, dy)

        @win.event
        def on_mouse_enter(x, y):
            self.on_mouse_enter(x, y)

        @win.event
        def on_mouse_leave(x, y):
            self.on_mouse_leave(x, y)

        @win.event
        def on_mouse_press(x, y, button, modifiers):
            self.on_mouse_press(x, y, button, modifiers)

        @win.event
        def on_mouse_release(x, y, button, modifiers):
            self.on_mouse_release(x, y, button, modifiers)

        @win.event
        def on_text(text):
            self.on_text(text)


    def on_key_press(self, symbol, modifiers):
        '''
        docstring
        '''
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_move(self, x, y, dx, dy):
        pass

    def on_mouse_enter(self, x, y):
        pass

    def on_mouse_leave(self, x, y):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_scroll(self, x, y, button, modifiers):
        pass

    def on_text(self, text):
        pass
