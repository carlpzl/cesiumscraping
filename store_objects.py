class StoreObjects(object):
    def __init__(self):
        self._list_objects = []

    def __len__(self):
        return len(self._list_objects)

    def __getitem__(self, item):
        return self._list_objects[item]

    def add_object(self, new_object_random):
        self._list_objects.append(new_object_random)

    def found_object_by_serial_number(self, serial_number):
        object_found = [object_in_list for object_in_list in self._list_objects if object_in_list.serial_number == serial_number]
        if object_found:
            return object_found[0]
        else:
            return None

