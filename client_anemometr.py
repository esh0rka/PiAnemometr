import socket
import struct
import datetime
from time import sleep


def run_client(value_list: list, parametrs):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('localhost', 51103))

    server_socket.listen(1)

    connection, client_address = server_socket.accept()

    while True:
        received_bytes = connection.recv(8)
        received_floats = struct.unpack('ff', received_bytes)

        speed_value = round(received_floats[0], 1)
        direction_value = round(received_floats[1], 2)

        print('speed_value:', speed_value, '\ndirection_value: ', direction_value)

        if parametrs[0]:
            continue

        if value_list:
            if (datetime.datetime.now() - value_list[-1][2]).total_seconds() > parametrs[1]:
                print('ALLO: ', (datetime.datetime.now() - value_list[-1][2]).total_seconds())
                print('ALLO: ', parametrs[1])
                value_list.append((speed_value, direction_value, datetime.datetime.now()))
        else:
            value_list.append((speed_value, direction_value, datetime.datetime.now()))

    connection.close()
    server_socket.close()
