#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains core data widgets for tpRigTask
"""

from __future__ import print_function, division, absolute_import

import os
import json

import tpDccLib as tp
from tpPyUtils import path, fileio


from tpDccLib.core import data


class ScriptTypes(object):
    """
    Class that defines different script types supported by DCCs
    """

    Unknown = 'Unknown'
    Python = 'script.python'
    Manifest = 'script.manifest'


class ScriptExtensions(object):
    """
    Class that defines different script extensions supported by DCCs
    """

    Python = 'py'
    Manifest = 'json'


class ScriptData(data.FileData, object):
    """
    Class used to define scripts stored in disk files
    """

    def save(self, lines, comment=None):
        file_path = path.join_path(self.directory, self._get_file_name())
        write_file = fileio.FileWriter(file_path=file_path)
        write_file.write(lines, last_line_empty=False)

        version = fileio.FileVersion(file_path=file_path)
        version.save(comment=comment)

    def set_lines(self, lines):
        self.lines = lines

    def create(self):
        super(ScriptData, self).create()

        file_name = self.get_file()
        if not hasattr(self, 'lines'):
            return

        if self.lines and file_name:
            write = fileio.FileWriter(file_path=file_name)
            write.write(self.lines)


class ScriptManifestData(ScriptData, object):
    """
    Class used to define manifest scripts stored in disk files
    """

    @staticmethod
    def get_data_type():
        return ScriptTypes.Manifest
        # return constants.ScriptLanguages.Manifest

    @staticmethod
    def get_data_extension():
        return ScriptExtensions.Manifest

    @staticmethod
    def get_data_title():
        return 'Scripts Manifest'


class ScriptPythonData(ScriptData, object):
    """
    Class used to define Python scripts stored in disk files
    """

    @staticmethod
    def get_data_type():
        # return constants.ScriptLanguages.Python
        return ScriptTypes.Python

    @staticmethod
    def get_data_extension():
        return ScriptExtensions.Python

    @staticmethod
    def get_data_title():
        return 'Python Script'

    def open(self):
        lines = ''
        return lines


class CustomData(data.FileData, object):
    """
    Class used to define custom data stored in disk files
    """

    def export_data(self, file_path, force=False):
        """
        Save data object to file on disk
        Override for custom export functionality
        :param file_path: str, file path to store the data in disk
        :param force: bool, True to force save if the file already exists (overwrite)
        """

        dir_path = os.path.dirname(file_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        if os.path.isfile(file_path) and not force:
            raise Exception('File "{}" already exists! Enable force saving to override the file.'.format(file_path))

        file_out = open(file_path, 'w')
        json.dump(self, file_out)
        file_out.close()

        tp.logger.debug('Saved {0}: "{1}"'.format(self.__class__.__name__, file_path))

        return file_path

    def export_data_as(self):
        """
        Save data object to file on disk by opening a file dialog to allow the user to specify a file path
        Override for custom export as functionality
        :param file_path: str, file path to store the data in disk
        :param force: bool, True to force save if the file already exists (overwrite)
        """

        from tpQtLib.core import dialog

        file_path_dialog = dialog.SaveFileDialog(parent=self, use_app_browser=False)
        file_path_dialog.set_filters(self.file_filter)
        file_path = file_path_dialog.exec_()
        if not file_path:
            return None
        file_path = file_path[0]
        file_path = self.save(file_path, force=True)

        return file_path

    def import_data(self, file_path=''):
        """
        Loads data object from JSON files
        Override for custom import functionality
        :param file_path: str, file path of file to load
        """

        from tpQtLib.core import dialog

        if not file_path:
            file_path_dialog = dialog.OpenFileDialog(parent=self, use_app_browser=False)
            file_path_dialog.set_filters(self.file_filter)
            file_path = file_path_dialog.exec_()
            if not file_path:
                return None
        else:
            if not os.path.isfile(file_path):
                raise Exception('File "{}" does not exists!'.format(file_path))

        file_in = open(file_path, 'rb')
        data_in = json.load(file_in)
        data_type = data_in.__class__.__name__
        tp.logger.debug('Loaded {0}: "{1}"'.format(data_type, file_path))

        return data_in
