import os
import json


metadata="/x5/cms/jwkim/gitdir/PY3_HEP/coffea/metadata/datalist.json"


with open(metadata) as fin:
    datadict = json.load(fin)


os.system('mkdir -p hists/run_condor/out hists/run_condor/err hists/run_condor/log hists/run_condor/condorOut')

jdl = """universe = vanilla
Executable = N02_run.sh
Transfer_Input_Files = N02_run.sh
Output = hists/run_condor/out/$ENV(SAMPLE)_$(Cluster)_$(Process).stdout
Error = hists/run_condor/err/$ENV(SAMPLE)_$(Cluster)_$(Process).stderr
Log = hists/run_condor/log/$ENV(SAMPLE)_$(Cluster)_$(Process).log
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Arguments = $ENV(METADATA) $ENV(SAMPLE)
transfer_output_files="hists/run_condor/condorOut"
Queue 1"""

jdl_file = open("run.submit", "w") 
jdl_file.write(jdl) 
jdl_file.close() 


for info,dataset in datadict.items():
    os.system('rm -rf hists/run_condor/err/'+info+'*')
    os.system('rm -rf hists/run_condor/log/'+info+'*')
    os.system('rm -rf hists/run_condor/out/'+info+'*')
    os.environ['SAMPLE'] = dataset
    os.environ['METADATA']   = metadata
    os.system('condor_submit run.submit')
os.system('rm run.submit')
