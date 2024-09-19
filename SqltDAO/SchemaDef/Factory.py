#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/12/19: File created

# Mission: Manage the factory order
# Status: Mutli-table serialization TESTING okay

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from collections import OrderedDict
from SqltDAO.SchemaDef.Table import TableDef
from SqltDAO.SchemaDef.OrderDef import OrderDef1 as OrderDef
from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.DaoExceptions import GenOrderError

from SqltDAO.CodeGen01.TextDataDetector import TextDataDetect, TextData 

class Factory1:

    ''' First OrderDef Factory (OrderDef1) '''
    
    @staticmethod
    def Detect(fqfn, has_header=True):
        ''' Detect + return an OrderDef for a fully-qualified file-name (fqfn.)
        Attempt is exhaustive. Return None on error, or proper OrderDef on success.
        Safe function: No exceptions are thrown.'''
        for ztype in OrderDef.DELIMITERS:
            try:
                text_info = TextDataDetect.GetFields(fqfn, sep=ztype[2], hasHeader=has_header)
                assert(isinstance(text_info, TextData))
                return text_info
            except Exception as ex:
                pass
        return None

    @staticmethod
    def Fixup(order_def):
        ''' Returns False if the order_def cannot be fixed, else True. '''
        if not isinstance(order_def, OrderDef):
            return False
        order_def.fixup()
        return True

    @staticmethod
    def Convert(order_class):
        ''' Convert an OrderClass to an OrderDef. Raise an exception on error. '''
        if isinstance(order_class, OrderClass) is False:
            raise TypeError("Error: Instance of OrderClass is required.")
        order_def = OrderDef()
        data = order_class.__dict__()
        for key in data:
            order_def._zdict[key] = data[key]
        order_def.fixup()
        return order_def

    @staticmethod
    def Create(order_class, detect):
        ''' Create an OrderDef from an OrderClass + Fields. Raise an exception on error. '''
        from SqltDAO.CodeGen01.TextDataDetector import TextData
        assert(isinstance(detect, TextData))
        order_def = Factory1.Convert(order_class)
        if not order_def.assign(detect, order_class.table_name):
            raise Exception("Error: Unable to convert detected data type.")
        return order_def

    @staticmethod
    def Extract(order_def, pref):
        from SqltDAO.GenGui.DataPreferences import Preferences
        ''' Extract an OrderClass from an OrderDef. Raise an exception on error.'''
        if isinstance(order_def, OrderDef) is False:
            raise TypeError("Error: Instance of OrderClass is required.")
        for key in order_def._zdict:
            if order_def._zdict[key] == OrderDef.NONAME:
                raise TypeError("Error: Please define a '" + key + "' value.")

        order_def.fixup()
        
        table_name = None
        for key in order_def._zdict_tables:
            table_name = order_def._zdict_tables[key].get_table_name()
            break # HIGHLANDER HACK
        if not table_name:
            raise TypeError("Error: No tables have been defined.")
        if isinstance(pref, Preferences) is False:
            raise TypeError("Error: DataPreferences.Preferences is required.")           
        return OrderClass(
            class_name  = table_name,
            table_name  = table_name,
            db_name     = pref['Csv Folder'] + "/"  + table_name + OrderDef.DbType,
            file_name   = pref['Code Folder'] + "/" + table_name + OrderDef.CodeType)
            
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
                order_def = OrderDef()
                for key in zdict:
                    if key == OrderDef.IOKEY:
                        pw_def = TableDef(name=OrderDef.NONAME)
                        zrows = eval(zdict[key])
                        for row in zrows:
                            if pw_def.get_table_name() != row[0]:
                                if pw_def.get_table_name() != OrderDef.NONAME:
                                    order_def.add_table(pw_def)
                                pw_def = TableDef(name=row[0])
                            pw_def.add_field(row[1], row[2])
                        order_def.add_table(pw_def)
                    else:
                        order_def._zdict[key] = zdict[key]
                order_def.fixup()
                return order_def
        except Exception as ex:
            print(ex.__traceback__)
            return False        

    @staticmethod
    def SaveFile(pref, order_def, overwrite=False):
        ''' Will always STORE an instance into a project_name, if accessable.
        True / False returned.
        '''
        from SqltDAO.GenGui.DataPreferences import Preferences
        if not isinstance(order_def, OrderDef):
            return False
        if isinstance(pref, Preferences) is False:
            raise TypeError("Error: Instance of OrderClass is required.")
        return Factory1.SaveAs(
            pref["Projects"] + os.path.sep + order_def.project_name,
        order_def, overwrite=overwrite)
    
    @staticmethod
    def SaveAs(fq_file, order_def, overwrite=False):
        ''' Will always STORE an instance into the file name, if accessable.
        Default file-type extension. True / False returned.
        '''
        if not Factory1.Fixup(order_def):
            return False
        if not fq_file.endswith(OrderDef.ProjType):
            fq_file = fq_file + OrderDef.ProjType
        bExists = os.path.exists(fq_file)
        if bExists and overwrite is False:
            return False
        try:
            if bExists:
                os.unlink(fq_file)
            with open(fq_file, 'w') as fh:
                zformat = OrderedDict(order_def._zdict)
                zval = list()
                for table in order_def._zdict_tables:
                    for zdef in order_def._zdict_tables[table]:
                        zval.append(zdef)
                zformat[OrderDef.IOKEY] = repr(zval)
                print(str(zformat), file=fh)

            return os.path.exists(fq_file)
        except Exception as ex:
            print(ex)
            return False


if __name__ == "__main__":
    ''' A few basic test cases ... '''
    if True:
##        import csv
##        with open("../DaoTest01/tc001_data.txt") as fh:
##            with open("../DaoTest01/tc002_data.txt", 'w') as fh2:
##                lines = csv.reader(fh)
##                for line in lines:
##                    newline = ''
##                    for col in line:
##                        col = col.replace('"', '').strip()
##                        newline += col + '\t'
##                    print(newline.strip(), file=fh2)
        files = (
            ("../DaoTest01/Income.csv", "COMMA"),
            ("../DaoTest01/nasdaqlisted.txt", "PIPE"),
            ("../DaoTest01/tc001_data.txt", "CSV"),
            ("../DaoTest01/tc002_data.txt", "TAB"),
            )
        for file, result in files:
            print(file, result)
            detect = Factory1.Detect(file)
            print(detect.__dict__)
    else:
        from SqltDAO.GenGui.DataPreferences import Dp1 as DataPreferences
        pref = DataPreferences.Load('.')
        zorder = OrderDef(name=OrderDef.DEFAULT_SCHEMA)
        zname = zorder.project_name
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
        zname = zorder.project_name
        # print("zname", zname)
        if os.path.exists(zname):
            print("unlinking", zname)
            os.unlink(zname)
        
        assert(Factory1.SaveFile(pref, zorder))
        
        zorder2 = Factory1.LoadFile(zname)
        # print("zorder2:\n", zorder2, '\n')
        assert(zorder2 is not False)
        assert(str(zorder) == str(zorder2))

        for ss, table in enumerate(zorder2, 1):
            print(ss, table)

        odd = Factory1.Extract(zorder2, pref)
        print(odd)

        os.unlink(zorder.project_name)

        # OrderClass Inter-Operation
        from SqltDAO.CodeGen01.TextDataDetector import TextData
        detect = TextData()
        detect.fields = list()
        detect.fields.append(("MyAccount", "Integer"))
        detect.fields.append(("MyField", "TEXT"))
        detect.encoding = "utf-8"
        detect.sep = 'CSV'
        order_class = OrderClass()
        order_def = Factory1.Create(order_class, detect)
