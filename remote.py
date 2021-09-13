
from tkinter import *
from tkinter import ttk
import tkinter as tk

from pathlib import Path

import os
import json

class Remote_farmer(tk.Frame):
    def __init__(self, master, ini_file,width=0, height=0, **kwargs):
        self.width = width
        self.height = height
        self.master= master
       
        self.name=StringVar()
        self.ip=StringVar()
        self.ini=ini_file
       
        self.name_lbl=Label(self.master,text='Name')
        self.ip_lbl=Label(self.master,text='IP or domain')

        self.name_entr=Entry(self.master,textvar=self.name)
        self.ip_entr=Entry(self.master,textvar=self.ip)
       
        self.name_lbl.grid(row=1,column=1)
        self.name_entr.grid(row=2,column=1)
        
        self.ip_lbl.grid(row=3,column=1)
        self.ip_entr.grid(row=4,column=1)

        self.add = Button(self.master,text='add',command=self.save_settings)
        self.add.grid(row=2,column=3)


        self.load_settings()


    def save_settings(self):
        with open(self.ini) as settings:
            data = json.load(settings)
            old_settings = data['remote_setup']
            old_settings.append({f"{self.name.get()}":f"{self.ip.get()}"})
            with open(self.ini, 'w') as settings:
                json.dump(data, settings)

    def load_settings(self):
        with open(self.ini) as settings:
            data = json.load(settings)
        settings= data['remote_setup']
        self.loadout={}
        self.loadout_id_text={}
        x= 5
        y=1
        for d in settings:
            for name in d:
                self.loadout[name]=Label(self.master,text=f"{name} {d[name]}", fg='white',font='Arial 16',compound=LEFT)
                self.loadout[name].grid(row =x,column=y)
                dlt=f"{name}_delete"
                self.loadout[dlt]=Button(self.master,text='delete')
                self.loadout[dlt].bind('<Button-1>',lambda event: self.delete(event))
                self.loadout[dlt].grid(row=x,column=y+2)
                self.loadout_id_text[id(self.loadout[dlt])]=dlt
                x+=1

    def delete(self,event):
        delete_this=self.loadout_id_text[id(event.widget)]
        delete_this=delete_this.split('_')[0]
        with open(self.ini) as settings:
            data = json.load(settings)
            old_settings = data['remote_setup']
            for d in old_settings:
                for name in d:
                    if name == delete_this:
                        old_settings.remove(d)
            with open(self.ini, 'w') as settings:
                json.dump(data, settings)


        
