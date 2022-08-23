# FORK_MANAGER
pour all forks into one venv (so far for Linux only, not tested on Mac)  

basic lightweight manager written in Python
  
pull source codes from github and install available forks into host blockchain environment  
  
features connection to a remote host to monitor remote farmer or harvester if an instance is installed on that host.
  
--To Install--  
  
clone this git repo and cd into the FORK_MANAGER  
  
python3 launcher.py to get started, if no tkinter do 'sudo apt-get install python3-tk', also requires gitPython repo. (pip3 install gitPython) or run pip3 install -r requirements.txt to install dependencies.
  
to run cli installer without tkinter do python3 launcher.py -i agem,flax,goji -d /home/{someuser}/{chia}-blockchain  

recommend pouring agem (the fork manager) into the host (chia) blockchain and then pour all successive forks into the host chain using that manager.
   
cd into the blockchain environment  
  
run . ./activate  
  
and run 'launcher' to run the manager from within the environment, as you would do 'chia' or any other fork once it has been poured into that environment
  
add forks direct from respective repos to your environemnt and run as usual chia, chaingreen, flax, goji, cannabis from the same environment
   
Features fork console with info on running ports, farming status and plots, stop all /start all and deleting specific forks   
  
Copy plot directory entry from chosen config.yaml into the rest of the forks  

To run a remote connection, install the fork manager on your remote machine following above instructions, copy the randomly generated .pem file either from your main machine to your remote machine, or vice versa, only ensure the same file is being used on both machines, and do 'launcher listen' command on your remote machine to start listening on port 5999  
  
add the remote connection via manager's console on your main machine, select '+ remote' and 'Detect' for it to query remote host along with your local pc for info on installed forks  
  
