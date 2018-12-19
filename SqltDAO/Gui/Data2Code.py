#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/12/19: Project Begun

# Mission: Create a graphical, data-file detection, UI for PyDAO.
# Status: WORK IN PROGRESS

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.SqlSyntax import SqliteCrud
from SqltDAO.SchemaDef.Order import OrderDef
from SqltDAO.CodeGen01.CodeGen import DaoGen

from collections import OrderedDict

class Data2Code(simpledialog.Dialog):

    def __init__(self, parent):
        self.ztitle = "Data2Code 0.01"
        self.txt_fn = None
        self.order_info = None
        self.file_name = ""
        self.display_info = OrderedDict()
        dum = dict(OrderClass())
        for key in dum:
            self.display_info[key] = StringVar()
        super().__init__(parent=parent)

    def _show_order(self):
        zdict = dict(self.order_info)
        for key in zdict:
            self.display_info[key].set(zdict[key])

    def on_txt_fn(self):
        self.attributes('-topmost',False)
        fn = askopenfilename()
        if len(fn):
            self.txt_fn.delete(0,END)
            self.txt_fn.insert(0,fn)
        self.attributes('-topmost',True)
        fbase = os.path.splitext(fn)[0]
        nodes = os.path.split(fn)
        fname = nodes[-1]
        subject = os.path.splitext(fname)[0]
        self.order_info = OrderClass(
            class_name=subject,
            table_name=subject,
            db_name=fbase + ".sqlt3",
            file_name=fbase + ".py")
        self._show_order()

    def apply(self):
        #gen = DaoGen()
        #print(gen.write_code(self.order_info, self.file_name, sep="|"))
        pass

    def body(self, zframe):
        self.title(self.ztitle)
        self.geometry("400x200")
        self.resizable(width=False, height=False)
        self.attributes('-topmost',True)
        zfa = LabelFrame(zframe, text=" Table ", bg="Light Green")
        
        Button(zfa,
               text=" ... ",
               bg="Light Green",
               command=self.on_txt_fn
               ).grid(column=0, row=0)
        Label(zfa, text="File: ",bg="Light Green").place(relx=0.1, rely=0.2)

        self.txt_fn = Entry(zfa, width=50)
        self.txt_fn.insert(0, self.file_name)
        self.txt_fn.place(relx=0.2, rely=0.2)

        zfb = LabelFrame(zframe, text=" Detection ", bg="Light Green")
        for ss, key in enumerate(self.display_info):
            Label(zfb, text=key + ": ", bg="Light Green").grid(column=0, row=ss)
            Entry(zfb, width=50, state='readonly',
                  textvariable=self.display_info[key]).grid(column=1, row=ss)

        zfa.pack(fill=BOTH)
        zfb.pack(fill=BOTH)
        zframe.pack(fill=BOTH)
        return self



if __name__ == "__main__":
    zroot = Tk()
    Data2Code(parent=zroot)
    zroot.destroy()


