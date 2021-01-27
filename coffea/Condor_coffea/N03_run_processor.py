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

## Prepare files
N_node = args.nWorker
metadata = args.metadata
data_sample = args.dataset


setname = metadata.split('.')[0].split('/')[1]

# ---> Class MuZPeak
class MyZPeak(processor.ProcessorABC):

	# -- Initializer
	def __init__(self):


		self._year = '2018'

		self._doubleelectron_triggers  ={
			'2018': [
					"Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", # Recomended
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
		dataset = setname
		#events.metadata['dataset']
		

		# flat dim for histo fill
		def flat_dim(arr):

			sub_arr = ak.flatten(arr)
			mask = ~ak.is_none(sub_arr)

			return ak.to_numpy(sub_arr[mask])
		

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
		print("{0} number of events are detected".format(len(Initial_events)))
		events = events[single_ele_triggers_arr | double_ele_triggers_arr]
		print("Total {0} number of events are remain after triggger | Eff: {1}".format(len(events), len(events) / len(Initial_events) * 100))
		
		
		# ---- Define Particles
		Electron = events.Electron

		def Electron_selection(ele):
			return(ele.pt > 20) & (np.abs(ele.eta) < 2.5) & (ele.cutBased > 1)
		

		# ---- Define Channel 
		Electron_mask = Electron_selection(Electron)
		Ele_channel_mask = ak.num(Electron[Electron_mask]) > 1
		Ele_channel_events = events[Ele_channel_mask]

		N_Ele_Channel_events = len(Ele_channel_events)
		print("#1 Ele channel evts: {0} --> {1}".format(len(events),N_Ele_Channel_events))

		# ---- Electron
		Ele = Ele_channel_events.Electron
		Electron_mask = Electron_selection(Ele)	
		Ele_sel = Ele[Electron_mask]	

		##  -- Define Ele-Pair --
		ele_pairs = ak.combinations(Ele_sel,2,axis=1)
		ele_left, ele_right = ak.unzip(ele_pairs)
		diele = ele_left + ele_right

		## -- Oposite Sign cut --
		os_mask		 = diele.charge == 0 
		os_diele	 = diele[os_mask]
		os_ele_left  = ele_left[os_mask]
		os_ele_right = ele_right[os_mask]
		

		## Validate test1 
		base_L = len(flat_dim(ele_left))
		base_R = len(flat_dim(ele_right))
		base_A = len(flat_dim(diele))
		
		os_L = len(flat_dim(os_ele_left))
		os_R = len(flat_dim(os_ele_right))
		os_A = len(flat_dim(os_diele))
		

		## -- Select Highest-PT pair -- 
		def make_leading_pair(target,base):

			return target[ak.argmax(base.pt,axis=1,keepdims=True)]


		# -- Only Leading pair --
		leading_diele = make_leading_pair(diele,diele)
		leading_ele   = make_leading_pair(ele_left,diele)
		subleading_ele= make_leading_pair(ele_right,diele)


		# --OS and Leading pair --
		leading_os_diele = make_leading_pair(os_diele,os_diele)
		leading_os_ele   = make_leading_pair(os_ele_left,os_diele)
		subleading_os_ele= make_leading_pair(os_ele_right,os_diele)


		

		## -- Z-mass window --
		def makeZmass_window_mask(dielecs,start=60,end=120):
			mask = (dielecs.mass >= start) & (dielecs.mass <= end)	
			return mask

		# -- Only Leading pair --
		Zmass_mask = makeZmass_window_mask(leading_diele)
		leading_Zwindow_ele = leading_ele[Zmass_mask]
		subleading_Zwindow_ele = subleading_ele[Zmass_mask]
		leading_Zwindow_diele = leading_diele[Zmass_mask]

		# -- OS and Leading pair --
		Zmass_mask_os = makeZmass_window_mask(leading_os_diele)
		leading_os_Zwindow_ele = leading_os_ele[Zmass_mask_os]
		subleading_os_Zwindow_ele = subleading_os_ele[Zmass_mask_os]
		leading_os_Zwindow_diele = leading_os_diele[Zmass_mask_os]


		ele1PT  = flat_dim(leading_Zwindow_ele.pt)
		ele1Eta = flat_dim(leading_Zwindow_ele.eta)
		ele1Phi = flat_dim(leading_Zwindow_ele.phi)
		ele2PT  = flat_dim(subleading_Zwindow_ele.pt)
		ele2Eta = flat_dim(subleading_Zwindow_ele.eta)
		ele2Phi = flat_dim(subleading_Zwindow_ele.phi)
		Mee     = flat_dim(leading_Zwindow_diele.mass)
		charge  = flat_dim(leading_Zwindow_diele.charge)

		os_ele1PT  = flat_dim(leading_os_Zwindow_ele.pt)
		os_ele1Eta = flat_dim(leading_os_Zwindow_ele.eta)
		os_ele1Phi = flat_dim(leading_os_Zwindow_ele.phi)
		os_ele2PT  = flat_dim(subleading_os_Zwindow_ele.pt)
		os_ele2Eta = flat_dim(subleading_os_Zwindow_ele.eta)
		os_ele2Phi = flat_dim(subleading_os_Zwindow_ele.phi)
		os_Mee     = flat_dim(leading_os_Zwindow_diele.mass)
		os_charge  = flat_dim(leading_os_Zwindow_diele.charge)



		print("#5 Leading PT : {0}".format(len(ele1PT)))
		print("#5 Leading os PT  {0}".format(len(os_ele1PT)))


		out["sumw"][dataset] += len(events)
	
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








## Json file reader
with open(metadata) as fin:
	datadict = json.load(fin)

filelist = glob.glob(datadict[data_sample])
print(filelist)
sample_name = data_sample.split('_')[0]


# test one file 
#sample_name="Egamma"
#filelist=["/x6/cms/store_Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON/data/Run2018A/EGamma/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/D628EAD9-EACA-0640-AF0C-A0698767F9DE_Skim.root"]


print(sample_name)
samples = {
	sample_name : filelist
}



## -->Multi-node Executor
result = processor.run_uproot_job(
	samples,  #dataset
	"Events", # Tree name
	MyZPeak(), # Class
	executor=processor.futures_executor,
	executor_args={"schema": NanoAODSchema, "workers": 20},
#maxchunks=4,
)




outname = data_sample + '.futures'
save(result,outname)


elapsed_time = time.time() - start
print("Time: ",elapsed_time)
## <-------------------------




