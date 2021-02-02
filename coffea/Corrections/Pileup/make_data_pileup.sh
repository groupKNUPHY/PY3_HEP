#!/bin/bash
export SCRAM_ARCH=slc7_amd64_gcc700
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
echo "$VO_CMS_SW_DIR $SCRAM_ARCH"
source $VO_CMS_SW_DIR/cmsset_default.sh


cd /cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_6_0/src/
eval `scramv1 runtime -sh`
cd - 

Golden_json_file=$1
Input_Latest_pileup_json_file=$2

pileupCalc.py -i $Golden_json_file --inputLumiJSON $Input_Latest_pileup_json_file --calcMode true --minBiasXsec 69200 --maxPileupBin 100 --numPileupBins 100 data_2018_pileup_out.root
