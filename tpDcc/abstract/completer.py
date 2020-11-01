#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains abstract Dcc completer class
"""

from __future__ import print_function, division, absolute_import

from tpDcc.libs.python import decorators


class AbstractCompleter(object):
    def __init__(self):
        super(AbstractCompleter, self).__init__()

    @staticmethod
    @decorators.abstractmethod
    def get_auto_import():
        pass

    @staticmethod
    @decorators.abstractmethod
    def wrap_dropped_text(namespace, text, event):
        pass
