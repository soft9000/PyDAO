#!/usr/bin/env python3
#
# Author: Soft9000.com
# 2018/12/27: Project Begun

# Mission: Theme-based API support. 
# Status:  Code Complete. Alpha. Rev 1.0.

''' Mission: A place to save our standard user
    experiences & layout re-use opportunities.
'''

from tkinter import *


class LabelEntry():
    '''
    Create a Tkinter native-type, data-entry display.
    Returns an unpacked frame sporting a grid layout
    of your dictionary-defined fields.

    Tags are field names, entries are rvalues for same.
    (Using Tkinter's smart-variables for the later.)
    '''
    
    @staticmethod
    def CreateFrame(parent, type_dict, title="Fill-out Form", entry_width=60):
        ''' Arrange data in a classic pattern. Returns unpacked Frame. '''
        zframe = Frame(parent)
        return LabelEntry.AddFields(zframe, type_dict, entry_width=entry_width)
    
    @staticmethod
    def CreateLframe(parent, type_dict, title="Fill-out Form", entry_width=60):
        ''' Arrange data in a classic pattern. Returns unpacked LabelFrame. '''
        zframe = LabelFrame(parent, text=title)
        return LabelEntry.AddFields(zframe, type_dict, entry_width=entry_width)
    
    @staticmethod
    def AddFields(zframe, type_dict, entry_width=60, row_start=0, readonly=False):
        ''' Append data in the classic pattern to YOUR frame. Returns unpacked zframe. '''
        for ss, key in enumerate(type_dict, row_start):
            Label(zframe, text=key + ": ").grid(column=0, row=ss)
            if readonly:
                Entry(zframe, width=entry_width,
                      textvariable=type_dict[key],
                      state='readonly').grid(column=1, row=ss)
            else:
                Entry(zframe, width=entry_width,
                      textvariable=type_dict[key]).grid(column=1, row=ss)
        return zframe

        

