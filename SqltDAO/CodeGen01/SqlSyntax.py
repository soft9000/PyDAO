# Author: Soft9000.com
# 2018/03/08: Class Created

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.CodeLevel import CodeLevel
from SqltDAO.CodeGen01.DaoExceptions import GenOrder


class SqliteCrud:

    def __init__(self, order, fields):
        if isinstance(order, OrderClass) is False:
            raise GenOrder("Error: ClassOrder is missing")
        self.order = order
        self.fields = fields
        self.level = CodeLevel()

    def code_class_template(self, data_file, sep=','):
        self.level.set(0)
        result = self.level.print("import sqlite3\n\n\nclass " + self.order.class_name + ":")
        result += self.level.print("")

        self.level.inc()
        result += self.level.print("def __init__(self):")

        self.level.inc()
        result += self.level.print("self.db = '" + self.order.db_name +"'")
        result += self.level.print("self.conn = None")
        result += self.level.print("self.curs = None")
        result += self.level.print("self.bOpen = False")
        result += self.level.print("self.fields = " + str(self.fields))
        result += self.level.print("self.table_name = '" + self.order.table_name + "'")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def open(self):")
        self.level.inc()
        result += self.level.print("if self.bOpen is False:")
        self.level.inc();
        result += self.level.print("self.conn = sqlite3.connect(self.db)")
        result += self.level.print("self.curs = self.conn.cursor()")
        result += self.level.print("self.bOpen = True")
        self.level.dec()
        result += self.level.print("return True")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def close(self):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print("self.conn.commit()")
        result += self.level.print("self.bOpen = False")
        self.level.dec()
        result += self.level.print("return True")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def count(self):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('res = self.curs.execute("SELECT count(*) FROM ' + self.order.table_name + ';")')
        result += self.level.print("return res.fetchone()[0]")
        self.level.dec()
        result += self.level.print("return -1")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def drop_table(self):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('self.curs.execute("DrOp TaBLe IF EXISTS ' + self.order.table_name + ';")')
        result += self.level.print("return True")
        self.level.dec()
        result += self.level.print("return False")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def create_table(self):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('self.curs.execute("' + self.sql_create_table() + '")')
        result += self.level.print("return True")
        self.level.dec()
        result += self.level.print("return False")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def insert(self, fields):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('self.curs.execute("' + self.sql_insert_row() + '", fields)')
        result += self.level.print("return True")
        self.level.dec()
        result += self.level.print("return False")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def delete(self, primary_key):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('self.curs.execute("DELETE from ' + self.order.table_name + ' WHERE ID = ?;", [primary_key])')
        result += self.level.print("return True")
        self.level.dec()
        result += self.level.print("return False")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def select(self, sql_select):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('self.curs.execute(sql_select)')
        result += self.level.print("zlist = self.curs.fetchall()")
        result += self.level.print("for ref in zlist:")
        self.level.inc();
        result += self.level.print("yield ref")
        self.level.dec()
        self.level.dec()
        result += self.level.print("return None")
        result += self.level.print("")
        self.level.dec()

        self.level.push()
        result += self.level.print("@staticmethod")
        result += self.level.print("def Import(dao, data_file='" + data_file + "', hasHeader=True, sep='" + sep + "'):")
        self.level.inc()
        result += self.level.print("try:")
        self.level.inc()
        result += self.level.print('# dao.open()')
        result += self.level.print("with open(data_file) as fh:")
        self.level.inc()
        result += self.level.print("line = fh.readline().strip()")
        result += self.level.print("if hasHeader is True:")
        self.level.inc()
        result += self.level.print("line = fh.readline().strip()")
        self.level.dec()
        result += self.level.print("while len(line) is not 0:")
        self.level.inc()
        result += self.level.print("dao.insert(line.split(sep))")
        result += self.level.print("line = fh.readline().strip()")
        self.level.dec()
        self.level.dec()
        result += self.level.print("# dao.close()")
        result += self.level.print("return True")
        self.level.dec()
        result += self.level.print("except:")
        self.level.inc()
        result += self.level.print("pass")
        self.level.dec()
        result += self.level.print("return False")
        result += self.level.print("")
        self.level.dec()
        self.level.pop()

        result += self.level.print("")
        return result


    def sql_create_table(self):
        result = "CREATE TABLE IF NOT EXISTS " + self.order.table_name
        result = result + '(ID INTEGER PRIMARY KEY AUTOINCREMENT,'
        for ss, val in enumerate(self.fields):
            result += ' '
            result += val[0] + " "
            result += val[1] + ","
        result = result[0:len(result) - 1]
        result = result + ');'
        return result


    def sql_insert_row(self):
        result = "INSERT INTO " + self.order.table_name + " ("
        for val in self.fields:
            result += ' '
            result += val[0] + ","
        result = result[0:len(result) - 1]
        result = result + ') VALUES ('
        for val in self.fields:
            result += '?,'
        result = result[0:len(result) - 1]
        result = result + ');'
        return result
