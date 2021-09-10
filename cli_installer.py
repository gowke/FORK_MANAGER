import sys,os,subprocess,shutil,git
from pathlib import Path
from OpenSSL import crypto,SSL

class nonGui (object):
    def __init__(self,repos,folder_names, bin_files, repo, homedir):
        self.repos=repos
        self.folder_names=folder_names
        self.bin_files=bin_files
        self.install(repo,homedir)


    def install(self,filename,folder):
          
            if 'venv' and 'install.sh' in os.listdir(folder):
                if (filename != 'agem') and (filename != 'madmax'):
                    print('existing install detected')
                    temp_folder= os.path.join(folder,'FORKS')
                    if os.path.isdir(temp_folder) is False:
                        os.mkdir(temp_folder)
                    install_folder=os.path.join(temp_folder,self.folder_names[filename])
                    if os.path.isdir(install_folder):
                        shutil.rmtree(install_folder)
                    try:
                        self.get_dir(temp_folder,install_folder,filename)
                    except Exception as e:
                        f=input('delete and re-install y/n?\n')
                        if f == 'y':
                            shutil.rmtree(install_folder)
                            get_dir(temp_folder,install_folder,filename)
                        
                    self.merge(folder,temp_folder,install_folder,filename)
                else:
                    install_folder=os.path.join(folder,self.folder_names[filename])
                    try:
                        self.get_dir(folder,install_folder,filename) 
                    except Exception as e:
                        f=input('delete and re-install y/n?\n')
                        if f == 'y':
                            shutil.rmtree(install_folder)
                            self.get_dir(folder,install_folder,filename) 
                
            else:
                install_folder=os.path.join(folder,self.folder_names[filename])
                try:
                    self.get_dir(folder,install_folder,filename) 
                except Exception as e:
                    f=input('delete and re-install y/n?\n')
                    if f == 'y':
                        shutil.rmtree(install_folder)
                        self.get_dir(folder,install_folder,filename)

    def get_dir(self,folder,install_folder,filename):
                git.Git(folder).clone(self.repos[filename])
                os.chdir(install_folder)
                if filename == 'madmax':
                    repo=git.Repo(os.getcwd())
                    output = repo.git.submodule('update', '--init')
                    subprocess.check_call(['sh','./make_devel.sh'])
                elif filename=='agem':
                    subprocess.check_call(['chmod', 'u+x','install_manager.sh'])
                    subprocess.check_call(['sh','./install_manager.sh'])
                    cur_folder=os.getcwd()
                    with open('console.py','r') as console:
                            lines = console.readlines()
                            lines[41] = f"        self.FORK_MANAGER_folder_ini = '{cur_folder}'\n" #adding line to console to indicate folder location 
                            print('done editing console')
                            with open('console.py','w') as console_out:
                                console_out.writelines(lines)
                    with open('listener.py','r') as listener:
                            lines = listener.readlines()
                            host_venv_folder=os.path.split(cur_folder)[0]
                            pthn_venv_lnk=os.path.join(host_venv_folder,'venv/bin/python3')
                            lines[1] = f"#!{pthn_venv_lnk}\n" #adding line to console to indicate folder location 
                            print('done editing listener')
                            with open('listener.py','w') as listener_out:
                                listener_out.writelines(lines)
                    input('create ssl key or use from other install y?') # creating ssl certs for the listener
                    if input =='y':
                                print(f'confirm got input {input}')
                                key = crypto.PKey()
                                key.generate_key(crypto.TYPE_RSA, 1024)
                                cert = crypto.X509()
                                cert.get_subject().C = 'AE'
                                cert.get_subject().ST = '                                           '
                                cert.get_subject().L = '                                            '
                                cert.get_subject().O = '    AGEM   '
                                cert.get_subject().OU = 'agem fork manager'
                                cert.get_subject().CN = '  organic farming division '
                                cert.get_subject().emailAddress = '              '
                                cert.set_serial_number(1000)
                                cert.gmtime_adj_notBefore(0)
                                cert.gmtime_adj_notAfter(10*365*24*60*60)
                                cert.set_issuer(cert.get_subject())
                                cert.set_pubkey(key)
                                cert.sign(key,'sha256')
                                with open('agem_cert.pem', "a") as f:
                                    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
                                with open('agem_cert.pem', "a") as f:
                                    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode("utf-8"))
                                print('done creating ssl certificates')
                                
                    else:
                        pass
                    venv_bin=os.path.join(folder,'venv/bin/launcher')
                    with open(venv_bin, 'w+') as launcher_file:
                        launcher_file.write('#!/bin/bash \n python3 {}/launcher.py $@'.format(install_folder))
                    subprocess.check_call(['chmod', 'u+x',venv_bin])            
                elif (filename != 'madmax') and (filename !='agem'):
                    subprocess.check_call(['sh','./install.sh'])
                print('\n \n INSTALLATION COMPLETED')

    def merge(self,folder,temp_dir,install_folder,filename):
        temp_bin=os.path.join(install_folder,'venv/bin')
        main_bin=os.path.join(folder,'venv/bin')
        dest_bin=[]
        bin_dict={}
        for file in self.bin_files:
            if filename=='chiarose':
                temp_bin_file=os.path.join(temp_bin,('chia'+file))
            else:
                temp_bin_file=os.path.join(temp_bin,(filename+file))
            main_bin_file=os.path.join(main_bin,(filename+file))
            bin_dict[temp_bin_file]=main_bin_file
            dest_bin.append(main_bin_file)

        for file in dest_bin:
            try:
                os.remove(file)
            except:
                pass

        for file in bin_dict:
            subprocess.check_call(['cp',file,bin_dict[file]])
            print('copying to {} completed'.format(bin_dict[file]))
            
        if filename=='chiarose':
            launch_file_temp=os.path.join(temp_bin,'chia')
        else:
            launch_file_temp=os.path.join(temp_bin,filename)
            
        launch_file_main=os.path.join(main_bin,filename)
            
        try:
            os.remove(launch_file_main)
        except:
            pass
        
        subprocess.check_call(['cp',launch_file_temp,launch_file_main])
        print('copying to {} completed'.format(launch_file_main))
