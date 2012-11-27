Official Resource For Writing Proper Visualizer Code
====================================================


Importing Modules
-----------------

Module imports should all appear at the very top of the file unless there is a good reason not to (e.g. a user selects if he wants OpenGL or DirectX rendering).  

``from module import *`` is never acceptable.  This can cause name conflicts, and makes it more difficult to determine the origin of objects.  For example::
    
    from application import *
    from renderer import *
    from widgets import *

    r = Rectangle()

makes it impossible to determine that Rectangle came from the module, renderer.  This is preferred::

    from application import Application
    from renderer import Renderer, Rectangle
    from widgets import Button

    r = Rectangle()

or::

    import application
    import renderer
    import widgets

    r = renderer.Rectangle()

In these cases, the origin of Rectangle is clearly visible. 

Docstrings
----------

Proper docstrings are required on all public methods (i.e. methods that do not start with a single underscore), and are suggested for usage with all private methods.  These docstrings generate the documentation used by sphinx and are easy-to-read when just reading code.  If someone ever has to look at the source to determine how to use a certain module, then the docstring is not clear enough. 


.. todo:: Write Example Docstrings Here



