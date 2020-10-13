#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains class that defines DCC libraries
"""

from __future__ import print_function, division, absolute_import

import os

from tpDcc.core import plugin


class DccLibrary(plugin.Plugin, object):
    def __init__(self, manager, config=None, dev=False, *args, **kwargs):
        super(DccLibrary, self).__init__(manager=manager)

        self._config = config
        self._dev = dev

    @property
    def config(self):
        return self._config

    @property
    def dev(self):
        return self._dev

    @classmethod
    def config_dict(cls, file_name=None):
        """
        Returns internal tool configuration dictionary
        :return: dict
        """

        file_name = file_name or ''

        return {
            'name': 'DccLib',
            'id': 'tpDcc-libs-library',
            'supported_dccs': dict(),
            'creator': 'Tomas Poveda',
            'tooltip': '',
            'logger_dir': os.path.join(os.path.expanduser('~'), 'tpDcc', 'logs', 'tools'),
            'logger_level': 'INFO',
            'resources_path': os.path.join(file_name, 'resources'),
            'logging_file': os.path.join(file_name, '__logging__.ini'),
        }
