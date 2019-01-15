# Opportunity to generate a DAO for Sqlite3 in Python 3

# Author: Soft9000.com
# 2018/03/08: Class Created
# Status: Code Complete. Alpha.

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.SchemaDef.OrderDef import OrderDef1 as OrderDef
from SqltDAO.SchemaDef.Factory import Factory1
from SqltDAO.CodeGen01.DaoExceptions import *
from SqltDAO.CodeGen01.SqlDetect import SqlDetect
from SqltDAO.CodeGen01.SqlSyntax import SqliteCrud
from SqltDAO.Gui.DataPreferences import Dp1 as DataPreferences


class DaoGen:

    def __init__(self):
        pass
    
    def get_fields(self, order_class, text_data_file, sep=','):
        '''
        Populate an OrderDef using an OrderClass + text_data_file.
        Returns OrderDef + Fields detected upon success,
        or an Exception on error.
        '''
        if isinstance(order_class, OrderClass) is False:
            raise TypeError("Instance of OrderClass is required.")
        if os.path.exists(text_data_file) is False:
            raise IOError("Data file not found.")
        header = SqlDetect.GetHeader(text_data_file, sep=sep)
        if header is None:
            raise IOError("Header not found.")
        fields = SqlDetect.GetFields(text_data_file, sep=sep)
        order_def = Factory1.Create(order_class, fields)
        return fields, order_def

    def gen_code(self, order_class, text_data_file, sep=','):
        ''' Detect tables & GET the CODE for a given a text_data_file.
        True or Exception returned.
        '''
        fields, order2 = self.get_fields(order_class, text_data_file, sep)
        if fields is None:
           raise GenException("Error: No data field(s) detected.")
        sql = SqliteCrud(order_class, fields)
        return sql.code_class_template(text_data_file, sep=sep)

    def write_project(self, pref, order_class, text_data_file, sep=','):
        ''' Detect tables & SAVE the PROJECT extracted from a user-selected text_data_file.
        True or Exception returned.
        '''
        fields, order2 = self.get_fields(order_class, text_data_file, sep)
        if fields is None:
           raise GenException("Error: No data field(s) detected.")
        return Factory1.SaveFile(pref, order2, overwrite=True)

    def write_code(self, pref, order_class, text_data_file, sep=','):
        ''' Write CODE from an OrderClass using data from a given text_data_file.
        True or Exception returned.
        '''
        source = self.gen_code(order_class, text_data_file, sep=sep)
        file_name = pref['Code Folder'] + os.path.sep + OrderDef.BaseName(order_class.file_name)            
        with open(file_name, "w") as fh:
            fh.write(source)
            return True
        return False

