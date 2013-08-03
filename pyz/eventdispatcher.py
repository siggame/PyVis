from __future__ import print_function
import inspect
import pyglet

EVENTS = [
    'on_load_gamelog_file',
    'on_load_gamelog_str',
    'on_run_gamelog',
    ]

def event_handler(func):
    '''
    Registered the function as an event handler

    :param func: Wrapped function to make an event handler
    :type func: function
    '''
    func.is_event_handler = True
    return func


class EventDispatcher(pyglet.event.EventDispatcher):
    '''
    '''
    def __init__(self):
        for e in EVENTS:
            self.register_event_type(e)

    def register_class_for_events(self, cls):
        '''
        This automatically looks through the class' methods and determines if they are a handler for any of our events.  If they are, then we'll tell them to take input from the event handler.
        '''
        methods = inspect.getmembers(cls, predicate=inspect.ismethod)

        handlers = {}

        for (method_name, method) in methods:
            try:
                if method.is_event_handler:
                    handlers[method_name] = method
                    # h = {method_name: method}
                    # setattr(self, method_name, method)
            except AttributeError:
                pass

        self.push_handlers(**handlers)

    def on_run_gamelog(self, gamelog_data):
        '''
        This event is triggered when a gamelog has finished being decompressed and is ready to be played.  

        :param gamelog_data: Is a JSON string of the gamelog.  This gamelog must have a 'gameName' attribute that specifies which plugin to load.
        :type gamelog_data: string
        '''

    def on_load_gamelog_file(self, gamelog_path):
        '''
        This event is triggered when a compressed (or decompressed) gamelog is sent to be loaded.  It should decompress the gamelog, if possible, then ready it to be loaded.

        :param gamelog: The gamelog file (compressed or decompressed)
        :type gamelog: string to gamelog to be loaded and ran
        ''' 

