import coffea.hist as hist
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt


xyz = np.random.multivariate_normal(mean=[1, 3, 7], cov=np.eye(3), size=10000)

xbins = np.linspace(-10, 10, 20)
ybins = np.linspace(-10, 10, 20)
zbins = np.linspace(-10, 10, 20)
hnumpy = np.histogramdd(xyz, bins=(xbins, ybins, zbins))


histo = hist.Hist("Counts",

	hist.Cat("sample","sample name"),
	hist.Bin("x","x value",20,-10,10),
	hist.Bin("y","y value",20,-10,10),
	hist.Bin("z","z value",20,-10,10),

	)

histo.fill(sample="sample 1", x=xyz[:,0], y=xyz[:,1], z=xyz[:,2])
xyz_sample2 = np.random.multivariate_normal(mean=[1,3,7], cov=np.eye(3), size=10000)

weight = np.arctan(np.sqrt(np.power(xyz_sample2, 2).sum(axis=1)))

histo.fill(sample="sample 2", x=xyz_sample2[:,0], y=xyz_sample2[:,1], z=xyz_sample2[:,2],weight=weight)


print("##"*20)
print(histo)
print(histo.sum("x",overflow='none'))
print("##"*20)


sliced = histo[:,0:,4:,0:]
#display(sliced)
#display(sliced.identifiers("y",overflow='all'))

histo.integrate("y", slice(0,10))

histo.rebin("z",hist.Bin("znew","rebinned z value",[-10,-6,6,10]))

mapping = {
	'all samples' : ['sample1', 'sample 2'],
	'just sample 1': ['sample 1'],
}

histo.group("sample",hist.Cat("cat","new category"),mapping)

histo.scale(3.)

scales = {

	'sample 1' : 1.2,
	'sample 2' : 0.2,	
}

histo.scale(scales, axis='sample')

#display(histo.identifiers('sample'))
#display(histo.identifiers('x'))




## Write root files
'''
import uproot
import os

if os.path.exists("output.root"):
    os.remove("output.root")
outputfile = uproot.create("output.root")
h = histo.sum('x', 'y')
for sample in h.identifiers('sample'):
	print(sample)
	outputfile[sample.name] = hist.export1d(h.integrate('sample', sample))
outputfile.close()
'''

## Plotting


hnew = (

	histo
	.rebin("y", hist.Bin("ynew","rebinned y value", [0,3,5]))
	.rebin("z", hist.Bin("znew","rebinned z value", [5,8,10]))

)

hist.plotgrid(hnew,row='ynew',col='znew',overlay='sample')
plt.show()













































