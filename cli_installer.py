import sys,os,subprocess,shutil,git
from pathlib import Path


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
                    with open('console.py','r') as console:
                            lines = console.readlines()
                            cur_folder=os.getcwd()
                            print(f'entered {cur_folder} and printed the lines?')
                            lines[41] = f"        self.FORK_MANAGER_folder_ini = '{cur_folder}'\n"
                            print('done editing console')
                            with open('console.py','w') as console_out:
                                console_out.writelines(lines)
                            
                    venv_bin=os.path.join(folder,'venv/bin/launcher')
                    with open(venv_bin, 'w+') as launcher_file:
                        launcher_file.write('#!/bin/bash \n python3 {}/launcher.py'.format(install_folder))
                    subprocess.check_call(['chmod', 'u+x',venv_bin])
                    subprocess.check_call(['chmod', 'u+x','install_manager.sh'])
                    subprocess.check_call(['sh','./install_manager.sh'])
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
