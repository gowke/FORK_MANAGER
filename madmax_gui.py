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

        self.install.set(self.homedir)

       
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

        self.copy_data="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h5HAIpaQgggZNZRRgYUorRopJtK0H/fwDzn+FLlkcpXByLGAKlRIjh/8D353axYmYm5SKA50v9j2xwgQ2AWaddv+Prbt5gngfwautLa/2gBmPkmvt7XIEdC/DVxctzV5D7jcAQafdMmQHMlPUygUgPcz+qYcMHAL9Ky5vbX2cfoAZKir5A1wcAiMFil73ePdwc7e/j3T6u8Hs5dywQkaVg8AAA+LaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczppcHRjRXh0PSJodHRwOi8vaXB0Yy5vcmcvc3RkL0lwdGM0eG1wRXh0LzIwMDgtMDItMjkvIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6cGx1cz0iaHR0cDovL25zLnVzZXBsdXMub3JnL2xkZi94bXAvMS4wLyIKICAgIHhtbG5zOkdJTVA9Imh0dHA6Ly93d3cuZ2ltcC5vcmcveG1wLyIKICAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICB4bXBNTTpEb2N1bWVudElEPSJnaW1wOmRvY2lkOmdpbXA6MDdlN2U5ODgtMWEwYi00NTEwLWExMWQtYTYyZDljNWE0ODlhIgogICB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjBhZmVlMzU2LWY1MGQtNGE3ZS1iMmZjLTQ3MGFkYzQwZmNhOSIKICAgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjUxY2I5NmQ4LWQwM2EtNDM4YS1iYzNlLWE4NWQxYTQxNGY5ZSIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iTGludXgiCiAgIEdJTVA6VGltZVN0YW1wPSIxNjI4MzM3MDk5MTU3MDk1IgogICBHSU1QOlZlcnNpb249IjIuMTAuMjIiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCI+CiAgIDxpcHRjRXh0OkxvY2F0aW9uQ3JlYXRlZD4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OkxvY2F0aW9uQ3JlYXRlZD4KICAgPGlwdGNFeHQ6TG9jYXRpb25TaG93bj4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OkxvY2F0aW9uU2hvd24+CiAgIDxpcHRjRXh0OkFydHdvcmtPck9iamVjdD4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OkFydHdvcmtPck9iamVjdD4KICAgPGlwdGNFeHQ6UmVnaXN0cnlJZD4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OlJlZ2lzdHJ5SWQ+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjVjYTk2ZGE4LWIxNTUtNDFlMC1hNTQxLTI0NDhmY2U5ODcwYyIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChMaW51eCkiCiAgICAgIHN0RXZ0OndoZW49IiswNDowMCIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgIDxwbHVzOkltYWdlU3VwcGxpZXI+CiAgICA8cmRmOlNlcS8+CiAgIDwvcGx1czpJbWFnZVN1cHBsaWVyPgogICA8cGx1czpJbWFnZUNyZWF0b3I+CiAgICA8cmRmOlNlcS8+CiAgIDwvcGx1czpJbWFnZUNyZWF0b3I+CiAgIDxwbHVzOkNvcHlyaWdodE93bmVyPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6Q29weXJpZ2h0T3duZXI+CiAgIDxwbHVzOkxpY2Vuc29yPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6TGljZW5zb3I+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz4V8AKqAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAAHYAAAB2AH6XKZyAAAAB3RJTUUH5QgHCzMnes5sUwAAAXBJREFUeNrtmcGuxCAIRcXI/38wi76VSdP0VUdFQGA5mZZyQTgqJKVGRFfP/xARZvyA5eBXiFCSAXsL8FeR1FZAK5Cv7M48Wy1bKnUOA82BtjI4I2B9N2gJfrabj4iCiJBPL3E1U4Czk4/6JKKr7M7yzqp4+kJEQES4/55PDb7Xf5F0rkGcsiqA/7q4ZNbrN319Q+YMXhs+q90LSApYRuBhRXDPcSQlTk7KjbuHZAu0tm0KSHVyCUr8bIK7q+KN2MQ4QCuwmN8MaTxPaE6BunngXv/iHKAZVDjhChGhnBLM6PtycmhEdNW+4lKAuxCuBXBfAcEBvQJw0p/0iM1Ws7tKWPEl0AssQYIxBUKAECA4IDggOGA9Bzyvi11yQMvB8RxwPyBwNwa93wwFCAUIBQecyQFmULinAjhFivMATw3vLZEur8bcbId7hA0Q8hp4XVbue0AsgdgLKMbUqACJCjgZe5sV4PF0CCwE7noMci/JP6ek7LWPcTk6AAAAAElFTkSuQmCC"
        self.copy_lbl=PhotoImage(data=self.copy_data)

        self.copy=Label(self.master,image=self.copy_lbl,text='copy command to clipboard',fg='white',font='Arial 16',compound=BOTTOM)
        self.copy.grid(row=5, column=4)
        self.copy.bind('<Button-1>',self.copy_cmd)

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

    def build_command(self,commands):
        

        self.command_handle_dict={'-n':self.count.get(),'-r':self.threads.get(),
                                  '-u':self.buckets.get(),'-f':self.farmer_key.get(),
                                  '-c':self.pool_contract.get(),'-t':self.temp_dir.get(),
                                  '-2':self.temp_dir2.get(),'-d':self.dest_dir.get(),
                                  '-p':self.public_pool.get(),'-w':self.wait_true.get()}        

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
        print('before return',commands)

        return commands
        

    def start(self):
        commands=['./chia_plot']
        commands=self.build_command(commands)
        madmax_dir=self.install.get()
        os.chdir(madmax_dir)
        subprocess.check_call(commands)

    def copy_cmd(self,event):
        commands=['./chia_plot']
        commands=self.build_command(commands)
        commands_str=' '.join(commands)
        print('cd {} && {}'.format(self.install.get(),commands_str))
        
