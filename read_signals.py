from sensor_emulating import init_sensors
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from time import sleep
import threading
import socket
import struct
from itertools import combinations
from datetime import datetime

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

    last_reading_time_speed_1 = datetime.now()
    last_reading_time_speed_2 = datetime.now()

    while True:
        if len(speed_bits) != 0 and len(speed_bits) != 14 and (datetime.now() - last_reading_time_speed_1).total_seconds() > 5:
            print('TIME: ', last_reading_time_speed_1, '\nCURR: ', datetime.now(), 'BITS: ', speed_bits)
            print('DIFF: ', (datetime.now() - last_reading_time_speed_1).total_seconds())
            speed_bits = '11111111111111'
            speed_bits_additional_sensor = '11111111111110'
            direction_bits = '000000000000'
        elif len(speed_bits_additional_sensor) != 14 \
                and (datetime.now() - last_reading_time_speed_2).total_seconds() > 5:
            speed_bits = '11111111111110'
            speed_bits_additional_sensor = '11111111111111'
            direction_bits = '000000000000'

        if len(speed_bits) != 14 and Device.pin_factory.pin(20).state == 0:
            last_reading_time_speed_1 = datetime.now()

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
            last_reading_time_speed_2 = datetime.now()

            if Device.pin_factory.pin(21).state == 1:
                speed_bits_additional_sensor += '1'
            else:
                speed_bits_additional_sensor += '0'

            if len(speed_bits_additional_sensor) == 14:
                speed_value_additional_sensor = str(int(speed_bits_additional_sensor, 2))
                speed_value_additional_sensor = float(
                    speed_value_additional_sensor[:-2] + '.' + speed_value_additional_sensor[-2:])
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

            if speed_bits == '11111111111111':
                output_speed_value = float(101)
                direction_value = float(0)
            elif speed_bits_additional_sensor == '11111111111111':
                output_speed_value = float(102)
                direction_value = float(0)
            else:
                speed_sensors_values = [speed_value, speed_value_additional_sensor]
                output_speed_value = speed_sensors_test(speed_sensors_values)

            float_bytes = struct.pack('ff', output_speed_value, direction_value)
            client_socket.sendall(float_bytes)

            speed_bits = ''
            speed_bits_additional_sensor = ''
            direction_bits = ''

            last_reading_time_speed_1 = datetime.now()
            last_reading_time_speed_2 = datetime.now()

            sleep(0.1)

    client_socket.close()


def speed_sensors_test(sensors_values):
    if len(sensors_values) < 2:
        return None

    pairs = list(combinations(sensors_values, 2))
    differences = [abs(x - y) for x, y in pairs]
    difference = sum(differences) / len(differences)

    if not difference >= 0.3:
        average_value = sum(sensors_values) / len(sensors_values)

        return float(average_value)
    else:
        return float(100.0)


handler_thread = threading.Thread(target=get_values)
handler_thread.start()

init_sensors.init_sensors(Device.pin_factory)
