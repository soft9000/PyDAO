#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/12/19: File created

# Mission: Manage the factory order
# Status: Mutli-table serialization testing okay

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from collections import OrderedDict
from SqltDAO.SchemaDef.Table import TableDef
from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.DaoExceptions import GenOrderError

from SqltDAO.Gui.DataPrefrences import Dp1 as DataPrefrences

class OrderDef():
    ''' Basic Factory-Order definition, multiple tables.
    Note: Schema name will be used as the Database file + folder / archive name.
    '''
    NONAME          = "_-$junker!__.~"  # Invalid SQL name - for "must init" testing
    FileType        = ".daop1"          # "Official Format, Version 1" - Always used.
    DEFAULT_SCHEMA  = "Default"
    IOKEY           = ".~OrdrDf Ky$."   # Space elimination marks unique key.
    
    def __init__(self, name=None):
        self.zdict = OrderedDict()
        if not name:
            name = OrderDef.NONAME
        self.zdict['schema_name']   = name
        self.zdict['class_name']    = name
        self.zdict['file_fname']    = name
        self.zdict['db_fname']      = name
        self.zdict_tables = OrderedDict()

    def home(self, opred):
        ''' Apply the user dictionary-preferences to this order, preserving the leaf-node.
        True if applied, False otherwise.'''
        if not isinstance(opred, dict):
            return False
        
        values = os.path.split(self.zdict['file_fname'])
        if not values:
            return False
        self.zdict['file_fname'] = opred['Sql Folder'] + "/" + values[-1]
        
        values = os.path.split(self.zdict['db_fname'])
        if not values:
            return False
        self.zdict['db_fname'] =  opred['Code Folder'] + "/" + values[-1]
        return True

    @property
    def name(self):
        return self.zdict['class_fname']

    @name.setter
    def name(self, name):
        if not name:
            name = OrderDef.NONAME
        for key in self.zdict:
            self.zdict[key] = name
        return True

    @property
    def file_name(self):
        ''' Concoct a file-name from the schema name. Asserts DEFAULT_SCHEMA if not defined.'''
        return self.zdict['file_fname'] + OrderDef.FileType

    @property
    def schema_name(self):
        ''' Query the schema name. '''
        return self.zdict['schema_name']

    @schema_name.setter
    def schema_name(self, name):
        ''' Change the schema name. True if all is well, else False. '''
        if not name:
            return False
        self.zdict['schema_name'] = TableDef.Normalize(name)
        return True

    def add_table(self, table_def):
        ''' Add a table. False if not added, or already added. '''
        if not isinstance(table_def, TableDef):
            return False
        if table_def._name in self.zdict_tables:
            return False
        self.zdict_tables[table_def._name] = table_def
        self.zdict['schema_name'] = table_def._name # TODO: Multi-Table - Rev 3.
        return True

    def find_table(self, name):
        ''' Lookup a table definition, by name. None if not found. '''
        if name in self.zdict_tables:
            return self.zdict_tables[table_def._name]
        return None

    def remove_table(self, name):
        ''' Remove a table. Always returns True. '''
        if name in self.zdict_tables:
            self.zdict_tables.pop(name)
        return True

    def change_table(self, name, table_def):
        ''' Change the definition for an existing TableDef. '''
        if name not in self.zdict_tables:
            return False
        self.zdict_tables[name] = table_def
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
        results = OrderedDict(self.zdict)
        for key in self.zdict_tables:
            results[key] = self.zdict_tables[key]
        return results

    def save(self):
        ''' Save using build-in schema name. '''
        if not schema_name():
            return False
        return OrderDef.SaveFile(self)

    @staticmethod
    def Create(order_class, fields):
        ''' Create an OrderDef from an OrderClass + Fields. Raise an exception on error. '''
        if isinstance(order_class, OrderClass) is False:
            raise TypeError("Error: Instance of OrderClass is required.")
        if not fields:
            raise TypeError("Error: No fields detected.")
        result = OrderDef()
        data = order_class.__dict__()
        for key in data:
            result.zdict[key] = data[key]
        ztable = TableDef(name=order_class.table_name)
        for field in fields:
            if ztable.add_field(field[0], field[1]) is False:
                raise GenOrderError("Error: Invalid Data Definition.")
        result.add_table(ztable)
        return result

    @staticmethod
    def Extract(order_def, pref):
        ''' Extract an OrderClass from an OrderDef. Raise an exception on error.'''
        if isinstance(order_def, OrderDef) is False:
            raise TypeError("Error: Instance of OrderClass is required.")
        if isinstance(pref, dict) is False:
            raise TypeError("Error: Dictionary of DataPrefrences is required.")
        for key in order_def.zdict:
            if order_def.zdict[key] == OrderDef.NONAME:
                raise TypeError("Error: Please define a '" + key + "' value.")

        try:
            for key in DataPrefrences.KEYS:
                if not pref[key]:
                    pass
        except:
            raise TypeError("Error: Key value '" + key + "' not found.")
        
        table_name = None
        for key in order_def.zdict_tables:
            table_name = order_def.zdict_tables[key].get_table_name()
            break # HIGHLANDER HACK
        if not table_name:
            raise TypeError("Error: No tables have been defined.")
        
        return OrderClass(
            class_name=table_name,
            table_name=table_name,
            db_name=pref['Csv Folder'] + "/" + table_name + ".sqlt3",
            file_name=pref['Projects'] + "/" + table_name + ".py")
            
    @staticmethod
    def LoadFile(fq_file):
        ''' Will always return an Instance, else False
        '''
        if not os.path.exists(fq_file):
            return False
        try:
            with open(fq_file, 'r') as fh:
                data = fh.readline()
                data = data.strip()
                zdict = eval(data)
                result = OrderDef()
                for key in zdict:
                    if key == OrderDef.IOKEY:
                        pw_def = TableDef(name=OrderDef.NONAME)
                        zrows = eval(zdict[key])
                        for row in zrows:
                            if pw_def.get_table_name() != row[0]:
                                if pw_def.get_table_name() != OrderDef.NONAME:
                                    result.add_table(pw_def)
                                pw_def = TableDef(name=row[0])
                            pw_def.add_field(row[1], row[2])
                        result.add_table(pw_def)
                    else:
                        result.zdict[key] = zdict[key]
                return result
        except Exception as ex:
            raise(ex)
            return False        
    
    @staticmethod
    def SaveFile(loaded_obj, overwrite=False):
        ''' Will always STORE an instance into the file name, if accessable.
        True / False returned.
        '''
        if not isinstance(loaded_obj, OrderDef):
            return False
        return OrderDef.SaveAs(
            loaded_obj.file_name,
            loaded_obj, overwrite=overwrite)
    
    @staticmethod
    def SaveAs(fq_file, loaded_obj, overwrite=False):
        ''' Will always STORE an instance into the file name, if accessable.
        Default file-type extension.
        True / False returned.
        '''
        if not isinstance(loaded_obj, OrderDef):
            return False
        if not fq_file.endswith(OrderDef.FileType):
            fq_file = fq_file + OrderDef.FileType
        bExists = os.path.exists(fq_file)
        if bExists and overwrite is False:
            return False
        try:
            if bExists:
                os.unlink(fq_file)
            with open(fq_file, 'w') as fh:
                zformat = OrderedDict(loaded_obj.zdict)
                zval = list()
                for table in loaded_obj.zdict_tables:
                    for zdef in loaded_obj.zdict_tables[table]:
                        zval.append(zdef)
                zformat[OrderDef.IOKEY] = repr(zval)
                print(str(zformat), file=fh)

            return os.path.exists(fq_file)
        except Exception as ex:
            raise(ex)
            return False


if __name__ == "__main__":
    ''' A few basic test cases ... '''    
    zorder = OrderDef(name=OrderDef.DEFAULT_SCHEMA)
    zname = zorder.file_name
    print("zname", zname)
    if os.path.exists(zname):
        print("unlinking", zname)
        os.unlink(zname)
    for ss in range(4):
        table = "zTable " + str(ss)
        ztable = TableDef(name=table)
        for ztype in TableDef.SupportedTypes:
            ztable.add_field(table + ' ' + ztype, ztype)
        zorder.add_table(ztable)

    print("zorder:\n", zorder, '\n')
    zname = zorder.file_name
    # print("zname", zname)
    if os.path.exists(zname):
        print("unlinking", zname)
        os.unlink(zname)
    
    assert(OrderDef.SaveFile(zorder))
    
    zorder2 = OrderDef.LoadFile(zname)
    # print("zorder2:\n", zorder2, '\n')
    assert(zorder2 is not False)
    assert(str(zorder) == str(zorder2))

    for ss, table in enumerate(zorder2, 1):
        if isinstance(table, TableDef):
            print("Table:", table.table_name())
            for field in table:
                print(field)
        else:
            print(ss, table)

    odd = OrderDef.Extract(zorder2, DataPrefrences.Load("."))
    print(odd)

    os.unlink(zorder.file_name)
    
    

