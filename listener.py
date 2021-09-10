

import socket, ssl, json
import subprocess
from os.path import expanduser
import os
import pickle,threading


class Listener(object):
    def __init__(self,cert,key,folder_names,ports_tf,**kwargs):
        

        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.context.load_cert_chain(certfile=cert, keyfile=key)
        self.folder_names=folder_names
        self.host_folder=self.get_env()
        self.run()

    def get_env(self):
        with open('console.py','r') as console:
            lines = console.readlines()
            ini_loc_line=lines[41]
            env_path=os.path.split(ini_loc_line)[0]
            return env_path

    def detect_no_gui():
                ports_true='FALSE'
                host_venv=os.path.join(self.host_folder,'venv/bin')
                forks_folder=os.path.join(self.host_folder,'FORKS')
                files_in_bin=os.listdir(host_venv)
                all_found_repos=[]
                config_yamls={}
                db_files={}
                folder_to_delete={}
        
                home = expanduser('~')
                for key in self.folder_names.keys():
                    folder_to_delete[key]={'home_folder':'','bin_files':'','FORKS_folder':'','fingerprint':'','host_venv':'','db_size':'','farm_status':'','plot_count':'','ports':''}
                    if key in files_in_bin:
                        for folder in os.listdir(home):
                            if '.{}'.format(key) in folder:
                                db_files[key]=os.path.join(home,folder,'mainnet','db','blockchain_v1_mainnet.sqlite')              
                                config_yamls[key]=os.path.join(home,folder,'mainnet','config','config.yaml')
                                folder_to_delete[key]['home_folder']=os.path.join(home,folder)


                bin_files=['_farmer','_full_node','_full_node_simulator','_harvester','_introducer',
                        '_timelord','_timelord_launcher','_wallet']

                for key in self.folder_names.keys():
                        if key in files_in_bin:
                            if key in folder_to_delete.keys():
                                folder_to_delete[key]['bin_files']=[]
                                folder_to_delete[key]['bin_files'].append(key)
                            for entry in bin_files:
                                folder_to_delete[key]['bin_files'].append(key+entry)
                        for folder in os.listdir(forks_folder):
                            if folder == self.folder_names[key]:
                                    folder_to_delete[key]['FORKS_folder']=os.path.join(forks_folder,folder)
                            elif self.host_folder == self.folder_names[key]:
                                folder_to_delete[key]['FORKS_folder']=host_venv_folder
                                folder_to_delete[key]['host_venv']='TRUE'

                for key in folder_to_delete:
                    if folder_to_delete[key]['FORKS_folder'] == '': #skips host folder
                        pass
                    else:
                        try:
                            key_path=os.path.join(host_venv,key)
                            p=subprocess.run([f"{key_path}","keys","show"],capture_output=True, shell=False)
                        except:
                            pass
                        try:
                            if p.returncode ==0:
                                a_key=[]
                                split_by_word = p.stdout.decode('utf-8').split()
                                a_key_indeces = [i for i, word in enumerate(split_by_word) if word == "Fingerprint:"]
                                for i in a_key_indeces:
                                    a_key.append(split_by_word[i+1])
                                folder_to_delete[key]['fingerprint'] =a_key
                            if p.returncode ==1:
                                 pass
                        except Exception as e:
                            pass
       
                for key in self.folder_names.keys():
                    if key in files_in_bin:
                        all_found_repos.append(key)
     

                for lbl in all_found_repos:
		#find size of DB

                        try:
                            file_size='{:,.0f}'.format(os.path.getsize(db_files[lbl])/float(1<<30))+" GB"
                        except:
                            file_size='no file, run init'
                        folder_to_delete[lbl]['db_size']=file_size
                    
                #get farm summary 
                        if lbl in config_yamls.keys():

                            try:
                                lbl_path=os.path.join(hots_venv,lbl) 
                                status=subprocess.run([lbl_path,'farm','summary'],capture_output=True, shell=False)
                                output =status.stdout.decode('utf-8')
                                lst= output.split('\n')
                                plot_status=str
                        
                                for line in lst:
                                    if 'Plot count' in line:
                                        plt_cnt=[lst[lst.index(line)],lst[lst.index(line)+1]]
                                        plot_status=' '.join(plt_cnt)
                                    if 'Farming status' in line:
                                        farm_status=lst[lst.index(line)]
                                folder_to_delete[lbl]['farm_status']={'plt_cnt':plot_status,'Farming status':farm_status}
                            except Exception as e:
                                print(e)

                   #ports check 
                            if ports_true =='TRUE':
                    
                                yaml_file=self.config_yamls[lbl]
                    
                                with open(yaml_file,'rb') as config:
                                    data_loaded = yaml.safe_load(config)

                                ports= {'daemon_port':data_loaded['daemon_port'],
                                    'full_node':data_loaded['full_node']['port'],
                                    'full_node_rpc_port':data_loaded['full_node']['rpc_port'],
                                    'harvester':data_loaded['harvester']['port'],
                                    'harv_farmer_peer':data_loaded['harvester']['farmer_peer']['port'],
                                    'harv_rpc_port':data_loaded['harvester']['rpc_port'],
                                    'farmer':data_loaded['farmer']['port'],
                                    'farm_harv_peer':data_loaded['farmer']['harvester_peer']['port'],
                                    'farm_rpc_port':data_loaded['farmer']['rpc_port'],
                                    'wallet':data_loaded['wallet']['port'],
                                    'wallet_rpc_port':data_loaded['wallet']['rpc_port']
                                     }

                                stdout_reply=[]

                                for key in ports:
                                    p=subprocess.run(['lsof','-i',':{}'.format(ports[key])],capture_output=True, shell=False)
                                    if p.returncode ==0:
                                        reply='{} : running {}'.format(key,ports[key])
                                    if p.returncode ==1:
                                        reply='{} : not running {}'.format(key,ports[key])

                            else:
                                pass

                        else:
                            pass
                repos_to_send={}
                for repo in folder_to_delete:
                    if repo in all_found_repos:
                        repos_to_send[repo]=folder_to_delete[repo]
                return repos_to_send

    def on_new_client(self,client_sock,addr):
            print(f"connection from {addr} has been established.")
            data=conn.recv(1024)
            if not data:
                client_sock.close()
            elif data.decode('UTF-8') == 'detect' :
                folder_to_delete=detect_no_gui()
                resp_enc=pickle.dumps(folder_to_delete,-1)
                client_sock.send(resp_enc)
                client_sock.close()
                
    def run(self):

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM,0) as sock:
                sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
                sock.bind(('',5999))
                sock.listen(5)
                with self.context.wrap_socket(sock,server_side=True) as ssock:
                        conn,addr = ssock.accept()
                        threading.Thread(self.on_new_client(conn,addr)).start()
        sock.close()
    
