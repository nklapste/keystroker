#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""pytests for sendkeys.py"""

import pytest

import platform
from ctypes import windll
from typing import Tuple, List
from unittest.mock import MagicMock

from keystroker.sendkeys import sendkeys, str2keys, playkeys, KeySequenceError

# global check if we are on windows
NOT_WINDOWS = platform.system() != "Windows"

KEY_STRINGS = [
    "a",
    "abc",
    "1",
    "123",
    "abc123",
]

KEY_CODES = [
    [(65, True), (65, False)],
    [(65, True), (65, False), (66, True), (66, False), (67, True), (67, False)],
    [(49, True), (49, False)],
    [(49, True), (49, False), (50, True), (50, False), (51, True), (51, False)],
    [(65, True), (65, False), (66, True), (66, False), (67, True), (67, False), (49, True), (49, False), (50, True), (50, False), (51, True), (51, False)]
]

# List[(key_string, key_code)]
STR2KEYS_TESTS = zip(KEY_STRINGS, KEY_CODES)


@pytest.mark.skipif(NOT_WINDOWS, reason="System is not Windows")
@pytest.mark.parametrize("key_string, expected", STR2KEYS_TESTS)
def test_str2keys(key_string: str, expected):
    """Test str2keys"""
    keys = str2keys(key_string)
    assert keys == expected


BAD_KEY_STRINGS = [
    "(",
    ")",
    "((",
    "()",
    "))",
]


@pytest.mark.skipif(NOT_WINDOWS, reason="System is not Windows")
@pytest.mark.parametrize("key_string", BAD_KEY_STRINGS)
def test_str2keys_fail(key_string: str):
    """Test str2keys with input that should fail"""
    with pytest.raises(KeySequenceError):
        str2keys(key_string)


# TODO maybe have a better mocking method?
windll.user32.keybd_event = MagicMock()
windll.user32.MapVirtualKeyA = MagicMock()


@pytest.mark.skipif(NOT_WINDOWS, reason="System is not Windows")
@pytest.mark.parametrize("keys", KEY_CODES)
def test_playkeys(keys: List[Tuple[int, bool]]):
    """Test playkeys"""
    playkeys(keys)


@pytest.mark.skipif(NOT_WINDOWS, reason="System is not Windows")
@pytest.mark.parametrize("key_string", KEY_STRINGS)
def test_sendkeys(key_string: str):
    """Test sendkeys"""
    sendkeys(key_string)
