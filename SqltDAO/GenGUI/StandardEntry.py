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
    def CreateFrame(parent, type_dict, entry_width=60):
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


class LabelEntryAction():

    ''' Like LabelEntry, except orders can include buttons (etc).
        Static entry-creation is managed by an instance of this class. '''

    def __init__(self):
        self.keys = ("label", "textvariable", "state", "actiontext", "action")
        self.orders = list()

    def add_entry(self, label, tv=None, state=None, action=None, actiontext=' ... '):
        '''
        Add an order to the internal order-list, returning the order added. Use
        'textvariable' to set/get same. Parameters:

        label: The label to use before the entry field.
        tv: Tkinter / Tk "smart variable." Creates StringVar() by default.
        state: The state for the entry field (e.g. 'readonly')
        action: A function to call when the OPTIONAL action-button is pressed.
        actiontext: The text to display in thine OPTIONAL action button.
        '''
        if not tv:
            tv = StringVar()
        order = dict()
        order['label'] = label
        order['state'] = state
        order['action'] = action
        order['actiontext'] = actiontext
        order['tv'] = tv
        self.orders.append(order)
        return order
    
    @staticmethod
    def CreateFrame(parent, zorders, entry_width=60):
        ''' Arrange data in a classic pattern.
        Returns unpacked Frame, or None on error. '''
        zframe = Frame(parent)
        return LabelEntryAction.AddFields(zframe, zorders, entry_width=entry_width)
    
    @staticmethod
    def CreateLframe(parent, zorders, title="Fill-out Form", entry_width=60):
        ''' Arrange data in a classic pattern.
        Returns unpacked LabelFrame, or None on error. '''
        zframe = LabelFrame(parent, text=title)
        return LabelEntryAction.AddFields(zframe, zorders, entry_width=entry_width)
    
    @staticmethod
    def AddFields(zframe, zorders, entry_width=60, row_start=0):
        ''' Append action-data in a classic pattern to YOUR frame.
        Returns unpacked zframe, or None on error. '''
        if not isinstance(zorders, LabelEntryAction):
            return None
        for ss, zorder in enumerate(zorders.orders, row_start):
            Label(zframe, text=zorder['label'] + ": ").grid(column=0, row=ss)
            if zorder['state']:
                Entry(zframe, width=entry_width,
                      textvariable=zorder['textvariable'],
                      state=zorder['state']).grid(column=1, row=ss)
            else:
                Entry(zframe, width=entry_width,
                      textvariable=zorder['tv']).grid(column=1, row=ss)
            if zorder['action']:
                Label(zframe, width=1).grid(column=2, row=ss)
                Button(zframe, text=zorder['actiontext'],
                       command=zorder['action']).grid(column=3, row=ss)
        return zframe
