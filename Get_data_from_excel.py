from zipfile import ZipFile
import xmltodict
import xml.etree.ElementTree as ET
import codecs
import sys
import datetime
import re
import xlwings as xw
import pandas as pd
import csv
import time

regex_letter = re.compile(r'^[A-Z]*')
regex_numbers = re.compile(r'[0-9]+')


class ExcelFileData:
    def __init__(self, path):
        self.path = path  # latest_xlsx_file1 = r'C:\Users\cperezlo\OneDrive - Cisco\Documents\Python_Control_Excel\Temp_Download\download.xlsx'
        self.zipObject = ZipFile(path)  # ZipFile(latest_xlsx_file1)
        self.path_fix_xlsx = r'C:\Users\cperezlo\PycharmProjects\Temp_download\download_fix.xlsx'
        self.path_csv = r'C:\Users\cperezlo\PycharmProjects\Temp_download\download_fix.csv'

    def get_data(self):

        self.zipObject.extract("xl/sharedStrings.xml",
                  path="C:\\Users\\cperezlo\\PycharmProjects\\Temp_download\\")
        self.zipObject.extract("xl/worksheets/sheet1.xml",
                  path="C:\\Users\\cperezlo\\PycharmProjects\\Temp_download\\")
        self.zipObject.close()
        self.zipObject = None
        def excel_date_to_str(d):
            # excel stores a date as days since 01/01/1900
            # by adding 6933594 to the excel value, we can use python's date module to format it correctly
            ret = None
            try:
                ret = datetime.date.fromordinal(int(d) + 693594).strftime("%A, %d %B %Y")
            finally:
                return ret

        # UTF8Writer = codecs.getwriter('utf8')
        # sys.stdout = UTF8Writer(sys.stdout)

        x = ET.parse(open(
            r'C:\Users\cperezlo\PycharmProjects\Temp_download\xl\sharedStrings.xml'))
        shared_strings = x.getroot()

        last_v = None
        last_type = None
        dict_out = {}
        dict_keys_vs_letters = {}
        for event, elem in ET.iterparse(
                r'C:\Users\cperezlo\PycharmProjects\Temp_download\xl\worksheets\sheet1.xml',
                events=('start', 'end')):
            uri, tag = elem.tag.split("}")

            if event == "start" and tag == "c":  # start c tag
                last_v = None
                if "t" in elem.attrib:
                    last_type = elem.attrib["t"]
                else:
                    last_type = None

            elif event == "end" and tag == "c":  # end c tag
                if "r" in elem.attrib:
                    rc = elem.attrib["r"]
                    if last_v != None:
                        print("RC is ", str(rc), " = ", str(last_v))

                        column = regex_letter.search(rc).group(0)
                        line = regex_numbers.search(rc).group(0)
                        if int(line) == 1:
                            dict_out[last_v] = {}
                            dict_keys_vs_letters[rc[0]] = last_v
                        else:
                            key_dict_out = dict_keys_vs_letters[column]
                            dict_out[key_dict_out][int(line)] = last_v

            elif event == "start" and tag == "v":  # start v tag

                value = "".join(elem.itertext())
                if value == "":
                    last_v = value
                    print("dato mal parseeado revisar")
                if last_type == "s":
                    if value != "":
                        last_v = "".join(shared_strings[int(value)].itertext())

                else:
                    last_v = value, "type is ", last_type, excel_date_to_str(value)

        return dict_out

    def dict_from_fix_xlsx_file(self):

        current_path = self.path
        xw.App(visible=False)
        wingsbook = xw.Book(current_path)
        wingsbook.save(self.path_fix_xlsx)
        time.sleep(1)
        wingsbook.close()
        time.sleep(1)
        wingsbook = None

        current_path = self.path_fix_xlsx

        df = pd.read_excel(current_path)
        df.to_csv(self.path_csv, index=None, header=True)
        df = None

        reader = csv.DictReader(open(self.path_csv))

        dict_csv = {}
        counter = 1
        for dict_line in reader:
            counter += 1
            # print(dict_line)
            for key, value in dict_line.items():
                if counter == 2:
                    dict_csv[key] = {counter: str(value)}
                else:
                    dict_csv[key].update({counter: str(value)})

        print(dict_csv)

        return dict_csv

