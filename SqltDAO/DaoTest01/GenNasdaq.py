import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.SchemaDef.OrderDef import OrderDef1 as OrderDef
from SqltDAO.CodeGen01.CodeGen import DaoGen
from SqltDAO.GenGUI.DataPreferences import Dp1 as DataPreferences

if __name__ == "__main__":
    data_file = "../DaoTest01/nasdaqlisted.txt"
    order = OrderClass(class_name='NasdaqDAO', table_name='TOK_NASDAQ', db_name='./StockInfo.sqlt3', file_name='./NasdaqDAO.py')
    order.sep = OrderDef.DELIMITERS[0] # Redundant - but informative!
    gen = DaoGen()
    print(gen.write_code(DataPreferences.Load('.'), order, data_file))
