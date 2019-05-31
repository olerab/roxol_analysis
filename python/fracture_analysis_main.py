#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:27:20 2019

@author: olerab
"""
import matplotlib.pyplot as plt
from FracArea import *
from FracOrientation import *

def main():
    """ INSERT DESCRIPTION HERE"""
    #insert all relevant paths
    paths =['/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/1perc/',
            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/5perc/',
            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/10perc/',
            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/200perc/']
     
    
    fpath_out = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/plots/'
    fname_out = 'plots_90deg_iso.png'
    frac_area = {}
    frac_length = {}
    cnt = 0

    for fpath in paths:
        fpath_in_fracNodes = fpath + '*_fracNodes.txt'
        fpath_in_dispVec = fpath + '*_dispVec.txt'
        frac_area[cnt], frac_length[cnt] = FracArea(fpath_in_fracNodes, fpath_in_dispVec, plotting = False, norm_by_len = False)
        cnt += 1

    # -------------------- plot total frac areas for all experiments

    fig = plt.figure(figsize=(15,7))
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    for i in range(0,cnt):
        line, = ax.plot(frac_area[i], lw=2, marker='o')
        ax.set_title(fpath_in_fracNodes[35:-16], fontsize=18)
        ax.set_xlabel("Simulation Step", fontsize=18)
        ax.set_ylabel("Total Fracture Area", fontsize=18)
        line2, = ax2.plot(frac_length[i], lw=2, marker='o', alpha = .5)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.grid(True)
#        plt.ylim([0, 0.5e-2])
        ax.legend(paths)
    plt.show()
    #fig.savefig(fpath_out + fname_out)
    
    
    return frac_area

# frac angles
path_in = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/compressional/10perc/'
FracOrientation(path_in)
    
if __name__ == "__main__":
    main()
    