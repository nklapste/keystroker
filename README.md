# keystroker
A Python 3 package for sending keystokes to active windows.

Currently, keystroker only supports windows builds (win 7 and higher).


## Requirements
Python 3.5+ (Lower Python 3 installs may work but are not supported)


## Installation
~~To install via pip use the following command:~~

~~`pip install keystroker`~~

Otherwise you can install keystroker through the source code by running the 
following command within the extracted keystroker source directory:

`python3 setup.py install`


## Usage
Keystroker can be either used as an Python 3 package allowing for a api to send 
keystrokes to a active window, or used as a terminal command to the same effect.


### Api Usage
A basic code example of using the keystroker api to send inputted keystrokes is shown below:
```
"""Simple test loop for sending user inputted keys"""

from keystroker.sendkeys import sendkeys

print("Testing SendKeys...")

while True:
    line = input("Please input text to print: ")
    sendkeys(line)
    print("\n")
```

To get advanced help in using keystrokers api, documentation is present within
the source code.


### Command Usage
To get help in using keystroker's terminal command use the following command:

`keystroker -h`

