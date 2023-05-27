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
from SqltDAO.SchemaDef.OrderDef import OrderDef1 as OrderDef
from SqltDAO.SchemaDef.Factory import Factory1

from SqltDAO.Gui.Data2Code import Data2Code
from SqltDAO.Gui.StandardEntry import LabelEntry
from SqltDAO.Gui.TableDef import TableDef as TableDef2
from SqltDAO.SchemaDef.Table import TableDef as TableDef1
from SqltDAO.Gui.DataPreferences import Dp1 as DataPreferences

class Main(Tk):

    def __init__(self, *args, **kwargs):
        from SqltDAO.CodeGen01.Meta import Meta
        super().__init__(*args, **kwargs)
        self.ztitle = Meta.Title()
        self.d2c = None
        self.project = None
        self.zoptions = (
            ("Projects",    [("New Project...", self._on_new),
                             ("Open Project...", self._on_open),
                             ("Save Project...", self._on_save),
                             ("Create Code", self._on_code_create)],),
            ("Tools",       [("Data2Code...", self._on_d2c),
                             ("Data2Project...", self._on_d2p),
                             ("Preferences...", self._on_d2pref)]),
            ("About",       [("About PyDao...", self._on_about),
                             ("Quit", self.destroy)]),
            )
        self.table_frame = None
        self.home = "."
        self.order_def = OrderDef()

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

    def _on_new(self):
        self.title(self.ztitle)
        self.order_def = OrderDef()
        self.table_frame.empty()
        self.table_frame.got_results()
        self.table_frame.table_name.set(TableDef1.DEFAULT_NAME)
        self._show_order()
    
    def _on_open(self):
        pref = DataPreferences.Load(self.home)
        self.project = askopenfilename(
            title="Open Project File",
            initialdir=pref['Projects'],
            filetypes=[("PyDAO Project", OrderDef.ProjType)]
            )
        if not self.project:
            return
        zdef = Factory1.LoadFile(self.project)
        if not zdef:
            messagebox.showerror(
                "Schema File / Format Error",
                "Unable to import " + self.project)
        else:
            self.table_frame.got_results()
            self.title(self.project)
            self.order_def = zdef
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
        self.order_def = OrderDef(name=ztbl.get_table_name())
        if not self.order_def.add_table(ztbl):
            messagebox.showerror(
                "Invalid Table",
                "Please verify SQL Table Definition.")
            return False
        if Factory1.SaveFile(DataPreferences.Load(self.home), self.order_def, overwrite=True) is False:
            messagebox.showerror(
                "Exportation Error",
                "Please verify user locations.")
            return False
        self.table_frame.got_results()
        return True
    
    def _on_save(self):
        if self.do_save() is True:
            val = os.path.split(self.order_def.project_name)
            messagebox.showinfo(
                "Project Saved",
                "Project file saved as " + val[-1] + " in preference location.")

    def _on_code_create(self):
        ''' Generate Python code '''
        if self.do_save() is True:
            pref = DataPreferences.Load(self.home)
            order_class = Factory1.Extract(self.order_def, pref)
            zfields = OrderedDict()
            ztables = self.order_def.table_names()
            table_def  = self.order_def.find_table(ztables[0]) # TODO: Highlander hack.
            for row in table_def:
                zfields[row[1]] = row[2]
            sql = SqliteCrud(order_class, zfields)
            zcode = sql.code_class_template(
                self.order_def.database_name + OrderDef.TEXT_DATA_TYPE)
            with open(self.order_def.code_name, 'w') as fh:
                print(zcode, file=fh)
            val = os.path.split(self.order_def.code_name)
            messagebox.showinfo(
                "Source Code Success",
                "Class created as " + val[-1] + " in preference location.")

    def _on_d2c(self):
        Data2Code(self, pref=DataPreferences.Load(self.home), verbose=True)

    def _on_d2p(self):
        Data2Code(self, pref=DataPreferences.Load(self.home), gendef=True, verbose=True)

    def _on_d2pref(self):
        zpref = DataPreferences(self, self.home)
        if zpref.has_changed():
            pass

    def _on_about(self):
        messagebox.showinfo(
            self.ztitle,
            "Official Release")

    def _show_order(self):
        if not self.order_def:
            return False
        self.table_frame.empty()
        for key in self.order_def._zdict_tables:
            td1 = self.order_def._zdict_tables[key]
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
        super().mainloop()
        return True

    def end(self):
        return True
    
    @staticmethod
    def mainloop():
        main = Main()
        try:
            if main.begin():
                main.run()
                return True
        except Exception as ex:
            print(str(ex))
            return False
        finally:
            try:
                main.end()
            except:
                pass



if __name__ == "__main__":
    Main.mainloop()


