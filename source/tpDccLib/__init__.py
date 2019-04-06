#! /usr/bin/env python
# # -*- coding: utf-8 -*-

"""
Initialization module for tpDccLib
"""

from __future__ import print_function, division, absolute_import

main = __import__('__main__')

import os
import types
import pkgutil
import importlib
from collections import OrderedDict

from tpPyUtils import dcc, logger as logger_utils

# =================================================================================

logger = None
Dcc = None

# =================================================================================


class Dccs(object):
    Houdini = 'houdini'
    Maya = 'maya'
    Max = 'max'
    Nuke = 'nuke'

# =================================================================================


class tpDccLib(object):

    loaded_modules = OrderedDict()
    reload_modules = list()

    @classmethod
    def initialize(cls, do_reload=False):

        import tpDccLib

        cls.create_logger()
        cls.init_dcc()
        cls.import_modules(os.path.join(tpDccLib.__path__[0], 'core'), only_packages=True, order=['tpDccLib.widgets'])

        if do_reload:
            cls.reload_all()

    @staticmethod
    def create_logger():
        """
        Creates and initializes tpDccLib logger
        """

        global logger
        logger = logger_utils.Logger(name='tpDccLib', level=logger_utils.LoggerLevel.WARNING)
        logger.debug('Initializing tpDccLib logger ...')
        return logger

    @classmethod
    def init_dcc(cls):
        """
        Checks DCC we are working on an initializes proper variables
        """

        if 'cmds' in main.__dict__:
            import tpMayaLib
            tpMayaLib.init()
        elif 'MaxPlus' in main.__dict__:
            import tpMaxLib
            tpMaxLib.init()
        elif 'hou' in main.__dict__:
            raise NotImplementedError('Houdini is not a supported DCC yet!')
        elif 'nuke' in main.__dict__:
            raise NotImplementedError('Nuke is not a supported DCC yet!')
        else:
            raise NotImplementedError('Current DCC is not supported yet!')

    @staticmethod
    def _explore_package(module_name, only_packages=False):
        """
        Load module iteratively
        :param module_name: str, name of the module
        :return: list<str>, list<str>, list of loaded module names and list of loaded module paths
        """

        import tpDccLib

        module_names = list()
        module_paths = list()

        def foo(name, only_packages):
            for importer, m_name, is_pkg in pkgutil.iter_modules([name]):
                mod_path = name + "//" + m_name
                mod_name = 'tpDccLib.' + os.path.relpath(mod_path, tpDccLib.__path__[0]).replace('\\', '.')
                if only_packages:
                    if is_pkg:
                        module_paths.append(mod_path)
                        module_names.append(mod_name)
                else:
                    module_paths.append(mod_path)
                    module_names.append(mod_name)
                # foo(mod_path, only_packages)

        foo(module_name, only_packages)

        return module_names, module_paths

    @staticmethod
    def _import_module(package_name):

        import tpDccLib

        try:
            mod = importlib.import_module(package_name)
            tpDccLib.logger.debug('Imported: {}'.format(package_name))
            if mod and isinstance(mod, types.ModuleType):
                return mod
            return None
        except (ImportError, AttributeError) as e:
            tpDccLib.logger.debug('FAILED IMPORT: {} -> {}'.format(package_name, str(e)))
            pass

    @classmethod
    def import_modules(cls, module_name, only_packages=False, order=[]):
        names, paths = cls._explore_package(module_name=module_name, only_packages=only_packages)
        ordered_names = list()
        ordered_paths = list()
        temp_index = 0
        i = -1
        for o in order:
            for n, p in zip(names, paths):
                if str(n) == str(o):
                    i += 1
                    temp_index = i
                    ordered_names.append(n)
                    ordered_paths.append(p)
                elif n.endswith(o):
                    ordered_names.insert(temp_index + 1, n)
                    ordered_paths.insert(temp_index + 1, n)
                    temp_index += 1
                elif str(o) in str(n):
                    ordered_names.append(n)
                    ordered_paths.append(p)

        ordered_names.extend(names)
        ordered_paths.extend(paths)

        names_set = set()
        paths_set = set()
        module_names = [x for x in ordered_names if not (x in names_set or names_set.add(x))]
        module_paths = [x for x in ordered_paths if not (x in paths_set or paths_set.add(x))]

        reloaded_names = list()
        reloaded_paths = list()
        for n, p in zip(names, paths):
            reloaded_names.append(n)
            reloaded_paths.append(p)

        for name, _ in zip(module_names, module_paths):
            if name not in cls.loaded_modules.keys():
                mod = cls._import_module(name)
                if mod:
                    if isinstance(mod, types.ModuleType):
                        cls.loaded_modules[mod.__name__] = [os.path.dirname(mod.__file__), mod]
                        cls.reload_modules.append(mod)

        for name, path in zip(module_names, module_paths):
            order = list()
            if name in cls.loaded_modules.keys():
                mod = cls.loaded_modules[name][1]
                if hasattr(mod, 'order'):
                    order = mod.order
            cls.import_modules(module_name=path, only_packages=False, order=order)

    @classmethod
    def reload_all(cls):
        """
        Reload all current loaded modules
        """

        import tpDccLib

        tpDccLib.logger.debug(' =========> Reloading tpDccLib ...')

        for mod in cls.reload_modules:
            if not hasattr(mod, 'no_reload'):
                tpDccLib.logger.debug('RELOADING: {}'.format(mod.__name__))
                reload(mod)
            else:
                tpDccLib.logger.debug('AVOIDING RELOAD OF {}'.format(mod))
        tpDccLib.logger.debug(' =========> tpDccLib reloaded successfully!')


def init(do_reload=False):
    tpDccLib.initialize(do_reload=do_reload)


def is_nuke():
    """
    Checks if Nuke is available or not
    :return: bool
    """

    return dcc == Dccs.Nuke


def is_maya():
    """
    Checks if Maya is available or not
    :return: bool
    """

    return dcc == Dccs.Maya


def is_max():
    """
    Checks if Max is available or not
    :return: bool
    """

    return dcc == Dccs.Max


def is_houdini():
    """
    Checks if Houdini is available or not
    :return: bool
    """

    return dcc == Dccs.Houdini
