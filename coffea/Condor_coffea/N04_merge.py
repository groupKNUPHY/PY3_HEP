import os
import numpy as np
from coffea.util import load, save
import matplotlib.pyplot as plt
import coffea.hist as hist
import numba




def reduce(folder):
	 
	variables = []
	print(os.listdir(folder))


	
	Null_hist = hist.Hist(
		"Events",
		hist.Cat("dataset","Dataset"),
		hist.Bin("mass","Z mass",60,60,120)	
	)


	hists={}
	for filename in os.listdir(folder):
		hin = load(folder + '/' + filename)
		hists[filename] = hin
		
		print("Entries of {0}: {1}".format(filename.split('.')[0],np.sum(hists[filename].sum('dataset').values()[()])))
		Null_hist.add(hists[filename])


	print("Entries of sum hist: ",np.sum(Null_hist.sum('dataset').values()[()]))

	return Null_hist
	


if __name__ == '__main__':


	import mplhep
	plt.style.use(mplhep.style.CMS)
	print("Start processing.. ")
	sum_hist  = reduce("condorOut")



	print("End processing.. make plot")
	stack_fill_opts = {
		'alpha': 0.5,
		'edgecolor':(0,0,0,.5)
	}

	
	
	
	hist.plot1d(
		sum_hist,
		fill_opts=stack_fill_opts,
	)
	plt.show()
