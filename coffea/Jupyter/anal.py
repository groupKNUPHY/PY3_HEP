import numpy as np
import awkward1 as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import processor, hist
import matplotlib.pyplot as plt
from coffea.nanoaod import NanoEvents

# flat dim for histo fill
def flat_dim(arr):
	sub_arr = ak.flatten(arr)
	mask = ~ak.is_none(sub_arr)
	return ak.to_numpy(sub_arr[mask])


# Z mass window

#fname = '/x6/cms/store/data/Run2018B/EGamma/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/50000/259E4654-F409-2F43-B2B0-E120BB0FC0AE.root'


#flist = ['/x6/cms/store/mc/RunIISummer19UL18NanoAODv2/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/84C4862F-224D-4D41-8124-6F9E40384B87.root', '/x6/cms/store/mc/RunIISummer19UL18NanoAODv2/DYToEE_M-50_NNPDF31_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/DF06C547-6727-0B4A-A3F3-51C3DC8C1AD7.root']


flist=['/x6/cms/store_Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON/data/Run2018A/EGamma/NANOAOD/UL2018_MiniAODv1_NanoAODv2-v1/280000/D628EAD9-EACA-0640-AF0C-A0698767F9DE_Skim.root']

fname = flist[0]

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
print("## 1 ------Total {0} number of events are remain after triggger | Eff: {1}".format(len(events), len(events) / len(Initial_events) * 100))

Electron = events.Electron



def Electron_selection(ele):
	# CutBased ID -->   0:fail, 1:veto, 2:loose, 3:medium, 4:tight
	return (ele.pt > 20) & (np.abs(ele.eta) < 2.5) & (ele.cutBased > 1)

#Electron_mask = (Electron.pt >20) & (np.abs(Electron.eta) < 2.5) & (Electron.cutBased > 1)
Electron_mask = Electron_selection(Electron)
Ele_channel_mask = ak.num(Electron[Electron_mask]) > 1
Ele_channel_events = events[Ele_channel_mask]


Ele_Channel_events = len(Ele_channel_events)

Nevt_passing_trigger = len(events)
Nevt_passing_Elech   = len(Ele_channel_events)
print("")
print("## 2 Passig Electron channel {0} --> {1}".format(Nevt_passing_trigger,Nevt_passing_Elech))



## 
Ele = Ele_channel_events.Electron
Electron_mask = Electron_selection(Ele)
Ele_sel = Ele[Electron_mask]


Nevt_passing_Elech = len(flat_dim(Ele))
Nevt_passing_EleSel = len(flat_dim(Ele_sel))
print("")
print("## 3 N of Electrons that passig Electron Selection {0} --> {1}".format(Nevt_passing_Elech,Nevt_passing_EleSel))


print("")
print("## Number of electron per events ")
print(ak.num(Ele_sel))



print(" --- Start Make Ele pair ---- ")
# All possible pairs of Electron in each event
ele_pairs = ak.combinations(Ele_sel,2,axis=1)

# Ele_pairs
ele_left, ele_right = ak.unzip(ele_pairs)
diele = ele_left + ele_right

print("## Printout left and right")
print(ele_left.pt)
print(ele_right.pt)
print("## Printout len(left) and len(right) (must be same)")
print(len(ele_left.pt))
print(len(ele_right.pt))
print("## Printout num(left) and num(right) (must be same)")
print(ak.num(ele_left.pt))
print(ak.num(ele_right.pt))

#cnti=0
#cntj=0
#for i ,j in zip(ak.num(ele_left.pt),ak.num(ele_right.pt)):
#	if i > 1:
#		cnti+=1
#		print("left:",i)
#	if j > 1:
#		cntj+=1
#		print("right:",j)
#
#print("more than one electron per evt: ",cnti,cntj)



print("## Printout flatten len(left) and len(right) (must be same)")
print(len(flat_dim(ele_left.pt)))
print(len(flat_dim(ele_right.pt)))


# Opposite sign cut 
os_mask	  = diele.charge==0
os_diele	 = diele[os_mask]
os_ele_left  = ele_left[os_mask]
os_ele_right = ele_right[os_mask]


## Validate test1 
base_L = len(flat_dim(ele_left))
base_R = len(flat_dim(ele_right))

os_L = len(flat_dim(os_ele_left))
os_R = len(flat_dim(os_ele_right))

print("")
print('## 4 N of Elctron-pairs that passing OS condition  L: {0} --> {1}'.format(base_L,os_L))
print('## 4 N of Elctrons-pairs that passing OS condition  R: {0} --> {1}'.format(base_R,os_R))
print('Validate OS Eff: L:', os_L / base_L)
print('Validate OS Eff: R:', os_R / base_R)
print("")



# Leading pair (Highest PT parir)
def make_leading_pair(target,base):
	return target[ak.argmax(base.pt,axis=1,keepdims=True)]


# Find one Electron-pari that have highest dielePT
# Leading set
leading_diele	 = make_leading_pair(diele,diele)
leading_ele	   = make_leading_pair(ele_left,diele)
subleading_ele	= make_leading_pair(ele_right,diele)



# OS and Leading set
leading_os_diele  = make_leading_pair(os_diele,os_diele)
leading_os_ele	= make_leading_pair(os_ele_left,os_diele)
subleading_os_ele = make_leading_pair(os_ele_right,os_diele)


## Validate test2
base_L = os_L
base_R = os_R
base_A = len(flat_dim(os_diele))

lead_L = len(flat_dim(leading_os_ele))
lead_R = len(flat_dim(subleading_os_ele))
lead_A = len(flat_dim(leading_os_diele))

print('## 5 Remove duplicated pairs')
print('## 5 N of Elctron-pairs that passing HighPT  condition  L: {0} --> {1}'.format(base_L,lead_L))
print('## 5 N of Elctron-pairs that passing HighPT  condition  R: {0} --> {1}'.format(base_R,lead_R))
print('## 5 N of Elctron-pairs that passing HighPT  condition  All: {0} --> {1}'.format(base_A,lead_A))
print('## 5 N of Evnets passing OSSF with High-PT condition {0} --> {1}'.format(Ele_Channel_events,lead_A))


print("")
print(" --- Leading-only  vs OS+Leading ----")
print(" ---- Leading-only must be same with Ele-channel events :  {0}".format(Ele_Channel_events))
print("diele :", len(flat_dim(leading_diele)),len(flat_dim(leading_os_diele)))
print("L :", len(flat_dim(leading_ele)),len(flat_dim(leading_os_ele)))
print("R :", len(flat_dim(subleading_ele)),len(flat_dim(subleading_os_ele)))
print("A :", len(flat_dim(leading_diele)),len(flat_dim(leading_os_diele)))




def makeZmass_window_mask(dielecs,start=60,end=120):
	mask = (dielecs.mass >=start) & (dielecs.mass <=end)
	return mask



## Leading-Only
Zmass_mask = makeZmass_window_mask(leading_diele)

leading_Zwindow_ele	= leading_ele[Zmass_mask]
subleading_Zwindow_ele = subleading_ele[Zmass_mask]
leading_Zwindow_diele  = leading_diele[Zmass_mask]

_baseL = len(flat_dim(leading_ele))
_baseR = len(flat_dim(subleading_ele))
_baseA = len(flat_dim(leading_diele))

_cutL  = len(flat_dim(leading_Zwindow_ele))
_cutR  = len(flat_dim(subleading_Zwindow_ele))
_cutA  = len(flat_dim(leading_Zwindow_diele))

## Leading-with-OSSF
Zmass_mask_os = makeZmass_window_mask(leading_os_diele)


leading_os_Zwindow_ele	  = leading_os_ele[Zmass_mask_os]
subleading_os_Zwindow_ele = subleading_os_ele[Zmass_mask_os]
leading_os_Zwindow_diele  = leading_os_diele[Zmass_mask_os]

baseL = len(flat_dim(leading_os_ele))
baseR = len(flat_dim(subleading_os_ele))
baseA = len(flat_dim(leading_os_diele))

cutL  = len(flat_dim(leading_os_Zwindow_ele))
cutR  = len(flat_dim(subleading_os_Zwindow_ele))
cutA  = len(flat_dim(leading_os_Zwindow_diele))


print("")
print(" --- Leading-OSSF ----")
print("## 6 N of Events passing Zmass window: {0} --> {1}".format(baseL,cutL))
print("## 6 N of Events passing Zmass window: {0} --> {1}".format(baseR,cutR))
print("## 6 N of Events passing Zmass window: {0} --> {1}".format(baseA,cutA))
print("## Ele-channel events -> OSSF -> Zmass: {0} --> {1} --> {2}".format(Ele_Channel_events,baseA,cutA))
print("")


print(" --- Leading-only ----")
print("## 6 N of Events passing Zmass window: {0} --> {1}".format(_baseL,_cutL))
print("## 6 N of Events passing Zmass window: {0} --> {1}".format(_baseR,_cutR))
print("## 6 N of Events passing Zmass window: {0} --> {1}".format(_baseA,_cutA))
print("## Ele-channel events -> OSSF -> Zmass: {0} --> {1} --> {2}".format(Ele_Channel_events,_baseA,_cutA))
print("")




ele1PT = flat_dim(leading_Zwindow_ele.pt)
ele2PT = flat_dim(subleading_Zwindow_ele.pt)

os_ele1PT = flat_dim(leading_os_Zwindow_ele.pt)
os_ele2PT = flat_dim(subleading_os_Zwindow_ele.pt)

print("Leading PT must be {0}, : {1}".format(_cutA,len(ele1PT)))
print("Leading os PT must be {0}, : {1}".format(cutA,len(os_ele1PT)))

import matplotlib.pyplot as plt


cnt=0
for i in os_ele2PT:
	if i <= 20:
		cout << i << endl;
		cnt+=1

print("overflow ele os 1pt : ",cnt)


bins = np.linspace(0,600,300)
plt.hist(ele1PT,bins=bins)
plt.xlim(0,300)
plt.yscale('log')
plt.savefig('ele1pt')
plt.close()

plt.hist(ele2PT,bins=bins)
plt.xlim(0,300)
plt.yscale('log')
plt.savefig('ele2pt')
plt.close()

plt.hist(os_ele1PT,bins=bins)
plt.xlim(0,300)
plt.yscale('log')
plt.savefig('os_ele1pt')
plt.close()

plt.hist(os_ele2PT,bins=bins)
plt.xlim(0,300)
plt.yscale('log')
plt.savefig('os_ele2pt')
plt.close()

