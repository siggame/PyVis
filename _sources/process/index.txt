Visualizer Development Process
==============================

This document will serve as the guidelines for writing, testing, and merging code with the core repository for the python visualizer to ensure only quality code is in the main repo.  

Submitting Code Changes
-----------------------

In order to write code, the `siggame visualizer repository <http://github.com/siggame/visualizer>`_ should be forked to your own account.  This forked repo should be where all your changes should take place.  Once you have made a change you feel is worthwhile, you should create a pull-request on github on the siggame repo.  Someone other than yourself should review your changes, make comments, and accept the request if everything checks out. 

Reviewing Code
--------------

Depending on your experience with python and the project, you should only review certain peoples' code.  Less experienced developers should only review more experienced developers' code.  More experienced developers should try to focus on those will little experience.  Occassionally more experienced developers should review each others code to make sure a sense of code consistency is kept throughout the project.  

The coding standard used for this project should follow the guidelines set forth by `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_ unless otherwise noted.  4 spaces should be used for indents and no tabs should be present in the file.  

Common Issues
-------------

When there are mistakes commonly seen in code-reviews, then an official response should be written :doc:`on this page </process/common-guidelines>` for consistency and quick reference by code-reviewers.

The Zen Of Python
-----------------

This should be followed whenever possible::

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
