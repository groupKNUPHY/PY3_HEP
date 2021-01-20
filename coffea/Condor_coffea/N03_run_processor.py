import awkward1 as ak
from coffea.nanoaod import NanoEvents
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import time
from coffea import processor, hist
from coffea.util import load, save
import json
import glob 
import os
import argparse
import numpy as np
from coffea import lumi_tools

start = time.time()




parser = argparse.ArgumentParser()

parser.add_argument('--nWorker', type=int,
			help=" --nWorker 2", default=20)
parser.add_argument('--metadata', type=str,
			help="--metadata xxx.json")
parser.add_argument('--dataset', type=str,
			help="--dataset ex) Egamma_Run2018A_280000")


args = parser.parse_args()



# ---> Class MuZPeak
class MyZPeak(processor.ProcessorABC):


	doubleelectron_triggers  ={
	'2018': [
	#		"HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
	#		"HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",
			"HLT_DiEle27_WPTightCaloOnly_L1DoubleEG",
	#		"HLT_DoubleEle33_CaloIdL_MW",
	#		"HLT_DoubleEle25_CaloIdL_MW"
	#		"HLT_DoubleEle27_CaloIdL_MW",
	#		"HLT_DoublePhoton70"
			]
	}



	singleelectron_triggers = { #2017 and 2018 from monojet, applying dedicated trigger weights
			'2016': [
				'Ele27_WPTight_Gsf',
				'Ele105_CaloIdVT_GsfTrkIdT'
			],
			'2017': [
				'Ele35_WPTight_Gsf',
				'Ele115_CaloIdVT_GsfTrkIdT',
				'Photon200'
			],
			'2018': [
				'Ele32_WPTight_Gsf',   # Isolated
				#'Ele115_CaloIdVT_GsfTrkIdT',  # Non-Isolated
				#'Photon200' # high PT
			]
		}




	# -- Initializer
	def __init__(self):
		
		self._accumulator = processor.dict_accumulator({

			"sumw": processor.defaultdict_accumulator(float),
			"mass": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("mass","$m_{e+e-}$ [GeV]", 100, 0, 200),
			),
			"mass_60_120": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("mass_60_120","$m_{e+e-}$ [GeV]", 60, 60, 120),
			),
			"nElectrons":hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("nElectrons","# of Electrons",10,0,10)
			)
		})
		
	# -- Accumulator: accumulate histograms
	@property
	def accumulator(self):
		return self._accumulator

	# -- Main function : Process events
	def process(self, events):

		# Initialize accumulator
		out = self.accumulator.identity()
		dataset = events.metadata['dataset']

		# Lumi section
		#print("############## Start ... Matching Golden Json files ##############")
		#Golden_json = "Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
		#print(lumi_tools.LumiMask(Golden_json)(events['run'],events['luminosityBlock']))
		

		## double lepton trigger
		# ---- Not applied yet-------------------------------#
		is_double_ele_trigger=False
		if not is_double_ele_trigger:
			double_ele_triggers_arr=np.ones(events.size, dtype=np.bool)
		else:
			double_ele_triggers_arr = np.zeros(events.size, dtype=np.bool)
			for path in doubleelectron_triggers[year]:
				if path not in events.HLT.columns: continue
				double_ele_triggers_arr = double_ele_triggers_arr | events.HLT[path]
		print("Double Electron triggers")
		print(double_ele_triggers_arr,double_ele_triggers_arr.shape)


		## single lepton trigger
		# ---- Not applied yet-------------------------------#
		is_single_ele_trigger=False
		if not is_single_ele_trigger:
			single_ele_triggers_arr=np.ones(events.size, dtype=np.bool)
		else:
			single_ele_triggers_arr = np.zeros(events.size, dtype=np.bool)
			for path in singleelectron_triggers[year]:
				if path not in events.HLT.columns: continue
				single_ele_triggers_arr = single_ele_triggers_arr | events.HLT[path]
		print("Single Electron triggers")
		print(single_ele_triggers_arr,single_ele_triggers_arr.shape)


		
		Initial_events = events
		print("{0} number of events are detected".format(Initial_events.shape[0]))
		events = events[single_ele_triggers_arr | double_ele_triggers_arr]
		print("Total {0} number of events are remain after triggger | Eff: {1}".format(events.shape[0], events.shape[0] / Initial_events.shape[0] * 100))
		

		# Electron selection
		Electron = events.Electron
			# CutBased ID -->   0:fail, 1:veto, 2:loose, 3:medium, 4:tight
		Electron_mask = (Electron.pt >20) & (np.abs(Electron.eta) < 2.5) & (Electron.cutBased > 1) 
		Ele_channel_mask = ak.num(Electron[Electron_mask]) > 1
		Ele_channel_events = events[Ele_channel_mask]
		Ele = Ele_channel_events.Electron
		

		# All possible pairs of Electron in each event
		ele_pairs = ak.combinations(Ele,2,axis=1)
		
		# TLorentz vector sum of ele_pairs
		ele_left, ele_right = ak.unzip(ele_pairs)
		diele = ele_left + ele_right
		
		# Opposite sign		
		diffsign_diele =  diele[diele.charge==0]

		# Leading pair (Highest PT parir)
		leading_diffsign_diele = diffsign_diele[ak.argmax(diffsign_diele.pt,axis=1,keepdims=True)]

		# Z mass window for h1_Mee_60_120 histo
		Zmass_mask = leading_diffsign_diele.mass >= 60 and leading_diffsign_diele.mass <= 120
		
		#Mee = ak.flatten(leading_diffsign_diele.mass) # This makes type error ( primitive expected but ?float given )
		
		Mee = leading_diffsign_diele.mass
		Mee_60_120 = Mee[Zmass_mask]
		Mee_60_120 = ak.to_numpy(ak.flatten(Mee_60_120))
		Mee = ak.to_numpy(Mee).flatten()
	

		out["sumw"][dataset] += len(events)
		out["nElectrons"].fill(
			dataset=dataset,
			#nElectrons= ak.to_numpy(ak.num(Ele))
			nElectrons= ak.num(Ele)
		)
		out["mass"].fill(
			dataset=dataset,
			mass=Mee
		)
		out["mass_60_120"].fill(
			dataset=dataset,
			mass_60_120=Mee_60_120
		)


		return out

	# -- Finally! return accumulator
	def postprocess(self,accumulator):
		return accumulator
# <---- Class MyZPeak




## Prepare files
N_node = args.nWorker
metadata = args.metadata
data_sample = args.dataset



with open(metadata) as fin:
	datadict = json.load(fin)

filelist = glob.glob(datadict[data_sample])


sample_name = data_sample.split('_')[0]
samples = {
	sample_name : filelist
}


## -->Multi-node Executor
result = processor.run_uproot_job(
	samples,  #dataset
	"Events", # Tree name
	MyZPeak(), # Class
	executor=processor.futures_executor,
	executor_args={"schema": NanoAODSchema, "workers": N_node},
	#maxchunks=4,
)




outname = data_sample + '.futures'
save(result,outname)


elapsed_time = time.time() - start
print("Time: ",elapsed_time)
## <-------------------------




