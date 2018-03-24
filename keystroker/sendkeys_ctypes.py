#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Sendkeys module moved back to ctypes. For x64 systems, for example.

(c) 2009 Igor S. Mandrigin, Agnitum Ltd.

Updated to Python3 by Nathan Klapstein <nklapste@ualberta.ca>
"""

from ctypes import windll

KEYEVENTF_KEYUP = 2
VK_NUMLOCK = 144
KEYEVENTF_EXTENDEDKEY = 1


def _key_down(vk):
    scan = windll.user32.MapVirtualKeyA(vk, 0)
    windll.user32.keybd_event(vk, scan, 0, 0)


def _key_up(vk):
    scan = windll.user32.MapVirtualKeyA(vk, 0)
    windll.user32.keybd_event(vk, scan, KEYEVENTF_KEYUP, 0)


def toggle_numlock(turn_on: bool) -> int:
    """Turns `NUMLOCK` on or off and returns whether it was originally on
    or off"""
    is_on = windll.user32.GetKeyState(VK_NUMLOCK) & 1

    if is_on != turn_on:
        windll.user32.keybd_event(
            VK_NUMLOCK,
            69,
            KEYEVENTF_EXTENDEDKEY | 0,
            0
        )
        windll.user32.keybd_event(
            VK_NUMLOCK,
            69,
            KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP,
            0
        )

    return is_on


def char2keycode(char: str) -> int:
    """Converts character to virtual key code"""
    vk = windll.user32.VkKeyScanA(ord(char))
    return vk


def key_down(key: int) -> None:
    """Generates a key pressed event

    :param key: a virtual key code
    """
    vk = key
    # XXX exception if >= 256
    _key_down(vk)


def key_up(key: int) -> None:
    """Generates a key released event

    :param key: a virtual key code
    """
    vk = key
    # XXX exception if >= 256
    _key_up(vk)
