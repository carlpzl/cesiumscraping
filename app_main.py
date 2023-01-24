import tkinter
from tkinter import *
from Control_main import ControlMain
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
import time
import threading


class AppMain(object):

    def __init__(self):
        self.__images = []
        self.__last_width_window = 0
        self.__last_height_window = 0
        self.__window = Tk()
        self.__window_image = ImageTk.PhotoImage(file="images/bg_cisco_2.jpg")
        self.__window_canvas = Canvas(self.__window, highlightthickness=0)

        self.__progress_bar_attribute_progress = 0
        self.__progress_bar_test_progress = 0
        self.__progress_bar_attribute = ttk.Progressbar(self.__window_canvas, orient=HORIZONTAL, length=200,
                                                        mode='determinate')

        self.__progress_bar_test = ttk.Progressbar(self.__window_canvas, orient=HORIZONTAL, length=200,
                                                   mode='determinate')

        self.__input_serial_number = Entry(self.__window_canvas)
        self.__input_test_area = Entry(self.__window_canvas)
        self.__input_log_name = Entry(self.__window_canvas)
        self.__input_attribute_name = Entry(self.__window_canvas)
        self.__input_show_file_name = Entry(self.__window_canvas)
        self.__input_show_file_name_test = Entry(self.__window_canvas)

        self.__download_log_button = ttk.Button(self.__window_canvas)
        self.__download_tst_button = ttk.Button(self.__window_canvas)
        self.__download_attributes_button = ttk.Button(self.__window_canvas)
        self.__open_file_button = ttk.Button(self.__window_canvas)
        self.__use_file_button = ttk.Button(self.__window_canvas)
        self.__open_file_test_button = ttk.Button(self.__window_canvas)
        self.__use_file_test_button = ttk.Button(self.__window_canvas)
        self.__create_csv_attribute_file = ttk.Button(self.__window_canvas)
        self.__get_data_from_log_button = ttk.Button(self.__window_canvas)

        self.__control_main = ControlMain()
        self.create_widgets()
        self.run_main_window()

    def create_widgets(self):
        self.__window.title("Cesium Scraping")
        self.__window.iconbitmap("images/Cisco2.ico")
        self.__window.geometry("800x500")
        self.__window_canvas.pack(fill="both", expand=True)

        self.__download_log_button['text'] = 'Download log'
        self.__download_log_button.bind('<Button-1>', self.download_log)

        self.__download_tst_button['text'] = 'Download logs by test area'
        self.__download_tst_button.bind('<Button-1>', self.download_logs_by_test_area)

        self.__download_attributes_button['text'] = "Download attributes"
        self.__download_attributes_button.bind('<Button-1>', self.download_attribute_excel)

        self.__get_data_from_log_button['text'] = "Get data log"
        self.__get_data_from_log_button.bind('<Button-1>', self.get_data_from_log)

        self.__create_csv_attribute_file['text'] = "get attribute"
        self.__create_csv_attribute_file['command'] = self.get_attribute_log_vs_cesium

        self.__input_show_file_name.insert(0, 'file to use')
        self.__open_file_button['text'] = "open file"
        self.__open_file_button['command'] = self.open_file

        self.__use_file_button['text'] = 'use file'
        self.__use_file_button['command'] = self.use_file_to_update_csv

        self.__input_show_file_name_test.insert(0, 'file to use test')
        self.__open_file_test_button['text'] = "open file"
        self.__open_file_test_button['command'] = self.open_file_test

        self.__use_file_test_button['text'] = 'use file'
        self.__use_file_test_button['command'] = self.use_file_to_test_unit

        self.__input_serial_number.place(relx=0.10, rely=0.25)
        self.__input_test_area.place(relx=0.10, rely=0.35)
        self.__input_log_name.place(relx=0.10, rely=0.45)
        self.__input_attribute_name.place(relx=0.10, rely=0.55)

        self.__create_csv_attribute_file.place(relx=0.10, rely=0.61)

        self.__input_show_file_name.place(relx=0.10, rely=0.78)
        self.__open_file_button.place(relx=0.35, rely=0.78)
        self.__use_file_button.place(relx=0.48, rely=0.78)
        self.__progress_bar_attribute.place(relx=0.61, rely=0.78)
        #self.__progress_bar_attribute.start()

        self.__input_show_file_name_test.place(relx=0.10, rely=0.91)
        self.__open_file_test_button.place(relx=0.35, rely=0.91)
        self.__use_file_test_button.place(relx=0.48, rely=0.91)
        self.__progress_bar_test.place(relx=0.61, rely=0.91)
        #self.__progress_bar_test.start()

        self.__window.bind('<Configure>', self.__resizer)

    def download_log(self, event):
        print('button working')
        print(self.__input_serial_number.get())
        self.__control_main.download_specific_log()

    def download_attribute_excel(self, event):
        print('button working')
        print(self.__input_serial_number.get())
        self.__control_main.download_attribute_by_serial_number()

    def get_data_from_log(self, event):
        print('button working for logs data')
        self.__control_main.get_data_from_buffer_log()

    def run_main_window(self):
        self.__window.mainloop()

    def download_logs_by_test_area(self, event):
        print('button to print last start by area from tst')
        serial_number_tst = self.__input_serial_number.get()
        test_area_tst = self.__input_test_area.get()
        log_name = self.__input_log_name.get()
        self.__control_main.download_logs_to_last_record_by_test_area(serial_number_tst, test_area_tst, log_name)

    def get_attribute_log_vs_cesium(self):
        inputs = self.__get_all_data_inputs()
        print(inputs)
        self.__control_main.all_steps_to_get_attribute(**inputs)

    def open_file(self):
        filename = filedialog.askopenfilename()
        self.__input_show_file_name.delete(0, END)
        self.__input_show_file_name.insert(0, filename)
        print(filename)

    def open_file_test(self):
        filename = filedialog.askopenfilename()
        self.__input_show_file_name_test.delete(0, END)
        self.__input_show_file_name_test.insert(0, filename)
        print(filename)

    def use_file_to_update_csv(self):

        worker = threading.Thread(target=self.run_serials_by_thread)
        worker.start()
        self.__use_file_button["state"] = "disabled"
        self.__progress_bar_attribute['value'] = 0
        self.__progress_bar_attribute_progress = 0
        self.__window_canvas.itemconfigure(self.__label_progress_attribute, text="0 %")

    def run_serials_by_thread(self):
        file_name = self.__input_show_file_name.get()
        print(self.__input_show_file_name.get())
        list_serial_numbers = self.__control_main.get_list_serial_numbers(file_name)

        for line in list_serial_numbers:
            inputs = {}
            inputs['serial_number'] = line[0]
            inputs['test_area'] = line[1]
            inputs['log_name'] = line[2]
            inputs['attribute_name'] = line[3].split("\n")[0]
            print(inputs)
            self.__control_main.all_steps_to_get_attribute(**inputs)

            self.__progress_bar_attribute['value'] += (100/len(list_serial_numbers))
            self.__progress_bar_attribute_progress = self.__progress_bar_attribute['value']
            self.__window_canvas.itemconfigure(self.__label_progress_attribute, text="{0} %".format(round(self.__progress_bar_attribute_progress, 1)))
            self.__window.update_idletasks()
            time.sleep(1)
            print('serial number done: {}'.format(inputs['serial_number']))
        self.__use_file_button["state"] = "enable"

    def use_file_to_test_unit(self):
        worker_test = threading.Thread(target=self.run_test_serials_by_thread)
        worker_test.start()
        self.__use_file_test_button["state"] = "disabled"
        self.__progress_bar_test['value'] = 0
        self.__progress_bar_test_progress = 0
        self.__window_canvas.itemconfigure(self.__label_progress_test, text="0 %")

    def run_test_serials_by_thread(self):
        file_name = self.__input_show_file_name_test.get()
        print(self.__input_show_file_name_test.get())
        #self.__control_main.test_units_by_file(file_name)
        list_info_to_process = self.__control_main.control_files.get_list_of_inputs(file_name)
        print(list_info_to_process)
        self.__control_main.open_ssh_connection()
        for line in list_info_to_process:
            inputs = {}
            inputs['serial_number'] = line[0]
            inputs['pid'] = line[1]
            inputs['new board id'] = line[4]
            inputs['result'] = line[5].split("\n")[0]
            print(inputs)
            if inputs["result"] == 'unmatch':
                print('RUN TEST APOLLO')
                self.__control_main.test_apollo(**inputs)

            self.__progress_bar_test['value'] += (100 / len(list_info_to_process))
            self.__progress_bar_test_progress = self.__progress_bar_test['value']
            self.__window_canvas.itemconfigure(self.__label_progress_test, text="{0} %".format(
                round(self.__progress_bar_test_progress, 1)))
            self.__window.update_idletasks()
            time.sleep(1)
            print('serial number done: {}'.format(inputs['serial_number']))
            self.__use_file_test_button["state"] = "enable"

        self.__control_main.close_ssh_connection()

    def __call_all_steps_attribute(self, **inputs):
        self.__control_main.all_steps_to_get_attribute(**inputs)

    def __get_all_data_inputs(self):
        inputs = {}
        inputs['serial_number'] = self.__input_serial_number.get()
        inputs['test_area'] = self.__input_test_area.get()
        inputs['log_name'] = self.__input_log_name.get()
        inputs['attribute_name'] = self.__input_attribute_name.get()
        return inputs

    def __resizer(self, event):
        global background_to_resize, resized_background, new_background_resized
        background_to_resize = Image.open("images/bg_cisco_2.jpg")
        widget_name = str(event.widget)
        if widget_name == '.!canvas':
            resized_background = background_to_resize.resize((event.width, event.height), Image.ANTIALIAS)
            new_background_resized = ImageTk.PhotoImage(resized_background)
            self.__create_canvas(event.width, event.height)

    def __create_canvas(self, current_width, current_height):
        print(current_width)
        print(current_height)
        if current_height > 400 and current_width > 600:
            self.__window_canvas.create_image(0, 0, image=new_background_resized, anchor="nw")
            self.__window_canvas.create_rectangle(50, current_height * 0.70,  current_width - 50, (current_height * 0.702), fill="black")
            self.__window_canvas.create_text(current_width * 0.10, current_height * 0.21, text="Serial Number",
                                             font=("Helvetica", 10),
                                             fill="white", anchor="nw")
            self.__window_canvas.create_text(current_width * 0.10, current_height * 0.31, text="Test Area",
                                             font=("Helvetica", 10),
                                             fill="white", anchor="nw")
            self.__window_canvas.create_text(current_width * 0.10, current_height * 0.41, text="Log Name",
                                             font=("Helvetica", 10),
                                             fill="white", anchor="nw")
            self.__window_canvas.create_text(current_width * 0.10, current_height * 0.51, text="Attribute Name",
                                             font=("Helvetica", 10),
                                             fill="white", anchor="nw")
            self.__window_canvas.create_text(current_width * 0.10, current_height * 0.73, text="Get logs and attributes by file",
                                             font=("Helvetica", 10),
                                             fill="white", anchor="nw")
            self.__window_canvas.create_text(current_width * 0.10, current_height * 0.86, text="Automatic test serial number by file",
                                             font=("Helvetica", 10),
                                             fill="white", anchor="nw")
            self.__label_progress_attribute = self.__window_canvas.create_text((current_width * 0.61) + 212, (current_height * 0.78) + 3, text="{0} %".format(round(self.__progress_bar_attribute_progress, 1)),
                                             font=("Helvetica", 10),
                                             fill="white", anchor="nw")

            self.__label_progress_test = self.__window_canvas.create_text((current_width * 0.61) + 212, (current_height * 0.91) + 3, text="{0} %".format(round(self.__progress_bar_test_progress, 1)),
                                             font=("Helvetica", 10),
                                             fill="white", anchor="nw")

            self.__last_width_window = current_width
            self.__last_height_window = current_height
        else:
            self.__window.resizable(False, False)
            self.__window.geometry("{0}x{1}".format(self.__last_width_window, self.__last_height_window))
            self.__window.resizable(True, True)

    def __create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.__window.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
            self.__images.append(ImageTk.PhotoImage(image))
            self.__window_canvas.create_image(x1, y1, image=self.__images[-1], anchor='nw')
        self.__window_canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
