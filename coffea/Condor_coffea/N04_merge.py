import concurrent.futures
import cloudpickle
import pickle
import gzip
import os
import numpy as np
from collections import defaultdict, OrderedDict
from coffea import hist, processor 
from coffea.util import load, save
import matplotlib.pyplot as plt





def reduce(folder):
	 
	variables = []
	print(os.listdir(folder))

	hists={}
	for filename in os.listdir(folder):
		#filename.split('.')[0]
		hin = load(folder + '/' + filename)
		hists[filename] = hin
		hist.plot1d(hists[filename])
		plt.savefig(filename + '.png')

	
	

		




if __name__ == '__main__':

	reduce("condorOut")
	
