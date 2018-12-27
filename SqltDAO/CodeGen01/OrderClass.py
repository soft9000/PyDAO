# Author: Soft9000.com
# 2018/03/08: Class Created

from collections import OrderedDict

class OrderClass:

    def __init__(self, class_name='SqltDAO', table_name='SqltDAO', db_name='./SqltDAO.sqlt3', file_name='./SqltDAO.py'):
        self.zdict = OrderedDict()
        self.zdict['class_name'] = class_name
        self.zdict['table_name'] = table_name
        self.zdict['file_name'] = file_name
        self.zdict['db_name'] = db_name

    def __dict__(self):
        return OrderedDict(self.zdict) # copy!

    def __iter__(self):
        results = self.__dict__()
        for key in results:
            yield key, results[key]

    def __str__(self):
        results = self.__dict__()
        return str(results)

    @staticmethod
    def Norm(name):
        if name is None:
            return ''
        name = str(name).strip()
        name = name.replace(' ', '_')
        return name

    @property
    def db_name(self):
        return self.zdict['db_name']

    @db_name.setter
    def table_name(self, name):
        if name is not None:
            try:
                self.zdict['db_name'] = name
                return True
            except:
                pass
        return False

    @property
    def table_name(self):
        return self.zdict['table_name']

    @table_name.setter
    def table_name(self, name):
        if name is not None:
            try:
                self.zdict['table_name'] = OrderClass.Norm(name)
                return True
            except:
                pass
        return False

    @property
    def class_name(self):
        return self.zdict['class_name']

    @class_name.setter
    def class_name(self, name):
        if name is not None:
            try:
                self.zdict['class_name'] = OrderClass.Norm(name)
                return True
            except:
                pass
        return False


    @property
    def file_name(self):
        return self.zdict['file_name']

    @file_name.setter
    def file_name(self, name):
        if name is not None:
            try:
                self.zdict['file_name'] = name
                return True
            except:
                pass
        return False
