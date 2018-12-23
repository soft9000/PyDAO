#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/12/20: Project Begun

# Mission: Create a Tkinter native-type, ordered, data-dictionary display / Frame.
# Status:  WORK IN PROGRESS
# Release: Blogged as 'FieldFrame': http://soft9000.com/blog9000/comments.php?y=18&m=12&entry=entry181220-100135

from tkinter import *
from collections import OrderedDict

class DataFrameOne():

    ''' Support a slightly more pythonic, ad-hoc way of displaying
    Tkinter's 'smart variables.' Additonal masking / data type
    validaiton / support as time permits.
    '''

    def __init__(self, parent, type_dict, title, entry_width=60):
        ''' Create + initialize your DataFrameOne.
        parent = Tkinter window / toplevel
        type_dict = Dictionary 'key' is label, value is smart-variable.
        title = Title frame / Labelframe title
        entry_width = Character width for all text-entry fields.
        '''
        self.parent = parent
        self.entry_width = entry_width
        self.bg = "Light Green"
        self.display_info = type_dict
        self.ztitle = title
        self.frames = dict()
        self.frames["root"]     = Frame(parent, bg=self.bg)
        self.frames["title"]    = self.mk_title(self.frames["root"])  # Container        
        self.frames["buttons"]  = self.mk_buttons(self.frames["title"]) # Siblings
        self.frames["body"]     = self.mk_body(self.frames["title"])    # Siblings
        self.do_pack()

    def do_pack(self):
        ''' An opportunity to provide your own packing logic. '''
        self.frames["body"].pack()
        self.frames["buttons"].pack()
        self.frames["title"].pack(fill=BOTH)
        self.frames["root"].pack(fill=BOTH)


    def get_frames(self):
        ''' Returns a dictionary of the frames in-play. '''
        return self.frames

    def get_data(self):
        ''' Retrieve the data / smart variables used to create instance. '''
        return self.display_info

    def show_data(self, zdict):
        ''' Update the smart variables ('show') by using a more classic means. '''
        for key in zdict:
            self.display_info[key].set(zdict[key])

    def apply(self):
        ''' An opportunity to perform additional "okay" validation. '''
        self.cancel()

    def cancel(self):
        ''' An opportunity to perform additional "cancel" validation. '''
        self.parent.destroy()

    def mk_title(self, zframe):
        ''' The title frame contains the button and body frames. '''
        return LabelFrame(
            zframe,
            text=" {} ".format(self.ztitle),
            bg=self.bg)

    def mk_buttons(self, zframe):
        ''' The button frame contains the display's lifecycle buttons. '''
        my_frame = Frame(zframe, bg=self.bg)
        Button(my_frame, text=" {} ".format("Okay"),
               bg=self.bg, command=self.apply
               ).grid(column=0, row=0)
        Label(my_frame, text="   ",
               bg=self.bg).grid(column=1, row=0)
        Button(my_frame, text=" {} ".format("Cancel"),
               bg=self.bg, command=self.cancel
               ).grid(column=2, row=0)
        return my_frame

    def mk_body(self, zframe):
        ''' The body frame is where the data-entry options are displayed. '''
        my_frame = Frame(zframe, bg=self.bg)
        for ss, key in enumerate(self.display_info):
            Label(my_frame, text=" {}: ".format(key), bg=self.bg).grid(column=0, row=ss)
            Entry(my_frame, width=self.entry_width,
                  textvariable=self.display_info[key]).grid(column=1, row=ss)
        return my_frame

    def __dict__(self):
        ''' Expresses smart variables using a classic dictionary. '''
        results = dict()
        for key in self.display_info:
            results[key] = self.display_info[key].get()
        return results

    def __iter__(self):
        ''' Iterate thru the presently displayed / smart variable values. '''
        for key in self.display_info:
            yield key, self.display_info[key].get()

    def __str__(self):
        ''' Handy for comparisons, but returns the present, smart-variable, values. '''
        results = self.__dict__()
        return str(results)

if __name__ == "__main__":
    zroot = Tk()
    zroot.title("DataFrameOne")
    data = OrderedDict()
    # The Variable Classes (BooleanVar, DoubleVar, IntVar, StringVar)
    data["Name"] = StringVar()
    data["User Age"] = StringVar()
    data["Account Balance"] = StringVar()
    zroot.zdata = DataFrameOne(zroot, data, "Drongo")
    stuff = dict()
    for key in zroot.zdata.get_data():
        stuff[key] = "This is " + key
    zroot.zdata.show_data(stuff)
    zroot.mainloop()
    for line in zroot.zdata:
        print(line)
    


