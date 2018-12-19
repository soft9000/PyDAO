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
from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.SqlSyntax import SqliteCrud
from SqltDAO.SchemaDef.Order import OrderDef

from tkinter import messagebox

class Main(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ztitle = "PyDAO 0.002"
        self.zsize = (600, 400)
        self.project = None
        self.schema_def = None
        self.zoptions = (
            ("Projects",    [("Open Project", self._on_open),
                             ("Save Project", self._on_save)]),
            ("Generate",    [("Create Code", self._on_create)]),
            ("About",       [("About PyDao", self._on_about),
                             ("Quit", self.destroy)]),
            )

    def _on_open(self):
        from tkinter.filedialog import askopenfilename
        self.project = askopenfilename()
        self.title(self.project)
        print(self.project)
        zdef = OrderDef.LoadFile(self.project)
        if not zdef:
            messagebox.showerror(
                "Schema File / Format Error",
                "Unable to import " + self.project)
        else:
            self.schema_def = zdef

    def _on_save(self):
        if not self.schema_def:
            messagebox.showerror(
                "No Data",
                "Schema Definition Required.")
            return False
        return True

    def _on_create(self):
        self._on_about()

    def _on_about(self):
        messagebox.showinfo(
            self.ztitle,
            "Work In Progress - Not For Use")

    def _set_frame(self):
        size = self.minsize()
        zframe = Frame(self)
        zfa = LabelFrame(zframe, text=" Project ", background="Light Green", width=size[0]/2, height=size[1])
        zfa.pack(side=LEFT)
        zfa = LabelFrame(zframe, text=" Fields ", background="Light Blue", width=size[0]/2, height=size[1])
        zfa.pack(side=RIGHT)
        zframe.pack()
        self.resizable(height=False, width=False)
        

    def _center(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = int((width - self.zsize[0]) / 2)
        y = int((height - self.zsize[1]) / 2)
        zstr = "+{}+{}".format(x, y)
        self.geometry(zstr)

    def begin(self):
        self.title(self.ztitle)
        self._center()
        self.minsize(*self.zsize)
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
    if True:
        main = Main()
        if main.begin():
            main.run()
    else:
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

