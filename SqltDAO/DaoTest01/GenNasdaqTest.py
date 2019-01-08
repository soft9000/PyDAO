import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from SqltDAO.DaoTest01.NasdaqDAO import NasdaqDAO

test = NasdaqDAO()

test.open()
test.create_table()

print('*' * 10)
if NasdaqDAO.Import(test) is False:
    print("Regression: Unable to import data.")
else:
    print('*' * 10)
    for row in test.select("Select * from " + test.table_name):
        print(row)
    print("Total is:", test.count())

test.drop_table()
test.close()
