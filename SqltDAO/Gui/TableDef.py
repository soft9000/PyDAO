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
from tkinter import simpledialog

from StandardEntry import LabelEntry
from SqltDAO.SchemaDef.Table import TableDef as TableDef1

from collections import OrderedDict

class TableDef(simpledialog.Dialog):

    def __init__(self, parent, title="Table Definition"):
        self.ztitle = title
        self.table_name = StringVar()
        self.field_type = StringVar()
        self.field_name = StringVar()
        self.field_types = ("text", "integer", "float")
        self.field_type.set(self.field_types[0])
        self.field_name.set("my_field")
        self.table_name.set("Default")
        self.zlb = None
        self.results = None
        super().__init__(parent=parent)

    def has_results(self):
        return (self.results != None)

    def get_results(self):
        return self.results

    def apply(self):
        self.results = TableDef1(name=self.table_name.get())
        zdict = self._get_fields()
        for key in zdict:
            self.results.add_field(key, zdict[key])       

    def _get_fields(self):
        results = OrderedDict()
        for ss in range(self.zlb.size()):
            entry = self.zlb.get(ss)
            split = entry.split(':')
            results[split[0]]=split[1]
        return results

    def _on_def(self):
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

    def _on_edit(self):
        ztuple = self.zlb.curselection()
        if ztuple:
            entry = self.zlb.get(ztuple[0])
            split = entry.split(':')
            self.field_name.set(split[0])
            self.field_type.set(split[1])

    def _on_delete(self):
        ztuple = self.zlb.curselection()
        if ztuple:
            self.zlb.delete(ztuple[0])

    def body(self, zframe):
        self.title(self.ztitle)
        self.resizable(width=False, height=False)
        self.attributes('-topmost',True)
        
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
    zroot = Tk(useTk=1)
    zroot.tk_setPalette(background="Light Green")
    zworks = TableDef(parent=zroot)
    if zworks.has_results():
        zdef = zworks.get_results()
        print("Got:", zdef)
    zroot.destroy()


