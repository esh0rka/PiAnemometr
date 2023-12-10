import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from client_anemometr import run_client
from time import sleep
import matplotlib.pyplot as plt
import datetime
import csv


def open_new_window():
    def open_file():
        file_path = filedialog.askopenfilename()

        listbox.delete(0, tk.END)

        with open(file_path, 'r', newline='') as csvfile:
            fieldnames = ['Speed', 'Direction', 'DataTime']
            csvreader = csv.reader(csvfile)
            header = next(csvreader)

            for row in csvreader:
                #columns = row.split(',')
                speed_value_row = float(row[0])

                if speed_value_row < 100:
                    string_value = 'Data: ' + str(row[2])[:22] + \
                                   ', speed: ' + str(row[0]) + ' м/с' + \
                                   ', direction: ' + str(row[1]) + '°'
                else:
                    if speed_value_row == 100:
                        string_value = 'Data: ' + str(row[2])[:22] + \
                                       ', speed sensor calibration error' + \
                                       ', direction: ' + str(row[1]) + '°'
                    else:
                        string_value = 'Data: ' + str(row[2])[:22] + \
                                       ', speed sensor ' + str(int(speed_value_row % 100)) + ' error' + \
                                       ', direction: ' + str(row[1]) + '°'
                listbox.insert(tk.END, string_value)

    def save_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['Speed', 'Direction', 'DataTime']
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fieldnames)
            for row in value_list:
                csvwriter.writerow(row)

    new_window = tk.Toplevel(root)
    new_window.title("Статистика считываний")

    button_frame = tk.Frame(new_window)
    button_frame.pack()

    button = tk.Button(button_frame, text="Открыть файл", command=open_file)
    button.pack(side='left')

    button = tk.Button(button_frame, text="Сохранить текущие данные", command=save_file)
    button.pack(side='right')

    listbox = tk.Listbox(new_window, width=60, height=30)
    listbox.pack()

    for value in value_list:
        speed_value = value[0]

        if speed_value < 100:
            string_value = 'Data: ' + str(value[2])[:22] + \
                           ', speed: ' + str(value[0]) + ' м/с' + \
                           ', direction: ' + str(value[1]) + '°'
        else:
            if speed_value == 100:
                string_value = 'Data: ' + str(value[2])[:22] + \
                               ', speed sensor calibration error' + \
                               ', direction: ' + str(value[1]) + '°'
            else:
                string_value = 'Data: ' + str(value[2])[:22] + \
                               ', speed sensor ' + str(int(speed_value % 100)) + ' error' + \
                               ', direction: ' + str(value[1]) + '°'
        listbox.insert(tk.END, string_value)


parameters = [True, 1.0]

value_list = []

client_thread = threading.Thread(target=run_client, args=(value_list, parameters,))
client_thread.start()

sleep(2)

reader_signal_script_path = './read_signals.py'
subprocess.Popen(['python', reader_signal_script_path])


def get_sideways(direction_degree: float):
    if 11.2 < direction_degree < 33.8:
        return 'ССВ'
    elif 33.8 <= direction_degree < 56.3:
        return 'СВ'
    elif 56.3 <= direction_degree < 78.8:
        return 'ВСВ'
    elif 78.8 <= direction_degree < 101.3:
        return 'В'
    elif 101.3 <= direction_degree < 123.8:
        return 'ВЮВ'
    elif 123.8 <= direction_degree < 146.3:
        return 'ЮВ'
    elif 146.3 <= direction_degree < 168.8:
        return 'ЮЮВ'
    elif 168.8 <= direction_degree < 191.3:
        return 'Ю'
    elif 168.8 <= direction_degree < 191.3:
        return 'Ю'
    elif 191.3 <= direction_degree < 213.8:
        return 'ЮЮЗ'
    elif 213.8 <= direction_degree < 236.3:
        return 'ЮЗ'
    elif 236.3 <= direction_degree < 258.8:
        return 'ЗЮЗ'
    elif 258.8 <= direction_degree < 281.3:
        return 'З'
    elif 281.3 <= direction_degree < 303.8:
        return 'ЗСЗ'
    elif 303.8 <= direction_degree < 326.3:
        return 'СЗ'
    elif 326.3 <= direction_degree < 348.8:
        return 'ССЗ'
    else:
        return 'С'


def value_visualization():
    while True:
        if parameters[0]:
            return
        sleep(1)
        if value_list:
            if not value_list[-1][0] >= 100:
                current_speed_value_label['text'] = str(value_list[-1][0]) + ' м/с'
            else:
                current_speed_value_label['text'] = 'error'
            current_direction_value_label['text'] = str(value_list[-1][1]) + '° (' + get_sideways(value_list[-1][1]) + ')'
            update_plot()


def start_read():
    value_visualization_thread = threading.Thread(target=value_visualization)
    global parameters

    if parameters[0]:
        start_read_button["text"] = 'Стоп'
        parameters[0] = False
        parameters[1] = float(interval_entry.get())
        value_visualization_thread.start()
    else:
        start_read_button["text"] = 'Начать считывание'
        parameters[0] = True


root = tk.Tk()

root.geometry("600x300")

root.title("Графическое приложение анемометра")

start_read_button = tk.Button(root, text="Начать считывание", font=("Arial", 15), command=start_read, width=15,
                              height=2)
start_read_button.place(x=5, y=5)

interval_label = tk.Label(root, text="Интервал (s): ", font=("Arial", 20))
interval_label.place(x=190, y=12)

interval_entry = tk.Entry(root, width=5, text="1", font=("Arial", 15))
interval_entry.place(x=325, y=15)
interval_entry.insert(0, '1')

current_speed_label = tk.Label(root, text="Текущая скорость: ", font=("Arial", 15))
current_speed_label.place(x=7, y=55)

current_direction_label = tk.Label(root, text="Текущее направление: ", font=("Arial", 15))
current_direction_label.place(x=225, y=55)

current_speed_value_label = tk.Label(root, text="0 м/с", font=("Arial", 15), fg="blue")
current_speed_value_label.place(x=145, y=55)

current_direction_value_label = tk.Label(root, text="0", font=("Arial", 15), fg="blue")
current_direction_value_label.place(x=393, y=55)

open_statistics_button = tk.Button(root, text="Открыть статистику", command=open_new_window)
open_statistics_button.place(x=430, y=5)

fig, ax = plt.subplots(figsize=(6, 2))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=0, y=90)


def update_plot():
    xs = []
    ys = []

    pickup_number = -101

    for value in value_list[-1:pickup_number:-1]:
        speed_value = float(value[0])

        if not speed_value >= 100:
            xs.append((value[2] - datetime.datetime.now()).total_seconds())
            ys.append(float(speed_value))
        else:
            pickup_number -= 1

    print('xs:', xs, ' ', ys)

    ax.clear()
    ax.plot(xs, ys)
    sleep(1)

    plt.xlabel('Количество секунд до текущего момента')
    plt.ylabel('Скорость')
    plt.title('Скорость потока воздуха за последниее 100 считываний')

    canvas.draw()

update_plot()

root.mainloop()
