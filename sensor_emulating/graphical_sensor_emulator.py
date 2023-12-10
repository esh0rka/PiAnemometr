import math
import tkinter as tk
import os


def start_drag(event):
    global arrow_end
    arrow_end = event.x, event.y


def drag(event, value_list: dict):
    global arrow_end

    canvas.coords(arrow, 200, 200, event.x, event.y)
    arrow_end = event.x, event.y

    new_degree_label_text = str(round(get_degrees(event.x, event.y), 1)) + "°"
    value_list["degree"] = round(get_degrees(event.x, event.y), 1)
    update_degree_label_text(new_degree_label_text)

    new_speed_label_text = str(round(get_speed(event.x, event.y), 2)) + " м/с"
    value_list["speed"] = round(get_speed(event.x, event.y), 2)
    update_speed_label_text(new_speed_label_text)



def stop_drag(event):
    pass


def update_degree_label_text(new_text):
    canvas.itemconfig(text, text=new_text)


def update_speed_label_text(new_text):
    canvas.itemconfig(speed_label_text, text=new_text)


def get_speed(arrow_x, arrow_y):
    COEFFICIENT_1 = 40
    COEFFICIENT_2 = 10
    COEFFICIENT_3 = 3

    center_x, center_y = 200, 200

    speed = math.sqrt(math.pow(arrow_x - center_x, 2) + math.pow(arrow_y - center_y, 2))

    if speed <= 40:
        speed /= COEFFICIENT_1
    elif speed <= 130:
        speed /= COEFFICIENT_2
        speed -= 3
    else:
        speed /= COEFFICIENT_3
        speed -= 33.3

    return speed


def get_degrees(arrow_x, arrow_y):
    center_x, center_y = 200, 200

    angle_radians = math.atan2(arrow_x - center_x, arrow_y - center_y)
    angle_degrees = math.degrees(angle_radians)
    angle_degrees = 180 - angle_degrees

    return angle_degrees


def init_window(values_list: dict, debug_values: list):
    def on_checkbox_debug_toggle():
        if checkbox_debug_var.get():
            debug_values[1] = True
        else:
            debug_values[1] = False

    def submit_debug_probability():
        entered_probability = float(debug_entry.get())
        debug_values[0] = entered_probability

    root = tk.Tk()
    root.title("Симуляция скорости и направления потока воздуха")

    global canvas
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    start_x, start_y = 200, 200

    IMAGE_SRC = "./sensor_emulating/img/339161_41_i_056.png"

    if not os.path.exists(IMAGE_SRC):
        IMAGE_SRC = "./img/339161_41_i_056.png"

    if os.path.exists(IMAGE_SRC):
        image = tk.PhotoImage(file=IMAGE_SRC)
        resized_image = image.subsample(2)
        canvas.create_image(start_x, start_y, image=resized_image, anchor=tk.CENTER)

    global arrow
    arrow = canvas.create_line(start_x, start_y, start_x, start_y, width=5, arrow=tk.LAST, fill="red")
    degree_label = canvas.create_text(20, 20, text="Направление потока воздуха: ", fill="black", anchor="w")
    global text
    text = canvas.create_text(215, 20, text="Не выбрано", fill="blue", anchor="w")
    speed_label = canvas.create_text(20, 40, text="Скорость потока воздуха: ", fill="black", anchor="w")
    global speed_label_text
    speed_label_text = canvas.create_text(190, 40, text="Не выбрано", fill="blue", anchor="w")

    checkbox_debug_var = tk.BooleanVar()
    checkbox_debug = tk.Checkbutton(root, text="Симуляция поломки", variable=checkbox_debug_var, command=on_checkbox_debug_toggle)
    checkbox_debug.place(x=15, y=48)

    debug_entry = tk.Entry(root, width=5)
    debug_entry.place(x=180, y=48)

    submit_button = tk.Button(root, text="Раскалибровать", command=submit_debug_probability)
    submit_button.place(x=240, y=46)

    canvas.bind("<Button-1>", start_drag)
    canvas.bind("<B1-Motion>", lambda event: drag(event, values_list))
    canvas.bind("<ButtonRelease-1>", stop_drag)

    root.mainloop()
