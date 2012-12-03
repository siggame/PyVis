Official Resource For Writing Proper Visualizer Code
====================================================


Importing Modules
-----------------

Module imports should all appear at the very top of the file unless there is a good reason not to (e.g. a user selects if he wants OpenGL or DirectX rendering (!!NOT A SUPPORTED FEATURE!!) ).  

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

Docstrings should try to follow the following format::
    
    def sum(arg1, arg2, arg3=0):
        '''
        Short one line description of FUNCTIONality (puns are encouraged)

        More detailed description of this function.  
        For docstring maintainability reasons, there is no 80 character limit imposed on these, but logical breaks are encouraged for readability.
        Trying to edit an existing paragraph that wraps at 80 characters, no matter what causes time lost in trying to re-organize everything.
        Your editor should, hopefully word-wrap these. 

        :param arg1: first number to be added with
        :param arg2: second number to add
        :type arg2: int 
        :param arg3: optional third number to add.
        :type arg3: float

        :raises: TypeError if NoneType passed in for arg3

        :rtype: float
        '''
        # function

Variable/Module Organization
----------------------------

Whenever groups of variables are present, their ordering should follow the following rule::

    Variables should be alphabetized when there is no prevailing convention for their order.  
    Otherwise, the existing conventions should be kept. 
    Alphabetize when possible.

The most common example of this is width and height.  While width follows height, alphabetically, the prevailing convention is that we state width before height (probably because they're analogues to x and y coordinates).
So this::

    BORDER_COLOR = (1, 1, 1, 1)
    BORDER_DASHED = True

    ENTRY_ONE = '1'
    ENTRY_TWO = '2'
    ENTRY_THREE = '3'
    ENTRY_FOUR = '4'
    ENTRY_FIVE = '5'

    WINDOW_X = 12
    WINDOW_Y = 15
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480

    XYLOPHONE_SOUND = 'funny'

is preferred to this::

    BORDER_COLOR = (1, 1, 1, 1)
    BORDER_DASHED = True

    ENTRY_FOUR = '4'
    ENTRY_FIVE = '5'
    ENTRY_ONE = '1'
    ENTRY_THREE = '3'
    ENTRY_TWO = '2'

    WINDOW_HEIGHT = 480
    WINDOW_WIDTH = 640
    WINDOW_X = 12
    WINDOW_Y = 15

    XYLOPHONE_SOUND = 'funny'

Likewise, modules should almost always be alphabetized, unless there is a strict ordering needed (hopefully we didn't write that library).

`Online Poll Of This Issue <http://css-tricks.com/poll-results-how-do-you-order-your-css-properties/>`_

List Comprehensions vs Loops
----------------------------

Some of you may be tempted to use a list comprehension to perform the task of a loop because... well, I don't know why.  I've just seen this places and it confuses me.  I'm talking about this::
    
    class Object(object):
        # code
        def print(self):
            print(self.value)

    list_of_objects = [Object(blah), Object(blerg), Object(foo), Object(bar), Object(spam), ... ]

    [i.print() for i in list_of_objects]

instead of::

    for i in list_of_objects:  
        i.print()

Functionally, they complete the same task, but there's reasons not to do the first one.  First of all, it's bad python.  Plain and simple you're over-complicating things.  You're using a list comprehension to do something it wasn't born to do.  List comprehensions are for building lists and they do it pretty quickly.  They are not, however, very good at iterating though items and running code.  That's because when you run a for loop, there's no implied list being built.  I see zero advantages for doing it this way, so don't.  List comprehensions should be used for building lists that are to be used and nothing else.  Use your tab key and build a loop instead.

Commit Messages
---------------

Commit messages should try to follow this model::

    Capitalized, short (50 chars or less) summary

    More detailed explanatory text, if necessary.  Wrap it to about 72
    characters or so.  In some contexts, the first line is treated as the
    subject of an email and the rest of the text as the body.  The blank
    line separating the summary from the body is critical (unless you omit
    the body entirely); tools like rebase can get confused if you run the
    two together.

    Write your commit message in the present tense: "Fix bug" and not "Fixed
    bug."  This convention matches up with commit messages generated by
    commands like git merge and git revert.

    Further paragraphs come after blank lines.

    - Bullet points are okay, too

    - Typically a hyphen or asterisk is used for the bullet, preceded by a
    single space, with blank lines in between, but conventions vary here

    - Use a hanging indent

Taken from http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html

See that post for reasons.

Exceptions
----------

Raising exceptions should occur in Python 3.x fashion::

    raise CustomException('data')

instead of::
    
    raise CustomException, 'data'

This is for stylistic reasons and to become accustomed with the python 3.x format.  Exceptions are classes and should be treated as such.

Print Statements
----------------

The print function is preferred over the print statement.  Since the future of python is 3.x, we should start to accustom ourselves with the new format for when we make the switch.

To use the print function, this must appear at the top of the source file before any other import::

    from __future__ import print_function

Likewise, any language feature which is available in 2.7, but not required until 3.x should use the 3.x format.

You can see these language features by looking for the back-porting notes in this document: http://docs.pythonsprints.com/python3_porting/py-porting.html

