#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version 2020.01.03

This script combines a number of functions for analysis for roxol(TM) XFEM fracture network simulations.
Parameters include total fracture length, fracture area (opening), propagation angles of propagating fracture elements, outflow.
Additionally a number of simple plots can be created and saved.


Note that: 
(1) the functions and scripts may contain errors and 
(2) were specifically designed for the study of Rabbel et al (2020, submitted).

Functionality and application beyond the purpose of this study is not guaranteed and should be assessed with care
For details feel free to contact me via e-mail.

@author: Ole Rabbel, University of Oslo, ole.rabbel@geo.uio.no // ole.rabbel@gmail.com
"""

# RESET ALL
from IPython import get_ipython
get_ipython().magic('reset -sf')
 
import numpy as np   
import matplotlib.pyplot as plt
from FracArea import *
from FracOrientation import *
from flow_analysis import *

def main():
    """ MAIN function calling the functions to perform the analysis
    
    
    """
    
    #insert all relevant paths
    paths =['/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/10perc/']
    
    #,
    #        '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/5perc/',
    #        '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress/']
    
#    choose calculations. somehow this needs to be coupled so that choosing the calculated parameters is only done once...
    calc_area = True
    calc_length = True
    calc_angles = True
    calc_flow = False
    
    # volume flow calculation parameters
    flow_max = 1 # upper cutoff for volume flow, e.g. to exclude numerical artefactcs
    flow_min = -1 # lower cutoff for volume flow, e.g. to exclude numerical artefactcs (+/- is directional indicator for x and y components)
    nstep=7 # number of calculation steps between two flow steps in roxol
    calcmode = 'nodes' # use node results for calculation. alternative: 'elements', but not properly implemented yet (Jan 2020)
    
    # ----------------------------------------------------------------------------------
    # -------------- for basic use, don't edit MAIN script below this line  ------------
    # ----------------------------------------------------------------------------------

    # prepare data dicts
    # NOTE: probably there is a more efficient way to do this
    frac_area = {}
    frac_length = {}
    segment_angle_data = {}
    volFlow_out = {}
    volFlow_out_x = {}
    volFlow_out_y = {}
    cnt = 0

    for fpath in paths:
        fpath_in_fracNodes = fpath + '*_fracNodes.txt'
        fpath_in_dispVec = fpath + '*_dispVec.txt'
        
        # Total Fracture Area and Length
        if calc_area == True:
            frac_area[cnt], frac_length[cnt] = FracArea(fpath_in_fracNodes, fpath_in_dispVec, plotting = False, norm_by_len = False)
        
        #Prpagated Fracture Segment Angles per step
        if calc_angles == True:
            segment_angle_data[cnt] = FracOrientation(fpath)
        
        if calc_flow == True:
            volFlow_out[cnt], volFlow_out_x[cnt], volFlow_out_y[cnt] = flow_analysis(fpath, flow_max, flow_min, nstep, calcmode)
    
        cnt += 1
    return frac_area, frac_length, segment_angle_data, volFlow_out, volFlow_out_x, volFlow_out_y

if __name__ == "__main__":
    """
    execute main function for calculations, then plot the results
    """
    frac_area, frac_length, segment_angle_data, volFlow_out, volFlow_out_x, volFlow_out_y = main()
    
    
    # -------------------- plot total frac areas for all experiments
    # choose plots. note that calculations must be performed in order to plot
    save_figs = False
    calc_area = True
    calc_length = True
    calc_angles = True
    calc_flow = False
    
    # choose path and filenames if saving plots
    fpath_out = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/plots/'
    fname_out_len = 'TotalLength_RandomOrientation_Aniso.pdf'
    fname_out_area = 'TotalArea_AllOrientations_Aniso.pdf'
    fname_out_ang = 'MedianAngles_AllOrientations_Aniso.pdf'
    fname_out_flow = 'Flow_AllOrientations_Aniso.pdf'
    
    # choose legend entries - should be descriptive of the result files chosen in the "main" function
    leg = ['random, 10 % extensional','random, 5 % extensional','random, isotropic']
    colors = ['blue', 'red', 'black']
    markers = ['o', 'P', 'd']

    # choose figure size in cm
    figsizex_cm = 6.8
    figsizey_cm = 4
    
    # initial average spacing between fractures (for x axis in angle plot)
    # note: not happy with having this parameter here. should be an option in the function.
    frac_spacing_init = 0.08
    
    # ----------------------------------------------------------------------------------
    # -------------- unless very unhappy with layout, don't edit below here ------------
    # ----------------------------------------------------------------------------------
    if calc_length == True:
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
    
    
    if calc_area == True:
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
    
    if calc_angles == True:
        fig3, axs = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(figsizex_cm,figsizey_cm))
        for i in range(0,len(segment_angle_data)):
            
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
            
    if calc_flow == True:
        fig4, ax4 = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(figsizex_cm,figsizey_cm))
        for i in range(0,len(volFlow_out)):
            ax4.plot(volFlow_out[i]/np.sum(volFlow_out[i]), lw=1, marker=markers[i], color = colors[i], linestyle = '-', markevery=1)
            ax4.set_xlabel('Calculation Step', fontsize=12)
            ax4.set_ylabel("Normalized Outward Flow", fontsize=12)
            plt.grid(True)
            ax4.set_ylim([0, 1])
            ax4.legend(leg, loc='upper left')
        plt.show()
        if save_figs == True:
            fig4.savefig(fpath_out+fname_out_flow)

    