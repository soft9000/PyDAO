# Opportunity to generate a DAO for Sqlite3 in Python 3
# Author: Soft9000.com
# 2018/03/08: Class Created

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from SqltDAO.CodeGen01.DaoExceptions import GenOrderError
from SqltDAO.SchemaDef.DataDetective import Inspector, InspectorCSV
from SqltDAO.CodeGen01.Normalizers import Norm

class TextData:

    ''' Telemetry from TextDataDetect. '''

    def __init__(self):
        self.encoding   = None
        self.fields     = None
        self.sep        = None
        self.header     = None
        self.lines_scanned  = 0
    

class TextDataDetect:

    ''' Detect the fields & encoding present in a textual data file. Relying
    as it must upon a user-provided artifact + name, this process is obviously
    an exception-laden undertaking.
    '''

    @staticmethod
    def _GetHeader(file, encoding='utf-8'):
        with open(file, encoding=encoding) as fh:
            line = fh.readline().strip()
            if ord(line[0]) == 65279:
                return line[1:] # skip the UTF-16 BOM
            return line

    @staticmethod
    def FixHeaderNames(headers, spacer=''):
        for ss, col in enumerate(headers):
            col = col.replace(' ', spacer)
            col = col.replace('"', spacer)
            headers[ss] = col
        return headers

    @staticmethod
    def GetHeader(file, sep=','):
        header = TextDataDetect._GetHeader(file)
        return Norm.NormLine(header, sep=sep)

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
        if TextDataDetect.IsInteger(field):
            return "INTEGER"
        elif TextDataDetect.IsFloating(field):
            return "REAL"
        elif TextDataDetect.IsText(field):
            return "TEXT"
        return None

    @staticmethod
    def GetTypes(line, sep=','):
        cols = Norm.NormLine(line, sep)
        results = []
        for col in cols:
            ztype = TextDataDetect.GetType(col)
            results.append(ztype)
        return results

    @staticmethod
    def Open(file):
        ''' Attempt to open a default / unicode encoded file. Returns the file
        handle, as well as the normative encoding type.

        Examples:
            fh, None    # Default / ASCII encoding
            fh, 'utf-8' # Opened as UNICODE
            None, None  # Unable to open at-all
        '''
        zStat = Inspector.Tally(file, line_max=200)
        if not zStat[2]:
            return None, None
        fh = open(file, 'r', encoding=zStat[1])
        return fh, zStat[1]
        
        

    @staticmethod
    def GetFieldsCSV(file, text_data, count=50):
        '''
        Success: A properly-ordered list() of (field-name, SQLite Type) values
        Failure: Check for 'None' or Exception
        '''
        import csv
        header = None
        zTup = InspectorCSV.Detect(file) # do, or die
        with open(file, encoding=zTup[1]) as fh:
            lines = csv.reader(fh)
            saved = None
            for ss, line in enumerate(lines, 1):
                text_data.lines_scanned = ss
                if not line:
                    break
                if ss >= count:
                    break
                if text_data.header:
                    if not header:
                        header = TextDataDetect.FixHeaderNames(line)
                        continue
                pw = []
                for col in line:
                    ztype = TextDataDetect.GetType(col)
                    pw.append(ztype)            
                if saved is None:
                    saved = pw
                    continue
                for ss, ref in enumerate(pw):
                    if ref is None:
                        pw[ss] = "Text" # UNIQUE OVERRIDE
                if pw != saved:
                    for ss, col in enumerate(pw):
                        if saved[ss] != col:
                            if saved[ss] == 'REAL' and col == 'INTEGER':
                                pw[ss] = saved[ss] # Keep it REAL
                                continue
                            pw[ss] = "TEXT" # UNIQUE OVERRIDE
                    saved = pw # Demoted!
            text_data.fields = list(zip(header, saved))
            return text_data
                
    @staticmethod
    def GetFields(file, sep=',', hasHeader=True, count=50):
        '''
        Success: A properly-ordered list() of (field-name, SQLite Type) values
        Failure: Check for 'None' or Exception
        '''
        text_data = TextData()
        text_data.sep = sep
        text_data.header = hasHeader
        try:
            if sep == '","':
                zCheck = TextDataDetect.GetFieldsCSV(file, text_data, count=count)
                return zCheck
            header = None
            zStat = TextDataDetect.Open(file)
            fh = zStat[0]
            if not fh:
                return None
            else:
                text_data.encoding = zStat[1]
                line = fh.readline()
                if not sep in line:
                    raise GenOrderError("Field separator not in row.") 
                if hasHeader is True:
                    header = Norm.NormLine(line, sep=sep)
                    line = fh.readline()
                saved = None
                while line and count > 0:
                    text_data.lines_scanned += 1
                    count -= 1
                    pw = TextDataDetect.GetTypes(line, sep=sep)
                    if pw is None:
                        return None
                    if saved is None:
                        saved = pw
                        continue
                    for ss, ref in enumerate(pw):
                        if ref is None:
                            pw[ss] = "Text" # UNIQUE OVERRIDE
                    if pw != saved:
                        for ss, col in enumerate(pw):
                            if saved[ss] != col:
                                if saved[ss] == 'REAL' and col == 'INTEGER':
                                    pw[ss] = saved[ss] # Keep it REAL
                                    continue
                                pw[ss] = "TEXT" # UNIQUE OVERRIDE
                        saved = pw # Demoted!
                    line = fh.readline()
                fh.close()
                text_data.fields = list(zip(TextDataDetect.FixHeaderNames(header), saved))
                return text_data
        except GenOrderError as ex:
            raise ex
        except Exception:
            return None


