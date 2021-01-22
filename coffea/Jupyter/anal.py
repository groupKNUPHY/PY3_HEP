import numpy as np
import awkward1 as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import processor, hist
import matplotlib.pyplot as plt
from coffea.nanoaod import NanoEvents


fname = '/x6/cms/store/data/Run2018A/EGamma/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/FFE5D456-902C-7944-A7E6-438068898290.root'
#fname = '/x6/cms/store/mc/RunIISummer19UL18NanoAODv2/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/280000/CA523346-37FF-9B47-BD1F-E278140A1570.root'
events = NanoEventsFactory.from_root(fname, schemaclass=NanoAODSchema).events()
#events = NanoEvents.from_file(fname)




doubleelectron_triggers  ={
'2018': [
#	   "Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
	   "Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",	# Recomended
 

#	   "DiEle27_WPTightCaloOnly_L1DoubleEG",
#	   "DoubleEle33_CaloIdL_MW",
#	   "DoubleEle25_CaloIdL_MW"
#	   "DoubleEle27_CaloIdL_MW",
#	   "DoublePhoton70"
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
		   'Ele32_WPTight_Gsf',   # Recomended
#		   'Ele27_WPTight_Gsf',   # All False
#			'Ele17_WPLoose_Gsf', # All False
#			'Ele15_WPLoose_Gsf', # All False

		]
	}

print("## Show column list ##")
print(events.fields)
#print(events.columns)
print("{0} number of events are detected".format(len(events)))

print("## start trigger ##")
#print(events.HLT['Ele27_WPTight_Gsf'])


## double lepton trigger
# ---- Not applied yet-------------------------------#
is_double_ele_trigger=True
year="2018"
if not is_double_ele_trigger:
	double_ele_triggers_arr=np.ones(len(events), dtype=np.bool)
else:
	double_ele_triggers_arr = np.zeros(len(events), dtype=np.bool)
	for path in doubleelectron_triggers[year]:
		if path not in events.HLT.fields: continue
		double_ele_triggers_arr = double_ele_triggers_arr | events.HLT[path]  # Or operation for same category of triggers
print("Double Electron triggers")


'''
## Trigger pass or not (Event by Event )
ispass=0
isblock=0
for i in double_ele_triggers_arr:
	if i:
		ispass+=1
	else:
		isblock+=1
print("Trigger pass: ",ispass)
print("Trigger blck: ",isblock)
'''
## single lepton trigger
# ---- Not applied yet-------------------------------#
is_single_ele_trigger=True
if not is_single_ele_trigger:
	single_ele_triggers_arr=np.ones(len(events), dtype=np.bool)
else:
	single_ele_triggers_arr = np.zeros(len(events), dtype=np.bool)
	for path in singleelectron_triggers[year]:
		if path not in events.HLT.fields: continue
		single_ele_triggers_arr = single_ele_triggers_arr | events.HLT[path]
'''
print("Single Electron triggers")

ispass=0
isblock=0
for i in single_ele_triggers_arr:
	if i:
		ispass+=1
	else:
		isblock+=1
print("Trigger pass: ",ispass)
print("Trigger blck: ",isblock)
'''

Initial_events = events
events = events[single_ele_triggers_arr | double_ele_triggers_arr]
print("Total {0} number of events are remain after triggger | Eff: {1}".format(len(events), len(events) / len(Initial_events) * 100))


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
os_mask	  = diele.charge==0
os_diele	 = diele[os_mask]
os_ele_left  = ele_left[os_mask]
os_ele_right = ele_right[os_mask]



# Leading pair (Highest PT parir)
def make_leading_pair(target,base):
	return target[ak.argmax(base.pt,axis=1,keepdims=True)]

# Leading set
leading_diele	 = make_leading_pair(diele,diele)
leading_ele	   = make_leading_pair(ele_left,diele)
subleading_ele	= make_leading_pair(ele_right,diele)


# OS and Leading set
leading_os_diele  = make_leading_pair(os_diele,os_diele)
leading_os_ele	= make_leading_pair(os_ele_left,os_diele)
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

print("### Before apply mass range ### ")
print(leading_diele.mass)
print(Zmass_mask)




leading_ele	= leading_ele[Zmass_mask]
leading_diele  = leading_diele[Zmass_mask]
subleading_ele = subleading_ele[Zmass_mask]

print("### After apply mass range ### ")
print(leading_diele.mass)
