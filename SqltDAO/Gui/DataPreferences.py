#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/11/29: Project Begun

# Mission: Permit user preferences for data, code, project, and default import locations.
# Status: Code Complete. Alpha.

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter import simpledialog

from collections import OrderedDict

from SqltDAO.Gui.StandardEntry import LabelEntryAction

class Preferences:
    ''' Opportunity to create an official class to manage those
    final resting places. '''

    def __init__(self, zdict):
        self._zdict = zdict
        
    def __iter__(self):
        ''' Classic usage requires that we make it scriptable... '''
        for key in self._zdict.keys():
            yield key
        
    def __getitem__(self, key):
        ''' Classic usage requires that we make it scriptable... '''
        return self._zdict[key]
        
    def __setitem__(self, key, value):
        ''' Classic usage requires that we make it scriptable... '''
        self._zdict[key] = value
    

class Dp1(simpledialog.Dialog):

    FILE_NAME = "DataPref.dp1"
    KEYS = ('Projects', 'Csv Folder', 'Sql Folder', 'Code Folder')

    def __init__(self, parent, home_dir):
        self.home_dir = Dp1.MkHome(home_dir)
        self.bChanged = False
        self.options = OrderedDict()
        for key in Dp1.KEYS:
            self.options[key] = StringVar()
        for line in self.options:
            self.options[line].set(self.home_dir)
        super().__init__(parent=parent)
        
    def has_changed(self):
        return self.bChanged

    def get_folder(self, key):
        var = self.options[key].get()
        self.attributes('-topmost',False)
        var = askdirectory(initialdir=var)
        self.attributes('-topmost',True)
        if not var:
            return
        self.options[key].set(var)

    def _on_project(self):
        self.get_folder('Projects')

    def _on_csv(self):
        self.get_folder('Csv Folder')

    def _on_sql(self):
        self.get_folder('Sql Folder')

    def _on_code(self):
        self.get_folder('Code Folder')

    def body(self, zframe):
        self.title("PyDAO Locations")
        legacy = Dp1.Load(self.home_dir)
        if legacy:
            for key in self.options:
                try:
                    self.options[key].set(legacy[key])
                except:
                    continue
        order = LabelEntryAction()
        order.add_entry('Projects', tv=self.options['Projects'], action=self._on_project)
        order.add_entry('Csv Folder', tv=self.options['Csv Folder'], action=self._on_csv)
        order.add_entry('Sql Folder', tv=self.options['Sql Folder'], action=self._on_sql)
        order.add_entry('Code Folder', tv=self.options['Code Folder'], action=self._on_code)
        LabelEntryAction.CreateLframe(self,order, title=' Folder Locations ').pack(fill=BOTH)
        self.attributes('-topmost',True)

    def __dict__(self):
        order = OrderedDict()
        for key in self.options:
            order[key] = self.options[key].get()
        return order

    def __iter__(self):
        order = self.__dict__()
        for key in order:
            yield key, order[key]

    def apply(self):
        self.bChanged = True
        order = self.__dict__()    
        ofile = os.path.normpath(self.home_dir + os.sep + Dp1.FILE_NAME)
        with open(ofile, 'w') as fh:
            fh.write(str(order))

    @staticmethod
    def MkHome(home_dir):
        home_dir = os.path.abspath(home_dir)
        home_dir = os.path.normpath(home_dir)
        if not os.path.exists(home_dir):
            home_dir = os.path.abspath('.')
            home_dir = os.path.normpath(home_dir)
        home_dir = home_dir.replace('\\', '/')
        if home_dir.endswith('/'):
            return home_dir[:-1]
        return home_dir

    @staticmethod
    def Load(home_dir):
        ''' Returns a dictionary if preferences are found. Defaults to home location if none. '''
        home_dir = Dp1.MkHome(home_dir)
        ofile = os.path.normpath(home_dir + os.sep + Dp1.FILE_NAME)
        try:
            with open(ofile) as fh:
                return Preferences(eval(fh.readline()))
        except:
            result = OrderedDict()
            for key in Dp1.KEYS:
                result[key] = home_dir
            return Preferences(result)



if __name__ == "__main__":
    ''' Manual testing '''
    try:
        zdict = Preferences({"One":"Ima One", "Two":"We Be Two"})
        for key in zdict:
            print(zdict[key])
    except Exception as ex:
        raise ex
    
    zroot = Tk()
    zword = Dp1(zroot, '.')
    zroot.mainloop()
    
    
