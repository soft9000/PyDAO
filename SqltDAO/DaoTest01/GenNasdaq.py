from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.CodeGen import DaoGen


if __name__ == "__main__":
    data_file = "../DaoTest01/nasdaqlisted.txt"
    order = OrderClass(class_name='NasdaqDAO', table_name='TOK_NASDAQ', db_name='./StockInfo.sqlt3', file_name='./NasdaqDAO.py')

    gen = DaoGen()
    print(gen.write_code(order, data_file, sep="|"))
