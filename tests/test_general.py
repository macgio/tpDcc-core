#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tests for tpDccLib
"""

import pytest

from tpDcc import __version__


def test_version():
    assert __version__.__version__
