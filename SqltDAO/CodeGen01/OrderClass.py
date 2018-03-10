# Author: Soft9000.com
# 2018/03/08: Class Created


class OrderClass:

    def __init__(self, class_name='SqltDAO', table_name='SqltDAO', db_name='./SqltDAO.sqlt3', file_name='./SqltDAO.py'):
        self._db_name = db_name
        self._class_name = None
        self.class_name = class_name
        self._table_name = table_name
        self._file_name = file_name

    @staticmethod
    def Norm(name):
        if name is None:
            return ''
        name = str(name).strip()
        name = name.replace(' ', '_')
        return name

    @property
    def db_name(self):
        return self._db_name

    @db_name.setter
    def table_name(self, name):
        if name is not None:
            try:
                self._db_name = name
                return True
            except:
                pass
        return False

    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, name):
        if name is not None:
            try:
                self._table_name = OrderClass.Norm(name)
                return True
            except:
                pass
        return False

    @property
    def class_name(self):
        return self._class_name

    @class_name.setter
    def class_name(self, name):
        if name is not None:
            try:
                self._class_name = OrderClass.Norm(name)
                return True
            except:
                pass
        return False


    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, name):
        if name is not None:
            try:
                self._file_name = name
                return True
            except:
                pass
        return False
