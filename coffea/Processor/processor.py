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
start = time.time()



parser = argparse.ArgumentParser()

parser.add_argument('--nWorker', type=int,
			help=" --nWorker 2", default=8)
parser.add_argument('--metadata', type=str,
			help="--metadata xxx.json")
parser.add_argument('--dataset', type=str,
			help="--dataset ex) Egamma_Run2018A_280000")


args = parser.parse_args()



# ---> Class MuZPeak
class MyZPeak(processor.ProcessorABC):

	# -- Initializer
	def __init__(self):
		self._histo = hist.Hist(
			"Events",
			hist.Cat("dataset","Dataset"),
			hist.Bin("mass", "Z mass", 60, 60, 120)
		)
	# -- Accumulator: accumulate histograms
	@property
	def accumulator(self):
		return self._histo

	# -- Main function : Process events
	def process(self, events):

		# Initialize accumulator
		out = self.accumulator.identity()

		# Event selection: opposite charged same flavor

		Electron = events.Electron
		Electron_mask = (Electron.pt >20) & (np.abs(Electron.eta) < 2.5) & (Electron.cutBased > 1) 
		Ele_channel_mask = ak.num(Electron[Electron_mask]) > 1
		Ele_channel_events = events[Ele_channel_mask]
		Ele = Ele_channel_events.Electron

		# All possible pairs of Electron in each event
		ele_pairs = ak.combinations(Ele,2,axis=1)
		
		# TLorentz vector sum of ele_pairs
		ele_left, ele_right = ak.unzip(ele_pairs)
		diele = ele_left + ele_right
		
		
		diffsign_diele =  diele[diele.charge==0]
		
		leading_diffsign_diele = diffsign_diele[ak.argmax(diffsign_diele.pt,axis=1,keepdims=True)]

		
		#Mee = ak.flatten(leading_diffsign_diele.mass) # This makes type error ( primitive expected but ?float given )
		Mee = ak.to_numpy(leading_diffsign_diele.mass)
		Mee = Mee.flatten()


		out.fill(
			dataset = events.metadata["dataset"],
			mass = Mee
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
samples = {
	"WZ" : filelist
}


## -->Multi-node Executor
result = processor.run_uproot_job(
	samples,  #dataset
	"Events", # Tree name
	MyZPeak(), # Class
	executor=processor.futures_executor,
	executor_args={"schema": NanoAODSchema, "workers": N_node},
	#executor_args={'nano':True, "workers": N_node},
	#maxchunks=4,
)


# Draw hist -- If you want to drwa hist
#import matplotlib.pyplot as plt
#hist.plot1d(result)
#plt.savefig("Zmumu.png")


outname = data_sample + '.futures'
save(result,outname)


elapsed_time = time.time() - start
print("Time: ",elapsed_time)
## <-------------------------



