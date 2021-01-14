import numpy as np
from scipy.stats import argus

vals = argus(chi=.5).rvs(size=1000)
hist = np.histogram(vals)
#print(hist)
bins = np.linspace(0,1,50)

def add_histos(h1,h2):
	h1sumw, h1bins = h1
	h2sumw, h2bins = h2
	if h1bins.shape == h2bins.shape and np.all(h1bins == h2bins):
		return h1sumw+h2sumw, h1bins
	else:
		raise ValueError("The histograms have inconsistent binning")

vals2 = argus(chi=.5).rvs(size=1000)
hist1 = np.histogram(vals,bins=bins)
hist2 = np.histogram(vals,bins=bins)


print("#### Show each histograms ###")
print(hist1)
print(hist2)


print("### Merged histograms ###")
hist = add_histo(hist1,hist2)
print(hist)
