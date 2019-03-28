#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/12/19: File created
# 2018/01/15: File renamed

''' Mission: Manage a factory-order for the GUI, with
legacy API (OrderClass) conversion. '''

# Status: Mutli-table serialization testing okay

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from collections import OrderedDict
from SqltDAO.SchemaDef.Table import TableDef
from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.DaoExceptions import GenOrderError
from SqltDAO.CodeGen01.Normalizers import Norm

class OrderDef1:
    ''' The official project-definition. Unlike OrderClass, an OrderDef
    is designed to be used in conjunction with 'Preferences.' As such,
    the use of fully-qualified path-names is discouraged. Rather,
    absolute OUTPUT file locations require user-preferenced to be
    specified.

    Designed for more comprehensive database support / user selectable
    support, things like schema names and multiple table definitions
    (etc.) are what this order-type is all about.

    A user-specified endpoint, note that the INPUT DATA FILE s-h-o-u-l-d never
    be saved by an order, because it m-u-s-t NEVER be changed. 
    '''
    NONAME          = "_-$junker!__.~"  # Invalid SQL name - for "must init" testing
    ProjType        = ".daop1"          # "Official Format, Version 1" - Always used.
    DbType          = ".sqlt3"
    CodeType        = ".py"
    TEXT_DATA_TYPE  = ".txt"
    DEFAULT_SCHEMA  = "Default"
    IOKEY           = ".~OrdrDf Ky$."   # Space elimination marks unique key.
    SEPS            = [os.path.sep, "/", "\\"]  # Zero tolerance for path names here.
    DELIMITERS = (
        (0, 'PIPE',  '|'), # Code-Base Default (positional.) We prefer PIPE or TAB!
        (1, 'TAB',   '\t'),
        (2, 'CSV',  '","'),# Classic support enabled.
        (3, 'COMMA', ','), # Catch-All: Try CSV before COMMA. (Might even be depricated, now?)
        )

    def __init__(self, name=None):
        if not name:
            name = OrderDef1.NONAME
        OrderDef1.PATH_EXCEPT(name)
        self._zdict = OrderedDict()
        self._zdict['schema_name']   = OrderDef1.DEFAULT_SCHEMA
        self._zdict['class_name']    = name
        self._zdict['code_fname']    = name
        self._zdict['db_fname']      = name
        self._zdict['project_fname'] = name
        self._zdict['data_encoding'] = None
        self._zdict['data_sep']      = OrderDef1.DELIMITERS[0]
        self._zdict_tables = OrderedDict()

    def assign(self, detect, table_name):
        ''' Populate ourselves based upon a detected set of fields. Effects are cumulative.
        Returns True upon success, else False. '''
        from SqltDAO.CodeGen01.TextDataDetector import TextData
        assert(isinstance(detect, TextData))
        self.sep = detect.sep
        self.encoding = detect.encoding
        ztable = TableDef(name=table_name)
        for field in detect.fields:
            if ztable.add_field(field[0], field[1]) is False:
                return False
        return self.add_table(ztable)

    @staticmethod
    def PATH_EXCEPT(name):
        ''' Raise an exception if a platform pathname is found. '''
        for sep in OrderDef1.SEPS:
            if name.find(sep) is not -1:
                raise TypeError("Error: Path name inclusion is not supported.")

    def fixup(self):
        ''' Enforce our "no file type" and "no file path" policies.
        '''
        self._zdict['project_fname'] = self.remove(self._zdict['project_fname'], OrderDef1.ProjType)
        self._zdict['db_fname']      = self.remove(self._zdict['db_fname'], OrderDef1.DbType)
        self._zdict['code_fname']    = self.remove(self._zdict['code_fname'], OrderDef1.CodeType)

    def coin_input_file(self):
        ''' Suggest a text-data file-name based upon the database file name & location.
        Handy when user has specified none, for example, when working in "ProjectMode."
        '''
        result = self._zdict['db_fname']
        if result is OrderDef1.NONAME:
            result = OrderDef1.DEFAULT_SCHEMA
        if result.endswith(OrderDef1.DbType):
            return result + OrderDef1.TEXT_DATA_TYPE
        return result

    @staticmethod
    def BaseName(source):
        ''' Remove any path characters. '''
        for sep in OrderDef1.SEPS:
            ipos = source.find(sep)
            if ipos is not -1:
                source = source.split(sep)[-1]
        return source

    def remove(self, source, suffix):
        ''' Detect & remove (1) file suffix, (2) junker name, and (3) Path Names.
        On (2) defers to (2.1) class-name when defined, else (2.2) NONAME is returned.
        
        A user-specified endpoint, note that the INPUT DATA FILE must NEVER be changed?
        '''
        source = OrderDef1.BaseName(source)
                
        if source.find(OrderDef1.NONAME) is not -1:
            if self.name.find(OrderDef1.NONAME) is not -1:
                return OrderDef1.DEFAULT
            else:
                return self.name
            
        if source.endswith(suffix):
            return source[0:-len(suffix)]
        return source

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
        ''' Delimiter can be specified by number, name, pattern, or unique.
        Unique patterns must follow those of DataDef.DELIMITERS.'''
        for line in OrderDef1.DELIMITERS:
            for row in line:
                if value == row:
                    self._zdict['data_sep'] = line
                    return
        if len(value) is 3:
            self._zdict['data_sep'] = value

    @property
    def name(self):
        return self._zdict['class_name']

    @property
    def project_name(self):
        ''' Concoct a file-name from the schema name.'''
        return self._zdict['project_fname'] + OrderDef1.ProjType

    @property
    def code_name(self):
        ''' Concoct a file-name from the schema name.'''
        return self._zdict['code_fname'] + OrderDef1.CodeType

    @property
    def database_name(self):
        ''' Concoct the database file name.'''
        result = self._zdict['db_fname']
        if result.endswith(OrderDef1.DbType):
            return result
        return result + OrderDef1.DbType

    @property
    def schema_name(self):
        ''' Query the schema name. '''
        return self._zdict['schema_name']

    @schema_name.setter
    def schema_name(self, name):
        ''' Change the schema name. True if all is well, else False. '''
        if not name:
            return False
        self._zdict['schema_name'] = Norm.NormCol(name)
        return True

    @property
    def class_name(self):
        ''' Query the class name. '''
        return self._zdict['class_name']

    def add_table(self, table_def):
        ''' Add a table. False if not added, or already added. '''
        if not isinstance(table_def, TableDef):
            return False
        if table_def._name in self._zdict_tables:
            return False
        self._zdict_tables[table_def._name] = table_def
        return True

    def table_names(self):
        ''' Return all of the table-names. Can be empty.'''
        return tuple(self._zdict_tables.keys())

    def find_table(self, name):
        ''' Lookup a table definition, by name. None if not found. '''
        if name in self._zdict_tables:
            return self._zdict_tables[name]
        return None

    def remove_table(self, name):
        ''' Remove a table. Always returns True. '''
        if name in self._zdict_tables:
            self._zdict_tables.pop(name)
        return True

    def change_table(self, name, table_def):
        ''' Change the definition for an existing TableDef. '''
        if name not in self._zdict_tables:
            return False
        self._zdict_tables[name] = table_def
        return True

    def __str__(self):
        ''' Program usable string. '''
        return str(self.__dict__())

    def __repr__(self):
        ''' Factory usable string. '''
        result = str(type(self)) + ' : '
        result = result + str(self)
        return result

    def __iter__(self):
        ''' Basic object iteration assured. '''
        values = self.__dict__()
        for key in values:
            yield key, values[key]

    def __dict__(self):
        results = OrderedDict(self._zdict)
        for key in self._zdict_tables:
            results[key] = self._zdict_tables[key]
        return results


# Main Test Case: ./Order.py
