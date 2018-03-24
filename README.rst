==========
keystroker
==========

A Python 3 package for sending keystokes to active windows.

Currently, keystroker only supports windows builds (win 7 and higher).


Requirements
============

Python 3.5+ (Lower Python 3 installs may work but are not supported)


Installation
============

To keystroker can be installed via pip use the following command:

.. code-block:: console

    pip install keystroker

Otherwise you can install keystroker through the source code by running the
contained ``setup.py`` within the extracted keystroker source directory:

.. code-block:: console

    python3 setup.py install


Usage
=====

Keystroker can be either used as an Python 3 package using its api to send
keystrokes to a active window, or used as a terminal launched command.


Api Usage
---------

A basic code example of using keystroker to send inputted keystrokes is shown
below:

.. code-block:: python
    :linenos:

    from keystroker.sendkeys import sendkeys


    while True:
        line = input("Please input text to print: ")
        sendkeys(line)
        print("\n")


To get advanced help in using keystroker's api, documentation is present
within the source code.


Command Usage
-------------

To get help in using keystroker's terminal command use the following command:

.. code-block:: console

    keystroker -h

