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
    paths =['/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/10perc/',
            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/5perc/',
            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress/']
     
#    paths =['/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress/',
#            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/5perc/',
#            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/10perc/']

    

    
    
    
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
    save_figs = True
    fpath_out = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/plots/'
    fname_out_len = 'TotalLength_RandomOrientation_Aniso.pdf'
    fname_out_area = 'TotalArea_AllOrientations_Aniso.pdf'
    fname_out_ang = 'MedianAngles_AllOrientations_Aniso.pdf'
    
    
    leg = ['random, 10 % extensional','random, 5 % extensional','random, isotropic']
    colors = ['blue', 'red', 'black']
    markers = ['o', 'P', 'd']
    figsizex_cm = 6.8
    figsizey_cm = 4
    
    fig1 = plt.figure(figsize=(figsizex_cm,figsizey_cm))
    ax1 = fig1.add_subplot(111)
    for i in range(0,len(frac_area)):
        ax1.set_xlabel("Computation Step", fontsize=12)
        ax1.set_ylabel("Total Fracture Length ($m$)", fontsize=12)
        line = ax1.plot(frac_length[i], lw=1, marker=markers[i], color = colors[i], markevery=2)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.grid(True)
        ax1.legend(leg, loc='bottom right')
    plt.show()
    if save_figs == True:
        fig1.savefig(fpath_out+fname_out_len)
    
    
    
    fig2 = plt.figure(figsize=(figsizex_cm,figsizey_cm))
    ax2 = fig2.add_subplot(111)
    for i in range(0,len(frac_area)):
        line2 = ax2.plot(frac_area[i], lw=1, marker=markers[i], color = colors[i], markevery=1)
        ax2.set_xlabel("Computation Step", fontsize=12)
        ax2.set_ylabel("Total Fracture Area ($m^2$)", fontsize=12)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.grid(True)
        ax2.legend(leg, loc='upper right')
    plt.show()
    if save_figs == True:
        fig2.savefig(fpath_out+fname_out_area)
    
    

    #  frac angles and plotting

    frac_spacing_init = 0.08
    
    
    fig3, axs = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(figsizex_cm,figsizey_cm))
    for i in range(0,len(segment_angle_data)):
        # Now switch to a more OO interface to exercise more features.
        
        avg_err_seg = segment_angle_data[i]
        # workaround for nan's from pumping steps (duplicate previous value)
        pump_ids = np.where(np.isnan(avg_err_seg))
        avg_err_seg[pump_ids[0]] = avg_err_seg[pump_ids[0]-1] 
        
        frac_len_by_spacing = [x / frac_spacing_init for x in frac_length[i]]
        axs.plot(frac_len_by_spacing[:], avg_err_seg[:,2], lw=1, marker=markers[i], color = colors[i], linestyle = '-', markevery=1)
        axs.set_xlabel('L/D$_{init}$', fontsize=12)
        axs.set_ylabel("Median propagation angle (deg)", fontsize=12)
        plt.grid(True)
        axs.set_ylim([0, 90])
        axs.legend(leg, loc='lower right')
    plt.show()
    if save_figs == True:
        fig3.savefig(fpath_out+fname_out_ang)