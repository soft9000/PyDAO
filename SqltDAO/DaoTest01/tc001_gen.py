import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.CodeGen import DaoGen
from SqltDAO.Gui.DataPreferences import Dp1 as DataPreferences

test = DaoGen()

data_file = "./tc001_data.txt"
order = OrderClass()
order.class_name = "TC001"
order.file_name = "./foo.py"
order.sep = 'CSV'
print("Order Delimiter:", order.sep)

print(test.write_code(DataPreferences.Load('.'), order, data_file))
