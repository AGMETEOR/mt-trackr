import uuid
import collections


class Data:
    def __init__(self):
        self.table = collections.OrderedDict()

    def add_to_db(self, data):
        id = str(uuid.uuid4())
        if id not in self.table:
            data["id"] = id
            self.table[id] = data
        return data

    def delete_from_db(self, id):

        id = str(id)
        if str(id) in self.table:
            del self.table[id]

    def update_table(self, id, data):
        if id in self.table:
            self.table[id] = data

    def get_single_item(self, id):
        if id in self.table:
            return self.table[id]

    def get_all_data(self):
        _list = []
        od = self.table.items()
        for x in od:
            _list.append(x[1])
        return _list
