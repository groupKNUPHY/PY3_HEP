import awkward1 as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import time
start = time.time()


## read NanoAOD file from link...

# 40 events
#fname = "https://raw.githubusercontent.com/CoffeaTeam/coffea/master/tests/samples/nano_dy.root"

# Many events
fname = "/x6/cms/store/mc/RunIISummer19UL18NanoAODv2/WZ_TuneCP5_13TeV-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/809D80E0-A0EB-5548-BCD1-58C4A1C1A71C.root"








## Procedural method Calculate Mass(mu+mu-)----> 
'''
events = NanoEventsFactory.from_file(fname, schemaclass=NanoAODSchema).events()

mmevents = events[ak.num(events.Muon) == 2]
zmm = mmevents.Muon[:, 0] + mmevents.Muon[:, 1]
print(zmm.mass)
'''
## <----------------------------





## OOP method: ProcessorABC  Calculate Mass(Mu+Mu-)---->
from coffea import processor, hist

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

samples = {
	"DrellYan" : [fname]
}



## Single node Executor
result = processor.run_uproot_job(
	samples,  #dataset
	"Events", # Tree name
	MyZPeak(), # Class
	processor.iterative_executor, #executor
	{"schema": NanoAODSchema}, # executor arguments
)


## Multi-node Executor
'''
result = processor.run_uproot_job(
	samples,  #dataset
	"Events", # Tree name
	MyZPeak(), # Class
	executor=processor.futures_executor,
    executor_args={"schema": NanoAODSchema, "workers": 2},
    maxchunks=4,
)
'''


# Draw hist
import matplotlib.pyplot as plt
hist.plot1d(result)
plt.savefig("Zmumu.png")



elapsed_time = time.time() - start
print("Time: ",elapsed_time)
## <-------------------------


