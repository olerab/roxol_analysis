#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:27:20 2019

@author: olerab
"""

# RESET ALL
from IPython import get_ipython
get_ipython().magic('reset -sf')
 
import numpy as np   
import matplotlib.pyplot as plt
from FracArea import *
from FracOrientation import *

def main():
    """ INSERT DESCRIPTION HERE"""
    
    #insert all relevant paths
#    paths =['/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/10perc/',
#            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress/',
#            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/compressional/10perc/']
     
    paths =['/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress/',
            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/5perc/',
            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/10perc/']

    
    fpath_out = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/plots/'
    fname_out = 'plots_90deg_iso.png'
    # prepare data dicts
    frac_area = {}
    frac_length = {}
    segment_angle_data = {}
    cnt = 0

    for fpath in paths:
        fpath_in_fracNodes = fpath + '*_fracNodes.txt'
        fpath_in_dispVec = fpath + '*_dispVec.txt'
        
        #Fracture Area
        frac_area[cnt], frac_length[cnt] = FracArea(fpath_in_fracNodes, fpath_in_dispVec, plotting = False, norm_by_len = False)
        
        #Fracture Segment Angles
        segment_angle_data[cnt] = FracOrientation(fpath)
        cnt += 1
    
    return frac_area, frac_length, segment_angle_data

if __name__ == "__main__":
    frac_area, frac_length, segment_angle_data = main()
    
    
    # -------------------- plot total frac areas for all experiments
    
    leg = ['10 percent extensional','isotropic','10 percent compressional']
    fig = plt.figure(figsize=(15,7))
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    for i in range(0,len(frac_area)):
        line, = ax.plot(frac_area[i], lw=2, marker='o')
        ax.set_xlabel("Simulation Step", fontsize=18)
        ax.set_ylabel("Total Fracture Area", fontsize=18)
        line2, = ax2.plot(frac_length[i], lw=2, marker='o', alpha = .5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.grid(True)
        ax.legend(leg, loc='upper left')
    plt.show()
    #fig.savefig(fpath_out + fname_out)
    
    

    #  frac angles and plotting

    frac_spacing_init = 0.08
    
    
    fig2, axs = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(15,7))
    for i in range(0,len(segment_angle_data)):
        # Now switch to a more OO interface to exercise more features.
        
        avg_err_seg = segment_angle_data[i]
        # workaround for nan's from pumping steps (duplicate previous value)
        pump_ids = np.where(np.isnan(avg_err_seg))
        avg_err_seg[pump_ids[0]] = avg_err_seg[pump_ids[0]-1] 
        
        frac_len_by_spacing = [x / frac_spacing_init for x in frac_length[i]]
        #axs.errorbar(frac_len_by_spacing[1:], avg_err_seg[1:,0], yerr=avg_err_seg[1:,1], fmt='o')
        axs.plot(frac_len_by_spacing[:], avg_err_seg[:,0], lw=2, marker='o')
        #axs.set_title(path_in[35:], fontsize=18)
        axs.set_xlabel('$L/D_{init}$', fontsize=16)
        axs.set_ylabel("Median angle from horizontal (deg)", fontsize=16)
        axs.set_ylim([0, 90])
        axs.legend(leg, loc='upper left')
    plt.show()