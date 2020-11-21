#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation for DCC tools
"""

from __future__ import print_function, division, absolute_import

import os
import logging
import inspect
from collections import OrderedDict

from tpDcc import dcc
from tpDcc.core import tool
from tpDcc.managers import plugins, configs, resources
from tpDcc.libs.python import decorators, python, path as path_utils
from tpDcc.libs.qt.core import contexts

import pkgutil
if python.is_python2():
    import pkgutil as loader
else:
    import importlib.util
    import importlib as loader

LOGGER = logging.getLogger('tpDcc-core')


@decorators.add_metaclass(decorators.Singleton)
class ToolsManager(plugins.PluginsManager, object):
    def __init__(self):
        super(ToolsManager, self).__init__(interface=tool.DccTool)

        self._layout = dict()
        self._loaded_tools = dict()
        self._tools_to_load = OrderedDict()
        self._hub_tools = list()

    # ============================================================================================================
    # BASE
    # ============================================================================================================

    def load_plugin(self, pkg_name, pkg_loaders, environment, root_pkg_name=None, config_dict=None, load=True):
        """
        Implements load_plugin function
        Registers a plugin instance to the manager
        :param pkg_name: str
        :param pkg_loaders: plugin instance to register
        :param environment:
        :param root_pkg_name:
        :param config_dict:
        :param load:
        :return: Plugin
        """

        if not pkg_loaders:
            return False

        package_loader = pkg_loaders[0] if isinstance(pkg_loaders, (list, tuple)) else pkg_loaders
        if not package_loader:
            return False

        if hasattr(package_loader, 'loader'):
            if not package_loader.loader:
                return False

        plugin_path = package_loader.filename if python.is_python2() else os.path.dirname(package_loader.loader.path)
        plugin_name = package_loader.fullname if python.is_python2() else package_loader.loader.name

        if not config_dict:
            config_dict = dict()

        local = os.getenv('APPDATA') or os.getenv('HOME')

        config_dict.update({
            'join': os.path.join,
            'user': os.path.expanduser('~'),
            'filename': plugin_path,
            'fullname': plugin_name,
            'root': path_utils.clean_path(plugin_path),
            'local': local,
            'home': local
        })

        if pkg_name not in self._plugins:
            self._plugins[pkg_name] = dict()

        tools_found = list()
        version_found = None
        packages_to_walk = [plugin_path] if python.is_python2() else [os.path.dirname(plugin_path)]
        for sub_module in pkgutil.walk_packages(packages_to_walk):
            importer, sub_module_name, _ = sub_module
            qname = '{}.{}'.format(plugin_name, sub_module_name)
            try:
                mod = importer.find_module(sub_module_name).load_module(sub_module_name)
            except Exception:
                # LOGGER.exception('Impossible to register plugin: "{}"'.format(plugin_path))
                continue

            if qname.endswith('__version__') and hasattr(mod, '__version__'):
                if version_found:
                    LOGGER.warning('Already found version: "{}" for "{}"'.format(version_found, plugin_name))
                else:
                    version_found = getattr(mod, '__version__')

            mod.LOADED = load

            for cname, obj in inspect.getmembers(mod, inspect.isclass):
                for interface in self._interfaces:
                    if issubclass(obj, interface):
                        tool_config_dict = obj.config_dict(file_name=plugin_path) or dict()
                        if not tool_config_dict:
                            continue
                        tool_id = tool_config_dict.get('id', None)
                        tool_config_name = tool_config_dict.get('name', None)
                        # tool_icon = tool_config_dict.get('icon', None)
                        if not tool_id:
                            LOGGER.warning(
                                'Impossible to register tool "{}" because its ID is not defined!'.format(tool_id))
                            continue
                        if not tool_config_name:
                            LOGGER.warning(
                                'Impossible to register tool "{}" because its name is not defined!'.format(
                                    tool_config_name))
                            continue
                        if root_pkg_name and root_pkg_name in self._plugins and tool_id in self._plugins[root_pkg_name]:
                            LOGGER.warning(
                                'Impossible to register tool "{}" because its ID "{}" its already defined!'.format(
                                    tool_config_name, tool_id))
                            continue

                        if not version_found:
                            version_found = '0.0.0'
                        obj.VERSION = version_found
                        obj.FILE_NAME = plugin_path
                        obj.FULL_NAME = plugin_name

                        tools_found.append((qname, version_found, obj))
                        version_found = True
                        break

        if not tools_found:
            LOGGER.warning('No tools found in module "{}". Skipping ...'.format(plugin_path))
            return False
        if len(tools_found) > 1:
            LOGGER.warning(
                'Multiple tools found ({}) in module "{}". Loading first one. {} ...'.format(
                    len(tools_found), plugin_path, tools_found[-1]))
            tool_found = tools_found[-1]
        else:
            tool_found = tools_found[0]
        tool_loader = loader.find_loader(tool_found[0])

        # Check if DCC specific implementation for plugin exists
        dcc_path = '{}.dccs.{}'.format(plugin_name, dcc.get_name())
        dcc_loader = None
        dcc_config = None
        try:
            dcc_loader = loader.find_loader(dcc_path)
        except ImportError:
            pass

        tool_config_dict = tool_found[2].config_dict(file_name=plugin_path) or dict()
        tool_id = tool_config_dict['id']
        _tool_name = tool_config_dict['name']
        tool_icon = tool_config_dict['icon']

        tool_config_name = plugin_name.replace('.', '-')
        tool_config = configs.get_config(
            config_name=tool_config_name, package_name=pkg_name, root_package_name=root_pkg_name,
            environment=environment, config_dict=config_dict, extra_data=tool_config_dict)

        if dcc_loader:
            dcc_path = dcc_loader.fullname
            dcc_config = configs.get_config(
                config_name=dcc_path.replace('.', '-'), package_name=pkg_name,
                environment=environment, config_dict=config_dict)
            if not dcc_config.get_path():
                dcc_config = None

        # Register resources
        def_resources_path = os.path.join(plugin_path, 'resources')
        # resources_path = plugin_config.data.get('resources_path', def_resources_path)
        resources_path = tool_config_dict.get('resources_path', None)
        if not resources_path or not os.path.isdir(resources_path):
            resources_path = def_resources_path
        if os.path.isdir(resources_path):
            resources.register_resource(resources_path, key='tools')
        else:
            pass
            # tp.logger.debug('No resources directory found for plugin "{}" ...'.format(_plugin_name))

        # Register DCC specific resources
        if dcc_loader and dcc_config:
            def_resources_path = os.path.join(dcc_loader.filename, 'resources')
            resources_path = dcc_config.data.get('resources_path', def_resources_path)
            if not resources_path or not os.path.isdir(resources_path):
                resources_path = def_resources_path
            if os.path.isdir(resources_path):
                resources.register_resource(resources_path, key='plugins')
            else:
                pass
                # tp.logger.debug('No resources directory found for plugin "{}" ...'.format(_plugin_name))

        # Create tool loggers directory
        default_logger_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'tpDcc', 'logs', 'tools'))
        default_logging_config = os.path.join(plugin_path, '__logging__.ini')
        logger_dir = tool_config_dict.get('logger_dir', default_logger_dir)
        if not os.path.isdir(logger_dir):
            os.makedirs(logger_dir)
        logging_file = tool_config_dict.get('logging_file', default_logging_config)

        tool_package = plugin_name
        tool_package_path = plugin_path
        dcc_package = None
        dcc_package_path = None
        if dcc_loader:
            dcc_package = dcc_loader.fullname if python.is_python2() else dcc_loader.loader.path
            dcc_package_path = dcc_loader.filename if python.is_python2() else dcc_loader.loader.name

        self._plugins[pkg_name][tool_id] = {
            'name': _tool_name,
            'icon': tool_icon,
            'package_name': pkg_name,
            'loader': package_loader,
            'config': tool_config,
            'config_dict': tool_config_dict,
            'plugin_loader': tool_loader,
            'plugin_package': tool_package,
            'plugin_package_path': tool_package_path,
            'version': tool_found[1] if tool_found[1] is not None else "0.0.0",
            'dcc_loader': dcc_loader,
            'dcc_package': dcc_package,
            'dcc_package_path': dcc_package_path,
            'dcc_config': dcc_config,
            'logging_file': logging_file,
            'plugin_instance': None
        }

        LOGGER.info('Tool "{}" registered successfully!'.format(plugin_name))

        return True

    def get_tool_settings_file_path(self, tool_id):
        """
        Returns the path where tool settings file is located
        :param tool_id:
        :return: str
        """

        settings_path = path_utils.get_user_data_dir(appname=tool_id)
        settings_file = path_utils.clean_path(os.path.expandvars(os.path.join(settings_path, 'settings.cfg')))

        return settings_file

    def get_tool_settings_file(self, tool_id):
        """
        Returns the settings file of the given tool
        :param tool_id: str
        :return: settings.QtSettings
        """

        from tpDcc.libs.qt.core import settings

        settings_file = self.get_tool_settings_file_path(tool_id)

        return settings.QtSettings(filename=settings_file)

    def get_tool_data_from_id(self, tool_id, package_name=None):
        """
        Returns registered plugin data from its id
        :param tool_id: str
        :param package_name: str
        :return: dict
        """

        if not tool_id:
            return None

        if not package_name:
            package_name = tool_id.replace('.', '-').split('-')[0]

        if package_name and package_name not in self._plugins:
            LOGGER.error('Impossible to retrieve data from id: {} package "{}" not registered!'.format(
                tool_id, package_name))
            return None

        return self._plugins[package_name][tool_id] if tool_id in self._plugins[package_name] else None

    def cleanup(self):
        """
        Cleanup all loaded tools
        :return:
        """

        from tpDcc.managers import menus

        LOGGER.info('Cleaning tools ...')
        for plug_name, plug in self._plugins.items():
            plug.cleanup()
            LOGGER.info('Shutting down tool: {}'.format(plug.ID))
            # plugin_id = plug.keys()[0]
            self._plugins.pop(plug_name)

        self._plugins = dict()
        for package_name in self._plugins.keys():
            menus.remove_previous_menus(package_name=package_name)

    # ============================================================================================================
    # TOOLS
    # ============================================================================================================

    def register_package_tools(self, pkg_name, root_pkg_name=None, tools_to_register=None, dev=True, config_dict=None):
        """
        Registers all tools available in given package
        """

        environment = 'development' if dev else 'production'

        if not tools_to_register:
            return
        tools_to_register = python.force_list(tools_to_register)

        if config_dict is None:
            config_dict = dict()

        tools_path = '{}.tools.{}'
        for tool_name in tools_to_register:
            pkg_path = tools_path.format(pkg_name, tool_name)
            if python.is_python2():
                pkg_loader = loader.find_loader(pkg_path)
            else:
                pkg_loader = importlib.util.find_spec(pkg_path)
            if not pkg_loader:
                # if tool_name in self._tools_to_load:
                #     self._tools_to_load.pop(tool_name)
                continue
            else:
                tool_data = {
                    'loaders': pkg_loader,
                    'pkg_name': pkg_name,
                    'root_pkg_name': root_pkg_name,
                    'environment': environment,
                    'config_dict': config_dict
                }
                self._tools_to_load[tool_name] = tool_data

        return self._tools_to_load

    def load_registered_tools(self, package_name):
        """
        Load all tools that were already registered
        :return:
        """
        if not self._tools_to_load:
            LOGGER.warning('No tools to register found!')
            return

        for tool_name, tool_data in self._tools_to_load.items():
            pkg_name = tool_data['pkg_name']
            if pkg_name != package_name:
                continue
            root_pkg_name = tool_data['root_pkg_name']
            pkg_loaders = tool_data['loaders']
            environment = tool_data['environment']
            config_dict = tool_data['config_dict']

            self.load_plugin(
                pkg_name=pkg_name, root_pkg_name=root_pkg_name, pkg_loaders=pkg_loaders, environment=environment,
                load=True, config_dict=config_dict)

    def get_registered_tools(self, package_name=None):
        """
        Returns all registered tools
        :param package_name: str or None
        :return: list
        """

        if not self._plugins:
            return None

        if package_name and package_name not in self._plugins:
            LOGGER.error('Impossible to retrieve data from instance: package "{}" not registered!'.format(package_name))
            return None

        if package_name:
            return self._plugins[package_name]
        else:
            all_tools = dict()
            for package_name, package_data in self._plugins.items():
                for tool_name, tool_data in package_data.items():
                    all_tools[tool_name] = tool_data

            return all_tools

    def get_package_tools(self, package_name):
        """
        Returns all tools of the given package
        :param package_name: str
        :return: list
        """

        if not package_name:
            LOGGER.error('Impossible to retrieve data from plugin with undefined package!')
            return None

        if package_name not in self._plugins:
            LOGGER.error('Impossible to retrieve data from instance: package "{}" not registered!'.format(package_name))
            return None

        package_tools = self.get_registered_tools(package_name=package_name)

        return package_tools

    def get_tool_by_plugin_instance(self, plugin, package_name=None):
        """
        Returns tool instance by given plugin instance
        :param plugin:
        :param package_name: str
        :return:
        """

        if not package_name:
            package_name = plugin.PACKAGE if hasattr(plugins, 'PACKAGE') else None
        if not package_name:
            LOGGER.error('Impossible to retrieve data from plugin with undefined package!')
            return None

        if package_name not in self._plugins:
            LOGGER.error(
                'Impossible to retrieve data from instance: package "{}" not registered!'.format(package_name))
            return None

        if hasattr(plugin, 'ID'):
            return self.get_tool_by_id(tool_id=plugin.ID, package_name=plugin.PACKAGE)

        return None

    def get_tool_by_id(self, tool_id, package_name=None, dev=False, *args, **kwargs):
        """
        Launches tool of a specific package by its ID
        :param tool_id: str, tool ID
        :param package_name: str, str
        :param dev: bool
        :param args: tuple, arguments to pass to the tool execute function
        :param kwargs: dict, keyword arguments to pas to the tool execute function
        :return: DccTool or None, executed tool instance
        """

        if not package_name:
            package_name = tool_id.replace('.', '-').split('-')[0]

        if package_name not in self._plugins:
            LOGGER.warning('Impossible to load tool by id: package "{}" is not registered!'.format(package_name))
            return None

        if tool_id in self._plugins[package_name]:
            tool_inst = self._plugins[package_name][tool_id].get('tool_instance', None)
            if tool_inst:
                return tool_inst

        tool_to_run = None

        for plugin_id in self._plugins[package_name].keys():
            tool_path = self._plugins[package_name][plugin_id]['plugin_package']
            sec_path = tool_path.replace('.', '-')
            if sec_path == tool_path or sec_path == tool_id:
                tool_to_run = tool_id
                break
            else:
                tool_name = tool_path.split('.')[-1]
                if tool_name == tool_path:
                    tool_to_run = tool_id
                    break

        if not tool_to_run or tool_to_run not in self._plugins[package_name]:
            LOGGER.warning('Tool "{}" is not registered!'.format(tool_id))
            return None

        tool_loader = self._plugins[package_name][tool_to_run]['loader']
        pkg_loader = self._plugins[package_name][tool_to_run]['loader']
        tool_config = self._plugins[package_name][tool_to_run]['config']
        tool_fullname = tool_loader.fullname if python.is_python2() else tool_loader.loader.name
        tool_version = self._plugins[package_name][tool_to_run]['version']

        pkg_name = pkg_loader.filename if python.is_python2() else os.path.dirname(pkg_loader.loader.path)
        pkg_path = pkg_loader.fullname if python.is_python2() else pkg_loader.loader.name

        tool_found = None
        for sub_module in pkgutil.walk_packages([self._plugins[package_name][tool_to_run]['plugin_package_path']]):
            tool_importer, sub_module_name, _ = sub_module
            mod = tool_importer.find_module(sub_module_name).load_module(sub_module_name)
            for cname, obj in inspect.getmembers(mod, inspect.isclass):
                if issubclass(obj, tool.DccTool):
                    obj.FILE_NAME = pkg_name
                    obj.FULL_NAME = pkg_path
                    tool_found = obj
                    break
            if tool_found:
                break

        if not tool_found:
            LOGGER.error("Error while launching tool: {}".format(tool_fullname))
            return None

        # if dcc_loader:
        #     tool_config = dcc_config

        tool_settings = self.get_tool_settings_file(tool_id)
        if not tool_settings.has_setting('theme'):
            tool_settings.set('theme', 'default')
        tool_settings.setFallbacksEnabled(False)

        tool_inst = tool_found(self, config=tool_config, settings=tool_settings, dev=dev, *args, **kwargs)
        tool_inst.ID = tool_id
        tool_inst.VERSION = tool_version
        tool_inst.AUTHOR = tool_inst.config_dict().get('creator', None)
        tool_inst.PACKAGE = package_name

        self._plugins[package_name][tool_id]['tool_instance'] = tool_inst
        # self._plugins[package_name][plugin_id]['tool_instance'] = tool_inst

        return tool_inst

    def launch_tool_by_id(self, tool_id, package_name=None, dev=False, *args, **kwargs):
        """
        Launches tool of a specific package by its ID
        :param tool_id: str, tool ID
        :param package_name: str, str
        :param dev: bool
        :param args: tuple, arguments to pass to the tool execute function
        :param kwargs: dict, keyword arguments to pas to the tool execute function
        :return: DccTool or None, executed tool instance
        """

        tool_inst = self.get_tool_by_id(
            tool_id=tool_id, package_name=package_name, dev=dev, *args, **kwargs)
        if not tool_inst:
            return None

        hub = kwargs.pop('hub', False)
        if hub and tool_id != 'tpDcc-tools-hub':
            hub_ui = self.get_last_focused_hub_ui(include_minimized=False)
            if hub_ui:
                hub_ui.toggle_toolset(tool_id)
                return tool_inst
            else:
                LOGGER.warning('No HubUI tool opened. Opening tool using standard method ...')

        self.close_tool(tool_id)
        with contexts.application():
            self._launch_tool(tool_inst, tool_id, *args, **kwargs)
            return tool_inst

    def close_tool(self, tool_id, force=True):
        """
        Closes tool with given ID
        :param tool_id: str
        """

        if tool_id not in self._loaded_tools:
            return False

        closed_tool = False
        parent = dcc.get_main_window()
        if parent:
            for child in parent.children():
                if child.objectName() == tool_id:
                    child.fade_close() if hasattr(child, 'fade_close') else child.close()
                    closed_tool = True

        tool_to_close = self._loaded_tools[tool_id].attacher
        try:
            if not closed_tool and tool_to_close:
                tool_to_close.fade_close() if hasattr(tool_to_close, 'fade_close') else tool_to_close.close()
            if force and tool_to_close:
                tool_to_close.setParent(None)
                tool_to_close.deleteLater()
        except RuntimeError:
            pass
        self._loaded_tools.pop(tool_id)

        return True

    def close_tools(self):
        """
        Closes all available tools
        :return:
        """

        for tool_id in self._loaded_tools.keys():
            self.close_tool(tool_id, force=True)

    def _launch_tool(self, tool_inst, tool_id, *args, **kwargs):
        """
        Launches given tool class
        :param tool_inst: cls, DccTool instance
        :param args: tuple, arguments to pass to tool execute function
        :param kwargs: dict, keyword arguments to pass to the tool execute function
        :return: DccTool or None, executed tool instance
        """

        if tool_id == 'tpDcc-tools-hub':
            tool_data = tool_inst._launch(*args, **kwargs)
            tool_ui = tool_data['tool']
            self._hub_tools.append(tool_ui)
        else:
            self.close_tool(tool_id)
            tool_inst._launch(*args, **kwargs)
            self._loaded_tools[tool_id] = tool_inst

        LOGGER.debug('Execution time: {}'.format(tool_inst.stats.execution_time))

        return tool_inst

    # ============================================================================================================
    # HUB
    # ============================================================================================================

    def close_hub_ui(self, hub_ui_inst):
        if hub_ui_inst in self._hub_tools:
            self._hub_tools.remove(hub_ui_inst)
            LOGGER.debug('Close tpDcc Hub UI: {}'.format(hub_ui_inst))

    def get_hub_uis(self):
        return self._hub_tools

    def get_last_focused_hub_ui(self, include_minimized=True):
        """
        Returns last focused Hub UI
        :param include_minimized: bool, Whether or not take into consideration Hub UIs that are minimized
        :return: HubUI
        """

        hub_ui_found = None
        max_time = 0

        all_hub_uis = self.get_hub_uis()
        for ui in all_hub_uis:
            if ui.isVisible() and ui.last_focused_time > max_time:
                if (not include_minimized and not ui.isMinimized()) or include_minimized:
                    hub_ui_found = ui
                    max_time = ui.last_focused_time

        return hub_ui_found

    def get_last_opened_hub_ui(self):
        """
        Returns last opened Hub UI
        :return: HubUI
        """

        hub_ui_found = None

        all_hub_uis = self.get_hub_uis()
        for ui in all_hub_uis:
            if ui.isVisible():
                hub_ui_found = ui

        return hub_ui_found

    # ============================================================================================================
    # CONFIGS
    # ============================================================================================================

    def get_tool_config(self, tool_id, package_name=None):
        """
        Returns config applied to given tool
        :param tool_id: str
        :param package_name: str
        :return: Theme
        """

        if not package_name:
            package_name = tool_id.replace('.', '-').split('-')[0]

        if package_name not in self._plugins:
            LOGGER.warning(
                'Impossible to retrieve tool config for "{}" in package "{}"! Package not registered.'.format(
                    tool_id, package_name))
            return None

        if tool_id not in self._plugins[package_name]:
            LOGGER.warning(
                'Impossible to retrieve tool config for "{}" in package "{}"! Tool not found'.format(
                    tool_id, package_name))
            return None

        config = self._plugins[package_name][tool_id].get('config', None)

        return config

    # ============================================================================================================
    # THEMES
    # ============================================================================================================

    def get_tool_theme(self, tool_id, package_name=None):
        """
        Returns theme applied to given tool
        :param tool_id: str
        :param package_name: str
        :return: Theme
        """

        found_tool = self.get_tool_by_id(tool_id, package_name=package_name)
        if not found_tool:
            return None

        theme_name = found_tool.settings.get('theme', 'default')
        return resources.theme(theme_name)
