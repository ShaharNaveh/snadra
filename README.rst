======
snadra
======
A metasploit clone, written in Python.

How to install
==============
Use ``pip`` to install your project in the virtual environment.

.. code-block:: none

    $ pip install -e .


This tells pip to find ``setup.py`` in the current directory and install
it in *editable* or *development* mode. Editable mode means that as you
make changes to your local code, you'll only need to re-install if you
change the metadata about the project, such as its dependencies.

You can observe that the project is now installed with ``pip list``.

.. code-block:: none

    Package           Version    Location
    ----------------- ---------- -----------------------------
    colorama          0.4.4
    commonmark        0.9.1
    pip               20.2.4
    prompt-toolkit    3.0.8
    Pygments          2.7.2
    rich              9.1.0
    setuptools        50.3.2
    snadra            0.0.1.dev0 /home/usr/snadra/src
    typing-extensions 3.7.4.3
    wcwidth           0.2.5


TODO
====
1. Add the "help" command.
2. connect to db.
