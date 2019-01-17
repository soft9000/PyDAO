# Author: Soft9000.com
# 2018/03/08: Class Created

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from collections import OrderedDict
from SqltDAO.Gui.DataPreferences import Dp1 as DataPreferences, Preferences

class OrderClass:

    ''' The official interface into the API. Used to generate code, without
    'Preferences.' As such, the fully-qualified _fnames are used to indicate
    where the code_ and db_ output should reside.

    A user-specified endpoint, the INPUT DATA FILE s-h-o-u-l-d never
    be saved by an order; it is part of the OUTPUT code, and associated
    with an order by the code-generation API. 

    '''

    def __init__(self, class_name='SqltDAO', table_name='SqltDAO', db_name='./SqltDAO.sqlt3', file_name='./SqltDAO.py'):
        from SqltDAO.SchemaDef.OrderDef import OrderDef1 as OrderDef
        self._zdict = OrderedDict()
        self._zdict['class_name']   = class_name
        self._zdict['table_name']   = table_name
        self._zdict['code_fname']   = file_name
        self._zdict['db_fname']     = db_name
        self._zdict['data_encoding']= None
        self._zdict['data_sep']     = OrderDef.DELIMITERS[0]

    def home(self, opred):
        ''' Apply the user dictionary-preferences to this order, preserving the leaf-node.
        True if applied, False otherwise.'''
        if not isinstance(opred, Preferences):
            return False
        
        values = os.path.split(self._zdict['code_fname'])
        if not values:
            return False
        self._zdict['code_fname'] = opred['Code Folder'] + "/" + values[-1]
        
        values = os.path.split(self._zdict['db_fname'])
        if not values:
            return False
        self._zdict['db_fname'] =  opred['Sql Folder'] + "/" + values[-1]
        return True

    def __dict__(self):
        return OrderedDict(self._zdict) # copy!

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
    def encoding(self):
        return self._zdict['data_encoding']

    @encoding.setter
    def encoding(self, value):
        self._zdict['data_encoding'] = value

    @property
    def sep(self):
        return self._zdict['data_sep']

    @sep.setter
    def sep(self, value):
        self._zdict['data_sep'] = value

    @property
    def db_name(self):
        return self._zdict['db_fname']

    @db_name.setter
    def db_name(self, name):
        if name is not None:
            try:
                self._zdict['db_fname'] = name
                return True
            except:
                pass
        return False

    @property
    def table_name(self):
        return self._zdict['table_name']

    @table_name.setter
    def table_name(self, name):
        if name is not None:
            try:
                self._zdict['table_name'] = OrderClass.Norm(name)
                return True
            except:
                pass
        return False

    @property
    def class_name(self):
        return self._zdict['class_name']

    @class_name.setter
    def class_name(self, name):
        if name is not None:
            try:
                self._zdict['class_name'] = OrderClass.Norm(name)
                return True
            except:
                pass
        return False


    @property
    def file_name(self):
        return self._zdict['code_fname']

    @file_name.setter
    def file_name(self, name):
        if name is not None:
            try:
                self._zdict['code_fname'] = name
                return True
            except:
                pass
        return False
