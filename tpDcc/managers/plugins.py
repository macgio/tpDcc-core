import os
import inspect

import tpDcc as tp
from tpDcc.core import plugin
from tpDcc.libs.python import python, modules


class PluginsManager(object):
    def __init__(self, interface=plugin.Plugin, variable_name='ID'):
        self._interfaces = python.force_list(interface)
        self._variable_name = variable_name
        self._plugins = dict()
        self._loaded_plugins = dict()
        self._base_paths = list()

    @property
    def interfaces(self):
        return self._interfaces

    def get_plugins(self, package_name):
        return self._plugins.get(package_name, None)

    def get_plugin_from_id(self, plugin_id, package_name=None):
        """
        Returns registered plugin data from its id
        :param plugin_id: str
        :param package_name: str
        :return: dict
        """

        if not plugin_id:
            return None

        if not package_name:
            package_name = plugin_id.replace('.', '-').split('-')[0]

        if package_name and package_name not in self._plugins:
            tp.logger.error('Impossible to retrieve data from id: {} package: "{}" not registered!'.format(
                plugin_id, package_name))
            return None

        return self._plugins[package_name][plugin_id] if plugin_id in self._plugins[package_name] else None

    def get_plugin_from_name(self, plugin_name, as_dict=False, package_name=None):
        """
        Returns registered plugin from its name
        :param plugin_name: str
        :param as_dict: bool
        :return:
        """

        if not plugin_name:
            return None

        if package_name and package_name not in self._plugins:
            tp.logger.error(
                'Impossible to retrieve data from name: package "{}" not registered!'.format(package_name))
            return None

        for plugin_id, plugin_data in self._plugins[package_name].items():
            current_name = plugin_data.get('name', None)
            if current_name == plugin_name:
                if as_dict:
                    return {
                        plugin_id: self._plugins[package_name][plugin_id]
                    }
                else:
                    return self._plugins[package_name][plugin_id]

        return None

    # def get_plugin_data_from_plugin_instance(self, plugin, as_dict=False, package_name=None):
    #     """
    #     Returns registered plugin data from a plugin object
    #     :return: dict
    #     """
    #
    #     if not package_name:
    #         package_name = plugin.PACKAGE
    #     if not package_name:
    #         tp.logger.error('Impossible to retrieve data from plugin with undefined package!')
    #         return None
    #
    #     if package_name not in self._plugins:
    #         tp.logger.error(
    #             'Impossible to retrieve data from instance: package "{}" not registered!'.format(package_name))
    #         return None
    #
    #     if hasattr(plugin, 'ID'):
    #         return self._plugins[package_name].get(plugin.ID, None)
    #
    #     return None

    def register_plugin(self, class_obj, package_name):
        """
        Registers a plugin instance to the manager
        :param class_obj:
        :param package_name: str
        :return: Plugin
        """

        for interface in self._interfaces:

            if not issubclass(class_obj, interface):
                continue

            plugin_id = getattr(
                class_obj, self._variable_name) if hasattr(class_obj, self._variable_name) else class_obj.__name__

            plugin_found = self._plugins.get(package_name, dict()).get(plugin_id)
            if plugin_found:
                continue

            self._plugins.setdefault(package_name, dict())
            self._plugins[package_name][plugin_id] = class_obj

    def register_plugin_by_package(self, module_path, package_name=None):
        """
        Registers a module by searching all class members of the package. This operation can be extensive.
        :param module_path: str
        :param package_name: str
        :return:
        """

        for sub_module in modules.iterate_modules(module_path):
            file_name = os.path.splitext(os.path.basename(sub_module))[0]
            if file_name.startswith('__') or sub_module.endswith('.pyc'):
                continue
            module_path = modules.convert_to_dotted_path(os.path.normpath(sub_module))
            try:
                sub_module_obj = modules.import_module(module_path, skip_errors=True)
            except Exception as exc:
                # tp.logger.error('Error while importing module: {} | {}'.format(module_path, traceback.format_exc()))
                continue
            if not sub_module_obj:
                return
            for member in modules.iterate_module_members(sub_module_obj, predicate=inspect.isclass):
                self.register_plugin(member[1], package_name=package_name)

    def register_plugin_by_module(self, module, package_name=None):
        """
        Registers a module by searching all class members of the module and registers any class that is an instance of
        the plugin class
        :param module: str, module path to register separated by . (for example, tpDcc.tools.renamer.widgets)
        :param package_name: str
        """

        if inspect.ismodule(module):
            for member in modules.iterate_module_members(module, predicate=inspect.isclass):
                self.register_plugin(member[1], package_name=package_name)

    def register_plugin_by_environment_variable(self, env_var, package_name=None):
        """
        Register a plugin by registering all the paths stored in the given environment variable
        :param env_var: str, environment variable we are going to retrieve paths from
        :param package_name: str
        """

        paths = os.environ.get(env_var, '').split(os.pathsep)
        if not paths:
            return

        self.register_paths(paths, package_name=package_name)

    def register_path(self, module_path, package_name=None):
        """
        Register the given path and maps it into the current package name
        :param module_path: str, path to register
        :param package_name: str
        :return: list(modules), list of registered Python modules
        """

        imported_module = None
        if os.path.isdir(module_path):
            self.register_plugin_by_package(module_path, package_name=package_name)
            return None
        elif os.path.isfile(module_path):
            try:
                imported_module = modules.import_module(modules.convert_to_dotted_path(os.path.normpath(module_path)))
            except Exception as exc:
                tp.logger.error('Failed to import Plugin module: {} | {}!'.format(module_path, exc), exc_info=True)
                return None
        elif modules.is_dotted_module_path(module_path):
            try:
                imported_module = modules.import_module(os.path.normpath(module_path))
            except Exception as exc:
                tp.logger.error('Failed to import Plugin module: {} | {}!'.format(module_path, exc), exc_info=True)
                return None
        if imported_module:
            self.register_plugin_by_module(imported_module, package_name=package_name)

        return imported_module

    def register_paths(self, paths_to_register, package_name=None):
        """
        Register the given list of paths and maps them into the current package
        :param paths_to_register: list(str), paths to register
        :return: list(modules), list of registered Python modules
        """

        self._base_paths.extend(paths_to_register)
        visited = set()
        for path_to_register in paths_to_register:
            if not path_to_register:
                continue
            if os.path.isfile(path_to_register):
                base_name = os.extsep.join(path_to_register.split(os.extsep)[:-1])
            else:
                base_name = path_to_register
            if base_name in visited:
                continue
            visited.add(base_name)
            self.register_path(path_to_register, package_name=package_name)
