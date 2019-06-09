#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

        raise NotImplementedError('abstract DCC function get_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_version():
        """
        Returns version of the DCC
        :return: int
        """

        raise NotImplementedError('abstract DCC function get_version() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_batch():
        """
        Returns whether DCC is being executed in batch mode or not
        :return: bool
        """

        raise NotImplementedError('abstract DCC function is_batch() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_main_window():
        """
        Returns Qt object that references to the main DCC window
        :return:
        """

        raise NotImplementedError('abstract DCC function get_main_window() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def execute_deferred(fn):
        """
        Executes given function in deferred mode
        """

        raise NotImplementedError('abstract DCC function execute_deferred() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def object_exists(node):
        """
        Returns whether given object exists or not
        :return: bool
        """

        raise NotImplementedError('abstract DCC function object_exists() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def object_type(node):
        """
        Returns type of given object
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function object_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def check_object_type(node, node_type):
        """
        Returns whether give node is of the given type or not
        :param node: str
        :param node_type: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function check_object_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_type(node):
        """
        Returns node type of given object
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def all_scene_objects(full_path=True):
        """
        Returns a list with all scene nodes
        :param full_path: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function all_scene_objects() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def select_object(node, replace_selection=False, **kwargs):
        """
        Selects given object in the current scene
        :param replace_selection: bool
        :param node: str
        """

        raise NotImplementedError('abstract DCC function select_object() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def clear_selection():
        """
        Clears current scene selection
        """

        raise NotImplementedError('abstract DCC function clear_selection() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def delete_object(node):
        """
        Removes given node from current scene
        :param node: str
        """

        raise NotImplementedError('abstract DCC function delete_object() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def selected_nodes(full_path=True):
        """
        Returns a list of selected nodes
        :param full_path: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function selected_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_short_name(node):
        """
        Returns short name of the given node
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_short_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_namespace(node):
        """
        Returns namespace of the given node
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_namespace() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_parent_namespace(node):
        """
        Returns namespace of the given node parent
        :param node: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_parent_namespace() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_referenced(node):
        """
        Returns whether given node is referenced or not
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_referenced() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_reference_path(node, without_copy_number=False):
        """
        Returns reference path of the referenced node
        :param node: str
        :param without_copy_number: bool
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_reference_path() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_is_loaded(node):
        """
        Returns whether given node is loaded or not
        :param node: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function node_is_loaded() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_children(node, all_hierarchy=True, full_path=True):
        """
        Returns a list of children of the given node
        :param node: str
        :param all_hierarchy: bool
        :param full_path: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function node_children() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_parent(node, full_path=True):
        """
        Returns parent node of the given node
        :param node: str
        :param full_path: bool
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_parent() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_root(node, full_path=True):
        """
        Returns hierarchy root node of the given node
        :param node: str
        :param full_path: bool
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_root() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_parent(node, parent):
        """
        Sets the node parent to the given parent
        :param node: str
        :param parent: str
        """

        raise NotImplementedError('abstract DCC function set_parent() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_nodes(node):
        """
        Returns referenced nodes of the given node
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function node_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def node_filename(node, no_copy_number=True):
        """
        Returns file name of the given node
        :param node: str
        :param no_copy_number: bool
        :return: str
        """

        raise NotImplementedError('abstract DCC function node_filename() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_node_types(type_string):
        """
        List all dependency node types satisfying given classification string
        :param type_string: str
        :return:
        """

        raise NotImplementedError('abstract DCC function list_node_types() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_nodes(node_name=None, node_type=None):
        """
        Returns list of nodes with given types. If no type, all scene nodes will be listed
        :param node_name:
        :param node_type:
        :return:  list<str>
        """

        raise NotImplementedError('abstract DCC function list_nodes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_children(node, all_hierarchy=True, full_path=True, children_type=None):
        """
        Returns a list of children nodes of the given node
        :param node:
        :param all_hierarchy:
        :param full_path:
        :param children_type:
        :return:
        """

        raise NotImplementedError('abstract DCC function list_children() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_relatives(
            node, all_hierarchy=True, full_path=True, relative_type=None, shapes=False, intermediate_shapes=False):
        """
        Returns a list of relative nodes of the given node
        :param node:
        :param all_hierarchy:
        :param full_path:
        :param relative_type:
        :param shapes:
        :param intermediate_shapes:
        :return:
        """

        raise NotImplementedError('abstract DCC function list_relatives() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_shapes(node, full_path=True, intermediate_shapes=False):
        """
        Returns a list of shapes of the given node
        :param node: str
        :param full_path: bool
        :param intermediate_shapes: bool
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_shapes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_children_shapes(node, all_hierarchy=True, full_path=True):
        """
        Returns a list of children shapes of the given node
        :param node:
        :param all_hierarchy:
        :param full_path:
        :return:
        """

        raise NotImplementedError('abstract DCC function list_children_shapes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_materials():
        """
        Returns a list of materials in the current scene
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_materials() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def scene_namespaces():
        """
        Returns all the available namespaces in the current scene
        :return: list(str)
        """

        raise NotImplementedError('abstract DCC function scene_namespaces() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def change_namespace(old_namespace, new_namespace):
        """
        Changes old namespace by a new one
        :param old_namespace: str
        :param new_namespace: str
        """

        raise NotImplementedError('abstract DCC function change_namespace() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def change_filename(node, new_filename):
        """
        Changes filename of a given reference node
        :param node: str
        :param new_filename: str
        """

        raise NotImplementedError('abstract DCC function change_filename() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def import_reference(filename):
        """
        Imports object from reference node filename
        :param filename: str
        """

        raise NotImplementedError('abstract DCC function import_reference() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_attributes(node, **kwargs):
        """
        Returns list of attributes of given node
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_user_attributes(node):
        """
        Returns list of user defined attributes
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_user_attributes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_string_attribute(node, attribute_name, keyable=False):
        """
        Adds a new string attribute into the given node
        :param node: str
        :param attribute_name: str
        :param keyable: bool
        """

        raise NotImplementedError('abstract DCC function add_string_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def attribute_query(node, attribute_name, **kwargs):
        """
        Returns attribute qyer
        :param node: str
        :param attribute_name: str
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC function attribute_query() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def attribute_exists(node, attribute_name):
        """
        Returns whether given attribute exists in given node
        :param node: str
        :param attribute_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function attribute_exists() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_attribute_locked(node, attribute_name):
        """
        Returns whether atribute is locked or not
        :param node: str
        :param attribute_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function is_attribute_locked() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def lock_attribute(node, attribute_name):
        """
        Locks given attribute in given node
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function lock_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def unlock_attribute(node, attribute_name):
        """
        Locks given attribute in given node
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function unlock_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_attribute_value(node, attribute_name):
        """
        Returns the value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :return: variant
        """

        raise NotImplementedError('abstract DCC function get_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_attribute_type(node, attribut_name):
        """
        Returns the type of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :return: variant
        """

        raise NotImplementedError('abstract DCC function get_attribute_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_attribute_by_type(node, attribute_name, attribute_value, attribute_type):
        """
        Sets the value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: variant
        :param attribute_type: str
        """

        raise NotImplementedError('abstract DCC function set_attribute_by_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_numeric_attribute_value(node, attribute_name, attribute_value, clamp=False):
        """
        Sets the integer value of the given attribute in the given node
       :param node: str
        :param attribute_name: str
        :param attribute_value: int
        :param clamp: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function set_numeric_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_integer_attribute_value(node, attribute_name, attribute_value, clamp=False):
        """
        Sets the integer value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: int
        :param clamp: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function set_string_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_float_attribute_value(node, attribute_name, attribute_value, clamp=False):
        """
        Sets the integer value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: int
        :param clamp: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function set_string_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_string_attribute_value(node, attribute_name, attribute_value):
        """
        Sets the string value of the given attribute in the given node
        :param node: str
        :param attribute_name: str
        :param attribute_value: str
        """

        raise NotImplementedError('abstract DCC function set_string_attribute_value() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def delete_attribute(node, attribute_name):
        """
        Deletes given attribute of given node
        :param node: str
        :param attribute_name: str
        """

        raise NotImplementedError('abstract DCC function delete_attribute() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_connections(node, attribute_name):
        """
        List the connections of the given out attribute in given node
        :param node: str
        :param attribute_name: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_connections() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_connections_of_type(node, connection_type):
        """
        Returns a list of connections with the given type in the given node
        :param node: str
        :param connection_type: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_connections_of_type() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_source_destination_connections(node):
        """
        Returns source and destination connections of the given node
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_source_destination_connections() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_source_connections(node):
        """
        Returns source connections of the given node
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_source_connections() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_destination_connections(node):
        """
        Returns source connections of the given node
        :param node: str
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_destination_connections() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def new_file(force=True):
        """
        Creates a new file
        :param force: bool
        """

        raise NotImplementedError('abstract DCC function new_file() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def open_file(file_path, force=True):
        """
        Open file in given path
        :param file_path: str
        :param force: bool
        """

        raise NotImplementedError('abstract DCC function open_file() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_plugin_loaded(plugin_name):
        """
        Return whether given plugin is loaded or not
        :param plugin_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function is_plugin_loaded() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def load_plugin(plugin_path, quiet=True):
        """
        Loads given plugin
        :param plugin_path: str
        :param quiet: bool
        """

        raise NotImplementedError('abstract DCC function load_plugin() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def list_old_plugins():
        """
        Returns a list of old plugins in the current scene
        :return: list<str>
        """

        raise NotImplementedError('abstract DCC function list_old_plugins() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def remove_old_plugin(plugin_name):
        """
        Removes given old plugin from current scene
        :param plugin_name: str
        """

        raise NotImplementedError('abstract DCC function list_old_plugins() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def is_component_mode():
        """
        Returns whether current DCC selection mode is component mode or not
        :return: bool
        """

        raise NotImplementedError('abstract DCC function is_component_mode() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def scene_name():
        """
        Returns the name of the current scene
        :return: str
        """

        raise NotImplementedError('abstract DCC function scene_name() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def scene_is_modified():
        """
        Returns whether current scene has been modified or not since last save
        :return: bool
        """

        raise NotImplementedError('abstract DCC function scene_is_modified() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def save_current_scene(force=True):
        """
        Saves current scene
        :param force: bool
        """

        raise NotImplementedError('abstract DCC function save_current_scene() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def confirm_dialog(title, message, button=None, cancel_button=None, default_button=None, dismiss_string=None):
        """
        Shows DCC confirm dialog
        :param title:
        :param message:
        :param button:
        :param cancel_button:
        :param default_button:
        :param dismiss_string:
        :return:
        """

        raise NotImplementedError('abstract DCC function confirm_dialog() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def warning(message):
        """
        Prints a warning message
        :param message: str
        :return:
        """

        raise NotImplementedError('abstract DCC function warning() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_shelf_menu_item(parent, label, command='', icon=''):
        """
        Adds a new menu item
        :param parent:
        :param label:
        :param command:
        :param icon:
        :return:
        """

        raise NotImplementedError('abstract DCC function add_shelf_menu_item() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_shelf_sub_menu_item(parent, label, icon=''):
        """
        Adds a new sub menu item
        :param parent:
        :param label:
        :param icon:
        :return:
        """

        raise NotImplementedError('abstract DCC function add_shelf_sub_menu_item() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def add_shelf_separator(shelf_name):
        """
        Adds a new separator to the given shelf
        :param shelf_name: str
        """

        raise NotImplementedError('abstract DCC function add_shelf_separator() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def shelf_exists(shelf_name):
        """
        Returns whether given shelf already exists or not
        :param shelf_name: str
        :return: bool
        """

        raise NotImplementedError('abstract DCC function shelf_exists() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def create_shelf(shelf_name, shelf_label=None):
        """
        Creates a new shelf with the given name
        :param shelf_name: str
        :param shelf_label: str
        """

        raise NotImplementedError('abstract DCC function create_shelf() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def delete_shelf(shelf_name):
        """
        Deletes shelf with given name
        :param shelf_name: str
        """

        raise NotImplementedError('abstract DCC function delete_shelf() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def select_file_dialog(title, start_directory=None, pattern=None):
        """
        Shows select file dialog
        :param title: str
        :param start_directory: str
        :param pattern: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function select_file_dialog() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def select_folder_dialog(title, start_directory=None):
        """
        Shows select folder dialog
        :param title: str
        :param start_directory: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function select_folder_dialog() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def save_file_dialog(title, start_directory=None, pattern=None):
        """
        Shows save file dialog
        :param title: str
        :param start_directory: str
        :param pattern: str
        :return: str
        """

        raise NotImplementedError('abstract DCC function save_file_dialog() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_current_frame():
        """
        Returns current frame set in time slider
        :return: int
        """

        raise NotImplementedError('abstract DCC function get_current_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_time_slider_range():
        """
        Return the time range from Maya time slider
        :return: list<int, int>
        """

        raise NotImplementedError('abstract DCC function get_time_slider_range() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def fit_view(animation=True):
        """
        Fits current viewport to current selection
        :param animation: bool, Animated fit is available
        """

        raise NotImplementedError('abstract DCC function fit_view() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def refresh_viewport():
        """
        Refresh current DCC viewport
        """

        raise NotImplementedError('abstract DCC function refresh_viewport() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_key_frame(node, attribute_name, **kwargs):
        """
        Sets keyframe in given attribute in given node
        :param node: str
        :param attribute_name: str
        :param kwargs:
        :return:
        """

        raise NotImplementedError('abstract DCC function set_key_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def copy_key(node, attribute_name, time=None):
        """
        Copy key frame of given node
        :param node: str
        :param attribute_name: str
        :param time: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function copy_key() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def cut_key(node, attribute_name, time=None):
        """
        Cuts key frame of given node
        :param node: str
        :param attribute_name: str
        :param time: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function cut_key() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def paste_key(node, attribute_name, option, time, connect):
        """
        Paste copied key frame
        :param node: str
        :param attribute_name: str
        :param option: str
        :param time: (int, int)
        :param connect: bool
        :return:
        """

        raise NotImplementedError('abstract DCC function paste_key() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def offset_keyframes(node, attribute_name, start_time, end_time, duration):
        """
        Offset given node keyframes
        :param node: str
        :param attribute_name: str
        :param start_time: int
        :param end_time: int
        :param duration: float
        """

        raise NotImplementedError('abstract DCC function offset_keyframes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def find_next_key_frame(node, attribute_name, start_time, end_time):
        """
        Returns next keyframe of the given one
        :param node: str
        :param attribute_name: str
        :param start_time: int
        :param end_time: int
        """

        raise NotImplementedError('abstract DCC function offset_keyframes() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def set_flat_key_frame(self, node, attribute_name, start_time, end_time):
        """
        Sets flat tangent in given keyframe
        :param node: str
        :param attribute_name: str
        :param start_time: int
        :param end_time: int
        """

        raise NotImplementedError('abstract DCC function set_flat_key_frame() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def find_first_key_in_anim_curve(curve):
        """
        Returns first key frame of the given curve
        :param curve: str
        :return: int
        """

        raise NotImplementedError('abstract DCC function find_first_key_in_curve() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def find_last_key_in_anim_curve(curve):
        """
        Returns last key frame of the given curve
        :param curve: str
        :return: int
        """

        raise NotImplementedError('abstract DCC function find_last_key_in_curve() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def copy_anim_curve(curve, start_time, end_time):
        """
        Copies given anim curve
        :param curve: str
        :param start_time: int
        :param end_time: int
        """

        raise NotImplementedError('abstract DCC function copy_anim_curve() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def get_current_model_panel():
        """
        Returns the current model panel name
        :return: str | None
        """

        raise NotImplementedError('abstract DCC function current_model_panel() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def enable_undo():
        """
        Enables undo functionality
        """

        raise NotImplementedError('abstract DCC function enable_undo() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def disable_undo():
        """
        Disables undo functionality
        """

        raise NotImplementedError('abstract DCC function disable_undo() not implemented!')

    @staticmethod
    @decorators.abstractmethod
    def focus(object_to_focus):
        """
        Focus in given object
        :param object_to_focus: str
        """

        raise NotImplementedError('abstract DCC function focus() not implemented!')

    # ================================================================================================================

    @staticmethod
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
    def get_progress_bar(**kwargs):
        """
        Returns utils class instance that will manage DCC progress bar
        :return: AbstractProgressBar
        """

        from tpDccLib.abstract import progressbar

        return progressbar.AbstractProgressBar(**kwargs)

    @staticmethod
    def get_progress_bar_class():
        """
        Return class of progress bar
        :return: class
        """

        from tpDccLib.abstract import progressbar

        return progressbar.AbstractProgressBar
