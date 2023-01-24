# Load selenium components
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import utilities

func_retry = utilities.func_retry


class HandleWebPag:

    def __init__(self, load_url):
        self.url = load_url

        self.op = webdriver.ChromeOptions()
        prefs = {'download.default_directory': r'C:\Users\cperezlo\PycharmProjects\Temp_download'}
        self.op.add_experimental_option('prefs', prefs)
        # driver = webdriver.Chrome(executable_path=driver_path, options=op)

    def start_pag(self):
        self.driver = webdriver.Chrome(options=self.op)
        self.driver.get(self.url)

    def refresh_web(self, new_url=""):

        new_url = self.url if new_url == "" else new_url
        self.driver.get(new_url)

        pass

    def close_pag(self):
        self.driver.close()

    def check_until_key_element_present_by_class_name(self, class_name):

        count = 0
        while True:
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
                print('bottom found')
                break
            except:
                print('elements no found')
                count += 1
                if count > 20:
                    break

        return True if count < 21 else False

    def look_for_element_by_full_path(self, full_path):

        count = 0
        while True:
            try:
                print('{0}'.format(full_path))
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, full_path)))
                break
            except:
                print('element no found')
                self.driver.refresh()
                count += 1
                if count > 20:
                    break

        return element if count < 21 else None

    def look_by_text_value(self, text):
        elements = self.driver.find_elements(by=By.XPATH, value="//*[text()='{0}']".format(text))
        if len(elements) == 1:
            return elements[0]
        return elements

    #@func_retry
    def return_wait_element(self, path):

        count = 0
        while True:
            try:
                element = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, path)))
                break
            except:
                print('element no found')
                self.driver.refresh()
                count += 1
                if count > 3:
                    break

        return element if count < 4 else None
