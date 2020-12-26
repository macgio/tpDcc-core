#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains DCC core functions an classes
"""

from __future__ import print_function, division, absolute_import

import logging
import importlib
from functools import wraps

from tpDcc.core import consts

LOGGER = logging.getLogger('tpDcc-core')

main = __import__('__main__')

# Cached current DCC name.
CURRENT_DCC = None

# Cached used to store all the reroute paths done during a session.
DCC_REROUTE_CACHE = dict()


class Dccs(object):
    Standalone = 'standalone'
    Maya = 'maya'
    Max = 'max'
    MotionBuilder = 'mobu'
    Houdini = 'houdini'
    Nuke = 'nuke'
    Unreal = 'unreal'

    packages = {
        'cmds': Maya,
        'pymxs': Max,
        'pyfbsdk': MotionBuilder,
        'hou': Houdini,
        'nuke': Nuke,
        'unreal': Unreal
    }


class DccCallbacks(object):
    Shutdown = ('Shutdown', {'type': 'simple'})
    Tick = ('Tick', {'type': 'simple'})
    ScenePreCreated = ('ScenePreCreated', {'type': 'simple'})
    ScenePostCreated = ('ScenePreCreated', {'type': 'simple'})
    SceneNewRequested = ('SceneNewRequested', {'type': 'simple'})
    SceneNewFinished = ('SceneNewFinished', {'type': 'simple'})
    SceneSaveRequested = ('SceneSaveRequested', {'type': 'simple'})
    SceneSaveFinished = ('SceneSaveFinished', {'type': 'simple'})
    SceneOpenRequested = ('SceneOpenRequested', {'type': 'simple'})
    SceneOpenFinished = ('SceneOpenFinished', {'type': 'simple'})
    UserPropertyPreChanged = ('UserPropertyPreChanged', {'type': 'filter'})
    UserPropertyPostChanged = ('UserPropertyPostChanged', {'type': 'filter'})
    NodeSelect = ('NodeSelect', {'type': 'filter'})
    NodeAdded = ('NodeAdded', {'type': 'filter'})
    NodeDeleted = ('NodeDeleted', {'type': 'filter'})


def current_dcc():
    global CURRENT_DCC
    if CURRENT_DCC:
        return CURRENT_DCC

    for dcc_package, dcc_name in Dccs.packages.items():
        if dcc_package in main.__dict__:
            CURRENT_DCC = dcc_name
            break
    if not CURRENT_DCC:
        try:
            import unreal
            CURRENT_DCC = Dccs.Unreal
        except ImportError:
            CURRENT_DCC = Dccs.Standalone

    return CURRENT_DCC


def get_dcc_loader_module(package='tpDcc.dccs'):
    """
    Checks DCC we are working on an initializes proper variables
    """

    dcc_mod = None
    for dcc_package, dcc_name in Dccs.packages.items():
        if dcc_package in main.__dict__:
            module_to_import = '{}.{}.loader'.format(package, dcc_name)
            try:
                dcc_mod = importlib.import_module(module_to_import)
            except ImportError:
                LOGGER.warning('DCC loader module {} not found!'.format(module_to_import))
                continue
            if dcc_mod:
                break
    if not dcc_mod:
        try:
            import unreal
            try:
                dcc_mod = importlib.import_module('{}.unreal.loader'.format(package))
            except ImportError:
                pass
        except Exception:
            pass

    return dcc_mod


def reroute(fn):
    """
    Decorator that reroutes the function call on runtime to the specific DCC implementation of the function
    Rerouted function calls are cached, and are only loaded once.
    The used DCC API will be retrieved from the current session, taking into account the current available
    implementations

    :param fn:
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):

        global DCC_REROUTE_CACHE

        dcc = current_dcc()
        if not dcc:
            return None

        # From the current function and DCC we retrieve module path where DCC implementation should be located
        fn_split = fn.__module__.split('.')
        dcc_reroute_path = '{}.{}'.format(consts.TPDCC_DCCS_NAMESPACE, dcc)
        fn_split_str = '.'.join(fn_split[3:])
        if fn_split_str:
            dcc_reroute_path = '{}.{}'.format(dcc_reroute_path, fn_split_str)
        dcc_reroute_path = '{}.dcc'.format(dcc_reroute_path)
        dcc_reroute_fn_path = '{}.{}'.format(dcc_reroute_path, fn.__name__)
        if dcc_reroute_fn_path not in DCC_REROUTE_CACHE:
            try:
                dcc_reroute_module = importlib.import_module(dcc_reroute_path)
            except ImportError as exc:
                raise NotImplementedError(
                    '{} | Function {} not implemented! {}'.format(dcc, dcc_reroute_fn_path, exc))
            except Exception as exc:
                raise exc

            # Cache reroute call, next calls to that function will use cache data
            if not hasattr(dcc_reroute_module, fn.__name__):
                raise NotImplementedError('{} | Function {} not implemented!'.format(dcc, dcc_reroute_fn_path))

            dcc_reroute_fn = getattr(dcc_reroute_module, fn.__name__)
            DCC_REROUTE_CACHE[dcc_reroute_fn_path] = dcc_reroute_fn

        return DCC_REROUTE_CACHE[dcc_reroute_fn_path](*args, **kwargs)

    return wrapper


def callbacks():
    """
    Return a full list of callbacks based on DccCallbacks dictionary
    :return: list<str>
    """

    new_list = list()
    for k, v in DccCallbacks.__dict__.items():
        if k.startswith('__') or k.endswith('__'):
            continue
        new_list.append(v[0])

    return new_list
