#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base classes to define preferences
"""

from __future__ import print_function, division, absolute_import


class PreferenceInterface(object):
    ID = ''

    def __init__(self, preference):
        self._preference = preference

    @property
    def preference(self):
        return self._preference


class ToolPreference(PreferenceInterface, object):
    ID = 'core_interface'
    _relative_path = 'prefs/global/stylesheet.pref'

    # ============================================================================================================
    # BASE
    # ============================================================================================================

    def default_preferences_path(self):
        """
        Returns path where preferences are located
        :return: str
        """

        return '~/tpDcc_preferences'

    # ============================================================================================================
    # THEME
    # ============================================================================================================

    def current_theme(self):
        """
        Returns current theme of the tool
        :return: str
        """

        return self._preference.find_setting(self._relative_path, root=None, name='current_theme')

    def themes(self):
        """
        Returns all tool themes available
        :return: list(str)
        """

        return self._preference.find_setting(self._relative_path, root=None, name='themes').keys()



