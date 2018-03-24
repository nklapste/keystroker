#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Functionality definitions for keystroker

See :func:`.sendkeys.sendkeys` for main usage.

Copyright (C) 2003 Ollie Rutherfurd <oliver@rutherfurd.net>

Updated to Python3 by Nathan Klapstein <nklapste@ualberta.ca>
"""

import time
from typing import List, Tuple, Dict

from keystroker.sendkeys_ctypes import char2keycode, key_up, key_down,\
    toggle_numlock

__all__ = ["KeySequenceError", "sendkeys"]

KEYEVENTF_KEYUP = 2
VK_SHIFT = 16
VK_CONTROL = 17
VK_MENU = 18

PAUSE = 50 / 1000.0  # 50 milliseconds

# "codes" recognized as {CODE( repeat)?}
CODES = {
    "BACK": 8,
    "BACKSPACE": 8,
    "BS": 8,
    "BKSP": 8,
    "BREAK": 3,
    "CAP": 20,
    "CAPSLOCK": 20,
    "DEL": 46,
    "DELETE": 46,
    "DOWN": 40,
    "END": 35,
    "ENTER": 13,
    "ESC": 27,
    "HELP": 47,
    "HOME": 36,
    "INS": 45,
    "INSERT": 45,
    "LEFT": 37,
    "LWIN": 91,
    "NUMLOCK": 144,
    "PGDN": 34,
    "PGUP": 33,
    "PRTSC": 44,
    "RIGHT": 39,
    "RMENU": 165,
    "RWIN": 92,
    "SCROLLLOCK": 145,
    "SPACE": 32,
    "TAB": 9,
    "UP": 38,
    "F1": 112,
    "F2": 113,
    "F3": 114,
    "F4": 115,
    "F5": 116,
    "F6": 117,
    "F7": 118,
    "F8": 119,
    "F9": 120,
    "F10": 121,
    "F11": 122,
    "F12": 123,
    "F13": 124,
    "F14": 125,
    "F15": 126,
    "F16": 127,
    "F17": 128,
    "F18": 129,
    "F19": 130,
    "F20": 131,
    "F21": 132,
    "F22": 133,
    "F23": 134,
    "F24": 135,
}

ESCAPE = "+^%~{}[]"
NO_SHIFT = "[]"

SHIFT = {
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
    "_": "-",
    "|": "\\",
    ":": ";",
    '"': "\'",
    "<": ",",
    ">": ".",
    "?": "/",
}

# modifier keys
MODIFIERS = {
    "+": VK_SHIFT,
    "^": VK_CONTROL,
    "%": VK_MENU,
}


class KeySequenceError(Exception):
    """Exception raised when a key sequence string has a syntax error"""

    def __str__(self):
        return " ".join(self.args)


def _append_code(keys: List[Tuple[int, bool]], code: int):
    keys.append((code, True))
    keys.append((code, False))


def _next_char(chars: List[str], error_msg: str = None):
    if error_msg is None:
        error_msg = "expected another character"
    try:
        return chars.pop()
    except IndexError:
        raise KeySequenceError(error_msg)


def _handle_char(c: str, keys: List[Tuple[int, bool]], shift: bool):
    if shift:
        keys.append((MODIFIERS["+"], True))
    _append_code(keys, char2keycode(c))
    if shift:
        keys.append((MODIFIERS["+"], False))


def _release_modifiers(keys: List[Tuple[int, bool]],
                       modifiers: Dict[str, bool]):
    for c in modifiers.keys():
        if modifiers[c]:
            keys.append((MODIFIERS[c], False))
            modifiers[c] = False


def str2keys(key_string: str, with_spaces: bool = False,
             with_tabs: bool = False, with_newlines: bool = False) \
        -> List[Tuple[int, bool]]:
    """Converts `key_string` string to a list of 2-tuples,
    ``(keycode, down)``, which  can be given to :func:`.sendkeys.playkeys`.

    :param key_string: a string of keys

    :param with_spaces: boolean indicating whether to treat spaces as
        ``{SPACE}``. If :obj:`False`, spaces are ignored

    :param with_tabs: boolean indicating whether to treat tabs as ``{TAB}``.
        If :obj:`False`, tabs are ignored

    :param with_newlines: boolean indicating whether to treat newlines as
        ``{ENTER}``. If :obj:`False`, newlines are ignored
    """
    # reading input as a stack
    chars = list(key_string)
    chars.reverse()
    # results
    keys = []
    # for keeping track of whether shift, ctrl, & alt are pressed
    modifiers = {}
    for k in MODIFIERS.keys():
        modifiers[k] = False

    while chars:
        c = chars.pop()

        if c in MODIFIERS.keys():
            keys.append((MODIFIERS[c], True))
            modifiers[c] = True

        # group of chars, for applying a modifier
        elif c == "(":
            while c != ")":
                c = _next_char(chars, "`(` without `)`")
                if c == ")":
                    raise KeySequenceError("expected a character before `)`")

                if c == " " and with_spaces:
                    _handle_char(CODES["SPACE"], keys, False)
                elif c == "\n" and with_newlines:
                    _handle_char(CODES["ENTER"], keys, False)
                elif c == "\t" and with_tabs:
                    _handle_char(CODES["TAB"], keys, False)
                else:
                    # if we need shift for this char and
                    # it's not already pressed
                    shift = (c.isupper() or c in SHIFT.keys()) and\
                            (not modifiers["+"])
                    if c in SHIFT.keys():
                        _handle_char(SHIFT[c], keys, shift)
                    else:
                        _handle_char(c.lower(), keys, shift)
                c = _next_char(chars, "`)` not found")
            _release_modifiers(keys, modifiers)

        # escaped code, modifier, or repeated char
        elif c == "{":
            saw_space = False
            name = [_next_char(chars)]
            arg = ["0"]
            c = _next_char(chars, "`{` without `}`")
            while c != "}":
                if c == " ":
                    saw_space = True
                elif c in ".0123456789" and saw_space:
                    arg.append(c)
                else:
                    name.append(c)
                c = _next_char(chars, "`{` without `}`")
            code = "".join(name)
            arg = float("0" + "".join(arg))
            if code == "PAUSE":
                if not arg:
                    arg = PAUSE
                keys.append((None, arg))
            else:
                # always having 1 here makes logic
                # easier -- we can always loop
                if arg == 0:
                    arg = 1
                for i in range(int(arg)):
                    if code in CODES.keys():
                        _append_code(keys, CODES[code])
                    else:
                        # must be an escaped modifier or a
                        # repeated char at this point
                        if len(code) > 1:
                            raise KeySequenceError("Unknown code: %s" % code)
                        # handling both {e 3} and {+}, {%}, {^}
                        shift = (code in ESCAPE) and (code not in NO_SHIFT)
                        # do shift if we've got an upper case letter
                        shift = shift or code[0].isupper()
                        c = code
                        if not shift:
                            # handle keys in SHIFT (!, @, etc...)
                            if c in SHIFT.keys():
                                c = SHIFT[c]
                                shift = True
                        _handle_char(c.lower(), keys, shift)
            _release_modifiers(keys, modifiers)

        # unexpected ")"
        elif c == ")":
            raise KeySequenceError("`)` should be preceeded by `(`")

        # unexpected "}"
        elif c == "}":
            raise KeySequenceError("`}` should be preceeded by `{`")

        # handling a single character
        else:
            if c == " " and not with_spaces:
                continue
            elif c == "\t" and not with_tabs:
                continue
            elif c == "\n" and not with_newlines:
                continue

            if c in ("~", "\n"):
                _append_code(keys, CODES["ENTER"])
            elif c == " ":
                _append_code(keys, CODES["SPACE"])
            elif c == "\t":
                _append_code(keys, CODES["TAB"])
            else:
                # if we need shift for this char and it"s not already pressed
                shift = (c.isupper() or c in SHIFT.keys()) and\
                        (not modifiers["+"])
                if c in SHIFT.keys():
                    _handle_char(SHIFT[c], keys, shift)
                else:
                    _handle_char(c.lower(), keys, shift)
                _release_modifiers(keys, modifiers)

    _release_modifiers(keys, modifiers)
    return keys


def playkeys(keys: List[Tuple[int, bool]], pause: float = 0.05) -> None:
    """Simulates pressing and releasing one or more keys.

    :param keys: a list of 2-tuples consisting of ``(keycode, down)``
        where ``down`` is :obj:`True` when the key is being pressed
        and :obj:`False` when it's being released

        ``keys`` is returned from :func:`.sendkeys.str2keys`

    :param pause: number of seconds between releasing a key and pressing the
        next one
    """
    for (vk, arg) in keys:
        if vk:
            if arg:
                key_down(vk)
            else:
                key_up(vk)
                if pause:  # pause after key up
                    time.sleep(pause)
        else:
            time.sleep(arg)


def sendkeys(keys: str, pause=0.05, with_spaces: bool = False,
             with_tabs: bool = False, with_newlines: bool = False,
             turn_off_numlock: bool = True) -> None:
    """Sends keys to the current window.

    :param keys: a string of keys

     :param pause: number of seconds to wait between sending each key
        or key combination.

      :param with_spaces: boolean indicating whether to treat spaces as
        ``{SPACE}``. If :obj:`False`, spaces are ignored

    :param with_tabs: boolean indicating whether to treat tabs as ``{TAB}``.
        If :obj:`False`, tabs are ignored

    :param with_newlines: boolean indicating whether to treat newlines as
        ``{ENTER}``. If :obj:`False`, newlines are ignored

    :param turn_off_numlock: boolean indicating whether to turn off
        `NUMLOCK` before sending keys.

    .. example::

        SendKeys("+hello{SPACE}+world+1")

    would result in ``"Hello World!"``
    """
    restore_numlock = False
    try:
        # read keystroke keys into a list of 2 tuples [(key,up),]
        _keys = str2keys(keys, with_spaces, with_tabs, with_newlines)

        # certain keystrokes don't seem to behave the same way if NUMLOCK
        # is on (for example, ^+{LEFT}), so turn NUMLOCK off, if it's on
        # and restore its original state when done.
        if turn_off_numlock:
            restore_numlock = toggle_numlock(False)

        # "play" the keys to the active window
        playkeys(_keys, pause)
    finally:
        if restore_numlock and turn_off_numlock:
            key_down(CODES["NUMLOCK"])
            key_up(CODES["NUMLOCK"])
