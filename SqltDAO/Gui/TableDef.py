#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/12/27: Project Begun

# Mission: GUI support for SchemaDef.TableDef.
# Status: Code Complete. Alpha.

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from tkinter import *
from tkinter import messagebox

from SqltDAO.Gui.StandardEntry import LabelEntry
from SqltDAO.SchemaDef.Table import TableDef as TableDef1

from collections import OrderedDict

class TableDef():
    ''' Add a table + field definition to a frame. Contents returned as a SchemaDef @TableDef. '''
    
    def __init__(self, frame):
        ''' Provide a frame. Use has_results() / get_results() to extract any updates. '''
        self.table_name = StringVar()
        self.field_type = StringVar()
        self.field_name = StringVar()
        self.field_types = TableDef1.SupportedTypes
        self.field_type.set(self.field_types[0])
        self.field_name.set("my_field")
        self.table_name.set("Default")
        self.zlb = None
        self.results = None
        self._body(frame)

    def got_results(self):
        ''' Preserve content, but detect any further user chances. '''
        self.results = None

    def empty(self):
        ''' Empty the list box. Remove previous results. '''
        self.results = None
        self.zlb.delete(0, last=END)

    def has_results(self):
        ''' Check to see if any field definitions were created or changed. '''
        return (self.results != None)

    def get_results(self):
        ''' Get the most recent results. Returns SchemaDef @TableDef'''
        return self.results

    def put_results(self, table_def):
        ''' Edit a previous SchemaDef @TableDef. Returns True if aplied, else False.
        Resets has_results() to False, pending any additional user machination.
        '''
        if not isinstance(table_def, TableDef1):
            return False
        self.table_name.set(table_def.get_table_name())
        for field in table_def:
            if field[1] == "ID":
                continue
            entry = field[1] + ":" + field[2]
            self.zlb.insert(END, entry)            
        self.results = None
        return True

    def pull_results(self):
        ''' Extract & return a SchemaDef @TableDef, no matter if the user changed it, or not.
        Also forces has_results() to True.
        '''
        self._apply()
        return self.results

    def _apply(self):
        ''' Extract results, as they become available. '''
        self.results = TableDef1(name=self.table_name.get())
        zdict = self._get_fields()
        for key in zdict:
            self.results.add_field(key, zdict[key])       

    def _get_fields(self):
        ''' Support routine to extract fields from the listbox. Returns an ordered dictionary. '''
        results = OrderedDict()
        for ss in range(self.zlb.size()):
            entry = self.zlb.get(ss)
            split = entry.split(':')
            results[split[0]]=split[1]
        return results

    def _on_def(self):
        ''' Validate + add a field definiton to the listbox. '''
        entry = self.field_name.get()
        ze = entry.lower()
        for ze2 in self._get_fields(): 
            if ze2.lower() == ze:
                messagebox.showerror(
                    "Field Exists",
                    "Field " + entry + " already defined. Edit or delete to change.")
                return
        entry = entry + ":" + self.field_type.get().strip()
        self.zlb.insert(END, entry)
        self._apply()

    def _on_edit(self):
        ''' Extract a selected listbox entry for editing. '''
        ztuple = self.zlb.curselection()
        if ztuple:
            entry = self.zlb.get(ztuple[0])
            split = entry.split(':')
            self.field_name.set(split[0])
            self.field_type.set(split[1])
        self._apply()

    def _on_delete(self):
        ''' Remove a selected listbox entry. '''
        ztuple = self.zlb.curselection()
        if ztuple:
            self.zlb.delete(ztuple[0])
        self._apply()

    def _body(self, zframe):
        ''' Prepares the frame for table management / creation during object initialization. '''
        # Table Selection
        zLF1 = LabelFrame(zframe, text=" Table ")
        
        Label(zLF1, text="Table: ").grid(row=0, column=0)
        efn = Entry(zLF1, width=30, textvariable=self.table_name)
        efn.grid(row=0, column=1)

        # Field Listbox
        self.zlb = Listbox(zLF1, width=40)
        sb = Scrollbar(zLF1, orient="vertical")
        sb.grid(row=0, column=2, rowspan=3, sticky=NS)
        self.zlb.grid(row=1, column=0, columnspan=2)
        self.zlb.config(yscrollcommand=sb.set)
        sb.config(command=self.zlb.yview)

        # Field Definition
        zfield = OrderedDict()
        zfield["Name"]=self.field_name; zfield["Type"]=self.field_type       
        LabelEntry.AddFields(zLF1, zfield, entry_width=30, row_start=3)
        oselect = OptionMenu(zLF1, self.field_type, *self.field_types)
        oselect.grid(row=5, column=1, stick=EW)

        # Control Frame
        zLF2 = LabelFrame(zframe, text=" Fields ")
        Button(zLF2, text="Define ...", width=10, command=self._on_def).pack()
        Button(zLF2, text="Edit ...", width=10, command=self._on_edit).pack()
        Button(zLF2, text="Delete", width=10, command=self._on_delete).pack()

        zLF2.pack(side=LEFT, fill=BOTH)
        zLF1.pack(side=LEFT, fill=BOTH)
        zframe.pack(fill=BOTH)
        return self


if __name__ == "__main__":
    ''' Manual testing. '''
    zroot = Tk(useTk=1)
    zroot.tk_setPalette(background="Light Green")
    zworks = TableDef(Frame(zroot))
    zroot.resizable(width=False, height=False)
    zroot.mainloop()   
    if zworks.has_results():
        zdef = zworks.get_results()
        print("Got:", zdef)
        zroot = Tk(useTk=1)
        zroot.tk_setPalette(background="Light Blue")
        zworks = TableDef(Frame(zroot))
        assert(zworks.put_results(zdef) == True)
        zroot.resizable(width=False, height=False)
        zroot.mainloop()   
        if zworks.has_results():
            zdef = zworks.get_results()
            print("Got2:", zdef)
        


