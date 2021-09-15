
from tkinter import *
from tkinter import filedialog
import tkinter as tk

from tkscrolledframe import ScrolledFrame

import git

import os
import subprocess
import shutil

from pathlib import Path

from cli_installer import nonGui


class File_Manager(tk.Frame):
    def __init__(self, master, repos, folder_names, logos, bin_files, **kwargs):
        self.width = '500'
        self.height = '430'
        self.master= master
        self.frame1 = ScrolledFrame(self.master, width=self.width, height=self.height)
        self.frame1.pack(side="top",fill="both", expand=1)
        self.frame1.bind_arrow_keys(self.master)
        self.frame1.bind_scroll_wheel(self.master)
        self.inner_frame=self.frame1.display_widget(Frame)
        self.inner_frame.configure(bg='turquoise')

        self.master.title('INSTALLER')

        self.repos = repos

        self.logos = logos

        self.bin_files=bin_files

        self.folder_names=folder_names

        self.build_menu()

    def install_all(self,event):
        self.popup_two=Toplevel()
        self.exclude= tk.StringVar()
        self.popup_two.title('EXCLUDE/INCLUDE')
        exclude_advice=Label(self.popup_two,text='list repos to exclude, using commas eg madmax,agem,chia',font='Arial 16',fg='white',bg='turquoise',compound=BOTTOM)
        exclude_entry=Entry(self.popup_two,textvariable=self.exclude)
        exclude_advice.pack()
        exclude_entry.pack()

        self.include= tk.StringVar()
        include_advice=Label(self.popup_two,text='list repos to include',font='Arial 16',fg='white',bg='turquoise',compound=BOTTOM)
        include_entry=Entry(self.popup_two,textvariable=self.include)
        include_advice.pack()
        include_entry.pack()
        
        exclude_entry.bind('<Return>',lambda event: self.exclude_and_install(event))
        include_entry.bind('<Return>',lambda event: self.exclude_and_install(event))

    def exclude_and_install(self,event):
        exclude_list=self.exclude.get().split(',')
        include_list=self.include.get().split(',')
        exclude_list.append('all')
        self.popup_two.destroy()
        install_list=[]

        if len(include_list) ==1:
            for repo in self.repos:
                if repo in exclude_list:
                    pass
                else:
                    install_list.append(repo)

        elif len(include_list) >1:
            for repo in self.repos:
                if repo in include_list:
                    if repo not in exclude_list:
                        install_list.append(repo)

        print(install_list)
                
        home = str(Path.home())
        folder=filedialog.askdirectory(parent=self.frame1,initialdir=home,
                                  title='Please select a directory for all installs')
        for repo in install_list:
            print('proceeding to install {}'.format(repo))
            self.wname(event,repo,folder)

        

    def wname(self,event,all_check,folder):

            if all_check == 'None':
                filename=self.label_id_text[id(event.widget)]
            else:
                filename=all_check
            if folder=='None':
                home = str(Path.home())
                folder=filedialog.askdirectory(parent=self.frame1,initialdir=home,
                                  title='Please select a directory')

            install_this=nonGui(self.repos,self.folder_names,self.bin_files,filename,folder)            



    def build_menu(self):

            self.image_vars={}

            for key in self.logos.keys():
                self.image_vars[key]=PhotoImage(data=self.logos[key])

            

            class File(object):
                def __init__(self,name,repo):
                      setattr(self,'name', 'repo')
                      self.name=name
                      self.repo=repo 
                def __repr__(self):
                    return "%s"%self.__dict__
                def __exit__(self,exc_type,exc_val,exc_tb):
                    pass
            all_repos=[]
            for repo in self.repos:
                all_repos.append(File(repo,self.repos[repo]))

            
            self.label={}
            self.label_id_text={}

            x=2
            y=0
        
            for lbl in all_repos:
            
                self.label[lbl.name]=Label(self.inner_frame,text=lbl.name, font=('Arial 16'),fg='white',bg='turquoise',compound=LEFT,image=self.image_vars[lbl.name])
                self.label[lbl.name].grid(row=x,column=y,sticky= NW)
                self.label[lbl.name].bind('<Double-Button-1>',lambda event:self.wname(event,'None','None'))
                self.label_id_text[id(self.label[lbl.name])]=lbl.name
                x=x+1
                if x==8:
                    y=y+1
                    x=2
            self.label['all'].unbind
            self.label['all'].bind('<Double-Button-1>',lambda event:self.install_all(event))
            self.master.geometry('790x580')
            

            
