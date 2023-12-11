import random
from time import sleep


def signaling(pin_factory, value, sensor_number=1, error_probability=0.0, malfunction_simulation=False):
    if sensor_number == 2:
        if error_probability != 0:
            random_number = random.randint(1, 100)
            if random_number < error_probability * 100:
                value += 2.0

        if malfunction_simulation:
            random_number = random.randint(1, 5)
            if random_number == 1:
                sleep(6)
                return

        value = str('{:.2f}'.format(value)).replace('.', '')
        value = "{0:014b}".format(int(value))

        for index, bit in enumerate(value):
            # match bit:
            #     case '1':
            #         pin_factory.pin(21).drive_high()
            #     case '0':
            #         pin_factory.pin(21).drive_low()

            if bit == '1':
                pin_factory.pin(21).drive_high()
            else:
                pin_factory.pin(21).drive_low()

            pin_factory.pin(22).drive_low()

            while pin_factory.pin(22).state == 0:
                if index == len(value) - 1:
                    return

    value = str('{:.2f}'.format(value)).replace('.', '')
    value = "{0:014b}".format(int(value))

    for index, bit in enumerate(value):
        # match bit:
        #     case '1':
        #         pin_factory.pin(19).drive_high()
        #     case '0':
        #         pin_factory.pin(19).drive_low()

        if bit == '1':
            pin_factory.pin(19).drive_high()
        else:
            pin_factory.pin(19).drive_low()

        pin_factory.pin(20).drive_low()

        while pin_factory.pin(20).state == 0:
            if index == len(value) - 1:
                return
