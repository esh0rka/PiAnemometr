def signaling(pin_factory, value):
    value = str('{:.1f}'.format(value)).replace('.', '')
    value = "{0:012b}".format(int(value))

    for index, bit in enumerate(value):
        match bit:
            case '1':
                pin_factory.pin(17).drive_high()

            case '0':
                pin_factory.pin(17).drive_low()
        pin_factory.pin(18).drive_low()
        while pin_factory.pin(18).state == 0:
            if index == len(value) - 1:
                return
