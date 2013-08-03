'''
The :mod:`application` module contains the Application class which builds the game window and starts calling functions in all the modules.
'''
from pyglet.window import Window
import pyglet
import imp
import os

import config
import gameloader 
import renderer
from eventdispatcher import EventDispatcher, event_handler

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480


class Application(object):
    '''
    This class creates a window with an OpenGL context, and contains hooks for components to call to request updates as apart of the 'game loop.'

    :param size: is a tuple representing the default size of the window (width, height).
    :type size: 2-tuple of integers

    :param title: is the title text at the top of the window.
    :type title: str

    :param fullscreen: tells the window to start fullscren or not.
    :type fullscreen: boolean
    '''
    def __init__(self, size=(DEFAULT_WIDTH, DEFAULT_HEIGHT),
            title='MegaMinerAI Bland Title Text', fullscreen=False):
        self.window = Window(width=size[0], height=size[1], caption=title,
                visible=True, fullscreen=fullscreen, resizable=True,
                style=Window.WINDOW_STYLE_DEFAULT, vsync=False, display=None,
                context=None, config=None)
        self.updates = []

        # Set up the event dispatcher
        self.ed = EventDispatcher()
        self.ed.register_class_for_events(self)

        # Build the game loader
        self.loader = gameloader.GameLoader(self.ed)

        #Build the renderer
        self.renderer = renderer.Renderer()
        
        # Request updates
        self.request_update_on_draw(self.renderer.init_frame, 0)
        self.request_update_on_draw(self.renderer.draw_frame, 100)


    @event_handler
    def on_run_gamelog(self, data):
        print('handler')
        game_name = data['gameName'].lower()
        path = os.path.join(config.PLUGIN_DIR, 
                game_name, 'main.py')

        self.game = imp.load_source(game_name, path)
        self.game.load(self, data)

        return True


    def request_update_on_draw(self, procedure, order=50):
        '''
        This method tells the application that whenever a draw occurs for the application, that *procedure* should be called.  

        :param order: specifies when *procedure* should be called.  All procedures with the same *order* will execute in a semi-random fashion after the previous *order* and before the next *order* value in the update queue.  In general, all procedures should be called sometime before the :mod:`renderer`'s update() function is called.  Procedures will be called with *order* from least to greatest.
        :type order: float or integer

        :param procedure: should not expect any arguments or an exception will be thrown.
        :type procedure: function or class method

        Example gameloop::

            >>> app.request_update_on_draw(game.update_objects)
            >>> app.request_update_on_draw(game.do_input_stuff, 10)
            >>> app.request_update_on_draw(game.render_frame, 100)
            >>> app.run()
            'processing user input'
            'updating game objects'
            'rendering frame'
        '''

        self.updates += [(order, procedure)]
        self.updates.sort(key=lambda x: x[0])

    def _update(self, dt):
        '''
        This function is called at the start of every loop in the 'game loop.'

        It calls all the procedures that requested updates in the game loop.
        
        *dt* is the time since the last call.
        '''
        # Forces a redraw
        # Trigger everything

        self.window.clear()

        for order, procedure in self.updates:
            procedure()

    def run(self, glog_list=[]):
        '''
        This method starts the 'game loop.'  It is a blocking function so at this, point all modules should have requested updates from the application or another thread should have been started.
        '''

        self.ed.dispatch_event('on_load_gamelog_file', glog_list)

        pyglet.clock.schedule(self._update)
        pyglet.app.run()
