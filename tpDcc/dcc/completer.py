#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains custom Dcc completer classes
"""

from __future__ import print_function, division, absolute_import

from tpDcc import dcc
from tpDcc.abstract import completer
from tpDcc.libs.python import decorators


class _MetaCompleter(type):

    def __call__(cls, *args, **kwargs):
        if dcc.is_maya():
            from tpDcc.dccs.maya.ui import completer
            return type.__call__(completer.MayaCompleter, *args, **kwargs)
        else:
            return type.__call__(BaseCompleter, *args, **kwargs)


class BaseCompleter(completer.AbstractCompleter):

    @staticmethod
    def get_auto_import():
        return None

    @staticmethod
    def wrap_dropped_text(namespace, text, event):
        return text


@decorators.add_metaclass(_MetaCompleter)
class Completer(completer.AbstractCompleter, object):
    pass
