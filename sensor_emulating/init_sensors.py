from sensor_emulating import graphical_sensor_emulator, airflow_speed_sensor, airflow_direction_sensor
import threading
import copy

value_dict = {"speed": 0, "degree": 0}


def check_pin(pin_factory):
    while True:
        if pin_factory.pin(20).state == 1 and pin_factory.pin(18).state == 1:
            current_values = copy.copy(value_dict)
            airflow_speed_sensor.signaling(pin_factory, current_values["speed"], 1)
            airflow_speed_sensor.signaling(pin_factory, current_values["speed"], 2)
            airflow_direction_sensor.signaling(pin_factory, current_values["degree"])
        else:
            continue


def init_sensors(pin_factory):
    thread_check_pin = threading.Thread(target=check_pin, args=(pin_factory,))
    thread_check_pin.start()

    graphical_sensor_emulator.init_window(value_dict)
