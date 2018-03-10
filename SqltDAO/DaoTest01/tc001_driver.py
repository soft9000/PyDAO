from SqltDAO.DaoTest01.foo import TC001

test = TC001()

test.open()
test.create_table()
test.insert(("First", "Last", "Age", "123-456-7890", 22.56, "farst@foo.net"))
test.insert(("First2", "Last2", "Age2", "123-456-7890", 22.56, "farst2@foo.net"))
for row in test.select("Select * from " + test.table_name):
    print(row)
test.delete(1)
print('*' * 10)
for row in test.select("Select * from " + test.table_name):
    print(row)
test.drop_table()
test.close()
