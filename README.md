# FORK_MANAGER
all forks in one (so far Linux) not tested on Unix  
pulls and installs available forks into host blockchain environment  
features connection to a remote host to monitor farming on remote machine  
--To Install--  
clone the git repo and cd into the FORK_MANAGER  
python3 launcher.py to get started, if no tkinter do sudo apt-get install python3-tk, also requires gitPython repo. (pip3 install gitPython) or run pip3 install -r requirements.txt to install dependencies  
to run cli installer without tkinter do python3 launcher.py -i agem,chia,goji -d /home/{someuser}/{host fork}-blockchain  
if planning to run fork manager it is recommended to install it alongside your forks using the above instruction 
 
cd into the blockchain environemnt  
run . ./activate  
and run 'launcher' to run the manager from within the environment  
add forks direct from respective repos to your environemnt and run as usual chia, chaingreen, flax, goji, cannabis from the same env
MADMAX Gui is not dependent on the environment.   

Features fork console with info on running ports, farming status and plots, stop all /start all  
Copy plot directory entry from chosen config.yaml into the rest of the forks

To run a remote connection, install the fork manager on remote machine following above instructions and do launcher listen command to start listeneing on port 5999  add the remote connection via manager's console on your main machine, select '+ remote' and it will query remote host for info on installed forks  

if so inclined a donation is welcome:   
cgn13lu3q74lsvc34cpwd56r35xj42cctvt60pqau675hut74h4nldcs53t8pp  
cans13lu3q74lsvc34cpwd56r35xj42cctvt60pqau675hut74h4nldcsspnlwl  
xch1aa4g07nh9fsepf9xamvy6lw8lkaqyh7xvczgkacz9mtt9sv7kqpqf87w6v  
