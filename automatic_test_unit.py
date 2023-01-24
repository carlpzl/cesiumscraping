import paramiko


class AutomaticUnitTest(object):

    def __init__(self, host):
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._host = host  # "172.30.85.120"
        #self._client.connect(self._host, username="cperezlo", password="L0p3z.C4rl0s8", port=22)

    def open_connection(self, username="cperezlo", password="C4rl0s.L0p3z1"):
        self._client.connect(self._host, username=username, password=password, port=22)

    def send_command_to_shell(self):
        stdin, stdout, stderr = self._client.exec_command("cd bin;ls -l")
        listado = stdout.readlines()
        for i in listado:
            print(i)

    def send_command_test_unit(self, serial_number='1920C54624004EM', pid='VEDGE-100B-AC-K9', new_board_id='10024DA1'):
        #command = 'python2.7 /opt/cisco/constellation/apollocli.py -pl "ASSY - BitBucket" --area "ASSY" -ts "ASSY STATION 11" -cn "UUT11" --log-level DEBUG --timeout 10000 --m DEBUG --body "[\'MDS\', \'SPARES\']"'
        line_apollo = 'Attributes Rework'
        area_data = 'SYSAPK'
        test_station_data = 'Attribute Rework'
        container_name = 'Slot 10'
        level_log_name = 'DEBUG'
        mode_name = 'DEBUG'

        path_command = 'python2.7 /opt/cisco/constellation/apollocli.py'
        product_line = ' -pl "{0}"'.format(line_apollo)
        area = ' --area "{0}"'.format(area_data)
        test_station = ' -ts "{0}"'.format(test_station_data)
        container = ' -cn "{0}"'.format(container_name)
        level_log = ' --log-level {0}'.format(level_log_name)
        time_out = ' --timeout 10000'
        mode = ' --m {0}'.format(mode_name)
        answers = ' --body "[\'{0}\', \'{1}\', \'{2}\']"'.format(pid, serial_number, new_board_id)

        command = '{0}{1}{2}{3}{4}{5}{6}{7}{8}'.format(path_command, product_line, area, test_station, container,
                                                       level_log, time_out, mode, answers)

        print(command)
        stdin, stdout, stderr = self._client.exec_command(command)
        # print(stdin, stdout, stderr)

        listado = stdout.readlines()
        for i in listado:
            print(i)

    def close_connection(self):
        self._client.close()

