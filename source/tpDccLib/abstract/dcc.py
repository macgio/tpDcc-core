#! /usr/bin/env python
# # -*- coding: utf-8 -*-

"""
Module that contains abstract definition of basic DCC functions
"""

from __future__ import print_function, division, absolute_import

from tpPyUtils import decorators


class AbstractDCC(object):

    @staticmethod
    @decorators.abstractmethod
    def get_name():
        """
        Returns the name of the DCC
        :return: str
        """

        return ''

    @staticmethod
    @decorators.abstractmethod
    def get_version():
        """
        Returns version of the DCC
        :return: int
        """

        return 0

    @staticmethod
    @decorators.abstractmethod
    def get_main_window():
        """
        Returns Qt object that references to the main DCC window
        :return:
        """

        return None

    @staticmethod
    @decorators.abstractmethod
    def get_dockable_window_class():
        """
        Returns class that should be used to instance an ew dockable DCC window
        :return: class
        """

        try:
            from tpQtLib.widgets import window
            return window.MainWindow
        except Exception:
            pass

        return None

    @staticmethod
    @decorators.abstractmethod
    def get_progress_bar(**kwargs):
        """
        Returns utils class instance that will manage DCC progress bar
        :return: AbstractProgressBar
        """

        from tpDccLib.abstract import progressbar

        return progressbar.AbstractProgressBar(**kwargs)

    @staticmethod
    @decorators.abstractmethod
    def get_progress_bar_class():
        """
        Return class of progress bar
        :return: class
        """

        from tpDccLib.abstract import progressbar

        return progressbar.AbstractProgressBar

    @staticmethod
    @decorators.abstractmethod
    def new_scene(force=True, do_save=True):
        """
        Creates a new DCC scene
        :param force: bool
        :param do_save: bool
        :return:
        """

        return NotImplementedError('New Scene functionality is not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def select_file(caption, filters, start_dir=None):
        """
        Opens a select file dialog with DCC dialog
        :param caption: str, caption of the dialog
        :param filters: str, filter to use
        :param start_dir: str, start directory of the dialog
        :return: str, selected path
        """

        raise NotImplementedError('Select File functionality is not implemented!')
