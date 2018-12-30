# Author: Soft9000.com
# 2018/03/08: Class Created

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from collections import OrderedDict
from SqltDAO.Gui.DataPrefrences import Dp1 as DataPrefrences

class OrderClass:

    def __init__(self, class_name='SqltDAO', table_name='SqltDAO', db_name='./SqltDAO.sqlt3', file_name='./SqltDAO.py'):
        self.zdict = OrderedDict()
        self.zdict['class_name'] = class_name
        self.zdict['table_name'] = table_name
        self.zdict['file_name'] = DataPrefrences.MkHome(file_name)
        self.zdict['db_name'] = DataPrefrences.MkHome(db_name)

    def home(self, opred):
        ''' Attempt to apply the user preferences (OrderedDict) to this order.
        True if applied, False otherwise.'''
        if not isinstance(opred, OrderedDict):
            return False
        
        values = os.path.split(self.zdict['file_name'])
        if not values:
            return False
        self.zdict['file_name'] = opred['Sql Folder'] + "/" + values[-1]
        
        values = os.path.split(self.zdict['db_name'])
        if not values:
            return False
        self.zdict['db_name'] =  opred['Code Folder'] + "/" + values[-1]
        return True

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
