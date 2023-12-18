# try wrapping the code below that reads a persons.csv file in a class
# and make it more general such that it can read in any csv file

import csv
import os
import copy


# persons = []
# with open(os.path.join(__location__, 'persons.csv')) as f:
#     rows = csv.DictReader(f)
#     for r in rows:
#         persons.append(dict(r))
# print(persons)

# add in code for a Database class

# add in code for a Table class

# modify the code in the Table class so that
# it supports the insert operation where an entry can be added to a list of dictionary

# modify the code in the Table class so that
# it supports the update operation where an entry's value associated with a key can be updated


class Database:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


# add in code for a Table class


class Table:
    def __init__(self, table_name):
        self.table_name = table_name
        self.table = []

    def insert(self, csv_file=str):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        with open(os.path.join(__location__, csv_file)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                self.table.append(dict(r))

    def update(self, id_value=str, values=dict):
        for i in self.table:
            if i['ID'] == id_value:
                i.update(values)

    def clear(self):
        self.table = []

    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name)
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered')
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def __is_float(self, element):
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def __str__(self):
        return self.table_name + ':' + str(self.table)

    def set_row(self, id_value, update_attribute, update_value):
        for item in self.table:
            if item['ID'] == id_value:
                item[update_attribute] = update_value
        set_table = Table(self.table_name + '_set')
        set_table.table = copy.copy(self.table)
        return set_table

    def set_row_advanced(self, id_value, extra_attribute, extra_value, update_attribute, update_value):
        for item in self.table:
            if item['ID'] == id_value and item[extra_attribute] == extra_value:
                item[update_attribute] = update_value
        set_table = Table(self.table_name + '_set')
        set_table.table = copy.copy(self.table)
        return set_table

    def get_row(self, id_value, attribute):
        for item in self.table:
            if item['ID'] == id_value:
                return item[attribute]
        return None

    def admin_modify(self):
        """
        function for admin role, especially modifying each table data
        :param self: name of csv file
        """
        for request in self.table:
            print(request)
        project_id = input('Input project ID to modify ')
        attribute = input('Input attribute that you want to modify ')
        print(f'{project_id} {attribute} is currently {self.get_row(project_id, attribute)}.')
        new_value = input('Insert new value ')
        print('Do you want to modify?')
        print()
        print('Press only Enter to Confirm')
        choice = input('Press other key to Cancel ')
        if choice == "":
            self.set_row(project_id, attribute, new_value)
            print('Modifying completed')
        else:
            print('Modifying canceled')
