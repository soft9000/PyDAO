import sqlite3


class Income:

    def __init__(self):
        self.db = 'C:/Users/Randall/Desktop/ProdSet/_etc/PyDAO-master.imda/SqltDAO/DaoTest01/Income.sqlt3'
        self.conn = None
        self.curs = None
        self.bOpen = False
        self.fields = [('FIPS', 'INTEGER'), ('State', 'TEXT'), ('County', 'TEXT'), ('MedHHInc', 'INTEGER'), ('PerCapitaInc', 'INTEGER'), ('PovertyUnder18Pct', 'REAL'), ('PovertyAllAgesPct', 'STRING'), ('Deep_Pov_All', 'REAL'), ('Deep_Pov_Children', 'REAL'), ('PovertyUnder18Num', 'INTEGER'), ('PovertyAllAgesNum', 'INTEGER')]
        self.table_name = 'Income'
        
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
            res = self.curs.execute("SELECT count(*) FROM Income;")
            return res.fetchone()[0]
        return -1
        
    def drop_table(self):
        if self.bOpen:
            self.curs.execute("DrOp TaBLe IF EXISTS Income;")
            return True
        return False
        
    def create_table(self):
        if self.bOpen:
            self.curs.execute("CREATE TABLE IF NOT EXISTS Income(ID INTEGER PRIMARY KEY AUTOINCREMENT, FIPS INTEGER, State TEXT, County TEXT, MedHHInc INTEGER, PerCapitaInc INTEGER, PovertyUnder18Pct REAL, PovertyAllAgesPct STRING, Deep_Pov_All REAL, Deep_Pov_Children REAL, PovertyUnder18Num INTEGER, PovertyAllAgesNum INTEGER);")
            return True
        return False
        
    def insert(self, fields):
        if self.bOpen:
            self.curs.execute("INSERT INTO Income ( FIPS, State, County, MedHHInc, PerCapitaInc, PovertyUnder18Pct, PovertyAllAgesPct, Deep_Pov_All, Deep_Pov_Children, PovertyUnder18Num, PovertyAllAgesNum) VALUES (?,?,?,?,?,?,?,?,?,?,?);", fields)
            return True
        return False
        
    def delete(self, primary_key):
        if self.bOpen:
            self.curs.execute("DELETE from Income WHERE ID = ?;", [primary_key])
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
    def Import(dao, data_file='C:/Users/Randall/Desktop/ProdSet/_etc/PyDAO-master.imda/SqltDAO/DaoTest01/Income.csv', hasHeader=True, sep=','):
        try:
            # dao.open()
            with open(data_file) as fh:
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
        
    
