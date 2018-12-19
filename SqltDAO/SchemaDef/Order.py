#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/12/19: File created

# Mission: Manage the factory order
# Status: Initial Release - Lightly Tested.

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from collections import OrderedDict
from SchemaDef.Table import TableDef

class OrderDef():
    ''' Basic Factory-Order definition.
    Note: Schema name will be used as the Database file + folder / archive name.
    '''
    FileType = ".x1" # "Experemental Format 1" - Always used. No forward support planned.

    def __init__(self):
        self._name = 'Default'
        self.tables = OrderedDict()

    def get_file_name(self):
        ''' Concoct a file name. '''
        return self.get_schema_name() + OrderDef.FileType

    def get_schema_name(self):
        ''' Query the schema name. '''
        return self._name

    def set_schema_name(self, name):
        ''' Change the schema name. '''
        self._name = TableDef.Normalize(name)

    def add_table(self, table_def):
        ''' Add a table. False if not added, or already added. '''
        if not isinstance(table_def, TableDef):
            return False
        if table_def._name in self.tables:
            return False
        self.tables[table_def._name] = table_def
        return True

    def get_table(self, name):
        ''' Lookup a table definition, by name. None if not found. '''
        if name in self.tables:
            return self.tables[table_def._name]
        return None

    def remove_table(self, name):
        ''' Remove a table. Always returns True. '''
        if name in self.tables:
            self.tables.pop(name)
        return True

    def change_table(self, name, table_def):
        ''' Change the definition for an existing TableDef. '''
        if name not in self.tables:
            return False
        self.tables[name] = table_def
        return True

    def __str__(self):
        ''' Program usable string. '''
        result = ''
        bFirst = True
        for key in self.tables:
            if not bFirst:
                result = result + ","
            result = result + str(self.tables[key])
            bFirst = False
        return result

    def __repr__(self):
        ''' Factory usable string. '''
        result = str(type(self)) + ' : '
        result = result + str(self)
        return result

    def __iter__(self):
        ''' Basic object iteration assured. '''
        for key in self.tables:
            yield self.tables[key]
    
    @staticmethod
    def LoadFile(fq_file):
        ''' Unsure if we want to use pickle here
        but will always return a Instance, else False
        '''
        if not os.path.exists(fq_file):
            return False
        try:
            import pickle
            return pickle.load(open(fq_file, 'rb'))
        except:
            return False
    
    @staticmethod
    def SaveFile(loaded_file):
        ''' Unsure if we want to use pickle here,
        but will always STORE an instance using defalt file name.
        True / False returned.
        '''
        if not isinstance(loaded_file, OrderDef):
            return False
        return OrderDef.SaveAs(loaded_file.get_file_name(), loaded_file)
    
    @staticmethod
    def SaveAs(fq_file, loaded_file, overwrite=False):
        ''' Unsure if we want to use pickle here,
        but will always STORE an instance using file name.
        Default file-type extension. True / False returned.
        '''
        if not isinstance(loaded_file, OrderDef):
            return False
        if not fq_file.endswith(OrderDef.FileType):
            fq_file = fq_file + OrderDef.FileType
        bExists = os.path.exists(fq_file)
        if bExists and overwrite is False:
            return False
        try:
            if bExists:
                os.unlink(fq_file)
            import pickle
            pickle.dump(loaded_file, open(fq_file, 'wb'))
            return os.path.exists(fq_file)
        except:
            return False


if __name__ == "__main__":
    ''' A few basic test cases ... '''
    
    zorder = OrderDef()
    zname = zorder.get_file_name()
    if os.path.exists(zname):
        os.unlink(zname)
    for ss in range(4):
        table = "zTable " + str(ss)
        ztable = TableDef(name=table)
        for ztype in TableDef.SupportedTypes:
            ztable.add_field(table + ' ' + ztype, ztype)
        zorder.add_table(ztable)
    
    print(repr(zorder))

    assert(OrderDef.SaveFile(zorder))
    zorder2 = OrderDef.LoadFile(zname)
    assert(str(zorder)==str(zorder2))
    print(repr(zorder2))

    for ss, table in enumerate(zorder2, 1):
        print(ss, table)

    os.unlink(zorder.get_file_name())
    
    

