#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base implementation for DCC commands executor
"""


from __future__ import print_function, division, absolute_import

from collections import deque

from tpDcc import register


class DccExecutor(object):
    def __init__(self):
        self._undo_stack = deque()
        self._redo_stack = deque()


register.register_class('Executor', DccExecutor)
