import numpy as np
import awkward1 as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import processor, hist
import matplotlib.pyplot as plt
from coffea.nanoaod import NanoEvents


fname = '/x6/cms/store/data/Run2018A/EGamma/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/FFE5D456-902C-7944-A7E6-438068898290.root'
events = NanoEventsFactory.from_root(fname, schemaclass=NanoAODSchema).events()
#events = NanoEvents.from_file(fname)




doubleelectron_triggers  ={
'2018': [
#       "Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
#       "Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",
        "DiEle27_WPTightCaloOnly_L1DoubleEG",
#       "DoubleEle33_CaloIdL_MW",
#       "DoubleEle25_CaloIdL_MW"
#       "DoubleEle27_CaloIdL_MW",
#       "DoublePhoton70"
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

print("## Show column list ##")
print(events.fields)
#print(events.columns)
print("{0} number of events are detected".format(len(events)))

print("## start trigger ##")
#print(events.HLT.columns)


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


Initial_events = events
events = events[single_ele_triggers_arr | double_ele_triggers_arr]
print("Total {0} number of events are remain after triggger | Eff: {1}".format(len(events), len(events) / len(Initial_events) * 100))


