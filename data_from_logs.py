import re


class DataFromLogs(object):
    def __init__(self, path):
        self.path = path
        self.map_regexp = {'BOARD_ID': r'Board ID serial number: ([A-Z0-9]+)'}

    def found_data(self, data_file_in_list, data_to_find):
        data_found = []

        for line in data_file_in_list:
            pattern = self.map_regexp[data_to_find]
            pattern_to_search = re.compile(pattern)
            match_with_pattern = pattern_to_search.findall(line)
            if match_with_pattern and match_with_pattern[0] != 'BOARD':
                print(match_with_pattern[0])
                data_found.append(match_with_pattern[0])

        return data_found
