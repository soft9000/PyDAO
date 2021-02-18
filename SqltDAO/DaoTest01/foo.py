#!/usr/bin/env python3

'''
Generated by Soft9000/PyDAO, Ver. 2.0 (Alpha)
Generated @ Thu Feb 18 17:27:08 2021
'''

from collections import OrderedDict

import sqlite3


class TC001:

    def __init__(self):
        self.db = './SqltDAO.sqlt3'
        self.conn = None
        self.curs = None
        self.bOpen = False
        self.fields = OrderedDict([('FirstName', 'TEXT'), ('LastName', 'TEXT'), ('Age', 'TEXT'), ('PhoneNumber', 'TEXT'), ('Balance', 'REAL'), ('EmailAddress', 'TEXT')])
        self.table_name = 'SqltDAO'
        
    @classmethod
    def get_fields(cls, value):
        if isinstance(value, cls):
            return list(value.fields.values())[1:]
        return value
        
    def open(self):
        if self.bOpen is False:
            self.conn = sqlite3.connect(self.db)
            self.conn.row_factory = sqlite3.Row
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
            res = self.curs.execute("SELECT count(*) FROM SqltDAO;")
            return res.fetchone()[0]
        return -1
        
    def drop_table(self):
        if self.bOpen:
            self.curs.execute("DrOp TaBLe IF EXISTS SqltDAO;")
            return True
        return False
        
    def create_table(self):
        if self.bOpen:
            self.curs.execute("CREATE TABLE IF NOT EXISTS SqltDAO(ID INTEGER PRIMARY KEY AUTOINCREMENT, FirstName TEXT, LastName TEXT, Age TEXT, PhoneNumber TEXT, Balance REAL, EmailAddress TEXT);")
            return True
        return False
        
    def insert(self, fields):
        fields = TC001.get_fields(fields)
        if self.bOpen:
            self.curs.execute("INSERT INTO SqltDAO ( FirstName, LastName, Age, PhoneNumber, Balance, EmailAddress) VALUES (?,?,?,?,?,?);", fields)
            return True
        return False
        
    def update(self, id_, fields):
        fields = TC001.get_fields(fields)
        if self.bOpen:
            self.curs.execute("UPDATE SqltDAO SET FirstName=?, LastName=?, Age=?, PhoneNumber=?, Balance=?, EmailAddress=? WHERE ID = {};".format(id_), fields)
            return True
        return False
        
    def delete(self, primary_key):
        if self.bOpen:
            self.curs.execute("DELETE from SqltDAO WHERE ID = ?;", [primary_key])
            return True
        return False
        
    def select(self, sql_select):
        if self.bOpen:
            self.curs.execute(sql_select)
            zlist = self.curs.fetchall()
            for ref in zlist:
                yield OrderedDict(ref)
        return None
        
    @staticmethod
    def Import(dao, encoding=None, text_file='./DaoTest01/tc001_data.txt', hasHeader=True, sep='","'):
        import csv
        with open(text_file, 'r', encoding=encoding) as fh:
            lines = csv.reader(fh)
            for line in lines:
                dao.insert(line)
        return True
        
   
