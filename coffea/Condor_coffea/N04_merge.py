import os
import numpy as np
from coffea.util import load, save
import matplotlib.pyplot as plt
import coffea.hist as hist
import time


def reduce(folder):
	 
	variables = []
	print(os.listdir(folder))


	hsum_Mee = hist.Hist(
		"Events",
		hist.Cat("dataset","Dataset"),
		hist.Bin("mass","Z mass",100,0,200)	
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
		
		#print("Gen Entries of {0}: {1}".format(filename.split('.')[0],hists[filename]['sumw']['WZ']))
		#print("Selected Entries of {0}: {1}".format(filename.split('.')[0],np.sum(hists[filename]['mass'][()])))
		
		hsum_Mee.add(hists[filename]['mass'])
		hsum_nElectrons.add(hists[filename]['nElectrons'])

	print("Selected Entries of sum hist: ",np.sum(hsum_Mee.sum('dataset').values()[()]))

	return hsum_Mee,hsum_nElectrons
	


if __name__ == '__main__':


	import mplhep
	plt.style.use(mplhep.style.CMS)
	print("Start processing.. ")


	start = time.time()

	h1_Mee, h1_nElectrons  = reduce("condorOut")
	elapsed_time = time.time() - start
	print("Time: ",elapsed_time)


	print("End processing.. make plot")
	stack_fill_opts = {
		'alpha': 0.5,
		'edgecolor':(0,0,0,.5)
	}

	hist.plot1d(
		h1_Mee,
		fill_opts=stack_fill_opts,
	)
	plt.savefig("Mee.png")
	
	plt.close()
	hist.plot1d(
		h1_nElectrons,
		fill_opts=stack_fill_opts,
	)
	plt.savefig("nElectrons.png")
	


	


