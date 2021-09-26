#!/usr/bin/env python3

'''
Generated by Soft9000/PyDAO, Ver. 1.01 (Alpha)
Generated @ Fri Jun  7 07:37:30 2019
'''

from collections import OrderedDict

import sqlite3


class MyTable:

    def __init__(self):
        self.db = '/d_drive/USR/code/Python3/PyDAO-master/SqltDAO/MyTable.sqlt3'
        self.conn = None
        self.curs = None
        self.bOpen = False
        self.fields = OrderedDict([('ID', 'integer'), ('name', 'text'), ('age', 'integer'), ('balance', 'real')])
        self.table_name = 'MyTable'
        
    def open(self):
        if self.bOpen is False:
            self.conn = sqlite3.connect(self.db)
            self.curs = self.conn.cursor()
            self.bOpen = True
        return True
        
    def close(self):
        if self.bOpen:
            self.conn.commit()
            self.bOpen = False
        return True
        
    def count(self):
        if self.bOpen:
            res = self.curs.execute("SELECT count(*) FROM MyTable;")
            return res.fetchone()[0]
        return -1
        
    def drop_table(self):
        if self.bOpen:
            self.curs.execute("DrOp TaBLe IF EXISTS MyTable;")
            return True
        return False
        
    def create_table(self):
        if self.bOpen:
            self.curs.execute("CREATE TABLE IF NOT EXISTS MyTable(ID INTEGER PRIMARY KEY AUTOINCREMENT, name text, age integer, balance real);")
            return True
        return False
        
    def insert(self, fields):
        if self.bOpen:
            self.curs.execute("INSERT INTO MyTable ( name, age, balance) VALUES (?,?,?);", fields)
            return True
        return False
        
    def update(self, id_, fields):
        if self.bOpen:
            self.curs.execute("UPDATE MyTable SET name=?, age=?, balance=? WHERE ID = {}".format(id_), fields);
            return True
        return False
        
    def delete(self, primary_key):
        if self.bOpen:
            self.curs.execute("DELETE from MyTable WHERE ID = ?;", [primary_key])
            return True
        return False
        
    def select(self, sql_select):
        if self.bOpen:
            self.curs.execute(sql_select)
            zlist = self.curs.fetchall()
            for ref in zlist:
                yield ref
        return None
        
    @staticmethod
    def Import(dao, encoding=None, text_file='MyTable.sqlt3.txt', hasHeader=True, sep='|'):
        try:
            # dao.open()
            with open(text_file, encoding=encoding) as fh:
                line = fh.readline().strip()
                if hasHeader is True:
                    line = fh.readline().strip()
                while len(line):
                    if dao.insert(line.split(sep)) is False:
                        return False
                    line = fh.readline().strip()
            # dao.close()
            return True
        except:
            pass
        return False
        
    
dao = MyTable()
dao.open()
dao.drop_table()
dao.create_table()
assert(dao.insert(['Nagy', 102, 22.22]) )
assert(dao.insert(['Bagy', 101, 222.22]) )
assert(dao.insert(['Ragy', 100, 2222.22]) )

row = list([*dao.select("SELECT * from MyTable where ID=1;")][0])
print(row)
TEST_NAME = "DANAG"
row[1] = TEST_NAME
assert(dao.update(row[0], row[1:]))
row = [*dao.select("SELECT * from MyTable where ID=1;")][0]
assert(row[1] == TEST_NAME)
for row in dao.select("SELECT * FROM MyTable ORDER BY ID;"):
    print(row)
dao.drop_table()
dao.close()

