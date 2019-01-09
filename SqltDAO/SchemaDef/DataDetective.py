#!/usr/bin/env python3

import os.path
import csv

class InspectorCSV:
    '''
    What to do when the user selects 'csv,' but things go boom.
    Emphasiss is upon Unicode detection + data-file conversion / re-writing
    to a FIXED_TAB or FIXED_PIPE format.
    '''

    FIXED_TAB =  ("/t", ".fxtab")
    FIXED_PIPE = ("|", ".fxpip")
    ENCODINGS = (None, 'utf-8', 'utf-16')

    @staticmethod
    def _encode(dlct):
        ''' internal use only '''
        if not dlct:
            return dict()
        pie = dlct()
        return {
            "delimiter":pie.delimiter,
            "doublequote":pie.doublequote,
            "doublequote":pie.doublequote,
            "quotechar":pie.quotechar,
            "skipinitialspace":pie.skipinitialspace,
            "quoting":pie.quoting,
            "lineterminator":pie.lineterminator
        }
    
    @staticmethod
    def _open(fqfile, ztype=None):
        ''' internal use only '''
        if ztype:
            return open(fqfile, 'r', encoding=ztype)
        else:
            return open(fqfile, 'r')
        
    @staticmethod
    def _count_lines(fh, line_max=-1):
        ''' internal use only '''
        result = 0
        if fh:
            try:
                for line in fh:
                    result += 1
                    if line_max >= 0:
                        if result >= line_max:
                            break
            except:
                pass
        return result

    @staticmethod
    def Tally(fqfile, line_max=-1):
        '''
        Check to see how many lines are in a data-file.
        Use line_max to prevent huge line-scans.
        Safe function - no exceptions are thrown.
        Result examples:
            (#, None) = Default encoding (classic bytes)
            (#, 'utf-8') = Unicode encoding (8 / 16 supported)
        '''
        rtype = None
        zmax = 0
        for ztype in InspectorCSV.ENCODINGS:
            try:
                fh = InspectorCSV._open(fqfile, ztype)
                count = InspectorCSV._count_lines(fh, line_max)
                if count > zmax:
                    zmax = count
                    rtype = ztype
            except:
                pass
            
        return zmax, rtype

    @staticmethod
    def Detect(fqfile):
        '''
        Detect file type, as well as how many lines can be read from same.
        Exception on error, else tuple with number read (#,) and encoding.
        Successfull result examples:
            (#, None) = Default encoding (classic bytes)
            (#, 'utf-8') = Unicode encoding (8 / 16 supported)
        '''
        if not fqfile:
            raise Exception("Input file is 'None'")
        if not os.path.exists(fqfile):
            raise Exception("Input file not found")
        max_read = 0
        encoding = None
        fh = None
        for ztype in InspectorCSV.ENCODINGS:
            try:
                result = 0
                fh = InspectorCSV._open(fqfile, ztype)
                result = InspectorCSV._count_lines(fh)                
                if result > max_read:
                    max_read = result
                    encoding = ztype
            except:
                if fh:
                    try:
                        fh.close()
                    except:
                        pass
                continue # Next encoding!
        return max_read, encoding

    @staticmethod
    def Sniff(fqfile, max_lines=20):
        '''
        Use the CSV 'Sniffer. Will not work on piped data.
        Returns strinigified dialect detected, or None
        '''
        if not fqfile:
            return None
        popSel = dict()

        fh = None
        for ztype in InspectorCSV.ENCODINGS:
            try:
                pop = dict()
                result = 0
                fh = InspectorCSV._open(fqfile, ztype)
                zcount = InspectorCSV._count_lines(fh)
                if not zcount:
                    continue
                fh.close()
                
                total = max_lines
                if total > zcount:
                    total = zcount
                    
                sn = csv.Sniffer()
                fh = InspectorCSV._open(fqfile, ztype)
                for ss, line in enumerate(fh):
                    if ss > total:
                        break
                    zdlg = sn.sniff(line)
                    if zdlg:
                        code = str(InspectorCSV._encode(zdlg))
                        if code in pop:
                            pop[code] = pop[code] + 1
                        else:
                            pop[code] = 1
                fh.close()
                popSel = pop
            except Exception as ex:
                continue
            finally:
                if fh:
                    try:
                        fh.close()
                    except:
                        pass

        zmax = 0
        result = None
        for key in popSel:
            if popSel[key] > zmax:
                zmax = popSel[key]
                result = key
        return zmax, result

    @staticmethod
    def Convert(fqfile, sep=FIXED_PIPE):
        '''
        Copy a data-file using a unified delimiter + factorized file-type suffix.
        Exception on error, else tuple with total lines (#), encoding, and result-file name.
        Successfull result examples:
            (#, None, fq_output) = Default encoding (classic bytes)
            (#, 'utf-8', fq_output) = Unicode encoding (8 / 16 supported)
        '''
        try:
            tr = InspectorCSV.Detect(fqfile)
            pig = fqfile + sep[1]
            if os.path.exists(pig):
                os.unlink(pig)
            fh = InspectorCSV._open(fqfile, tr[1])
            if tr[1]:
                pig = fqfile + '.' + tr[1] + sep[1]
                fout = open(pig, 'w', encoding=tr[1])
            else:
                fout = open(pig, 'w')
            lines = csv.reader(fh)
            for ss, line in enumerate(lines, 1):
                print(*line,sep=sep[0], file=fout)
            max_read = ss
            encoding = tr[1]
            if ss >= tr[0]:
                return max_read, encoding, pig
            raise Exception("Partial file read: {}/{}".format(ss,tr[0]))
        except Exception as ex:
            raise(ex)
        
        raise Exception("File format error.")

#R-n-D: Please ignore.
#file = 'C:/Users/Randall/Desktop/ProdSet/_etc/PyDAO-Student-Stats/RawData/Udemy/Py1200_Practice_2019-01-08_10-33-57.csv'
#print(InspectorCSV.Convert(file, InspectorCSV.FIXED_TAB))
#file = 'C:/Users/Randall/Desktop/ProdSet/_etc/PyDAO-master/SqltDAO/DaoTest01/nasdaqlisted.txt'
#print(InspectorCSV.Sniff(file))
print(InspectorCSV.Tally(file))
