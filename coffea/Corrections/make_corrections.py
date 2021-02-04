from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import uproot
from coffea.util import save, load
from coffea import hist, lookup_tools
from coffea.lookup_tools import extractor, dense_lookup

'''
pu_files = {
    '2018':uproot.open('Pileup/data_2018_pileup_out.root'),
}
get_pu_weight={}
for year in ['2018']:
    pu_hist = pu_files[year]['pileup']
    get_pu_weight[year] = lookup_tools.dense_lookup.dense_lookup(pu_hist.values, pu_hist.edges)
'''


###
# Electron id SFs. depends on supercluster eta and pt.
###

ele_loose_files = {
    '2018': uproot.open("Egamma/Electron_hist_root/egammaEffi.txt_Ele_Loose_EGM2D.root")
}
get_ele_loose_id_sf = {}
for year in ['2018']:
    ele_loose_sf_hist = ele_loose_files[year]["EGamma_SF2D"]
    get_ele_loose_id_sf[year]  = lookup_tools.dense_lookup.dense_lookup(ele_loose_sf_hist.values, ele_loose_sf_hist.edges)


###
# Electron reconstruction SFs. Depends on supercluster eta and pt.    
###

ele_reco_files = {
    '2018': uproot.open("Egamma/Electron_hist_root/egammaEffi_ptAbove20.txt_EGM2D_UL2018.root")
}
get_ele_reco_sf = {}
for year in ['2018']:
    ele_reco_hist = ele_reco_files[year]["EGamma_SF2D"]
    get_ele_reco_sf[year]=lookup_tools.dense_lookup.dense_lookup(ele_reco_hist.values, ele_reco_hist.edges)

ele_reco_lowet_hist = uproot.open("Egamma/Electron_hist_root/egammaEffi_ptBelow20.txt_EGM2D_UL2018.root")['EGamma_SF2D']
get_ele_reco_lowet_sf=lookup_tools.dense_lookup.dense_lookup(ele_reco_lowet_hist.values, ele_reco_lowet_hist.edges)







corrections = {
    
#    'get_pu_weight' : get_pu_weight,
'get_ele_loose_id_sf':get_ele_loose_id_sf,
'get_ele_reco_sf':get_ele_reco_sf,
'get_ele_reco_lowet_sf':get_ele_reco_lowet_sf
}


save(corrections,'corrections.coffea')

