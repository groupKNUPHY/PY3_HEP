import os
import numpy as np
from coffea.util import load, save
import matplotlib.pyplot as plt
import coffea.hist as hist
import time


#import mplhep
#plt.style.use(mplhep.style.CMS)

filename="WZ_Run2018_40000.futures"
histo = load(filename)


h1_mass = histo['mass']
h1_Nele = histo['nElectrons']
nWZ = histo['sumw']['WZ']


if not isinstance(h1_mass,hist.Hist):
	raise "Error type is not hist"

if not isinstance(h1_Nele,hist.Hist):
	raise "Error type is not hist"


hist.plot1d(h1_mass,overlay='dataset')
plt.show()


plt.close()
hist.plot1d(h1_Nele,overlay='dataset')
plt.show()



