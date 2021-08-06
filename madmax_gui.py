from tkinter import filedialog

from tkinter import *
from tkinter import ttk
import tkinter as tk

from pathlib import Path

import os,subprocess

import json


class Madmaxx(tk.Frame):
    def __init__(self, master, width=0, height=0, **kwargs):
        self.width = width
        self.height = height
        self.master= master

        self.homedir=os.getcwd()

        self.install=StringVar()
        self.count=StringVar()
        self.threads=StringVar()
        self.buckets=StringVar()
        self.farmer_key=StringVar()
        self.pool_contract=StringVar()
        self.temp_dir=StringVar()
        self.temp_dir2=StringVar()
        self.dest_dir=StringVar()
        self.public_pool=StringVar()

        self.wait_true=StringVar()


        #self.install=self.location

        self.install_lbl=Label(self.master,text='Madmax Install')
        self.count_lbl=Label(self.master,text='plots -n')
        self.threads_lbl=Label(self.master,text='threads -r')
        self.buckets_lbl=Label(self.master,text='buckets -u')
        self.farmer_lbl=Label(self.master,text='farmer key -f')
        self.pool_c_lbl=Label(self.master,text='contract -c')
        self.t_dir_lbl=Label(self.master,text='temp dir -t')
        self.t2_dir_lbl=Label(self.master,text='temp dir2 -2')
        self.dest_lbl=Label(self.master,text='destination -d')
        self.public_pool_lbl=Label(self.master,text='public pool key -p')

        self.install_entr=Entry(self.master,textvar=self.install)
        self.count_entr=Entry(self.master,textvar=self.count)
        self.threads_entr=Entry(self.master,textvar=self.threads)
        self.buckets_entr=Entry(self.master,textvar=self.buckets)
        self.farmer_entr=Entry(self.master,textvar=self.farmer_key)
        self.pool_c_entr=Entry(self.master,textvar=self.pool_contract)
        self.t_dir_entr=Entry(self.master,textvar=self.temp_dir)
        self.t2_dir_entr=Entry(self.master,textvar=self.temp_dir2)
        self.dest_entr=Entry(self.master,textvar=self.dest_dir)
        self.public_pool_entr=Entry(self.master,textvar=self.public_pool)


        self.install_lbl.grid(row=1,column=1)
        self.count_lbl.grid(row=2,column=1)
        self.threads_lbl.grid(row=3,column=1)
        self.buckets_lbl.grid(row=4,column=1)
        self.farmer_lbl.grid(row=5,column=1)
        self.pool_c_lbl.grid(row=6,column=1)
        self.t_dir_lbl.grid(row=7,column=1)
        self.t2_dir_lbl.grid(row=8,column=1)
        self.dest_lbl.grid(row=9,column=1)
        self.public_pool_lbl.grid(row=10,column=1)

        self.install_entr.grid(row=1,column=2)
        self.count_entr.grid(row=2,column=2)
        self.threads_entr.grid(row=3,column=2)
        self.buckets_entr.grid(row=4,column=2)
        self.farmer_entr.grid(row=5,column=2)
        self.pool_c_entr.grid(row=6,column=2)
        self.t_dir_entr.grid(row=7,column=2)
        self.t2_dir_entr.grid(row=8,column=2)
        self.dest_entr.grid(row=9,column=2)
        self.public_pool_entr.grid(row=10,column=2)

        self.wait_true_btn= Radiobutton(master, text ='click to wait to copy -w', variable = self.wait_true,
                value='TRUE', indicator = 0,
                background = "light blue").grid(row=11,column=2)

        self.find = Button(self.master,text='FIND',command=self.find)
        self.find.grid(row=1,column=3)
        self.start = Button(self.master,text='START',command=self.start)
        self.start.grid(row=11,column=4)

        self.save=Button(self.master,text='save',command=self.save_settings)
        self.save.grid(row=11,column=5)

        self.load=Button(self.master,text='load',command=self.load_settings)
        self.load.grid(row=11,column=6)

    def save_settings(self):
        data={}
        data['madmax_setup']=[]
        data['madmax_setup'].append({'install':self.install.get(),
                                     'count':self.count.get(),
                                     'threads':self.threads.get(),
                                     'buckets':self.buckets.get(),
                                     'farmer_key':self.farmer_key.get(),
                                     'contract':self.pool_contract.get(),
                                     'temp_dir':self.temp_dir.get(),
                                     'temp_dir2':self.temp_dir2.get(),
                                     'dest':self.dest_dir.get(),
                                     'pool key':self.public_pool.get()
                                     })
        os.chdir(self.homedir)
        with open('settings.ini', 'w') as settings:
                json.dump(data, settings)

    def load_settings(self):
        os.chdir(self.homedir)
        with open('settings.ini') as settings:
            data = json.load(settings)
        settings= data['madmax_setup'][0]
        self.install.set(settings['install'])
        self.count.set(settings['count'])
        self.threads.set(settings['threads'])
        self.buckets.set(settings['buckets'])
        self.farmer_key.set(settings['farmer_key'])
        self.pool_contract.set(settings['contract'])
        self.temp_dir.set(settings['temp_dir'])
        self.temp_dir2.set(settings['temp_dir2'])
        self.dest_dir.set(settings['dest'])
        self.public_pool.set(settings['pool key'])

    def find(self):
        self.home = str(Path.home())
        madmax_folder=filedialog.askdirectory(parent=self.master,initialdir=self.home,
                                  title='Please select madmax dir')
        madmax_folder=os.path.join(madmax_folder,'build')
        self.install.set(madmax_folder)

    def start(self):

        self.command_handle_dict={'-n':self.count.get(),'-r':self.threads.get(),
                                  '-u':self.buckets.get(),'-f':self.farmer_key.get(),
                                  '-c':self.pool_contract.get(),'-t':self.temp_dir.get(),
                                  '-2':self.temp_dir2.get(),'-d':self.dest_dir.get(),
                                  '-p':self.public_pool.get(),'-w':self.wait_true.get()}
        commands=['./chia_plot']
        for key in self.command_handle_dict:
            if key == '-w':
                if self.command_handle_dict[key] != 'TRUE':
                        pass
                else:
                    commands.append(key)
                    commands.append(self.command_handle_dict[key])
            elif self.command_handle_dict[key] =='':
                pass
            else:
                commands.append(key)
                commands.append(self.command_handle_dict[key])

        madmax_dir=self.install.get()
        os.chdir(madmax_dir)
        subprocess.check_call(commands)
