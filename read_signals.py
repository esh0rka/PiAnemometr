from sensor_emulating import init_sensors
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from time import sleep
import threading
import socket
import struct

Device.pin_factory = MockFactory()
Device.pin_factory.pin(18).drive_low()
Device.pin_factory.pin(20).drive_low()
Device.pin_factory.pin(22).drive_low()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 51103))


def get_values():
    sleep(1)
    Device.pin_factory.pin(18).drive_high()
    Device.pin_factory.pin(20).drive_high()
    Device.pin_factory.pin(22).drive_high()

    speed_bits = ''
    speed_bits_additional_sensor = ''
    direction_bits = ''

    while True:
        if len(speed_bits) != 14 and Device.pin_factory.pin(20).state == 0:
            if Device.pin_factory.pin(19).state == 1:
                speed_bits += '1'
            else:
                speed_bits += '0'

            if len(speed_bits) == 14:
                speed_value = str(int(speed_bits, 2))
                speed_value = float(speed_value[:-2] + '.' + speed_value[-2:])
                print('speed_value = ', speed_value)
                print('speed_bits = ', speed_bits)
            else:
                Device.pin_factory.pin(20).drive_high()

        if len(speed_bits_additional_sensor) != 14 and Device.pin_factory.pin(22).state == 0:
            if Device.pin_factory.pin(21).state == 1:
                speed_bits_additional_sensor += '1'
            else:
                speed_bits_additional_sensor += '0'

            if len(speed_bits_additional_sensor) == 14:
                speed_value_additional_sensor = str(int(speed_bits_additional_sensor, 2))
                speed_value_additional_sensor = float(speed_value_additional_sensor[:-2] + '.' + speed_value_additional_sensor[-2:])
                print('speed_value_additional_sensor = ', speed_value_additional_sensor)
                print('speed_bits_additional_sensor = ', speed_bits_additional_sensor)
            else:
                Device.pin_factory.pin(22).drive_high()

        if len(direction_bits) != 12 and Device.pin_factory.pin(18).state == 0:
            if Device.pin_factory.pin(17).state == 1:
                direction_bits += '1'
            else:
                direction_bits += '0'

            if len(direction_bits) == 12:
                direction_value = str(int(direction_bits, 2))
                direction_value = float(direction_value[:-1] + '.' + direction_value[-1:])
                print('direction_value = ', direction_value)
                print('direction_bits = ', direction_bits)
            else:
                Device.pin_factory.pin(18).drive_high()

        if len(speed_bits) == 14 and len(speed_bits_additional_sensor) == 14 and len(direction_bits) == 12:
            Device.pin_factory.pin(18).drive_high()
            Device.pin_factory.pin(20).drive_high()
            Device.pin_factory.pin(22).drive_high()

            float_bytes = struct.pack('ff', speed_value, direction_value)
            client_socket.sendall(float_bytes)

            speed_bits = ''
            speed_bits_additional_sensor = ''
            direction_bits = ''
            sleep(0.1)

    client_socket.close()

handler_thread = threading.Thread(target=get_values)
handler_thread.start()

init_sensors.init_sensors(Device.pin_factory)


