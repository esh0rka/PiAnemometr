from sensor_emulating import init_sensors
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from time import sleep
import threading

Device.pin_factory = MockFactory()
Device.pin_factory.pin(18).drive_low()
Device.pin_factory.pin(20).drive_low()


def get_values():
    sleep(1)
    Device.pin_factory.pin(18).drive_high()
    Device.pin_factory.pin(20).drive_high()

    speed_bits = ''
    direction_bits = ''

    while True:
        if len(speed_bits) != 14 and Device.pin_factory.pin(20).state == 0:
            if Device.pin_factory.pin(19).state == 1:
                speed_bits += '1'
            else:
                speed_bits += '0'

            if len(speed_bits) == 14:
                print('speed_bits = ', speed_bits)
            else:
                Device.pin_factory.pin(20).drive_high()

        if len(direction_bits) != 12 and Device.pin_factory.pin(18).state == 0:
            if Device.pin_factory.pin(17).state == 1:
                direction_bits += '1'
            else:
                direction_bits += '0'

            if len(direction_bits) == 12:
                print('direction_bits = ', direction_bits)
            else:
                Device.pin_factory.pin(18).drive_high()

        if len(speed_bits) == 14 and len(direction_bits) == 12:
            Device.pin_factory.pin(20).drive_high()
            Device.pin_factory.pin(18).drive_high()
            speed_bits = ''
            direction_bits = ''
            sleep(1)


handler_thread = threading.Thread(target=get_values)
handler_thread.start()

init_sensors.init_sensors(Device.pin_factory)


