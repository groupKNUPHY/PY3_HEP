import uproot
import matplotlib.pyplot as plt
import mplhep
import boost_histogram as bh
import numpy as np



f = uproot.open('Pileup/data_2018_pileup_out.root')
hist = f['pileup']


x = np.arange(len(hist.edges)-1)
y = hist.values


print(x)
print(y)

plt.step(x,y)
plt.show()



