import os
import numpy as np
from coffea.util import load, save
import matplotlib.pyplot as plt
import coffea.hist as hist
import time
import mplhep
plt.style.use(mplhep.style.CMS)


lumi= 21.1 * 1000
GenDY = 1933600
xsecDY=2137.0

weightDY = lumi * xsecDY / GenDY

def reduce(folder,sample_list):
	 
	variables = []
	print(os.listdir(folder))


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
	hsum_nElectrons = hist.Hist(
		"Events",
		hist.Cat("dataset","Dataset"),
		hist.Bin("nElectrons","# of Electrons",10,0,10)
	)


	hists={}
	for filename in os.listdir(folder):
		hin = load(folder + '/' + filename)
		hists[filename] = hin.copy()

		if filename.split('_')[0] not in sample_list:
			continue;

		
		#hsum_Mee.add(hists[filename]['mass'])
		hsum_Mee_60_120.add(hists[filename]['mass_60_120'])
		hsum_nElectrons.add(hists[filename]['nElectrons'])
		
		#hsum_Mee.add(hists[filename])
		#hsum_Mee_60_120.add(hists[filename])
		#hsum_nElectrons.add(hists[filename])


	return hsum_Mee_60_120,hsum_nElectrons
	


if __name__ == '__main__':


# ---->  Make hist
	print("Start processing.. ")
	start = time.time()

	#sample_list = ['WZ','DY','Egamma']
	sample_list = ['DY','Egamma']

	h1_Mee, h1_nElectrons  = reduce("condorOut",sample_list)


	print("######## Loaded hist ############" )
	print(h1_Mee)

	## Noramlize	
	scales={
		'DY' : weightDY
	}
	h1_Mee.scale(scales,axis='dataset')


	elapsed_time = time.time() - start
	print("Time: ",elapsed_time)
# <--------- 



# ----> Plotting 
	print("End processing.. make plot")

	# make a nice ratio plot, adjusting some font sizes
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

		h1_Mee['DY'],
		ax=ax,
		clear=False,
		stack=True,
		fill_opts=fill_opts,
		error_opts = error_opts
	)

	# DATA plotting
	hist.plot1d(
	
		h1_Mee['Egamma'],
		ax=ax,
		clear=False,
		error_opts=data_err_opts
	)



	# Ratio Plot
	hist.plotratio(
	    num=h1_Mee['Egamma'].sum("dataset"),
	    denom=h1_Mee['DY'].sum("dataset"),
	    ax=rax,
	    error_opts=data_err_opts,
	    denom_fill_opts={},
	    guide_opts={},
	    unc='num'
	)


	
	rax.set_ylabel('Ratio')
	rax.set_ylim(0,2)
	ax._get_lines.prop_cycler = ax._get_patches_for_fill.prop_cycler
	ax.autoscale(axis='x', tight=True)
	ax.set_ylim(1, 1e+9)
	ax.set_yscale('log')
	ax.set_xlabel(None)
	ax.set_yscale('log')
	leg = ax.legend()

	plt.savefig("Mee.png")	



