def signaling(pin_factory, value, sensorNumber = 1):
    value = str('{:.2f}'.format(value)).replace('.', '')
    value = "{0:014b}".format(int(value))

    if sensorNumber == 2:
        for index, bit in enumerate(value):
            match bit:
                case '1':
                    pin_factory.pin(21).drive_high()
                case '0':
                    pin_factory.pin(21).drive_low()

            pin_factory.pin(22).drive_low()

            while pin_factory.pin(22).state == 0:
                if index == len(value) - 1:
                    return

    for index, bit in enumerate(value):
        match bit:
            case '1':
                pin_factory.pin(19).drive_high()
            case '0':
                pin_factory.pin(19).drive_low()

        pin_factory.pin(20).drive_low()

        while pin_factory.pin(20).state == 0:
            if index == len(value) - 1:
                return
