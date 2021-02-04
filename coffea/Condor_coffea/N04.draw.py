import os
import numpy as np
from coffea.util import load, save
import matplotlib.pyplot as plt
import coffea.hist as hist
import time

## Parameter set
lumi= 21.01 * 1000
GenDY = 1933600
xsecDY=2137.0


hsum_cutflow = hist.Hist(
    'Events',
    hist.Cat('dataset', 'Dataset'),
    hist.Bin('cutflow', 'Cut index', [0, 1, 2, 3,4])
)

hsum_charge= hist.Hist(
       "Events",
       hist.Cat("dataset","Dataset"),
       hist.Bin("charge","charge sum of electrons", 6, -3, 3),
)
hsum_nPV = hist.Hist(
    "Events",
    hist.Cat("dataset","Dataset"),
    hist.Bin("nPV","Number of Primary vertex",100,0,100)	
)
hsum_Mee = hist.Hist(
    "Events",
    hist.Cat("dataset","Dataset"),
    hist.Bin("mass","Z mass",100,0,200)	
)
hsum_Mee_60_120 = hist.Hist(
    "Events",
    hist.Cat("dataset","Dataset"),
    hist.Bin("mass_60_120","Z mass",60,60,120)	
)
hsum_ele1pt = hist.Hist(
    "Events",
    hist.Cat("dataset","Dataset"),
    hist.Bin("ele1pt","Leading Electron $P_{T}$ [GeV]",300,0,600)	
)
hsum_ele2pt =  hist.Hist(
    "Events",
    hist.Cat("dataset","Dataset"),
    hist.Bin("ele2pt","Subleading $Electron P_{T}$ [GeV]", 300, 0, 600),
)

hsum_ele1eta= hist.Hist(
    "Events",
    hist.Cat("dataset","Dataset"),
    hist.Bin("ele1eta","Leading Electron $\eta$ [GeV]", 20, -5, 5),
)

hsum_ele2eta =  hist.Hist(
    "Events",
    hist.Cat("dataset","Dataset"),
    hist.Bin("ele2eta","Subleading Electron $\eta$ [GeV]", 20, -5, 5),
)
hsum_ele1phi =  hist.Hist(
    "Events",
    hist.Cat("dataset","Dataset"),
    hist.Bin("ele1phi","Leading Electron $\phi$ [GeV]", 20, -3.15, 3.15),
)

hsum_ele2phi =  hist.Hist(
    "Events",
    hist.Cat("dataset","Dataset"),
    hist.Bin("ele2phi","Subleading Electron $\phi$ [GeV]", 20, -3.15, 3.15),
)
hsum_nElectrons = hist.Hist(
    "Events",
    hist.Cat("dataset","Dataset"),
    hist.Bin("nElectrons","# of Electrons",10,0,10)
)



histdict = {'nPV':hsum_nPV, "cutflow":hsum_cutflow,"ele1pt":hsum_ele1pt,"ele2pt":hsum_ele2pt,"mass":hsum_Mee,
"ele1eta":hsum_ele1eta, "ele2eta":hsum_ele2eta,"ele1phi":hsum_ele1phi, "ele2phi":hsum_ele2phi}



def reduce(folder,sample_list,histname):
    hists={}
    sumw_DY=0
    sumw_Egamma=0
    
    
    for filename in os.listdir(folder):
        hin = load(folder + '/' + filename)
        hists[filename] = hin.copy()
        
        if filename.split('_')[0] not in sample_list:
            continue
        sumw_DY += hists[filename]['sumw']['DY']
        sumw_Egamma += hists[filename]['sumw']['Egamma_RunAB']
        hist_ = histdict[histname]
        hist_.add(hists[filename][histname])
        
    return hist_


## --File Directories

isPU=False

if isPU:
	file_path="condorOut_PU"
else:
	file_path="condorOut"



## --Sample Lists
#sample_list = ['WZ','DY','Egamma']
sample_list = ['DY','Egamma']

##############################################################33 --Hist names
#histname = "mass"; xmin=60; xmax=120; ymin=1000; ymax=1e+7;
#histname = "nPV"; xmin=0; xmax=100; ymin=1; ymax=7e+5;

#histname = "ele1pt"; xmin=1; xmax=200; ymin=1; ymax=2e+6;
#histname = "ele2pt"; xmin=1; xmax=200; ymin=1; ymax=2e+6;

#histname = "ele1eta"; xmin=-2.5; xmax=2.5; ymin=100; ymax=5e+6;
#histname = "ele2eta"; xmin=-2.5; xmax=2.5; ymin=100; ymax=5e+6;

#histname = "ele1phi"; xmin=-3.15; xmax=3.15; ymin=100; ymax=5e+6;
#histname = "ele2phi"; xmin=-3.15; xmax=3.15; ymin=100; ymax=5e+6;

histname = "cutflow"; xmin=0; xmax=5; ymin=1; ymax=1e+10

################################################################
## --All-reduce 
h1= reduce(file_path,sample_list,histname)


## --Noramlize    
scales={
    'DY' : lumi * xsecDY / GenDY
}
h1.scale(scales,axis='dataset')


# ----> Plotting 
print("End processing.. make plot")
print(" ")
# make a nice ratio plot, adjusting some font sizes


import mplhep as hep
plt.style.use(hep.style.CMS)



plt.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 18,
    'axes.labelsize': 18,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12
})
fig, (ax, rax) = plt.subplots(
    nrows=2,
    ncols=1,
    figsize=(7,7),
    gridspec_kw={"height_ratios": (3, 1)},
    sharex=True
)

fig.subplots_adjust(hspace=.07)


from cycler import cycler
colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c']
ax.set_prop_cycle(cycler(color=colors))


fill_opts = {
    'edgecolor': (0,0,0,0.3),
    'alpha': 0.8
}
error_opts = {
    'label': 'Stat. Unc.',
    'hatch': '///',
    'facecolor': 'none',
    'edgecolor': (0,0,0,.5),
    'linewidth': 0
}
data_err_opts = {
    'linestyle': 'none',
'marker': '.',
'markersize': 4.,
'color': 'k',
}



# MC plotting
hist.plot1d(

    h1['DY'],
    ax=ax,
    clear=False,
    stack=True,
    fill_opts=fill_opts,
    error_opts = error_opts,
    
)

# DATA plotting
hist.plot1d(

    h1['Egamma_RunAB'],
    ax=ax,
    clear=False,
    error_opts=data_err_opts
    
)



# Ratio Plot
hist.plotratio(
    num=h1['Egamma_RunAB'].sum("dataset"),
    denom=h1['DY'].sum("dataset"),
    ax=rax,
    error_opts=data_err_opts,
    denom_fill_opts={},
    guide_opts={},
    unc='num'
)




rax.set_ylabel('Data/MC')
rax.set_ylim(0,2)


ax._get_lines.prop_cycler = ax._get_patches_for_fill.prop_cycler
ax.autoscale(axis='x', tight=True)
ax.set_ylim(ymin,ymax)
ax.set_xlim(xmin,xmax)
ax.set_xlabel('')
ax.set_yscale('log')


#rax.set_xlabel('# of Priamary vertex')
#leg = ax.legend()





lum = plt.text(1., 1., r"53 fb$^{-1}$ (13 TeV)",
                fontsize=16,
                horizontalalignment='right',
                verticalalignment='bottom',
                transform=ax.transAxes
               )


if isPU:
	outname = histname + "_PU" + ".png"
else:
	outname = histname  + ".png"


#plt.show()
plt.savefig(outname)
