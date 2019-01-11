Greetings!

Setting our sights upon importing data from the stock market, we felt the need to
create a tool that will quickly allow our students to convert delimited text + headers
into a Python class.

The Graphical User Interface (GUI) is in Alpha. See ./main.py to give it a try.

GUI Quick Start
===============
(0) Install Python 3
    Source: http://www.python.org
(1) Create Home Folder
    Example: C:\Study
(2) Download ZIP File
    From https://github.com/soft9000/PyDAO
(3) Copy ZIP to Home Folder
    Example: C:\Study\PyDAO-master.zip
(4) Unzip ZIP File into Home Folder
    Results: C:\Study\PyDAO-master\
(5) Locate & Run "main.py"
    Example: python C:\Study\PyDAO-master\SqltDAO\main.py
(6) Use Soft9000/PyDAO
    Video: https://youtu.be/azCokv4iI8k
    
Known Limitations
=================
Support is in the works for:
    o Unicode
    o Asymmetrical CSV
See ./SchemaDef/DataDetective.py for the finalized R&D results.

API Example:
===========
./Demo123.py

The above demonstrates how to generate a HUGE amount of code w/o using any data file(s).

Basic Tests:
===========
SqltDAO.DaoTest01.tc001_gen.py
SqltDAO.DaoTest01.tc001_driver.py

Note that you will need to copy the above into this folder to locate the packages.

For Students:
============
SqltDAO.DaoTest01.GenNasdaq.py

For an example of how to create an Order so as to generate your code!

Note that you will also need to copy the above into this folder to locate the packages.
