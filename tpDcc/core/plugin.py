#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains classes to create plugins
"""

from __future__ import print_function, division, absolute_import

import time
import inspect

import tpDcc as tp


class Plugin(object):
    """
    Base class for plugins
    """

    ID = ''
    VERSION = None
    PACKAGE = None

    def __init__(self, manager=None):
        self._manager = manager
        self._stats = PluginStats(self)

    @property
    def manager(self):
        return self._manager

    @property
    def stats(self):
        return self._stats


class PluginStats(object):
    def __init__(self, plugin):
        self._plugin = plugin
        self._id = self._plugin.ID
        self._start_time = 0.0
        self._end_time = 0.0
        self._execution_time = 0.0

        self._info = dict()

        self._init()

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value

    @property
    def execution_time(self):
        return self._execution_time

    def _init(self):
        """
        Internal function that initializes info for the plugin and its environment
        """

        self._info.update({
            'name': self._plugin.__class__.__name__,
            'creator': self._plugin.creator,
            'module': self._plugin.__class__.__module__,
            'filepath': inspect.getfile(self._plugin.__class__),
            'id': self._id,
            'application': tp.Dcc.get_name()
        })

    def start(self):
        """
        Starts the execution of the plugin
        """

        self._start_time = time.time()

    def finish(self, trace=None):
        """
        Function that is called when plugin finishes its execution
        :param trace: str or None
        """

        self._end_time = time.time()
        self._execution_time = self._end_time - self._start_time
        self._info['executionTime'] = self._execution_time
        self._info['lastUsed'] = self._end_time
        if trace:
            self._info['traceback'] = trace
