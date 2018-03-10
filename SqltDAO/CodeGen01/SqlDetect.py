# Opportunity to generate a DAO for Sqlite3 in Python 3
# Author: Soft9000.com
# 2018/03/08: Class Created

class SqlDetect:

    @staticmethod
    def _GetHeader(file):
        with open(file) as fh:
            return fh.readline().strip()

    @staticmethod
    def FixHeaderNames(headers, spacer=''):
        for ss, col in enumerate(headers):
            col = col.replace(' ', spacer)
            headers[ss] = col
        return headers

    @staticmethod
    def Norm(line, sep=','):
        cols = line.split(sep)
        results = []
        for col in cols:
            col = col.replace('"', ' ').strip()
            results.append(col)
        return results

    @staticmethod
    def GetHeader(file, sep=','):
        header = SqlDetect._GetHeader(file)
        return SqlDetect.Norm(header, sep=sep)


    @staticmethod
    def IsFloating(value):
        try:
            float(value)
            return True
        except:
            pass
        return False

    @staticmethod
    def IsInteger(value):
        try:
            int(value)
            if str(value).find('.') != -1:
                return False # Get Real!
            return True
        except:
            pass
        return False

    @staticmethod
    def IsText(value):
        try:
            str(value)
            return True
        except:
            pass
        return False

    @staticmethod
    def GetType(field):
        if SqlDetect.IsInteger(field):
            return "INTEGER"
        elif SqlDetect.IsFloating(field):
            return "REAL"
        elif SqlDetect.IsText(field):
            return "TEXT"
        return None

    @staticmethod
    def GetTypes(line, sep=','):
        cols = SqlDetect.Norm(line, sep)
        results = []
        for col in cols:
            ztype = SqlDetect.GetType(col)
            results.append(ztype)
        return results

    @staticmethod
    def GetFields(file, sep=',', hasHeader=True, count=50):
        '''
        Success: A properly-ordered list() of (field-name, SQLite Type) values
        Failure: Check for 'None'
        '''
        try:
            header = None
            with open(file) as fh:
                line = fh.readline()
                if hasHeader is True:
                    header = SqlDetect.Norm(line, sep=sep)
                    line = fh.readline()
                saved = None
                while len(line) > 0 and count > 0:
                    count -= 1
                    pw = SqlDetect.GetTypes(line, sep=sep)
                    if pw is None:
                        return None
                    if saved is None:
                        saved = pw
                        continue
                    for ss, ref in enumerate(pw):
                        if ref is None:
                            pw[ss] = "String" # UNIQUE OVERRIDE
                    if pw != saved:
                        for ss, col in enumerate(pw):
                            if saved[ss] != col:
                                if saved[ss] == 'REAL' and col == 'INTEGER':
                                    pw[ss] = saved[ss] # Keep it REAL
                                    continue
                                pw[ss] = "STRING" # UNIQUE OVERRIDE
                        saved = pw # Demoted!
                    line = fh.readline()
                results = zip(SqlDetect.FixHeaderNames(header), saved)
                return list(results)
        except:
            return None


