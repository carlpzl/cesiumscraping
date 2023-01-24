import csv
import os
import shutil
import time

FIELDS_ATTRIBUTES = ['serial number', 'pid', 'area', 'cesium board id', 'logs board id', 'result']


class ControlFiles(object):

    def __init__(self):
        self.base_path = "C:\\Users\\cperezlo\\PycharmProjects\\Temp_download\\"
        self.logs_path = "{0}{1}".format(self.base_path, "logs\\")
        self.path_log_dowloaded = ''

    def remove_file(self, path):
        if os.path.exists(path):
            os.remove(path)
        else:
            print("The file does not exist")

    def get_log_downloaded(self):
        folder_content = os.listdir(self.base_path)
        file = ''
        for element in folder_content:
            if not os.path.isdir(os.path.join(self.base_path, element)):
                file = element
        return file

    def move_and_rename_file(self, file, unit_data):
        new_name_file = '{0}_{1}_{2}'.format(unit_data.serial_number, unit_data.area, unit_data.log_name)
        shutil.move('{0}{1}'.format(self.base_path, file), '{0}{1}'.format(self.logs_path, new_name_file))
        return new_name_file

    def open_file_logs_by_lines(self, file_name):
        file = open("{0}{1}".format(self.logs_path, file_name), encoding="utf-8")
        data_file = file.readlines()
        file.close()

        return data_file

    def create_or_add_data_csv_file(self, path_file, dictionary_data):

        with open(path_file, mode='a', newline='', encoding='utf-8') as file:
            writer_file = csv.DictWriter(file, fieldnames=FIELDS_ATTRIBUTES)
            writer_file.writerow(dictionary_data)

            file.close()

    def get_list_of_inputs(self, file_name):
        file = open(file_name, encoding="utf-8")
        data_file = file.readlines()
        file.close()
        list_of_list = [line.split(',') for line in data_file]
        return list_of_list

    def wait_download_file(self):
        downloading = self.__download_started()
        while downloading:
            time.sleep(0.2)
            downloading = False
            for file_name in os.listdir(self.base_path):
                print(file_name)
                if file_name.endswith('.crdownload') or file_name.endswith('.tmp'):
                    print(file_name)
                    downloading = True

        print('DONWLOAD FINISHED')

    def __download_started(self):
        download_started = False
        count = 0
        while not download_started:

            for file_name in os.listdir(self.base_path):
                if file_name.endswith('.crdownload') or file_name.endswith('.tmp'):
                    print(file_name)
                    download_started = True
                    print('DOWNLOAD STARTED')
            if count == 10000:
                raise Exception("the download never started")
            count += 1
        return download_started

    def clear_temp_download_folder(self):
        for file_name in os.listdir(self.base_path):
            print(file_name)
            if not os.path.isdir(os.path.join(self.base_path, file_name)):
                os.remove("{0}{1}".format(self.base_path, file_name))
