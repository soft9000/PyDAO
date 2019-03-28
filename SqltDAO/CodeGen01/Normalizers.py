from collections import OrderedDict

class Norm:
    ''' With the use of other data-conversion packages, the opportunities
    for data-normalization have expanded considerably. It's time to combine
    them so as to use / maintain each, in a common location.
    '''

    @staticmethod
    def NormPath(path):
        ''' Convert a path to evaluatable path-name. '''
        if path:
            return path.replace('\\', '/')
        return path
    
    @staticmethod
    def NormLine(line, sep=','):
        ''' Normalize & split the first line / header line from a data-file. '''
        if ord(line[0]) == 65279:
            line = line[1:] # skip the UTF-16 BOM
        cols = line.split(sep)
        results = []
        for col in cols:
            col = col.replace('"', ' ').strip()
            results.append(col)
        return results        

    @staticmethod
    def NormCol(name):
        ''' Normalize an SQL column-name '''
        if name is None:
            return ''
        if ord(name[0]) == 65279:
            name = eval(name[1:])
        name = str(name).strip()
        for bad in (' ', '\\', '/', ':', ';'):
            name = name.replace(bad, '_')
        return name

    @staticmethod
    def NormCols(fields):
        ''' Fields are managed as an ordered dictionary. Uses NormCol(.)'''
        if not fields:
            return fields # gigo - (commonly used asa flag!)
        if isinstance(fields, list):
            zdict = OrderedDict()
            for field in fields:
                zdict[field[0]] = field[1]
            fields = zdict
        results = OrderedDict()
        bFirst = True
        for key in fields:
            key2 = Norm.NormCol(key)
            results[key2] = fields[key]
        return results
