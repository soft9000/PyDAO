#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/11/24: Project Begun

# Mission: Create a graphical user interface to PyDAO.
# Status: WORK IN PROGRESS

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from collections import OrderedDict

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.SqlSyntax import SqliteCrud
from SqltDAO.SchemaDef.Order import OrderDef
from SqltDAO.CodeGen01.CodeGen import DaoGen

from SqltDAO.Gui.Data2Code import Data2Code
from SqltDAO.Gui.StandardEntry import LabelEntry
from SqltDAO.Gui.TableDef import TableDef as TableDef2
from SqltDAO.SchemaDef.Table import TableDef as TableDef1
from SqltDAO.Gui.DataPrefrences import Dp1 as DataPrefrences

class Main(Tk):

    def __init__(self, *args, **kwargs):
        from SqltDAO.CodeGen01.Meta import Meta
        super().__init__(*args, **kwargs)
        self.ztitle = Meta.Title()
        self.d2c = None
        self.project = None
        self.zoptions = (
            ("Projects",    [("Open Project...", self._on_open),
                             ("Save Project...", self._on_save),
                             ("Create Code", self._on_create)],),
            ("Tools",       [("Data2Code...", self._on_d2c),
                             ("Data2Project...", self._on_d2p),
                             ("Preferences...", self._on_d2pref)]),
            ("About",       [("About PyDao...", self._on_about),
                             ("Quit", self.destroy)]),
            )
        self.table_frame = None
        self.orderDef = OrderDef()
        self.home = "."

        '''
        activeBackground, foreground, selectColor,
        activeForeground, highlightBackground, selectBackground,
        background, highlightColor, selectForeground,
        disabledForeground, insertBackground, troughColor.
        '''
        self.tk_setPalette(
                background="Light Green",# e.g. Global
                foreground="dark blue",  # e.g. Font color
                insertBackground="blue", # e.g. Entry cursor
                selectBackground="gold", # e.g. Editbox selections
                activeBackground="gold", # e.g. Menu selections
                )
    
    def _on_open(self):
        pref = DataPrefrences.Load(self.home)
        self.project = askopenfilename(
            title="Open Project File",
            initialdir=pref['Projects'],
            filetypes=[("PyDAO Project", OrderDef.FileType)]
            )
        if not self.project:
            return
        zdef = OrderDef.LoadFile(self.project)
        if not zdef:
            messagebox.showerror(
                "Schema File / Format Error",
                "Unable to import " + self.project)
        else:
            self.table_frame.got_results()
            self.title(self.project)
            self.orderDef = zdef
            self._show_order()

    def do_save(self):
        ''' Project file must be created for both saving same, as well as for creating code. '''
        ztbl = self.table_frame.pull_results()
        zdict = ztbl.__dict__()
        if not zdict:
            messagebox.showerror(
                "No Data",
                "Schema Definition Required.")
            return False
        self.orderDef = OrderDef(name=ztbl.get_table_name())
        if not self.orderDef.add_table(ztbl):
            messagebox.showerror(
                "Invalid Table",
                "Please verify SQL Table Definition.")
            return False
        if not self.orderDef.home(DataPrefrences.Load(self.home)):
            messagebox.showerror(
                "Invalid Locations",
                "Please verify user locations.")
            return False
        if OrderDef.SaveFile(self.orderDef, overwrite=True) is False:
            messagebox.showerror(
                "Exportation Error",
                "Please verify user locations.")
            return False
        self.table_frame.got_results()
        return True
    
    def _on_save(self):
        if self.do_save() is True:
            val = os.path.split(self.orderDef.file_name)
            messagebox.showinfo(
                "Project Saved",
                "Project file saved as " + val[-1] + " in preference location.")

    def _on_create(self):
        if self.do_save() is True:
            pref = DataPrefrences.Load(self.home)
            order_class = OrderDef.Extract(self.orderDef, pref)
            zfields = OrderedDict()
            ztables = self.orderDef.table_names()
            table_def  = self.orderDef.find_table(ztables[0]) # TODO: Highlander hack.
            for row in table_def:
                zfields[row[1]] = row[2]
            sql = SqliteCrud(order_class, zfields)
            zcode = sql.code_class_template(self.orderDef.db_name, sep='","')
            with open(self.orderDef.code_name, 'w') as fh:
                print(zcode, file=fh)
            val = os.path.split(self.orderDef.code_name)
            messagebox.showinfo(
                "Source Code Success",
                "Class created as " + val[-1] + " in preference location.")

    def _on_d2c(self):
        Data2Code(self, verbose=True)

    def _on_d2p(self):
        Data2Code(self, gendef=True, verbose=True)

    def _on_d2pref(self):
        zpref = DataPrefrences(self, self.home)
        if zpref.has_changed():
            pass

    def _on_about(self):
        messagebox.showinfo(
            self.ztitle,
            "Work In Progress - Not For Use")

    def _show_order(self):
        if not self.orderDef:
            return False
        self.table_frame.empty()
        for key in self.orderDef.zdict_tables:
            td1 = self.orderDef.zdict_tables[key]
            if self.table_frame.put_results(td1) is False:
                messagebox.showerror(
                    "Display Error",
                    "Critical: _show_order regression.")
                return False

    def _set_frame(self):
        zframe = Frame(self)
        self.table_frame = TableDef2(zframe)
        zframe.pack(fill=BOTH)

    def begin(self):
        self.title(self.ztitle)
        try:
            image = PhotoImage(file="zicon.png")
            self.wm_iconphoto(self, image)
        except:
            pass
        zmain = Menu(self)
        for zsub in self.zoptions:
            zdrop = Menu(zmain, tearoff=False)
            zmain.add_cascade(label=zsub[0], menu=zdrop)
            for zz in zsub[1]:
                zdrop.add_command(label=zz[0], command=zz[1])
        self.config(menu=zmain)
        self._set_frame()
        return True

    def run(self):
        self.mainloop()
        return True

    def end(self):
        return True


if __name__ == "__main__":
    main = Main()
    try:
        if main.begin():
            main.run()
    except Exception as ex:
        print(str(ex))
    finally:
        try:
            main.end()
        except:
            pass

