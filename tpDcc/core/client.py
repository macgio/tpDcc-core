#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains DCC core client implementation
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import time
import json
import socket
import pkgutil
import logging
import weakref
import importlib
import traceback
from collections import OrderedDict

from Qt.QtCore import Signal, QObject

import tpDcc.loader
import tpDcc.config
from tpDcc import dcc
from tpDcc.managers import configs
import tpDcc.libs.python
import tpDcc.libs.resources
import tpDcc.libs.qt.loader
from tpDcc.libs.python import path as path_utils

if sys.version_info[0] == 2:
    from socket import error as ConnectionRefusedError

LOGGER = logging.getLogger('tpDcc-core')


class DccClientSignals(QObject, object):
    dccDisconnected = Signal()


class DccClient(object):

    PORT = 17344
    HEADER_SIZE = 10

    signals = DccClientSignals()

    class Status(object):
        ERROR = 'error'
        WARNING = 'warning'
        SUCCESS = 'success'
        UNKNOWN = 'unknown'

    def __init__(self, timeout=10):
        self._timeout = timeout
        self._port = self.__class__.PORT
        self._discard_count = 0
        self._server = None
        self._connected = False
        self._status = dict()

    def __getattribute__(self, name):
        try:
            attr = super(DccClient, self).__getattribute__(name)
        except AttributeError:
            def new_fn(*args, **kwargs):
                cmd = {
                    'cmd': name,
                    'args': args
                }
                cmd.update(kwargs)
                reply_dict = self.send(cmd)
                if not self.is_valid_reply(reply_dict):
                    return False
                return reply_dict['result']
            return new_fn

        return attr

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    @property
    def server(self):
        return self._server

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    @classmethod
    def create_and_connect_to_server(cls, tool_id, *args, **kwargs):

        def _update_client():
            config_dict = configs.get_tool_config(tool_id) or dict()
            supported_dccs = config_dict.get(
                'supported_dccs', dict()) if config_dict else kwargs.get('supported_dccs', dict())

            valid_connect = client.connect()
            if not valid_connect:
                _register_client()
                return False

            if dcc.is_standalone():
                success, dcc_exe = client.update_paths()
                if not success:
                    return False

                success = client.update_dcc_paths(dcc_exe)
                if not success:
                    return False

                success = client.init_dcc()
                if not success:
                    return False

            dcc_name, dcc_version, dcc_pid = client.get_dcc_info()
            if not dcc_name or not dcc_version:
                return False

            if dcc_name not in supported_dccs:
                client.set_status(
                    'Connected DCC {} ({}) is not supported!'.format(dcc_name, dcc_version), client.Status.WARNING)
                return False

            supported_versions = supported_dccs[dcc_name]
            if dcc_version not in supported_versions:
                client.set_status(
                    'Connected DCC {} is support but version {} is not!'.format(
                        dcc_name, dcc_version), client.Status.WARNING)
                return False

            msg = 'Connected to: {} {} ({})'.format(dcc_name, dcc_version, dcc_pid)
            client.set_status(msg, client.Status.SUCCESS)
            LOGGER.info(msg)

            _register_client()

        def _register_client():
            """
            Internal function that registers given client in global Dcc clients variable
            """

            if not client:
                return
            client_found = False
            current_clients = dcc._CLIENTS
            for current_client in list(current_clients.values()):
                if client == current_client():
                    client_found = True
                    break
            if client_found:
                return
            dcc._CLIENTS[tool_id] = weakref.ref(client)

        # If a client with given ID is already registered, we return it
        client = dcc.client(tool_id, only_clients=True)
        if client:
            return client

        client = cls()

        parent = kwargs.get('parent', None)
        server_class_name = kwargs.get('server_name', cls.__name__.replace(
            'Client', 'Server').replace('client', 'server'))
        server_module_name = kwargs.get('server_module_name', server_class_name.lower())

        if not dcc.is_standalone():
            dcc_mod_name = '{}.dccs.{}.{}'.format(tool_id.replace('-', '.'), dcc.get_name(), server_module_name)
            try:
                mod = importlib.import_module(dcc_mod_name)
                if hasattr(mod, server_class_name):
                    server = getattr(mod, server_class_name)(parent, client=client, update_paths=False)
                    client.set_server(server)
                    _update_client()
            except Exception as exc:
                LOGGER.warning(
                    'Impossible to launch Renamer server! Error while importing: {} >> {}'.format(dcc_mod_name, exc))
                try:
                    server.close_connection()
                except Exception:
                    pass
                return None
        else:
            _update_client()

        return client

    def set_server(self, server):
        self._server = server

    def connect(self, port=-1):
        if self._server:
            self._status = {'msg': 'Client connected successfully!', 'level': self.Status.SUCCESS}
            self._connected = True
            return True

        if port > 0:
            self._port = port
        try:
            self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._client_socket.connect(('localhost', self._port))
            # self._client_socket.setblocking(False)
        except ConnectionRefusedError as exc:
            LOGGER.warning(exc)
            self._status = {'msg': 'Client connection was refused.', 'level': self.Status.ERROR}
            self._connected = False
            return False
        except Exception:
            LOGGER.exception(traceback.format_exc())
            self._status = {'msg': 'Error while connecting client', 'level': self.Status.ERROR}
            self._connected = False
            return False

        self._connected = True

        return True

    def disconnect(self):
        try:
            self._client_socket.close()
            self.signals.dccDisconnected.emit()
        except Exception:
            traceback.print_exc()
            self._status = {'msg': 'Error while disconnecting client', 'level': self.Status.ERROR}
            return False

        return True

    def send(self, cmd_dict):
        json_cmd = json.dumps(cmd_dict)

        # If we use execute the tool inside DCC we execute client/server in same process. We can just launch the
        # function in the server
        if self._server:
            reply_json = self._server._process_data(cmd_dict)
            if not reply_json:
                self._status = None
                return {'success': False}
            return json.loads(reply_json)
        else:
            if not self._connected:
                cmd = cmd_dict.pop('cmd', None)
                if cmd and hasattr(dcc, cmd):
                    try:
                        res = getattr(dcc, cmd)(**json_cmd)
                    except TypeError:
                        res = getattr(dcc, cmd)()
                    if res is not None:
                        return {'success': True, 'result': res}
                return None

            message = list()
            message.append('{0:10d}'.format(len(json_cmd.encode())))    # header (10 bytes)
            message.append(json_cmd)

            try:
                msg_str = ''.join(message)
                self._client_socket.sendall(msg_str.encode())
            except OSError as exc:
                LOGGER.debug(exc)
                return None
            except Exception:
                LOGGER.exception(traceback.format_exc())
                return None

            res = self.recv()
            self._status = res.pop('status', dict())

            return res

    def recv(self):
        total_data = list()
        reply_length = 0
        bytes_remaining = DccClient.HEADER_SIZE

        start_time = time.time()
        while time.time() - start_time < self._timeout:
            try:
                data = self._client_socket.recv(bytes_remaining)
            except Exception as exc:
                time.sleep(0.01)
                print(exc)
                continue

            if data:
                total_data.append(data)
                bytes_remaining -= len(data)
                if bytes_remaining <= 0:
                    for i in range(len(total_data)):
                        total_data[i] = total_data[i].decode()

                    if reply_length == 0:
                        header = ''.join(total_data)
                        reply_length = int(header)
                        bytes_remaining = reply_length
                        total_data = list()
                    else:
                        if self._discard_count > 0:
                            self._discard_count -= 1
                            return self.recv()

                        reply_json = ''.join(total_data)
                        return json.loads(reply_json)

        self._discard_count += 1

        # If timeout is checked, before raising timeout we make sure that all remaining data is processed
        try:
            data = self._client_socket.recv(bytes_remaining)
        except Exception as exc:
            time.sleep(0.01)
            print(exc)
        if data:
            total_data.append(data)
            bytes_remaining -= len(data)
            if bytes_remaining <= 0:
                for i in range(len(total_data)):
                    total_data[i] = total_data[i].decode()

                if reply_length == 0:
                    header = ''.join(total_data)
                    reply_length = int(header)
                else:
                    self._discard_count -= 1
                    reply_json = ''.join(total_data)
                    return json.loads(reply_json)

        raise RuntimeError('Timeout waiting for response')

    def is_valid_reply(self, reply_dict):
        if not reply_dict:
            LOGGER.debug('Invalid reply')
            return False

        if not reply_dict['success']:
            LOGGER.error('{} failed: {}'.format(reply_dict['cmd'], reply_dict['msg']))
            return False

        self._status = reply_dict.pop(
            'status', None) or {'msg': self.get_status_message(), 'level': self.get_status_level()}

        return True

    def ping(self):
        cmd = {
            'cmd': 'ping'
        }

        reply = self.send(cmd)

        if not self.is_valid_reply(reply):
            return False

        return True

    def update_paths(self):

        paths_to_update = self._get_paths_to_update()

        cmd = {
            'cmd': 'update_paths',
            # NOTE: The order is SUPER important, we must load the modules in the client in the same order
            'paths': OrderedDict(paths_to_update)
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            self._status = {'msg': 'Error while connecting to Dcc: update paths ...', 'level': self.Status.ERROR}
            return False

        exe = reply_dict.get('exe', None)

        return reply_dict['success'], exe

    def update_dcc_paths(self, dcc_executable):
        if not dcc_executable:
            return False

        dcc_name = None
        if 'maya' in dcc_executable:
            dcc_name = 'maya'
        elif '3dsmax' in dcc_executable:
            dcc_name = 'max'
        elif 'houdini' in dcc_executable:
            dcc_name = 'houdini'
        elif 'nuke' in dcc_executable:
            dcc_name = 'nuke'
        elif 'unreal' in dcc_executable or os.path.basename(dcc_executable).startswith('UE'):
            dcc_name = 'unreal'
        if not dcc_name:
            msg = 'Executable DCC {} is not supported!'.format(dcc_executable)
            LOGGER.warning(msg)
            self._status = {'msg': msg, 'level': self.Status.WARNING}
            return False

        module_name = 'tpDcc.dccs.{}.loader'.format(dcc_name)
        try:
            mod = pkgutil.get_loader(module_name)
        except Exception:
            try:
                self._status = {
                    'msg': 'Error while connecting to Dcc: update dcc paths ...', 'severity': self.Status.ERROR}
                LOGGER.error('FAILED IMPORT: {} -> {}'.format(str(module_name), str(traceback.format_exc())))
                return False
            except Exception:
                self._status = {
                    'msg': 'Error while connecting to Dcc: update dcc paths ...', 'severity': self.Status.ERROR}
                LOGGER.error('FAILED IMPORT: {}'.format(module_name))
                return False
        if not mod:
            msg = 'Impossible to import DCC specific module: {} ({})'.format(module_name, dcc_name)
            LOGGER.warning(msg)
            self._status = {'msg': msg, 'severity': self.Status.WARNING}
            return False

        cmd = {
            'cmd': 'update_dcc_paths',
            'paths': OrderedDict({
                'tpDcc.dccs.{}'.format(dcc_name): path_utils.clean_path(
                    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(mod.get_filename())))))
            })
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            self._status = {
                'msg': 'Error while connecting to Dcc: update dcc paths ...', 'level': self.Status.ERROR}
            return False

        return reply_dict['success']

    def init_dcc(self):
        cmd = {
            'cmd': 'init_dcc'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            self._status = {'msg': 'Error while connecting to Dcc: init dcc ...', 'level': self.Status.ERROR}
            return False

        return reply_dict['success']

    def get_dcc_info(self):
        cmd = {
            'cmd': 'get_dcc_info'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            self._status = {'msg': 'Error while connecting to Dcc: get dcc info ...', 'level': self.Status.ERROR}
            return None, None

        return reply_dict['name'], reply_dict['version'], reply_dict['pid']

    def select_node(self, node, **kwargs):
        cmd = {
            'cmd': 'select_node',
            'node': node
        }
        cmd.update(**kwargs)

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def selected_nodes(self, full_path=True):
        cmd = {
            'cmd': 'selected_nodes',
            'full_path': full_path
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict.get('result', list())

    def clear_selection(self):
        cmd = {
            'cmd': 'clear_selection'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['success']

    def get_control_colors(self):
        cmd = {
            'cmd': 'get_control_colors'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict.get('result', list())

    def get_fonts(self):
        cmd = {
            'cmd': 'get_fonts'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict.get('result', list())

    def enable_undo(self):
        cmd = {
            'cmd': 'enable_undo'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def disable_undo(self):
        cmd = {
            'cmd': 'disable_undo'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return list()

        return reply_dict['success']

    def get_status_message(self):
        return self._status.get('msg', '')

    def get_status_level(self):
        return self._status.get('level', self.Status.UNKNOWN)

    def set_status(self, status_message, status_level):
        self._status = {
            'msg': str(status_message), 'level': status_level
        }

    def _get_paths_to_update(self):
        """
        Internal function that returns all the paths that DCC server should include to properly work with the client
        """

        return {
            'tpDcc.loader': path_utils.clean_path(os.path.dirname(os.path.dirname(tpDcc.loader.__file__))),
            'tpDcc.config': path_utils.clean_path(
                os.path.dirname(os.path.dirname(os.path.dirname(tpDcc.config.__file__)))),
            'tpDcc.libs.python': path_utils.clean_path(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.dirname(tpDcc.libs.python.__file__))))),
            'tpDcc.libs.resources': path_utils.clean_path(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.dirname(tpDcc.libs.resources.__file__))))),
            'tpDcc.libs.qt.loader': path_utils.clean_path(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(tpDcc.libs.qt.loader.__file__)))))
        }


class ExampleClient(DccClient, object):

    PORT = 17337

    def echo(self, text):
        cmd_dict = {
            'cmd': 'echo',
            'text': text
        }

        reply_dict = self.send(cmd_dict)

        if not self.is_valid_reply(reply_dict):
            return None

        return reply_dict['result']

    def set_title(self, title):
        cmd_dict = {
            'cmd': 'set_title',
            'title': title
        }

        reply_dict = self.send(cmd_dict)

        if not self.is_valid_reply(reply_dict):
            return None

        return reply_dict['result']

    def sleep(self):
        cmd_dict = {
            'cmd': 'sleep'
        }

        reply_dict = self.send(cmd_dict)

        if not self.is_valid_reply(reply_dict):
            return None

        return reply_dict['result']


if __name__ == '__main__':
    client = ExampleClient(timeout=10)
    if client.connect():
        print('Connected successfully!')

        print(client.ping())
        print(client.echo('Hello World!'))
        print(client.set_title('New Server Title'))
        print(client.sleep())

        if client.disconnect():
            print('Disconnected successfully!')
    else:
        print('Failed to connect')
