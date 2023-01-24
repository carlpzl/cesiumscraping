class SerialNumberObject(object):

    def __init__(self, serial_number, area, log_name):
        self._serial_number = serial_number
        self._area = area
        self._log_name = log_name

    @property
    def serial_number(self):
        return self._serial_number
    @serial_number.setter
    def name(self, serial_number):
        self._serial_number = serial_number

    @property
    def area(self):
        return self._area
    @area.setter
    def area(self, area):
        self._area = area

    @property
    def log_name(self):
        return self._log_name
    @log_name.setter
    def log_name(self, log_name):
        self._log_name = log_name
