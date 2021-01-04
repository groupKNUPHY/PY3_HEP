#!/bin/bash

export USER=${3}
echo "User is: ${3}"
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
echo $(hostname)


source /home/jwkim/Anaconda3/setup.sh 
echo "python run.py --metadata ${1} --dataset ${2}"




#python run.py --metadata ${1} --dataset ${2}
#ls hists/${2}.futures
#cp hists/${2}.futures ${_CONDOR_SCRATCH_DIR}/${2}.futures
