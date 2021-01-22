import awkward1 as ak
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

	# -- Initializer
	def __init__(self):


		self._year = '2018'

		self._doubleelectron_triggers  ={
			'2018': [
			#		"HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
					"HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", # Recomended
			#		"HLT_DiEle27_WPTightCaloOnly_L1DoubleEG",
			#		"HLT_DoubleEle33_CaloIdL_MW",
			#		"HLT_DoubleEle25_CaloIdL_MW"
			#		"HLT_DoubleEle27_CaloIdL_MW",
			#		"HLT_DoublePhoton70"
					]
		}
	
	
	
		self._singleelectron_triggers = { #2017 and 2018 from monojet, applying dedicated trigger weights
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
					'Ele32_WPTight_Gsf',   # Recomended
				]
			}
		
		self._accumulator = processor.dict_accumulator({

			"sumw": processor.defaultdict_accumulator(float),

			"mass": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("mass","$m_{e+e-}$ [GeV]", 100, 0, 200),
			),
			"charge": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("charge","charge sum of electrons", 6, -3, 3),
			),
			"ele1pt": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("ele1pt","Leading Electron $P_{T}$ [GeV]", 300, 0, 600),
			),

			"ele2pt": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("ele2pt","Subleading $Electron P_{T}$ [GeV]", 300, 0, 600),
			),
			"ele1eta": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("ele1eta","Leading Electron $\eta$ [GeV]", 20, -5, 5),
			),

			"ele2eta": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("ele2eta","Subleading Electron $\eta$ [GeV]", 20, -5, 5),
			),
			"ele1phi": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("ele1phi","Leading Electron $\phi$ [GeV]", 20, -3.15, 3.15),
			),

			"ele2phi": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("ele2phi","Subleading Electron $\phi$ [GeV]", 20, -3.15, 3.15),
			),

			"os_mass": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("os_mass","$m_{e+e-}$ [GeV]", 100, 0, 200),
			),
			"os_ele1pt": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("os_ele1pt","Leading Electron $P_{T}$ [GeV]", 300, 0, 600),
			),

			"os_ele2pt": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("os_ele2pt","Subleading $Electron P_{T}$ [GeV]", 300, 0, 600),
			),
			"os_ele1eta": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("os_ele1eta","Leading Electron $\eta$ [GeV]", 20, -5, 5),
			),

			"os_ele2eta": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("os_ele2eta","Subleading Electron $\eta$ [GeV]", 20, -5, 5),
			),
			"os_ele1phi": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("os_ele1phi","Leading Electron $\phi$ [GeV]", 20, -3.15, 3.15),
			),

			"os_ele2phi": hist.Hist(
				"Events",
				hist.Cat("dataset","Dataset"),
				hist.Bin("os_ele2phi","Subleading Electron $\phi$ [GeV]", 20, -3.15, 3.15),
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
		is_double_ele_trigger=True
		if not is_double_ele_trigger:
			double_ele_triggers_arr=np.ones(len(events), dtype=np.bool)
		else:
			double_ele_triggers_arr = np.zeros(len(events), dtype=np.bool)
			for path in self._doubleelectron_triggers[self._year]:
				if path not in events.HLT.fields: continue
				double_ele_triggers_arr = double_ele_triggers_arr | events.HLT[path]
		#print("Double Electron triggers")
		#print(double_ele_triggers_arr,len(double_ele_triggers_arr))


		## single lepton trigger
		# ---- Not applied yet-------------------------------#
		is_single_ele_trigger=True
		if not is_single_ele_trigger:
			single_ele_triggers_arr=np.ones(len(events), dtype=np.bool)
		else:
			single_ele_triggers_arr = np.zeros(len(events), dtype=np.bool)
			for path in self._singleelectron_triggers[self._year]:
				if path not in events.HLT.fields: continue
				single_ele_triggers_arr = single_ele_triggers_arr | events.HLT[path]
		#print("Single Electron triggers")
		#print(single_ele_triggers_arr,len(single_ele_triggers_arr))


		
		Initial_events = events
		#print("{0} number of events are detected".format(len(Initial_events)))
		events = events[single_ele_triggers_arr | double_ele_triggers_arr]
		#print("Total {0} number of events are remain after triggger | Eff: {1}".format(len(events), len(events) / len(Initial_events) * 100))
		

		# Electron selection
		Electron = events.Electron
			# CutBased ID -->   0:fail, 1:veto, 2:loose, 3:medium, 4:tight
		Electron_mask = (Electron.pt >20) & (np.abs(Electron.eta) < 2.5) & (Electron.cutBased > 1) 
		Ele_channel_mask = ak.num(Electron[Electron_mask]) > 1
		Ele_channel_events = events[Ele_channel_mask]
		Ele = Ele_channel_events.Electron
		

		# All possible pairs of Electron in each event
		ele_pairs = ak.combinations(Ele,2,axis=1)
		
		# Ele_pairs
		ele_left, ele_right = ak.unzip(ele_pairs)
		diele = ele_left + ele_right
			
		# Opposite sign cut	
		os_mask		 = diele.charge==0
		os_diele	 = diele[os_mask]
		os_ele_left  = ele_left[os_mask]
		os_ele_right = ele_right[os_mask]

		# Leading pair (Highest PT parir)
		def make_leading_pair(target,base):
			return target[ak.argmax(base.pt,axis=1,keepdims=True)]

		# Leading set
		leading_diele	  = make_leading_pair(diele,diele)
		leading_ele		  = make_leading_pair(ele_left,diele)
		subleading_ele    = make_leading_pair(ele_right,diele)


		# OS and Leading set
		leading_os_diele  = make_leading_pair(os_diele,os_diele)
		leading_os_ele    = make_leading_pair(os_ele_left,os_diele)
		subleading_os_ele = make_leading_pair(os_ele_right,os_diele)
		
		

		# Electron kinematics
		def makeZmass_window_mask(dielecs,start=60,end=120):
			mask = (dielecs.mass >=start) & (dielecs.mass <=end)
			return mask

		# flat dim for histo fill
		def flat_dim(arr):
			return ak.to_numpy(ak.flatten(arr))


		# -----Basic

		Zmass_mask = makeZmass_window_mask(leading_diele)
	
		#--  If you need Z mass window cut
		leading_ele    = leading_ele[Zmass_mask]
		leading_diele  = leading_diele[Zmass_mask]
		subleading_ele = subleading_ele[Zmass_mask]


		ele1PT  = flat_dim(leading_ele.pt)
		ele1Eta = flat_dim(leading_ele.eta)
		ele1Phi = flat_dim(leading_ele.phi)
		ele2PT  = flat_dim(subleading_ele.pt)
		ele2Eta = flat_dim(subleading_ele.eta)
		ele2Phi = flat_dim(subleading_ele.phi)
		Mee     = flat_dim(leading_diele.mass)
		charge  = flat_dim(leading_diele.charge)
		
		
		# -----OS
		Zmass_mask = makeZmass_window_mask(leading_os_diele)
		#Mee_60_120 = Mee[Zmass_mask]
		#Mee_60_120 = ak.to_numpy(ak.flatten(Mee_60_120))
	
		#--  If you need Z mass window cut
		leading_os_ele    = leading_os_ele[Zmass_mask]
		leading_os_diele  = leading_os_diele[Zmass_mask]
		subleading_os_ele = subleading_os_ele[Zmass_mask]

		os_ele1PT  = flat_dim(leading_os_ele.pt)
		os_ele1Eta = flat_dim(leading_os_ele.eta)
		os_ele1Phi = flat_dim(leading_os_ele.phi)
		os_ele2PT  = flat_dim(subleading_os_ele.pt)
		os_ele2Eta = flat_dim(subleading_os_ele.eta)
		os_ele2Phi = flat_dim(subleading_os_ele.phi)
		os_Mee     = flat_dim(leading_os_diele.mass)


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
		out["charge"].fill(
			dataset=dataset,
			charge=charge
		)
		out["ele1pt"].fill(
			dataset=dataset,
			ele1pt=ele1PT
		)
		out["ele1eta"].fill(
			dataset=dataset,
			ele1eta=ele1Eta
		)
		out["ele1phi"].fill(
			dataset=dataset,
			ele1phi=ele1Phi
		)
		out["ele2pt"].fill(
			dataset=dataset,
			ele2pt=ele2PT
		)
		out["ele2eta"].fill(
			dataset=dataset,
			ele2eta=ele2Eta
		)
		out["ele2phi"].fill(
			dataset=dataset,
			ele2phi=ele2Phi
		)

		out["os_mass"].fill(
			dataset=dataset,
			os_mass=os_Mee
		)
		out["os_ele1pt"].fill(
			dataset=dataset,
			os_ele1pt=os_ele1PT
		)
		out["os_ele1eta"].fill(
			dataset=dataset,
			os_ele1eta=os_ele1Eta
		)
		out["os_ele1phi"].fill(
			dataset=dataset,
			os_ele1phi=os_ele1Phi
		)
		out["os_ele2pt"].fill(
			dataset=dataset,
			os_ele2pt=os_ele2PT
		)
		out["os_ele2eta"].fill(
			dataset=dataset,
			os_ele2eta=os_ele2Eta
		)
		out["os_ele2phi"].fill(
			dataset=dataset,
			os_ele2phi=os_ele2Phi
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




