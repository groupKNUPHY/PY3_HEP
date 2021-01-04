import awkward1 as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import time
from coffea import processor, hist
from coffea.util import load, save
start = time.time()



import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--nWorker', type=int,
            help=" --nWorker 2", default=4)
parser.add_argument('--nData', type=str,
            help="--nData datalist")


args = parser.parse_args()


## Single events process
# Many events
#filelist = "/x6/cms/store/mc/RunIISummer19UL18NanoAODv2/WZ_TuneCP5_13TeV-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/809D80E0-A0EB-5548-BCD1-58C4A1C1A71C.root"



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
		mmevents = events[
			(ak.num(events.Muon) == 2) 
			& (ak.sum(events.Muon.charge, axis=1) == 0 )
		]

		# Select Muon and do Lorentz sum
		zmm = mmevents.Muon[:,0] + mmevents.Muon[:,1]
		
		out.fill(
			dataset = events.metadata["dataset"],
			mass = zmm.mass
		)

		return out
	
	# -- Finally! return accumulator
	def postprocess(self,accumulator):
		return accumulator	
# <---- Class MyZPeak

#samples = {
#	"DrellYan" : [fname]
#}



## Single node Executor
'''
result = processor.run_uproot_job(
	samples,  #dataset
	"Events", # Tree name
	MyZPeak(), # Class
	processor.iterative_executor, #executor
	{"schema": NanoAODSchema}, # executor arguments
)
'''

## Prepare files
N_node = args.nWorker
datalist = args.nData

filelist=[]
with open(datalist) as fhand:
	for line in fhand:
		line = line.rstrip()
		filelist.append(line)
	fhand.seek(0)
	
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
    #maxchunks=4,
)


# Draw hist
#import matplotlib.pyplot as plt
#hist.plot1d(result)
#plt.savefig("Zmumu.png")

import os
os.system("mkdir hists")
save(result,'hists/Zmm.futures')




elapsed_time = time.time() - start
print("Time: ",elapsed_time)
## <-------------------------


