#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/12/19: Project Begun

# Mission: Create a graphical, data-file detection, UI for PyDAO.
# Status: Heavily refactored. Testing success. Alpha.

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.SchemaDef.OrderDef import OrderDef1 as OrderDef
from SqltDAO.CodeGen01.SqlSyntax import SqliteCrud
from SqltDAO.CodeGen01.CodeGen import DaoGen
from SqltDAO.Gui.DataPreferences import Dp1 as DataPreferences
from SqltDAO.SchemaDef.Factory import Factory1

from collections import OrderedDict

class DataAI(simpledialog.Dialog):

    def __init__(self, parent, pref, verbose=False):
        self.gen_ok = False
        self.verbose = verbose
        self.ztitle = "DataAI, Rev 0.1"
        self.order_class = None
        self.import_file_name = StringVar()
        self.import_file_name.set(" ")
        self.field_seps = "Gen Proj", "Gen Code", "Gen Both"
        self.field_sel = StringVar()
        self.field_sel.set(0)

        if not pref:
            self.pref = DataPreferences.Load('.')
        else:
            self.pref = pref

        self.display_info = OrderedDict()
        dum = dict(OrderClass())
        for key in dum:
            self.display_info[key] = StringVar()
        super().__init__(parent=parent)

    def _show_order(self):
        zdict = dict(self.order_class)
        for key in zdict:
            self.display_info[key].set(zdict[key])

    def on_txt_fn(self):
        self.attributes('-topmost', False)
        fn = askopenfilename(
            title="Open Text File",
            initialdir=self.pref['Csv Folder'])
        if not fn:
            return
        detect = Factory1.Detect(fn)
        if not detect:
            messagebox.showerror("Data Format Error", "Unsupported input data / file format.")
            return
        self.import_file_name.set(fn)
        self.attributes('-topmost', True)
        fbase = os.path.splitext(fn)[0]
        nodes = os.path.split(fn)
        fname = nodes[-1]
        subject = os.path.splitext(fname)[0]
        self.order_class = OrderClass(
            class_name=subject,
            table_name=subject,
            db_name=fbase + OrderDef.DbType,
            file_name=fbase + OrderDef.CodeType)
        self.pref['Csv Folder'] = os.path.dirname(fn)
        self.order_class.home(self.pref)
        self.order_class.encoding = detect.encoding 
        self.order_class.sep      = detect.sep
        self._show_order()

    def can_create(self, gen):
        return True # TODO: Check for input & output file existance

    def _create_project(self):
        gen = DaoGen()
        if self.can_create(gen):
            self.gen_ok = gen.write_project(
                self.pref,
                self.order_class,
                self.import_file_name.get())
            return self.gen_ok
        return False

    def _create_code(self):
        gen = DaoGen()
        if self.can_create(gen):
            self.gen_ok = gen.write_code(
                self.pref,
                self.order_class,
                self.import_file_name.get())
            return self.gen_ok
        return False

    def apply(self):
        zsel = self.field_seps[int(self.field_sel.get())]
        try:
            if zsel == "Gen Proj":
                if self.verbose:
                    print("Verbose: Creating Project")
                    self.gen_ok = self._create_project()
            elif zsel == "Gen Code":
                    print("Verbose: Creating Code")
                    self.gen_ok = self._create_code()
            else:
                    print("Verbose: Creating Both")
                    self.gen_ok = self._create_project()
                    if self.gen_ok:
                        self.gen_ok = self._create_code()
        except Exception as ex:
            self.gen_ok = False
            if self.verbose:
                print(ex)
        finally:
            if self.verbose:
                if self.gen_ok:
                    messagebox.showinfo("Generation Success", "File has been generated.")
                else:
                    messagebox.showerror("Data Format Error", "Review input file & definitions to try again.")

    def body(self, zframe):
        self.title(self.ztitle)
        self.resizable(width=False, height=False)
        self.attributes('-topmost',True)
        
        # File Selection
        zfa = LabelFrame(zframe, text=" Table ")
        
        Button(zfa,
               text=" ... ",
               command=self.on_txt_fn
               ).grid(column=0, row=0)
        Label(zfa, text="File: ").place(relx=0.1, rely=0.2)
        efn = Entry(zfa, width=50, textvariable=self.import_file_name)
        efn.place(relx=0.2, rely=0.2)

        # Radio Group
        fradio = LabelFrame(zframe, text = " Field Sep")

        for ss, key in enumerate(self.field_seps):
            zrb = Radiobutton(
                fradio, text=" " + key,
                variable=self.field_sel,
                value=ss)
            zrb.grid(column=ss, row=0)

        # Order Metadata
        zfb = LabelFrame(zframe, text=" Detection ")
        for ss, key in enumerate(self.display_info):
            zShow = self.display_info[key]
            print(key, zShow)
            Label(zfb, text=key + ": ").grid(column=0, row=ss)
            Entry(zfb, width=50, state='readonly',
                  textvariable=zShow).grid(column=1, row=ss)

        zfa.pack(fill=BOTH)
        fradio.pack(fill=BOTH)
        zfb.pack(fill=BOTH)
        zframe.pack(fill=BOTH)
        return self



if __name__ == "__main__":
    pref = DataPreferences.Load('.')
    pref['Csv Folder']  =   "../DaoTest01"
    pref['Projects']    =   "../../Proj"
    pref['Sql Folder']  =   "../../Sql"
    pref['Code Folder'] =   "../../Code"

    for key in pref:
        if not os.path.exists(pref[key]):
            os.mkdir(pref[key])
    
    zroot = Tk(useTk=1)
    zroot.tk_setPalette(background="Light Green")
    zworks = DataAI(parent=zroot, pref=pref, verbose=True)
    zroot.destroy()
    if zworks.gen_ok:
        print("gen okay")
    else:
        print("gen nokay")


