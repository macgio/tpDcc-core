#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base classes to handle options
"""

from __future__ import print_function, division, absolute_import

import tpDcc as tp
from tpDcc.libs.python import settings


class OptionObject(object):
    def __init__(self):
        super(OptionObject, self).__init__()

        self._option_settings = None

    def get_option_file(self):
        """
        Returns options file
        :return: str
        """

        self._setup_options()

        return self._option_settings.get_file()

    def has_options(self):
        """
        Returns whether the current has options or not
        :return: bool
        """

        self._setup_options()

        return self._option_settings.has_settings()

    def has_option(self, name, group=None):
        """
        Returns whether the current object has given option or not
        :param name: str, name of the option
        :param group: variant, str || None, group of the option (optional)
        :return: bool
        """

        self._setup_options()
        if group:
            name = '{}.{}'.format(group, name)
        else:
            name = str(name)

        return self._option_settings.has_setting(name)

    def add_option(self, name, value, group=None, option_type=None):
        """
        Adds a new option to the options file
        :param name: str, name of the option
        :param value: variant, value of the option
        :param group: variant, str || None, group of the option (optional)
        :param option_type: variant, str || None, option type (optional)
        """

        self._setup_options()

        if group:
            name = '{}.{}'.format(group, name)
        else:
            name = str(name)

        if option_type == 'script':
            value = [value, 'script']
        elif option_type == 'dictionary':
            value = [value, 'dictionary']
        elif option_type == 'nonedittext':
            value = [value, 'nonedittext']
        elif option_type == 'directory':
            value = [value, 'directory']
        elif option_type == 'file':
            value = [value, 'file']

        self._option_settings.set(name, value)

    def set_option(self, name, value, group=None):
        """
        Set an option of the option settings file. If the option does not exist, it will be created
        :param name: str, name of the option we want to set
        :param value: variant, value of the option
        :param group: variant, str || None, group of the option (optional)
        """

        if group:
            name = '{}.{}'.format(group, name)
        else:
            name = str(name)

        self._option_settings.set(name, value)

    def get_unformatted_option(self, name, group=None):
        """
        Returns option without format (string format)
        :param name: str, name of the option we want to retrieve
        :param group: variant, str || None, group of the option (optional)
        :return: str
        """

        self._setup_options()
        if group:
            name = '{}.{}'.format(group, name)
        else:
            name = str(name)

        value = self._option_settings.get(name)

        return value

    def get_option(self, name, group=None):
        """
        Returns option by name and group
        :param name: str, name of the option we want to retrieve
        :param group: variant, str || None, group of the option (optional)
        :return: variant
        """

        self._setup_options()

        value = self.get_unformatted_option(name, group)
        if value is None:
            tp.logger.warning(
                'Impossible to access option with proper format from {}'.format(self._option_settings.directory))
            if self.has_option(name, group):
                if group:
                    tp.logger.warning('Could not find option: "{}" in group: "{}"'.format(name, group))
                else:
                    tp.logger.warning('Could not find option: {}'.format(name))

        value = self._format_option_value(value)

        tp.logger.debug('Accessed Option - Option: "{}" | Group: "{}" | Value: "{}"'.format(name, group, value))

        return value

    def get_option_match(self, name, return_first=True):
        """
        Function that tries to find a matching option in all the options
        :param name: str
        :param return_first: bool
        :return: variant
        """

        self._setup_options()
        options_dict = self._option_settings.settings_dict
        found = dict()
        for key in options_dict:
            if key.endswith(name):
                if return_first:
                    value = self._format_option_value(options_dict[key])
                    tp.logger.debug('Accessed - Option: {}, value: {}'.format(name, options_dict[key]))
                    return value
                found[name] = options_dict[key]

        return found

    def get_options(self):
        """
        Returns all options contained in the settings file
        :return: str
        """

        self._setup_options()
        options = list()
        if self._option_settings:
            options = self._option_settings.get_settings()

        return options

    def clear_options(self):
        """
        Clears all the options
        """

        if self._option_settings:
            self._option_settings.clear()

    def _setup_options(self):
        """
        Internal function that initializes option files
        """

        if not self._option_settings:
            self._option_settings = settings.JSONSettings()