import awkward1 as ak
from coffea.nanoaod import NanoEvents
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import time
from coffea import processor, hist
from coffea.util import load, save
import json
start = time.time()
import glob 
import os
import argparse



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


# Draw hist
#import matplotlib.pyplot as plt
#hist.plot1d(result)
#plt.savefig("Zmumu.png")


outname = data_sample + '.futures'
save(result,outname)




elapsed_time = time.time() - start
print("Time: ",elapsed_time)
## <-------------------------


