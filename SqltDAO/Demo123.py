# DEMO: How to generate a database WITHOUT
# using an SQL / external file
#
# Author: Soft9000.com
# 2018/05/31: Demonstration Created

from collections import OrderedDict

# ######
# STEP 1: Define your tables
# ######

employee = OrderedDict()
employee["ObjectName"]      = "Employee"
employee["Description"]     = "Someone who works for someone else"
employee["Fields"]          = [('Name', 'Text'),
                               ('Email1', 'Text'),
                               ('Email2', 'Text'),
                               ('Email3', 'Text'),
                               ('Phone1', 'Text'),
                               ('Phone2', 'Text'),
                               ('Phone3', 'Text'),
                               ('Notes', 'Text')
                               ]

principal = OrderedDict(employee)
principal['ObjectName']     = 'Principal'
principal['Description']    = 'Someone who can make a financial decision'

event = OrderedDict()
event["ObjectName"]         = "Event"
event["Description"]        = "Officially scheduled activity"
event["Fields"]             = [('Name', 'Text'),
                               ('Start', 'Text'),
                               ('Stop', 'Text')
                               ]
    
todo = OrderedDict()
todo["ObjectName"]          = "ToDo"
todo["Description"]         = "Activity in-progress"
todo["Fields"]              = [('Name', 'Text'),
                               ('Description', 'Text')
                               ]
    
entry = OrderedDict()
entry["ObjectName"]          = "Entry"
entry["Description"]         = "Official status / log entry"
entry["Fields"]              = [('DateTime','Text'),
                                ('ObjectName', 'Text'),
                                ('ObjectId', 'Integer'),
                                ('Description', 'Text')
                                ]

tables = [employee, principal, event, todo, entry]

# ######
# STEP 2: Define your artifact (code and database) names
# ######

output_file = "./CrudMeister"
try:
    import os
    os.remove(output_file + '.py')
    # os.remove(output_file + '.sqlt3')
except:
    pass

# ######
# STEP 3: Enjoy!
# ######

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.SqlSyntax import SqliteCrud    
for line in tables:
    zname = line["ObjectName"]
    print("Table:", zname)
    order = OrderClass(
        db_name=output_file + ".sqlt3",
        class_name=zname,
        table_name=zname,
        file_name="./" + zname + ".py")
    zfields = line["Fields"]
    sql = SqliteCrud(order, zfields)
    data_file = str(zname + '.csv')
    result = sql.code_class_template(data_file, sep='","')
    with open(output_file + ".py", 'a') as fh:
        print(result, file=fh)
