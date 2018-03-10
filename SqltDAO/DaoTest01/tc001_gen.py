from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.CodeGen import DaoGen

test = DaoGen()

data_file = "./tc001_data.txt"
order = OrderClass()
order.class_name = "TC001"
order.file_name = "./foo.py"

print(test.write_code(order, data_file))
