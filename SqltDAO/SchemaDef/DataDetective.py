#!/usr/bin/env python3

# 2019/01/07: Class Created
# Status: Work-In-Progress
#         - Refactored + minor updates. Code paths needs re-testing.

import os.path
import csv

class Inspector:
    '''
    Line oriented: A field-independant way to scan for the
    encoding + successfull reading of a partial / complete,
    textual, data-file.
    '''
    ENCODINGS = (None, 'utf-8', 'utf-16')    
        
    @staticmethod
    def _count_lines(fh, line_max=-1):
        ''' internal use only '''
        tally = 0
        bokay = False
        if fh:
            try:
                for line in fh:
                    tally += 1
                    if line_max >= 0:
                        if tally >= line_max:
                            break
                bokay = True
            except:
                pass
        return tally, bokay


    @staticmethod
    def Tally(fqfile, line_max=-1):
        '''
        Check to see how many lines (#) are in a data-file.
        The 2nd result is the file encoding. None = Classic / ASCII encoding.
        The 3rd result is boolean. Indicates if the file was read completely ('toeof.')

        Use line_max to prevent huge line-scans. 
        
        Safe function - no exceptions are thrown.
        
        Result examples:
            (#, None, toeof)    = Default encoding (classic bytes)
            (#, 'utf-8', toeof) = Unicode encoding (8 / 16 supported)
        '''
        rtype = None
        zmax = 0
        bokay = False
        for ztype in Inspector.ENCODINGS:
            try:
                fh = open(fqfile, 'r', encoding=ztype)
                count = Inspector._count_lines(fh, line_max)
                if count[0] > zmax:
                    zmax  = count[0]
                    bokay = count[1]
                    rtype = ztype
            except:
                try:
                    close(fh)
                except:
                    pass
            finally:
                try:
                    close(fh)
                except:
                    pass
            
        results = zmax, rtype, bokay
        return results



class InspectorCSV:
    '''
    What to do when the user selects 'csv,' but things go boom.
    Emphasis is upon Unicode detection + data-file conversion / re-writing
    to a FIXED_TAB or FIXED_PIPE format.
    '''

    FIXED_TAB =  ("\t", ".fxtab")
    FIXED_PIPE = ("|", ".fxpip")

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
    def Detect(fqfile, max_lines=20):
        '''
        Detect file type, as well as how many lines can be read from same.
        Exception on error, else tuple with number read (#,) and encoding.
        Successfull result examples:
            (#, None, toeof)    = Default encoding (classic bytes)
            (#, 'utf-8', toeof) = Unicode encoding (8 / 16 supported)
        '''
        if not fqfile:
            raise Exception("Input file is 'None'")
        if not os.path.exists(fqfile):
            raise Exception("Input file not found")
        max_read = 0
        encoding = None
        bokay = False
        fh = None
        for ztype in Inspector.ENCODINGS:
            try:
                result = 0
                fh = open(fqfile, encoding=ztype)
                result = Inspector._count_lines(fh, line_max=max_lines)                
                if result[0] > max_read:
                    max_read = result[0]
                    bokay    = result[1]
                    encoding = ztype
            except:
                if fh:
                    try:
                        fh.close()
                    except:
                        pass
                continue # Next encoding!
        results = max_read, encoding, bokay
        return results

    @staticmethod
    def Sniff(fqfile, max_lines=20):
        '''
        Use the CSV 'Sniffer. Will not work on piped data.
        Returns strinigified dialect detected, or None.
        No exceptions are thrown.

        Successfull result examples:
            (#, None, toeof)    = Default encoding (classic bytes)
            (#, 'utf-8', toeof) = Unicode encoding (8 / 16 supported)
        '''
        if not fqfile:
            return None
        popSel = dict()
        bokay = False
        fh = None
        for ztype in Inspector.ENCODINGS:
            try:
                pop = dict()
                result = 0
                fh = open(fqfile, 'r', encoding=ztype)
                zcount = Inspector._count_lines(fh, line_max=max_lines)
                try:
                    fh.close()
                except:
                    pass

                if not zcount[0]: # no lines
                    continue
                if not zcount[1]: # no completion
                    continue
                
                total = max_lines
                if total > zcount[0]:
                    total = zcount[0]
                    
                sn = csv.Sniffer()
                fh = open(fqfile, 'r', encoding=ztype)
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
                bokay = True
            except Exception as ex:
                bokay = False
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
        return zmax, result, bokay

    @staticmethod
    def Convert(fqfile, sep=FIXED_PIPE):
        '''
        Copy a data-file using a unified delimiter + factorized file-type suffix.
        Exception on error, else tuple with total lines (#), encoding, and result-file name.
        Successfull result examples:
            (#, None, fq_output)    = Default encoding (classic bytes)
            (#, 'utf-8', fq_output) = Unicode encoding (8 / 16 supported)
        '''
        try:
            tr = InspectorCSV.Detect(fqfile)
            pig = fqfile + sep[1]
            if os.path.exists(pig):
                os.unlink(pig)
            fh = open(fqfile, 'r', encoding=ztype)
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
        finally:
            try:
                close(fh)
                close(fout)
            except:
                pass
        
        raise Exception("File format error.")


if __name__ == "__main__":
    #R-n-D: Please ignore.
    #file = '../../../PyDAO-Student-Stats/RawData/Udemy/Py1200_Practice_2019-01-08_10-33-57.csv'
    #print(InspectorCSV.Convert(file, InspectorCSV.FIXED_TAB))
    file = '../DaoTest01/nasdaqlisted.txt'
    #print(InspectorCSV.Sniff(file))
    print(Inspector.Tally(file))
