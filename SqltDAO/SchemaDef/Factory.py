#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/12/19: File created

# Mission: Manage the creation order
# Status: WORK IN PROGRESS

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # SchemaDef
sys.path.insert(1, os.path.join(sys.path[0], '../..')) # SqltDAO

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.SqlSyntax import SqliteCrud
from collections import OrderedDict
from SchemaDef.Order import OrderDef
from SchemaDef.Table import TableDef

class Factory():
    ''' Basic Factory-Order definition.
    Note: Schema name will be used as the Database file + folder / archive name.
    '''

    @staticmethod
    def CreateDatabase(order_def):
        if isinstance(order_def, OrderDef) is False:
            return False
        for table in order_def:
            pass
