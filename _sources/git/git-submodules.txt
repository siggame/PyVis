How Git Submodules Work
=======================

Git submodules are a semi-convenient way to nest git repositories.  PyVis will be using submodules as a way of isolating binary assets (e.g. textures, executables, etc.) from the core development repository.  Keeping binaries away from source code keeps the source code repository quick and easy to manage.

Adding A Submodule
------------------

Adding a submodule is easy::

    git submodule add -b submoduleBranch remote@address:of/submodule.git desired/submodule/path


Cloning a Repository With A Submodule
-------------------------------------

Also easy::

    git clone remote@base:repository.git repo
    cd repo
    git submodule init
    git submodule update

Making Changes in a Submodule
-----------------------------

You can use any git commands that you would in a normal git repo, but they all must occur in the submodule.  

The only thing that is different is that you also have to commit and push the new tip of the submodule for the base repo.  Otherwise, your base repo will still point to the old tip.  (It doesn't have to be the tip.  As long as your submodule is at the commit you want to be checked out with your base repo when you commit it, then you're good.)

.. warning::

    Make sure you always push your submodule or your base repo may point to a commit that doesn't exist for anyone else, but you.
