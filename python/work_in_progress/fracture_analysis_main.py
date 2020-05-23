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
from flow_analysis import *
from FracTopoConnectivity import *
from roxol_preproc import *

def main():
    """ INSERT DESCRIPTION HERE"""
    
    #insert all relevant paths
    paths =['/Users/olerab/Documents/PhD/work_projects/geomechanical_modelling/roxol_analysis/90deg_ext10perc/',
            '/Users/olerab/Documents/PhD/work_projects/geomechanical_modelling/roxol_analysis/45deg_ext10perc/',
            '/Users/olerab/Documents/PhD/work_projects/geomechanical_modelling/roxol_analysis/15deg_ext10perc/']
#            '/Volumes/PVPLAB2/OLE/roxol/RESULTS/45deg_semialigned/extensional/10perc/',
#           '/Volumes/PVPLAB2/OLE/roxol/RESULTS/15deg_aligned/extensional/10perc/']

    
#    choose calculations
    preproc = 0 #pre-processing (result file zero padding and node and displacement extraction as txt files)

    calc_area = True
    calc_length = True
    calc_angles = True
    calc_flow = False
    calc_connect = False
    
    
    # prepare data dicts
    frac_area = {}
    frac_length = {}
    segment_angle_data = {}
    volFlow_out = {}
    volFlow_out_x = {}
    volFlow_out_y = {}
    conn_per_line = {}
    cnt = 0

    for fpath in paths:
        
        # run preprocessing
        if preproc == 1:
            zero_padding(fpath)
            FN_extract(fpath)
        
        
        fpath_in_fracNodes = fpath + '*_fracNodes.txt'
        fpath_in_dispVec = fpath + '*_dispVec.txt'
        
        #Fracture Area
        if calc_area == True:
            frac_area[cnt], frac_length[cnt] = FracArea(fpath_in_fracNodes, fpath_in_dispVec, plotting = False, norm_by_len = False)
        
        #Fracture Segment Angles
        if calc_angles == True:
            segment_angle_data[cnt] = FracOrientation(fpath)
            
        #Fracture Segment Angles
        if calc_connect == True:
            conn_per_line[cnt] = FracTopoConnectivity(fpath, NX_init = 0, NY_init = 0)
        
        if calc_flow == True:
        # volume flow
            flow_max = 1
            flow_min = -1
            nstep=7
            calcmode = 'nodes'
            volFlow_out[cnt], volFlow_out_x[cnt], volFlow_out_y[cnt] = flow_analysis(fpath, flow_max, flow_min, nstep, calcmode)
    
        cnt += 1
    return frac_area, frac_length, segment_angle_data, volFlow_out, volFlow_out_x, volFlow_out_y, conn_per_line

if __name__ == "__main__":
    frac_area, frac_length, segment_angle_data, volFlow_out, volFlow_out_x, volFlow_out_y, conn_per_line = main()
    
    
    # -------------------- plot total frac areas for all experiments
    # choose plots. note that calculations must be performed in order to plot
    save_figs = True
    calc_area = False
    calc_length = True
    calc_angles = True
    calc_connect = False
    calc_flow = False
    
    fpath_out = '/Users/olerab/Documents/PhD/work_projects/geomechanical_modelling/roxol_analysis/'
    fname_out_len = 'TotalLength_RandomOrientation_Aniso.pdf'
    fname_out_area = 'TotalArea_AllOrientations_Aniso.pdf'
    fname_out_ang = 'MedianAngles_ligned_10ext_quantiles.pdf'#MedianAngles_RandomOrientations_Aniso.pdf'
    fname_out_connect = 'Connectivity_90deg_All_Aniso.pdf'
    fname_out_flow = 'Flow_AllOrientations_Aniso.pdf'
    
    #leg = ['random, 10 % extensional','random, 5 % extensional','random, isotropic']
    #colors = ['blue', 'red', 'black']
    #markers = ['o', 'P', 'd']
    leg = ['random, 10 % extensional','semialigned, 10 % extensional','aligned, 10 % extensional']
    colors = ['blue', 'orange', 'green']
    markers = ['o', 'x', 'v']

    figsizex_cm = 12.5
    figsizey_cm = 3.2
    
    
    
    if calc_length == True:
        fig1 = plt.figure(figsize=(figsizex_cm,figsizey_cm))
        ax1 = fig1.add_subplot(111)
        for i in range(0,len(frac_area)):
            ax1.set_xlabel("Computation Step", fontsize=12)
            ax1.set_ylabel("Total Fracture Length ($m$)", fontsize=12)
            line = ax1.plot(frac_length[i], lw=1, marker=markers[i], color = colors[i], markevery=2)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            plt.grid(True)
            ax1.legend(leg, loc='lower right')
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

    frac_spacing_init = 0.08
    
    if calc_angles == True:
        fig3, axs = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(figsizex_cm,figsizey_cm))
        for i in range(2,3):#len(segment_angle_data)):
            # Now switch to a more OO interface to exercise more features.
            
            avg_err_seg = segment_angle_data[i]
            # workaround for nan's from pumping steps (duplicate previous value)
            pump_ids = np.where(np.isnan(avg_err_seg))
            avg_err_seg[pump_ids[0]] = avg_err_seg[pump_ids[0]-1] 
            
            frac_len_by_spacing = [x / frac_spacing_init for x in frac_length[i]]
            
            #axs.plot(frac_len_by_spacing[:], avg_err_seg[:,2], lw=1, marker=markers[i], color = colors[i], linestyle = '-', markevery=1)
            axs.plot(frac_len_by_spacing[:], avg_err_seg[:,4], lw=1, marker=markers[i], color = colors[i], linestyle = '-', markevery=1)
            axs.vlines(frac_len_by_spacing[:],avg_err_seg[:,3],avg_err_seg[:,5],color = colors[i], lw = 4, alpha = None)
            axs.vlines(frac_len_by_spacing[:],avg_err_seg[:,2],avg_err_seg[:,3],color = colors[i], lw = 1.5, linestyle = 'dotted', alpha = None)
            axs.vlines(frac_len_by_spacing[:],avg_err_seg[:,5],avg_err_seg[:,6],color = colors[i], lw = 1.5, linestyle = 'dotted', alpha = None)
            
            #axs.errorbar(frac_len_by_spacing[:], avg_err_seg[:,4], ylolims = avg_err_seg[:,3], yuplims = avg_err_seg[:,5], lw=1, marker=markers[i], color = colors[i], linestyle = '-', markevery=1)
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
            ax4.set_ylabel("Normalized Expulsion", fontsize=12)
            plt.grid(True)
            ax4.set_ylim([0, 1])
            ax4.legend(leg, loc='upper left')
        plt.show()
        if save_figs == True:
            fig4.savefig(fpath_out+fname_out_flow)
            
        fig5, ax5 = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(figsizex_cm,figsizey_cm))
        for i in range(0,len(volFlow_out)):
            ax5.plot(volFlow_out_y[i]/volFlow_out[i], lw=1, marker=markers[i], color = colors[i], linestyle = '-', markevery=1)
            ax5.set_xlabel('Calculation Step', fontsize=12)
            ax5.set_ylabel("Normalized Expulsion in y direction", fontsize=12)
            plt.grid(True)
            ax5.set_ylim([0, 1])
            ax5.legend(leg, loc='upper left')
        plt.show()
        #if save_figs == True:
        #    fig5.savefig(fpath_out+fname_out_flow)
            
    if calc_connect == True:
        fig5 = plt.figure(figsize=(figsizex_cm,figsizey_cm))
        ax5 = fig5.add_subplot(111)
        for i in range(0,len(conn_per_line)):
            line5 = ax5.plot(conn_per_line[i], lw=1, marker=markers[i], color = colors[i], markevery=1)
            ax5.set_xlabel("Computation Step", fontsize=12)
            ax5.set_ylabel("Connections per line ($C_L$)", fontsize=12)
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            #plt.grid(True)
            ax5.set_ylim([0.75, 2])
            ax5.set_xlim([0.95, 5.05])
            #ax5.legend(leg, loc='upper left')
        plt.show()
        if save_figs == True:
            fig5.savefig(fpath_out+fname_out_connect) 