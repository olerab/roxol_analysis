#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:27:20 2019

@author: olerab
"""
import matplotlib.pyplot as plt
from FracArea import *

def main():
    """ INSERT DESCRIPTION HERE"""
    #insert all relevant paths
    paths =['/Volumes/PVPLAB2/OLE/roxol/RESULTS/15deg_aligned/extensional/200perc/',
            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/45deg_semialigned/extensional/200perc/',
            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/200perc/']#,
            #'/Volumes/PVPLAB2/OLE/roxol/RESULTS/15deg_aligned/compressional/100perc/']#,            
#            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/1perc/', #           '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/5perc/',
  #         '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/200perc/',
    #        '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress/',
     #       '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/unconfined/']
    
    frac_area = {}
    cnt = 0

    for fpath in paths:
        fpath_in_fracNodes = fpath + '*_fracNodes.txt'
        fpath_in_dispVec = fpath + '*_dispVec.txt'
        
        frac_area[cnt] = FracArea(fpath_in_fracNodes, fpath_in_dispVec, plotting = True)
        cnt += 1

    # -------------------- plot total frac areas for all experiments

    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    for i in range(0,cnt):
        line, = ax.plot(frac_area[i], lw=2, marker='o')
        ax.set_title(fpath_in_fracNodes[35:-16], fontsize=18)
        ax.set_xlabel("Simulation Step", fontsize=18)
        ax.set_ylabel("Total Fracture Area", fontsize=18)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.grid(True)
        #plt.ylim([0, 1e-2])
        ax.legend(paths)
    plt.show()
    
    
    return frac_area

    
    
    
if __name__ == "__main__":
    main()
    