#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpDccLib
"""

from __future__ import print_function, division, absolute_import

main = __import__('__main__')

import os
import inspect

from tpPyUtils import importer
from tpQtLib.core import resource as resource_utils

# =================================================================================

logger = None
resource = None
Dcc = None

# =================================================================================


class Dccs(object):
    Houdini = 'houdini'
    Maya = 'maya'
    Max = 'max'
    Nuke = 'nuke'

# =================================================================================


class tpDccLibResource(resource_utils.Resource, object):
    RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')


class tpDccLib(importer.Importer, object):
    def __init__(self):
        super(tpDccLib, self).__init__(module_name='tpDccLib')

    def get_module_path(self):
        """
        Returns path where tpDccLib module is stored
        :return: str
        """

        try:
            mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
        except Exception:
            try:
                mod_dir = os.path.dirname(__file__)
            except Exception:
                try:
                    import tpDccLib
                    mod_dir = tpDccLib.__path__[0]
                except Exception:
                    return None

        return mod_dir


def init(do_reload=False):
    """
    Initializes module
    :param do_reload: bool, Whether to reload modules or not
    """

    dcclib_importer = importer.init_importer(importer_class=tpDccLib, do_reload=do_reload)
    init_dcc(do_reload=do_reload)

    global logger
    global resource
    logger = dcclib_importer.logger
    resource = tpDccLibResource

    dcclib_importer.import_modules()
    dcclib_importer.import_packages(only_packages=True)

def init_dcc(do_reload=False):
    """
    Checks DCC we are working on an initializes proper variables
    """

    if 'cmds' in main.__dict__:
        import tpMayaLib
        tpMayaLib.init(do_reload=do_reload)
    elif 'MaxPlus' in main.__dict__:
        import tpMaxLib
        tpMaxLib.init(do_reload=do_reload)
    elif 'hou' in main.__dict__:
        raise NotImplementedError('Houdini is not a supported DCC yet!')
    elif 'nuke' in main.__dict__:
        raise NotImplementedError('Nuke is not a supported DCC yet!')
    else:
        raise NotImplementedError('Current DCC is not supported yet!')


def is_nuke():
    """
    Checks if Nuke is available or not
    :return: bool
    """

    return Dcc.get_name() == Dccs.Nuke


def is_maya():
    """
    Checks if Maya is available or not
    :return: bool
    """

    return Dcc.get_name() == Dccs.Maya


def is_max():
    """
    Checks if Max is available or not
    :return: bool
    """

    return Dcc.get_name() == Dccs.Max


def is_houdini():
    """
    Checks if Houdini is available or not
    :return: bool
    """

    return Dcc.get_name() == Dccs.Houdini
