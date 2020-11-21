#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains DCC functionality for standalone applications
"""

from __future__ import print_function, division, absolute_import

import logging

from tpDcc.core import dcc
from tpDcc.libs.python import decorators

LOGGER = logging.getLogger('tpDcc-core')


# =================================================================================================================
# GENERAL
# =================================================================================================================

def get_name():
    """
    Returns the name of the DCC
    :return: str
    """

    return dcc.Dccs.Standalone


def get_extensions():
    """
    Returns supported extensions of the DCC
    :return: list(str)
    """

    return []


def get_version():
    """
    Returns version of the DCC
    :return: int
    """

    return 0


def get_version_name():
    """
    Returns version of the DCC
    :return: str
    """

    return '0.0.0'


def is_batch():
    """
    Returns whether DCC is being executed in batch mode or not
    :return: bool
    """

    return False


def execute_deferred(fn):
    """
    Executes given function in deferred mode
    """

    return fn()


def deferred_function(fn, *args, **kwargs):
    """
    Calls given function with given arguments in a deferred way
    :param fn:
    :param args: list
    :param kwargs: dict
    """

    return fn(*args, **kwargs)


def warning(message):
    """
    Prints a warning message
    :param message: str
    :return:
    """

    LOGGER.warning(message)


def error(message):
    """
    Prints a error message
    :param message: str
    :return:
    """

    LOGGER.error(message)


# =================================================================================================================
# GUI
# =================================================================================================================

def get_dpi(value=1):
    """
    Returns current DPI used by DCC
    :param value: float
    :return: float
    """

    return 1.0


def get_dpi_scale(value):
    """
    Returns current DPI scale used by DCC
    :return: float
    """

    return 1.0


def get_main_window():
    """
    Returns Qt object that references to the main DCC window
    :return:
    """

    return None


def get_main_menubar():
    """
    Returns Qt object that references to the main DCC menubar
    :return:
    """

    return None


# def new_scene(force=True, do_save=True):
#     """
#     Creates a new DCC scene
#     :param force: bool, True if we want to save the scene without any prompt dialog
#     :param do_save: bool, True if you want to save the current scene before creating new scene
#     :return:
#     """
#
#     return None
#
#
# def object_exists(node):
#     """
#     Returns whether given object exists or not
#     :return: bool
#     """
#
#     return False
#
#
# def object_type(node):
#     """
#     Returns type of given object
#     :param node: str
#     :return: str
#     """
#
#     return None
#
#
# def check_object_type(node, node_type, check_sub_types=False):
#     """
#     Returns whether give node is of the given type or not
#     :param node: str
#     :param node_type: str
#     :param check_sub_types: bool
#     :return: bool
#     """
#
#     return False
#
#
# def node_is_empty(node, *args, **kwargs):
#     """
#     Returns whether given node is an empty one.
#     In Maya, an emtpy node is the one that is not referenced, has no child transforms, has no custom attributes
#     and has no connections
#     :param node: str
#     :return: bool
#     """
#
#     return True
#
#
# def node_is_transform(node):
#     """
#     Returns whether or not given node is a transform node
#     :param node: str
#     :return: bool
#     """
#
#     return False
#
#
# def all_scene_objects(full_path=True):
#     """
#     Returns a list with all scene nodes
#     :param full_path: bool
#     :return: list<str>
#     """
#
#     return list()
#
#
# def rename_node(node, new_name, **kwargs):
#     """
#     Renames given node with new given name
#     :param node: str
#     :param new_name: str
#     :return: str
#     """
#
#     return False
#
#
# def rename_transform_shape_nodes(node):
#     """
#     Renames all shape nodes of the given transform node
#     :param node: str
#     """
#
#     return False
#
#
# def show_object(node):
#     """
#     Shows given object
#     :param node: str
#     """
#
#     return False
#
#
# def select_node(node, replace_selection=True, **kwargs):
#     """
#     Selects given object in the current scene
#     :param replace_selection: bool
#     :param node: str
#     """
#
#     return False
#
#
# def select_hierarchy(root=None, add=False):
#     """
#     Selects the hierarchy of the given node
#     If no object is given current selection will be used
#     :param root: str
#     :param add: bool, Whether new selected objects need to be added to current selection or not
#     """
#
#     return False
#
#
# def deselect_node(node):
#     """
#     Deselects given node from current selection
#     :param node: str
#     """
#
#     return False
#
#
# def clear_selection():
#     """
#     Clears current scene selection
#     """
#
#     return False
#
#
# def duplicate_object(node, name='', only_parent=False, return_roots_only=False):
#     """
#     Duplicates given object in current scene
#     :param node: str
#     :param name: str
#     :param only_parent: bool, If True, only given node will be duplicated (ignoring its children)
#     :param return_roots_only: bool, If True, only the root nodes of the new hierarchy will be returned
#     :return: list(str)
#     """
#
#     return False
#
#
# def delete_object(node):
#     """
#     Removes given node from current scene
#     :param node: str
#     """
#
#     return False
#
#
# def clean_construction_history(node):
#     """
#     Removes the construction history of the given node
#     :param node: str
#     """
#
#     return False


def selected_nodes(full_path=True, **kwargs):
    """
    Returns a list of selected nodes
    :param full_path: bool
    :return: list<str>
    """

    return list()


# def selected_nodes_of_type(node_type, full_path=True):
#     """
#     Returns a list of selected nodes of given type
#     :param node_type: str
#     :param full_path: bool
#     :return: list(str)
#     """
#
#     return list()
#
#
# def selected_hilited_nodes(full_path=True):
#     """
#     Returns a list of selected nodes that are hilited for component selection
#     :param full_path: bool
#     :return: list(str)
#     """
#
#     return list()
#
#
# def confirm_dialog(title, message, button=None, cancel_button=None, default_button=None, dismiss_string=None):
#     """
#     Shows DCC confirm dialog
#     :param title:
#     :param message:
#     :param button:
#     :param cancel_button:
#     :param default_button:
#     :param dismiss_string:
#     :return:
#     """
#
#     from tpDcc.libs.qt.widgets import messagebox
#
#     new_buttons = None
#     if button:
#         if python.is_string(button):
#             if button == 'Yes':
#                 new_buttons = QDialogButtonBox.Yes
#             elif button == 'No':
#                 new_buttons = QDialogButtonBox.No
#         elif isinstance(button, (tuple, list)):
#             for i, btn in enumerate(button):
#                 if i == 0:
#                     if btn == 'Yes':
#                         new_buttons = QDialogButtonBox.Yes
#                     elif btn == 'No':
#                         new_buttons = QDialogButtonBox.No
#                 else:
#                     if btn == 'Yes':
#                         new_buttons = new_buttons | QDialogButtonBox.Yes
#                     elif btn == 'No':
#                         new_buttons = new_buttons | QDialogButtonBox.No
#     if new_buttons:
#         buttons = new_buttons
#     else:
#         buttons = button or QDialogButtonBox.Yes | QDialogButtonBox.No
#
#     if cancel_button:
#         if python.is_string(cancel_button):
#             if cancel_button == 'No':
#                 buttons = buttons | QDialogButtonBox.No
#             elif cancel_button == 'Cancel':
#                 buttons = buttons | QDialogButtonBox.Cancel
#         else:
#             buttons = buttons | QDialogButtonBox.Cancel
#
#     return messagebox.MessageBox.question(None, title=title, text=message, buttons=buttons)
#
#
# def warning(message):
#     """
#     Prints a warning message
#     :param message: str
#     :return:
#     """
#
#     print('WARNING: {}'.format(message))
#
#
# def error(message):
#     """
#     Prints a error message
#     :param message: str
#     :return:
#     """
#
#     print('ERROR: {}'.format(message))
#
#
# def get_control_colors():
#     """
#     Returns control colors available in DCC
#     :return: list(float, float, float)
#     """
#
#     return []
#
#
# def get_all_fonts():
#     """
#     Returns all fonts available in DCC
#     :return: list(str)
#     """
#
#     # TODO: We can use Qt to retrieve system fonts
#     return []

# =================================================================================================================
# DECORATORS
# =================================================================================================================

def undo_decorator():
    """
    Returns undo decorator for current DCC
    """

    return decorators.empty_decorator


def repeat_last_decorator(command_name=None):
    """
    Returns repeat last decorator for current DCC
    """

    return decorators.empty_decorator(command_name)


def restore_selection_decorator():
    """
    Returns decorators that selects again the objects that were selected before executing the decorated function
    """

    return decorators.empty_decorator