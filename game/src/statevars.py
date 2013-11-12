#!/usr/bin/env python

"""
Keeps track of game accomplishments, past events, and current state values.  Used for saving and loading the game.
"""

# Todo: Exception handling
# Todo: Logging

import assets

_filename = None
variables = {}

def load(filename=None):
    global variables, _filename

    if filename is None:
        filename = _filename
    variables = assets.getData(filename, False)
    _filename = filename

def save(filename=None):
    global _filename

    if filename is None:
        filename = _filename

    _filename = filename

    assets.saveData(variables, filename)
