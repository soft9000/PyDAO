import sqlite3


class TC001:

    def __init__(self):
        self.db = './SqltDAO.sqlt3'
        self.conn = None
        self.curs = None
        self.bOpen = False
        self.fields = [('FirstName', 'TEXT'), ('LastName', 'TEXT'), ('Age', 'INTEGER'), ('PhoneNumber', 'TEXT'), ('Balance', 'REAL'), ('EmailAddress', 'TEXT')]
        self.table_name = 'SqltDAO'
        
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
            self.curs.execute("CREATE TABLE IF NOT EXISTS SqltDAO(ID INTEGER PRIMARY KEY AUTOINCREMENT, FirstName TEXT, LastName TEXT, Age INTEGER, PhoneNumber TEXT, Balance REAL, EmailAddress TEXT);")
            return True
        return False
        
    def insert(self, fields):
        if self.bOpen:
            self.curs.execute("INSERT INTO SqltDAO ( FirstName, LastName, Age, PhoneNumber, Balance, EmailAddress) VALUES (?,?,?,?,?,?);", fields)
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
                yield ref
        return None
        
    @staticmethod
    def Import(dao, data_file='./tc001_data.txt', hasHeader=True, sep=','):
        try:
            # dao.open()
            with open(data_file) as fh:
                line = fh.readline().strip()
                if hasHeader is True:
                    line = fh.readline().strip()
                while len(line) is not 0:
                    dao.insert(line.split(sep))
                    line = fh.readline().strip()
            # dao.close()
            return True
        except:
            pass
        return False
        
    
