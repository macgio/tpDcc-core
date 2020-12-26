#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains class that defines DCC libraries
"""

from __future__ import print_function, division, absolute_import

import os


class DccLibrary(object):

    ID = None
    VERSION = '0.0.0'

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
    def load(cls):
        """
        Function that is called when library is discovered by the Library Manager

        NOTE: This function is called during import time, so we should try to reduce as much as possible the amount
        of code that we call here
        :return:
        """

        pass

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

