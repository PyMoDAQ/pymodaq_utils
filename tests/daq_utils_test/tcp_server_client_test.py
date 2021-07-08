import pytest
import numpy as np
import socket
import socket as native_socket

from unittest import mock
from pymodaq.daq_utils.parameter import ioxml
from pymodaq.daq_utils.parameter import utils as putils
from pymodaq.daq_utils.daq_utils import ThreadCommand
from PyQt5.QtCore import pyqtSignal, QObject
from pymodaq.daq_utils.tcp_server_client import MockServer, TCPClient, TCPServer, Socket

from pyqtgraph.parametertree import Parameter

from time import sleep
from collections import OrderedDict
import sys
from packaging import version as version_mod


class MockPythonSocket:  # pragma: no cover
    def __init__(self):
        self._send = []
        self._sendall = []
        self._recv = []
        self._socket = None
        self.AF_INET = None
        self.SOCK_STREAM = None
        self._closed = False
        self._fileno = 1

    def bind(self, *args, **kwargs):
        arg = args[0]
        if len(arg) != 2:
            raise TypeError(f'{args} must be a tuple of two elements')
        else:
            if arg[0] == '':
                self._sockname = ('0.0.0.0', arg[1])
            else:
                self._sockname = (arg[0], arg[1])

    def listen(self):
        pass

    def accept(self):
        return (self, '0.0.0.0')

    def getsockname(self):
        return self._sockname

    def connect(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs):
        self._send.append(args[0])
        return len(str(self._send[-1]))

    def sendall(self, *args, **kwargs):
        self._sendall.append(args[0])

    def recv(self, *args, **kwargs):
        if len(self._send) > 0:
            return self._send.pop(0)

    def close(self):
        self._closed = True

    def fileno(self):
        return self._fileno


class TestSocket:
    def test_init(self):
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_Socket = Socket(test_socket)
        assert isinstance(test_Socket, Socket)
        assert test_Socket.socket == test_socket
        assert test_Socket.__eq__(test_Socket)
    
    def test_base_fun(self):
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_Socket = Socket(test_socket)
        test_Socket.bind(('', 5544))
        test_Socket.listen
        assert test_Socket.getsockname() == ('0.0.0.0', 5544)
        assert test_Socket.accept
        assert test_Socket.connect
        assert test_Socket.send
        assert test_Socket.sendall
        assert test_Socket.recv
        test_Socket.close()

        test_socket = MockPythonSocket()
        test_Socket = Socket(test_socket)
        test_Socket.bind(('', 5544))
        test_Socket.listen()
        test_Socket.getsockname() == ('0.0.0.0', 5544)
        test_Socket.accept()
        test_Socket.connect()
        test_Socket.send(b'test')
        test_Socket.sendall(b'test')
        test_Socket.recv(4)
        test_Socket.close()
        
    def test_message_to_bytes(self):
        message = 10
        bytes_message = Socket.message_to_bytes(message)
        assert isinstance(bytes_message[0], bytes)
        assert isinstance(bytes_message[1], bytes)

    def test_int_to_bytes(self):
        integer = 5
        bytes_integer = Socket.int_to_bytes(integer)
        assert isinstance(bytes_integer, bytes)

        with pytest.raises(TypeError):
            Socket.int_to_bytes(1.5)
            
    def test_bytes_to_int(self):
        integer = 5
        bytes_integer = Socket.int_to_bytes(integer)
        integer_2 = Socket.bytes_to_int(bytes_integer)
        assert isinstance(integer_2, int)
        assert integer_2 == integer
        
        with pytest.raises(TypeError):
            Socket.bytes_to_int(integer)

    def test_check_sended(self):
        test_Socket = Socket(MockPythonSocket())
        test_Socket.check_sended(b'test')

        with pytest.raises(TypeError):
            test_Socket.check_sended('test')

    def test_check_received_length(self):
        test_Socket = Socket(MockPythonSocket())
        test_Socket.send(b'test')
        test_Socket.check_received_length(4)

        for i in range(1025):
            test_Socket.send(b'test')
        test_Socket.check_received_length(4100)

        with pytest.raises(TypeError):
            test_Socket.check_received_length(100)

        with pytest.raises(TypeError):
            test_Socket.check_received_length(1.5)

    def test_send_string(self):
        test_Socket = Socket(MockPythonSocket())
        test_Socket.send_string('test')
        assert test_Socket.recv() == b'\x00\x00\x00\x04'
        assert test_Socket.recv() == b'test'

    def test_get_string(self):
        test_Socket = Socket(MockPythonSocket())
        test_Socket.send_string('test')
        assert test_Socket.get_string() == 'test'

    def test_get_int(self):
        test_Socket = Socket(MockPythonSocket())
        test_Socket.send_string('test')
        assert test_Socket.get_int() == 4

    def test_send_scalar(self):
        test_Socket = Socket(MockPythonSocket())
        scalar = 7
        test_Socket.send_scalar(scalar)

        data = np.array(scalar)
        data_bytes = data.tobytes()
        data_type = data.dtype.descr[0][1]
        cmd_bytes, cmd_length_bytes = test_Socket.message_to_bytes(data_type)

        assert test_Socket.recv() == cmd_length_bytes
        assert test_Socket.recv() == cmd_bytes
        assert test_Socket.recv() == test_Socket.int_to_bytes(len(data_bytes))
        assert test_Socket.recv() == data_bytes
        assert not test_Socket.recv()

        with pytest.raises(TypeError):
            test_Socket.send_scalar('5')

    def test_get_scalar(self):
        test_Socket = Socket(MockPythonSocket())
        test_Socket.send_scalar(7.5)
        assert test_Socket.get_scalar() == 7.5

    def test_send_array(self):
        test_Socket = Socket(MockPythonSocket())
        data = np.array([1, 2, 3])
        test_Socket.send_array(data)

        data_bytes = data.tobytes()
        data_type = data.dtype.descr[0][1]
        cmd_bytes, cmd_length_bytes = test_Socket.message_to_bytes(data_type)

        assert test_Socket.recv() == cmd_length_bytes
        assert test_Socket.recv() == cmd_bytes
        assert test_Socket.recv() == test_Socket.int_to_bytes(len(data_bytes))
        assert test_Socket.recv() == test_Socket.int_to_bytes(len(data.shape))
        for i in range(len(data.shape)):
            assert test_Socket.recv() == test_Socket.int_to_bytes(data.shape[i])
        assert test_Socket.recv() == data_bytes
        assert not test_Socket.recv()

        data = np.array([[1, 2], [2, 3]])
        test_Socket.send_array(data)

        data_bytes = data.tobytes()
        data_type = data.dtype.descr[0][1]
        cmd_bytes, cmd_length_bytes = test_Socket.message_to_bytes(data_type)

        assert test_Socket.recv() == cmd_length_bytes
        assert test_Socket.recv() == cmd_bytes
        assert test_Socket.recv() == test_Socket.int_to_bytes(len(data_bytes))
        assert test_Socket.recv() == test_Socket.int_to_bytes(len(data.shape))
        for i in range(len(data.shape)):
            assert test_Socket.recv() == test_Socket.int_to_bytes(data.shape[i])
        assert test_Socket.recv() == data_bytes
        assert not test_Socket.recv()

        with pytest.raises(TypeError):
            test_Socket.send_array(10)

    def test_get_array(self):
        test_Socket = Socket(MockPythonSocket())
        array = np.array([1, 2.1, 3.0])
        test_Socket.send_array(array)
        result = test_Socket.get_array()
        assert np.array_equal(array, result)

    def test_send_list(self):
        test_Socket = Socket(MockPythonSocket())
        data_list = [np.array([1, 2]), 'test', 47]
        test_Socket.send_list(data_list)
        assert test_Socket.recv() == b'\x00\x00\x00\x03'
        assert test_Socket.get_string() == 'array'
        assert np.array_equal(test_Socket.get_array(), data_list[0])
        assert test_Socket.get_string() == 'string'
        assert test_Socket.get_string() == data_list[1]
        assert test_Socket.get_string() == 'scalar'
        assert test_Socket.get_scalar() == data_list[2]

        with pytest.raises(TypeError):
            test_Socket.send_list([test_Socket])

        with pytest.raises(TypeError):
            test_Socket.send_list(15)

    def test_get_list(self):
        test_Socket = Socket(MockPythonSocket())
        data_list = [np.array([1, 2]), 'test', 47]
        test_Socket.send_list(data_list)
        np_list = np.array(data_list)
        result = np.array(test_Socket.get_list())
        for elem1, elem2 in zip(np_list, result):
            if isinstance(elem1, np.ndarray):
                assert np.array_equal(elem1, elem2)
            else :
                assert elem1 == elem2


class TestTCPClient:
    def test_init(self):
        params_state = {'Name': 'test_params', 'value': None}
        test_TCP_Client = TCPClient(params_state=params_state)
        assert isinstance(test_TCP_Client, TCPClient)

        params_state = Parameter(name='test')
        test_TCP_Client = TCPClient(params_state=params_state)
        assert isinstance(test_TCP_Client, TCPClient)

    def test_socket(self):
        test_TCP_Client = TCPClient()
        assert test_TCP_Client.socket == None

        test_TCP_Client.socket = Socket(MockPythonSocket())
        assert isinstance(test_TCP_Client.socket, Socket)

    def test_close(self):
        test_TCP_Client = TCPClient()
        test_TCP_Client.socket = Socket(MockPythonSocket())
        test_TCP_Client.close()
        assert test_TCP_Client.socket.socket._closed

    def test_send_data(self):
        test_TCP_Client = TCPClient()
        test_TCP_Client.socket = Socket(MockPythonSocket())
        data_list = [14, 1.1, 'test', np.array([1, 2, 3])]
        test_TCP_Client.send_data(data_list)
        assert test_TCP_Client.socket.get_string() == 'Done'
        np_list = np.array(data_list)
        result = test_TCP_Client.socket.get_list()
        for elem1, elem2 in zip(np_list, result):
            if isinstance(elem1, np.ndarray):
                assert np.array_equal(elem1, elem2)
            else:
                assert elem1 == elem2

        with pytest.raises(TypeError):
            test_TCP_Client.send_data([1j])

    def test_send_infos_xml(self):
        test_TCP_Client = TCPClient()
        test_TCP_Client.socket = Socket(MockPythonSocket())
        test_TCP_Client.send_infos_xml('test_send_infos_xml')
        assert test_TCP_Client.socket.get_string() == 'Infos'
        assert test_TCP_Client.socket.get_string() == 'test_send_infos_xml'

    def test_send_infos_string(self):
        test_TCP_Client = TCPClient()
        test_TCP_Client.socket = Socket(MockPythonSocket())
        info_to_display = 'info to display'
        value_as_string = 192.7654
        test_TCP_Client.send_info_string(info_to_display, value_as_string)
        assert test_TCP_Client.socket.get_string() == 'Info'
        assert test_TCP_Client.socket.get_string() == info_to_display
        assert test_TCP_Client.socket.get_string() == str(value_as_string)

    def test_queue_command(self):
        test_TCP_Client = TCPClient()
        command = mock.Mock()
        command.attributes = {'ipaddress': '0.0.0.0', 'port': 5544, 'path': [1, 2, 3],
                              'param': Parameter(name='test_param')}
        command.command = 'quit'
        test_TCP_Client.queue_command(command)

        test_TCP_Client.socket = Socket(MockPythonSocket())
        test_TCP_Client.queue_command(command)
        assert test_TCP_Client.socket.socket._closed

        test_TCP_Client.socket = Socket(MockPythonSocket())
        command.command = 'update_connection'
        test_TCP_Client.queue_command(command)
        assert test_TCP_Client.ipaddress == command.attributes['ipaddress']
        assert test_TCP_Client.port == command.attributes['port']

        command.command = 'send_info'
        test_TCP_Client.queue_command(command)
        assert test_TCP_Client.socket.get_string() == 'Info_xml'
        assert test_TCP_Client.socket.get_list() == command.attributes['path']
        assert test_TCP_Client.socket.get_string()

        command.attributes = [{'data': [1, 1.1, 5]}]
        command.command = 'data_ready'
        test_TCP_Client.queue_command(command)
        assert test_TCP_Client.socket.get_string() == 'Done'
        assert test_TCP_Client.socket.get_list() == command.attributes[0]['data']

        command.attributes = [10]
        command.command = 'position_is'
        test_TCP_Client.queue_command(command)
        assert test_TCP_Client.socket.get_string() == 'position_is'
        assert test_TCP_Client.socket.get_scalar() == command.attributes[0]

        command.command = 'move_done'
        test_TCP_Client.queue_command(command)
        assert test_TCP_Client.socket.get_string() == 'move_done'
        assert test_TCP_Client.socket.get_scalar() == command.attributes[0]

        command.attributes = [np.array([1, 2, 3])]
        command.command = 'x_axis'
        test_TCP_Client.queue_command(command)
        assert test_TCP_Client.socket.get_string() == 'x_axis'
        array = command.attributes[0]
        result = test_TCP_Client.socket.get_array()
        for val1, val2 in zip(array, result):
            assert val1 == val2
        assert test_TCP_Client.socket.get_string() == ''
        assert test_TCP_Client.socket.get_string() == ''

        command.command = 'y_axis'
        test_TCP_Client.queue_command(command)
        assert test_TCP_Client.socket.get_string() == 'y_axis'
        result = test_TCP_Client.socket.get_array()
        for val1, val2 in zip(array, result):
            assert val1 == val2
        assert test_TCP_Client.socket.get_string() == ''
        assert test_TCP_Client.socket.get_string() == ''

        command.command = 'x_axis'
        command.attributes = [{'data': np.array([1, 2, 3]), 'label': 'test', 'units': 'cm'}]
        test_TCP_Client.queue_command(command)
        assert test_TCP_Client.socket.get_string() == 'x_axis'
        array = command.attributes[0]['data']
        result = test_TCP_Client.socket.get_array()
        for val1, val2 in zip(array, result):
            assert val1 == val2
        assert test_TCP_Client.socket.get_string() == 'test'
        assert test_TCP_Client.socket.get_string() == 'cm'

        command.command = 'y_axis'
        test_TCP_Client.queue_command(command)
        assert test_TCP_Client.socket.get_string() == 'y_axis'
        result = test_TCP_Client.socket.get_array()
        for val1, val2 in zip(array, result):
            assert val1 == val2
        assert test_TCP_Client.socket.get_string() == 'test'
        assert test_TCP_Client.socket.get_string() == 'cm'

        command.command = 'test'
        with pytest.raises(IOError):
            test_TCP_Client.queue_command(command)

    @mock.patch('pymodaq.daq_utils.tcp_server_client.QtWidgets.QApplication.processEvents')
    @mock.patch('pymodaq.daq_utils.tcp_server_client.select.select')
    @mock.patch('pymodaq.daq_utils.tcp_server_client.Socket')
    def test_init_connection(self, mock_Socket, mock_select, mock_events):
        mock_Socket.return_value = Socket(MockPythonSocket())
        mock_select.side_effect = [([], [], []), Exception]
        mock_events.return_value = None
        test_TCP_Client = TCPClient()
        test_TCP_Client.init_connection(extra_commands=[ThreadCommand('test')])

        command = mock.Mock()
        command.command = 'ini_connection'
        test_TCP_Client.queue_command(command)

        test_Socket = Socket(MockPythonSocket())
        test_Socket.send_string('init')
        mock_Socket.return_value = test_Socket
        mock_select.side_effect = [(['init'], [], ['error'])]
        test_TCP_Client.init_connection()

        assert not test_TCP_Client.connected

        mock_Socket.side_effect = [ConnectionRefusedError]
        test_TCP_Client.init_connection()

    def test_get_data(self):
        test_TCP_Client = TCPClient()
        test_TCP_Client.socket = Socket(MockPythonSocket())
        data_list = [1, 2, 3]
        data_param = 'test'
        test_TCP_Client.socket.send_list(data_list)
        test_TCP_Client.socket.send_string(data_param)
        test_TCP_Client.get_data('set_info')

        test_TCP_Client.socket.send_scalar(10)
        test_TCP_Client.get_data('move_abs')

        test_TCP_Client.socket.send_scalar(7)
        test_TCP_Client.get_data('move_rel')


class TestTCPServer:
    def test_init(self):
        test_TCP_Server = TCPServer()
        assert isinstance(test_TCP_Server, TCPServer)

    def test_close_server(self):
        test_TCP_Server = TCPServer()
        test_TCP_Server.close_server()

    # @mock.patch('pymodaq.daq_utils.tcp_server_client.Socket')
    # def test_init_server(self, mock_Socket):
    #     mock_Socket.return_value = Socket(MockPythonSocket())
    #
    #     value = mock.Mock()
    #     value.value.return_value = 'test'
    #     child = mock.Mock()
    #     child.return_value = value
    #     test_TCP_Server = TCPServer()
    #     test_TCP_Server.settings = child
    #     test_TCP_Server.init_server()

    @mock.patch('pymodaq.daq_utils.tcp_server_client.TCPServer.select')
    def test_timerEvent(self, mock_select):
        mock_select.return_value = Exception
        test_TCP_Server = TCPServer()
        test_TCP_Server.timerEvent(None)

    def test_find_socket_within_connected_clients(self):
        test_TCP_Server = TCPServer()
        dict_list = [{'socket': 'Client_1', 'type': 'Server'},
                     {'socket': 'Client_2', 'type': 'Client'}]
        test_TCP_Server.connected_clients = dict_list

        assert not test_TCP_Server.find_socket_within_connected_clients(None)
        assert test_TCP_Server.find_socket_within_connected_clients('Server') == 'Client_1'
        assert test_TCP_Server.find_socket_within_connected_clients('Client') == 'Client_2'

    def test_find_socket_type_within_connected_clients(self):
        test_TCP_Server = TCPServer()
        dict_list = [{'socket': 'Client_1', 'type': 'Server'},
                     {'socket': 'Client_2', 'type': 'Client'}]
        test_TCP_Server.connected_clients = dict_list

        assert not test_TCP_Server.find_socket_type_within_connected_clients(None)
        assert test_TCP_Server.find_socket_type_within_connected_clients('Client_1') == 'Server'
        assert test_TCP_Server.find_socket_type_within_connected_clients('Client_2') == 'Client'

    def test_set_connected_clients_table(self):
        test_TCP_Server = TCPServer()

        socket_1 = Socket(MockPythonSocket())
        socket_1.bind(('0.0.0.1', 4455))
        socket_2 = Socket(MockPythonSocket())
        socket_2.bind(('0.0.0.2', 4456))
        dict_list = [{'socket': socket_1, 'type': 'Server'},
                     {'socket': socket_2, 'type': 'Client'}]
        test_TCP_Server.connected_clients = dict_list
        result = test_TCP_Server.set_connected_clients_table()
        assert isinstance(result, OrderedDict)
        assert result['Server'] == "('0.0.0.1', 4455)"
        assert result['Client'] == "('0.0.0.2', 4456)"

        socket_except = Socket(MockPythonSocket())
        socket_except._sockname = Exception
        test_TCP_Server.connected_clients = [{'socket': socket_except, 'type': None}]
        result = test_TCP_Server.set_connected_clients_table()
        assert result[None] == 'unconnected invalid socket'

    def test_print_status(self):
        test_TCP_Server = TCPServer()
        test_TCP_Server.print_status('test')

    def test_remove_client(self):
        test_TCP_Server = TCPServer()

        socket_1 = Socket(MockPythonSocket())
        socket_1.bind(('0.0.0.1', 4455))
        socket_2 = Socket(MockPythonSocket())
        socket_2.bind(('0.0.0.2', 4456))
        dict_list = [{'socket': socket_1, 'type': 'Server'},
                     {'socket': socket_2, 'type': 'Client'}]
        test_TCP_Server.connected_clients = dict_list

        settings = mock.Mock()
        test_TCP_Server.settings = settings

        test_TCP_Server.remove_client(socket_1)

        is_removed = True
        for socket_dict in test_TCP_Server.connected_clients:
            if 'Server' in socket_dict['type']:
                is_removed = False

        assert is_removed

        socket_except = mock.Mock()
        socket_except.close.side_effect = [Exception]

        dict_list = [{'socket': socket_except, 'type': 'Exception'}]
        test_TCP_Server.connected_clients = dict_list

        test_TCP_Server.remove_client(socket_except)

    @mock.patch('pymodaq.daq_utils.tcp_server_client.select.select')
    def test_select(self, mock_select):
        mock_select.return_value = ([1], [2], [3])
        test_TCP_Server = TCPServer()
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_mock_socket = MockPythonSocket()
        test_mock_socket.socket = test_socket
        result = np.array(test_TCP_Server.select([test_mock_socket]))
        assert np.array_equal(result, np.array([[1], [2], [3]]))

    @mock.patch('pymodaq.daq_utils.tcp_server_client.TCPServer.select')
    def test_listen_client(self, mock_select):
        socket_1 = Socket(MockPythonSocket())
        socket_1.bind(('0.0.0.1', 4455))
        socket_2 = Socket(MockPythonSocket())
        socket_2.bind(('0.0.0.2', 4456))
        socket_3 = Socket(MockPythonSocket())
        socket_3.bind(('0.0.0.3', 4457))
        socket_4 = Socket(MockPythonSocket())
        socket_4.bind(('0.0.0.4', 4458))
        socket_5 = Socket(MockPythonSocket())
        socket_5.bind(('0.0.0.5', 4459))
        socket_6 = Socket(MockPythonSocket())
        socket_6.bind(('0.0.0.6', 4460))

        socket_1.send_string('')
        socket_2.send_string('Done')
        socket_3.send_string('Quit')
        socket_4.send_string('unknown')
        socket_5.send_string('test')
        socket_6.send_string('Server')
        mock_select.return_value = [[socket_2, socket_3, socket_4, socket_5],
                                    [],
                                    [socket_1]]

        test_TCP_Server = TCPServer()
        dict_list = [{'socket': socket_1, 'type': 'Server'},
                     {'socket': socket_2, 'type': 'Client'},
                     {'socket': socket_3, 'type': 'Client'},
                     {'socket': socket_4, 'type': 'Unknown'},
                     {'socket': socket_5, 'type': 'test'},
                     {'socket': socket_6, 'type': 'serversocket'}]

        test_TCP_Server.connected_clients = dict_list
        settings = mock.Mock()
        test_TCP_Server.settings = settings
        test_TCP_Server.serversocket = socket_5
        test_TCP_Server.socket_types = []
        test_TCP_Server.listen_client()

        is_removed = True
        for socket_dict in test_TCP_Server.connected_clients:
            if 'Server' in socket_dict['type']:
                is_removed = False
        assert is_removed

        mock_select.return_value = [[socket_6], [], []]

        test_TCP_Server.serversocket = socket_6
        test_TCP_Server.socket_types = ['Server']
        test_TCP_Server.listen_client()

    def test_send_command(self):
        test_TCP_Server = TCPServer()
        test_Socket = Socket(MockPythonSocket())
        test_TCP_Server.message_list = []
        test_TCP_Server.send_command(test_Socket)

        test_TCP_Server.message_list = ['move_at']
        test_TCP_Server.send_command(test_Socket)

    @mock.patch('pymodaq.daq_utils.tcp_server_client.print')
    def test_emit_status(self, mock_print):
        mock_print.side_effect = [ValueError]
        test_TCP_Server = TCPServer()

        with pytest.raises(TypeError):
            test_TCP_Server.emit_status()

    def test_read_data(self):
        test_TCP_Server = TCPServer()
        assert not test_TCP_Server.read_data(MockPythonSocket())

    def test_send_data(self):
        test_TCP_Server = TCPServer()
        assert not test_TCP_Server.send_data(MockPythonSocket(), [1, 2, 3])

    @mock.patch('pymodaq.daq_utils.tcp_server_client.TCPServer.find_socket_within_connected_clients')
    def test_process_cmds(self, mock_find_socket):
        mock_find_socket.return_value = Socket(MockPythonSocket())
        test_TCP_Server = TCPServer()
        commands = ['Done', 'Infos', 'Info_xml', 'Info', 'test']

        test_TCP_Server.message_list = commands
        assert not test_TCP_Server.process_cmds('unknown')

        assert not test_TCP_Server.process_cmds('Done')

        test_Socket = Socket(MockPythonSocket())
        test_Socket.send_string('test')
        mock_find_socket.return_value = test_Socket
        test_TCP_Server.process_cmds('Infos')

        test_Socket = Socket(MockPythonSocket())
        test_Socket.send_list([1, 2, 3])
        test_Socket.send_string('test')
        mock_find_socket.return_value = test_Socket
        with pytest.raises(Exception):
            test_TCP_Server.process_cmds('Info_xml')

        test_Socket = Socket(MockPythonSocket())
        test_Socket.send_string('info')
        test_Socket.send_string('data')
        mock_find_socket.return_value = test_Socket
        test_TCP_Server.process_cmds('Info')

        assert not test_TCP_Server.process_cmds('test')

    @mock.patch('pymodaq.daq_utils.parameter.ioxml.XML_string_to_parameter')
    def test_read_infos(self, mock_string):
        mock_string.return_value = 'test'
        settings = mock.Mock()
        child = mock.Mock()
        child.restoreState.side_effect = [TypeError]
        settings.child.return_value = child

        test_TCP_Server = TCPServer()
        test_TCP_Server.settings = settings

        with pytest.raises(TypeError):
            test_TCP_Server.read_infos()

    @mock.patch('pymodaq.daq_utils.parameter.ioxml.XML_string_to_parameter')
    def test_read_info_xml(self, mock_string):
        mock_string.return_value = ['test']
        test_TCP_Server = TCPServer()
        settings = mock.Mock()
        settings.child.side_effect = [Exception]
        test_TCP_Server.settings = settings
        test_Socket = Socket(MockPythonSocket())
        test_Socket.send_list(['test'])
        test_Socket.send_string('test')

        with pytest.raises(Exception):
            test_TCP_Server.read_info_xml(test_Socket)

        param_here = mock.Mock()
        param_here.restoreState.side_effect = [TypeError]
        settings = mock.Mock()
        settings.child.return_value = param_here
        test_TCP_Server.settings = settings
        test_Socket.send_list(['test'])
        test_Socket.send_string('test')
        with pytest.raises(TypeError):
            test_TCP_Server.read_info_xml(test_Socket)

    @mock.patch('pymodaq.daq_utils.parameter.utils.iter_children')
    def test_read_info(self, mock_iter_children):
        mock_iter_children.return_value = ['an_info']
        test_TCP_Server = TCPServer()
        settings = mock.Mock()
        child = mock.Mock()
        child.addChild.side_effect = [None, TypeError]
        child.setValue.side_effect = [ValueError]
        settings.child.return_value = child
        test_TCP_Server.settings = settings

        test_TCP_Server.read_info(test_info='another_info')
        with pytest.raises(TypeError):
            test_TCP_Server.read_info(test_info='another_info')

        with pytest.raises(ValueError):
            test_TCP_Server.read_info()


class TestMockServer:
    def test_init(self):
        test_MockServer = MockServer()
        assert isinstance(test_MockServer, MockServer)