from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import uproot
from coffea.util import save, load
from coffea import hist, lookup_tools
from coffea.lookup_tools import extractor, dense_lookup

pu_files = {
    '2018':uproot.open('Pileup/data_2018_pileup_out.root'),
}

get_pu_weight={}
for year in ['2018']:
    pu_hist = pu_files[year]['pileup']
    get_pu_weight[year] = lookup_tools.dense_lookup.dense_lookup(pu_hist.values, pu_hist.edges)


corrections = {
    
    'get_pu_weight' : get_pu_weight,
    
}


toy_pdf  = np.random.poisson(32, 1000000)
get_pu_weight = corrections['get_pu_weight']['2018']


pu = get_pu_weight(toy_pdf)
print(pu)


print(len(pu))
x = np.arange(len(pu))

import matplotlib.pyplot as plt
plt.plot(x,pu,'.')
plt.show()



#save(corrections,'corrections.coffea')

