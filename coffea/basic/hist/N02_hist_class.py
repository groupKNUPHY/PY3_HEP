import numpy as np
from scipy.stats import argus




class myTH1:
	def __init__(self,bins):
		self._bins = bins
		self._sumw = np.zeros(bins.size - 1)
	
	def fill(self,values,weights=None):
		sumw, _ = np.histogram(values, bins=self._bins, weights = weights)
		self._sumw += sumw

	def __add__(self,other):
		if not isinstance(other,myTH1):
			raise ValueError
		if not np.array_equal(other._bins, self._bins):
			raise ValueError("The histograms have inconsistent binning")

		out = myTH1(self._bins)
		out._sumw = self._sumw + other._sumw
		return out


vals = argus(chi=.5).rvs(size=1000)
bins = np.linspace(0,1,50)

h1 = myTH1(bins)
h1.fill(vals)
print("######## y h1 #######")
print(h1._sumw)


h2 = myTH1(bins)
h2.fill(vals)
print("######## y h2 #######")
print(h2._sumw)

h = h1+h2
print("######## y hsum #######")
print(h._sumw)




import matplotlib.pyplot as plt


fig,axs = plt.subplots(1,3,figsize=(30,10))
bins =  np.linspace(0,1,49)

axs[0].bar(bins,h1._sumw,color='r',alpha=0.5,label='h1')
axs[1].bar(bins,h2._sumw,color='b',alpha=0.5,label='h2')
axs[2].bar(bins,h._sumw,color='g',alpha=0.5,label='hsum')
plt.legend()
plt.show()

			
