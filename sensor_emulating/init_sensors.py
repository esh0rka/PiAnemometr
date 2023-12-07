from sensor_emulating import graphical_sensor_emulator, airflow_speed_sensor, airflow_direction_sensor
import threading

value_dict = {"speed": 0, "degree": 0}


def check_pin(pin_factory):
    while True:
        if pin_factory.pin(20).state == 1 and pin_factory.pin(18).state == 1:
            airflow_speed_sensor.signaling(pin_factory, value_dict["speed"])
            airflow_direction_sensor.signaling(pin_factory, value_dict["degree"])
        else:
            continue


def init_sensors(pin_factory):
    thread_check_pin = threading.Thread(target=check_pin, args=(pin_factory,))
    thread_check_pin.start()

    graphical_sensor_emulator.init_window(value_dict)
