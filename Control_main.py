from Class_selenium_object import HandleWebPag
from Get_data_from_excel import ExcelFileData
from Control_file_system import ControlFiles
from store_objects import StoreObjects
from serial_number_object import SerialNumberObject
from data_from_logs import DataFromLogs
from automatic_test_unit import AutomaticUnitTest

import utilities
func_retry = utilities.func_retry

import time
import re
import datetime

PATH_EXCEL = r'C:\Users\cperezlo\PycharmProjects\Temp_download\download.xlsx'
PATH_LOGS = 'C:\\Users\\cperezlo\\PycharmProjectsl\\Temp_download\\logs\\'
PATH_CSV_ATTRIBUTE = r'C:\Users\cperezlo\PycharmProjects\Temp_download\csv_files\attribute.csv'


class ControlMain(object):

    def __init__(self):

        self.url = "https://cesium.cisco.com/apps/cesiumhome/overview" # "https://cesium.cisco.com/apps/PolarisSearch/Measures?SI=JAD26260C40&SearchIn=S&timeId=2022-06-27%2017:52:37"
        self.key_class_name = 'fi-setting'
        self.control_files = ControlFiles()
        self.element_path = {
            'filter_select': '//*[@id="main"]/div/div/div[2]/div[1]/div[3]/div[2]/div/div[1]/gridtable/span[2]/input',
            'type_input': '//*[@id="main"]/div/div/div[2]/div[1]/div[3]/div[2]/div/div[1]/gridtable/div[2]/div/div[2]/div[1]/div/div/div/div/div/div[6]/div[2]/div[3]/div/div/input',
            'name-input': '//*[@id="main"]/div/div/div[2]/div[1]/div[3]/div[2]/div/div[1]/gridtable/div[2]/div/div[2]/div[1]/div/div/div/div/div/div[3]/div[2]/div[3]/div/div/input',
            'close_name_input': '//*[@id="main"]/div/div/div[2]/div[1]/div[3]/div[2]/div/div[1]/gridtable/div[2]/div/div[2]/div[1]/div/div/div/div/div/div[3]/div[2]/div[3]/div/div/div/i',
            'button_download': '/html/body/div[12]/div/div/div[3]/button[1]',
            'button_close': '/html/body/div[12]/div/div/div[3]/button[2]',
            'button_toolings': '//*[@id="main"]/div/div/div[2]/div[1]/div[3]/div[2]/div/div[3]/div/div[1]/div[1]/i',
            'button_export_excel': '//*[@id="main"]/div/div/div[2]/div[1]/div[3]/div[2]/div/div[3]/div/div[1]/div[2]/div/div/ul/li[8]',
            'button_option_attribute_page': '//*[@id="main"]/div/div/div[2]/div[1]/div[3]/div[2]/div/gridtable[1]/div[2]/div/div[1]',
            'button_download_attribute_page': '//*[@id="main"]/div/div/div[2]/div[1]/div[3]/div[2]/div/gridtable[1]/div[2]/div/div[1]/div[2]/div/div/ul/li[4]',
        }

        self.unit_object = None

        self.list_names = ["sequence_log"]

        self.pag1 = HandleWebPag(self.url)

        self.store_objects = StoreObjects()

        self.data_logs = DataFromLogs(PATH_LOGS)

    @func_retry
    def download_specific_log(self, serial_number='JAD26260C40', record_date='2022-06-28 05:36:11', test_area='PCBST', log_name='sequence_log'):

        self.control_files.clear_temp_download_folder()
        self.__create_object(serial_number, test_area, log_name)
        self.list_names = [log_name]
        record_date_split = record_date.split(' ')
        url_beginnig = "https://cesium.cisco.com/apps/PolarisSearch/Measures?SI="
        url_middle = "&SearchIn=S&timeId="
        new_url = "{0}{1}{2}{3}%20{4}".format(url_beginnig, serial_number, url_middle,
                                            record_date_split[0], record_date_split[1])

        try:
            self.pag1.refresh_web(new_url)

        except:
            print('not page web starting')
            self.__start_web_pag()
            self.pag1.refresh_web(new_url)
        status_page = self.pag1.check_until_key_element_present_by_class_name(self.key_class_name)

        # Buscamos filter
        element = self.pag1.look_for_element_by_full_path(self.element_path['filter_select'])
        # dar click en filter select
        element.click()
        # buscar ahora el input type
        element = self.pag1.look_for_element_by_full_path(self.element_path['type_input'])
        # poner B en input type
        element.send_keys("B")
        # buscar el input names

        # recorrer cada name en ela lista name
        for name in self.list_names:
            element = self.pag1.look_for_element_by_full_path(self.element_path['name-input'])
            # poner el name actual
            element.send_keys(name)
            # buscar el elemento que tenga el view attach
            element = self.pag1.look_by_text_value("view attachment")
            # dar click sobre view attach
            element.click()
            # espera a encontar el donwload
            element = self.pag1.return_wait_element(self.element_path['button_download'])
            # dar click en download
            element.click()
            self.control_files.wait_download_file()
            # espera a que se descargue
            #time.sleep(20)
            # espera a encontrar el close
            element = self.pag1.return_wait_element(self.element_path['button_close'])
            # dar click en close
            element.click()
            # buscar el close del input name
            element = self.pag1.look_for_element_by_full_path(self.element_path['close_name_input'])
            # dar click en close de name
            element.click()
            # continuar con el siguente nombre
            time.sleep(2)
            file = self.control_files.get_log_downloaded()
            new_name_file = self.control_files.move_and_rename_file(file, self.unit_object)
            self.unit_object.file_buffer_log = new_name_file

        print('END PROCESS')
        #self.pag1.close_pag()

    @func_retry
    def download_logs_to_last_record_by_test_area(self, serial_number, test_area, log_name):
        self.__create_object(serial_number, test_area, log_name)
        self.control_files.clear_temp_download_folder()
        self.__download_tst_by_sn(serial_number)
        self.__get_all_data_from_excel()
        start_date = self.__get_date_start_by_test_area(test_area)
        print(start_date)
        self.download_specific_log(serial_number=serial_number, record_date=start_date, test_area=self.unit_object.area, log_name=self.unit_object.log_name)

    @func_retry
    def download_attribute_by_serial_number(self, serial_number='1920C541180825J', attribute='board id'):

        self.control_files.clear_temp_download_folder()

        url_beginnig = "https://cesium.cisco.com/apps/PolarisSearch/Attributes?SI="
        url_end = "&SearchIn=S"
        new_url = "{0}{1}{2}".format(url_beginnig, serial_number, url_end)

        try:
            self.pag1.refresh_web(new_url)
        except:
            print('not page web starting')
            self.__start_web_pag()
            self.pag1.refresh_web(new_url)

        element = self.pag1.return_wait_element(self.element_path['button_option_attribute_page'])
        element.click()
        element = self.pag1.return_wait_element(self.element_path['button_download_attribute_page'])
        element.click()
        self.control_files.wait_download_file()
        self.__get_all_data_from_excel()
        boards_id_found = self.__get_attribute_from_excel(attribute=attribute)
        self.unit_object.data['attributes']['board_id_cesium'] = boards_id_found
        print(boards_id_found)
        self.control_files.remove_file(PATH_EXCEL)

        print('END PROCESS')

    def get_data_from_buffer_log(self, data_to_find='BOARD_ID'):
        #self.unit_object = SerialNumberObject('1920C541180825J', 'FSYSFT', 'N818_SERVICE_CONSOLE_buffer')
        #self.unit_object.file_buffer_log = '1920C541180825J_FSYSFT_N818_SERVICE_CONSOLE_buffer'
        #self.unit_object.data = {'attributes': {}}
        file = self.unit_object.file_buffer_log
        lines_file = self.control_files.open_file_logs_by_lines(file)
        print(lines_file)
        found_data = self.data_logs.found_data(lines_file, data_to_find)
        print(found_data)
        if len(found_data) == 1:
            self.unit_object.data['attributes']['board_id_log'] = found_data[0]
            self.unit_object.board_id = found_data[0]
        else:
            self.unit_object.data['attributes']['board_id_log'] = found_data
        #self.__update_csv_attribute()

    def all_steps_to_get_attribute(self, **kwargs):
        print('into all steps funtion control main')
        print(kwargs)
        serial_number = kwargs.get('serial_number', 'no serial number')
        test_area = kwargs.get('test_area', 'none')
        log_name = kwargs.get('log_name', 'none')
        attribute_name = kwargs.get('attribute_name', 'none')
        self.download_logs_to_last_record_by_test_area(serial_number, test_area, log_name)
        self.download_attribute_by_serial_number(serial_number, attribute_name)
        self.get_data_from_buffer_log(attribute_name)
        self.__update_csv_attribute()

    def get_list_serial_numbers(self, file_name):
        list_info_to_process = self.control_files.get_list_of_inputs(file_name)
        print(list_info_to_process)
        return list_info_to_process

    def test_units_by_file(self, file_name):
        list_info_to_process = self.control_files.get_list_of_inputs(file_name)
        print(list_info_to_process)

        self.ssh_server_to_test = AutomaticUnitTest('172.30.85.120')
        self.ssh_server_to_test.open_connection()
        for line in list_info_to_process:
            inputs = {}
            inputs['serial_number'] = line[0]
            inputs['pid'] = line[1]
            inputs['new board id'] = line[4]
            inputs['result'] = line[5].split("\n")[0]
            print(inputs)
            if inputs["result"] == 'unmatch':
                print('RUN TEST APOLLO')
                self.test_apollo(**inputs)

        self.ssh_server_to_test.close_connection()

    def open_ssh_connection(self):
        self.ssh_server_to_test = AutomaticUnitTest('172.30.85.120')
        self.ssh_server_to_test.open_connection()

    def close_ssh_connection(self):
        self.ssh_server_to_test.close_connection()

    @func_retry
    def __download_tst_by_sn(self, serial_number_tst):

        url_part1 = "https://cesium.cisco.com/apps/PolarisSearch/Test?SI="
        url_sn = str(serial_number_tst)
        url_part2 = "&SearchIn=S"
        new_url = '{0}{1}{2}'.format(url_part1, url_sn, url_part2)
        try:
            self.pag1.refresh_web(new_url)
        except:
            print('not page web starting')
            self.__start_web_pag()
            self.pag1.refresh_web(new_url)

        element = self.pag1.return_wait_element(self.element_path['button_toolings'])
        element.click()
        element = self.pag1.return_wait_element(self.element_path['button_export_excel'])
        element.click()
        self.control_files.wait_download_file()

    def __get_all_data_from_excel(self):
        obj_excel_data = ExcelFileData(PATH_EXCEL)
        self.dict_data_excel = obj_excel_data.get_data()
        print(self.dict_data_excel)
        obj_excel_data = None

    def __get_date_start_by_test_area(self, test_area_to_look=''):

        field_record_time_name = self.__return_key_time_record_field_excel_dict()
        sign, time_offset = self.__get_time_offset_of_record_time_field(field_record_time_name)

        last_start_date_test_area = self.__get_last_test_area_time_start(field_record_time_name, test_area_to_look)

        if sign == '+':
            print(sign)
            print(int(time_offset))
            last_start_date_test_area = last_start_date_test_area + datetime.timedelta(hours=int(time_offset))
        elif sign == '-':
            last_start_date_test_area = last_start_date_test_area - datetime.timedelta(hours=int(time_offset))

        return str(last_start_date_test_area)

    def __return_key_time_record_field_excel_dict(self):
        field_time_key = ''
        for current_key in self.dict_data_excel.keys():
            if 'Record Time' in current_key:
                field_time_key = current_key
                break

        return field_time_key

    def __get_time_offset_of_record_time_field(self, record_time_name):
        pattern_sign = re.compile(r'(-|\+)')
        pattern_hours = re.compile(r'([0-9]+:[0-9]+)')

        time_offset = re.search(pattern_hours, record_time_name)
        sign = re.search(pattern_sign, record_time_name).group()

        return sign, time_offset.group().split(':')[0]

    def __get_last_test_area_time_start(self, field_record_time_name, test_area_to_look):
        list_test_area_match = self.__made_list_test_area_match_records(field_record_time_name, test_area_to_look)
        list_test_area_match_at_date = [datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S') for
                                        date_string in list_test_area_match]
        print(list_test_area_match_at_date)
        last_time_start = self.__most_current_date_start(list_test_area_match_at_date)
        return last_time_start

    def __most_current_date_start(self, list_test_area_match_date):
        if len(list_test_area_match_date) == 1:
            return list_test_area_match_date[0]
        else:
            most_current_date = self.__most_current_date_start(list_test_area_match_date[1:])
            first_index = list_test_area_match_date[0]
            return most_current_date if most_current_date > first_index else first_index

    def __made_list_test_area_match_records(self, field_record_time_name, test_area_to_look):
        list_test_area_match = []
        for key_1, val in self.dict_data_excel['Test Area'].items():
            test_area_in_list = self.dict_data_excel['Test Area'][key_1]
            status_in_list = self.dict_data_excel['Status'][key_1]
            if test_area_in_list == test_area_to_look and status_in_list == 'Start':
                list_test_area_match.append(self.dict_data_excel[field_record_time_name][key_1])

        return list_test_area_match

    def __start_web_pag(self):
        self.pag1.start_pag()
        print('start sleep to manual logging')
        time.sleep(120)
        print('end sleep to manual logging')

    def __create_object(self, serial_number, test_area, log_name):
        object_found = self.store_objects.found_object_by_serial_number(serial_number)
        if not object_found:
            self.unit_object = SerialNumberObject(serial_number, test_area, log_name)
            self.unit_object.data = {'attributes': {}}
        else:
            self.unit_object = object_found

    def __get_attribute_from_excel(self, attribute='BOARD_ID'):
        dict_same_attribute = {}
        for key_1, val in self.dict_data_excel['Name'].items():
            if attribute == self.dict_data_excel['Name'][key_1]:
                print(self.dict_data_excel['Item Number'][key_1])
                print(self.dict_data_excel['Value'][key_1])
                dict_same_attribute[self.dict_data_excel['Item Number'][key_1]] = self.dict_data_excel['Value'][key_1]

        return dict_same_attribute

    def __update_csv_attribute(self):
        #self.unit_object.data['attributes']['cesium board id'] = {'VEDGE-100B-AC-K9': 'BOARD_ID', 'VEDGE-100B-AC-K9=': '10027FB0'}

        for pid, board_id in self.unit_object.data['attributes']['board_id_cesium'].items():
            dictionary_data = self.__create_dictionary_row_attribute(pid, board_id)
            self.control_files.create_or_add_data_csv_file(PATH_CSV_ATTRIBUTE, dictionary_data)

    def __create_dictionary_row_attribute(self, pid, board_id):
        dictionary_row_attributes = {
            'serial number': self.unit_object.serial_number,
            'pid': pid,
            'area': self.unit_object.area,
            'cesium board id': board_id,
            'logs board id': self.unit_object.data['attributes']['board_id_log']
        }
        if dictionary_row_attributes['logs board id'] == dictionary_row_attributes['cesium board id']:
            dictionary_row_attributes['result'] = 'match'
        else:
            dictionary_row_attributes['result'] = 'unmatch'

        return dictionary_row_attributes

    def test_apollo(self, **kwargs):
        serial_number = kwargs.get('serial_number', 'no serial number')
        pid = kwargs.get('pid', 'none')
        new_board_id = kwargs.get('new board id', 'none')
        #self.ssh_server_to_test.open_connection()
        self.ssh_server_to_test.send_command_test_unit(serial_number, pid, new_board_id)
