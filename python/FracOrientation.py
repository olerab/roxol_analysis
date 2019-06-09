#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:37:43 2019

@author: olerab
"""

#from IPython import get_ipython
#get_ipython().magic('reset -sf')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import glob
from scipy import stats

def SegmentAngle(node1,node2):
    #calculates positive angle (0,180) between two fracture nodes in 2D space with respect to the vertical axis. Nodes should be given as numpy array or list and as x,y pairs
    seg = np.array(node1)-np.array(node2)
    hor_ang = np.arctan2(seg[1],seg[0]) * 180 /np.pi
    
    if hor_ang > 90:
        seg_ang = -180 + hor_ang
    elif hor_ang < -90:
        seg_ang = 180 + hor_ang
    else:
        seg_ang = hor_ang
    
    return seg_ang




def FracOrientation(path_in):
    seg_angles_all = {}
    avg_angles_all = {}
    cnt = 0
    
    names = glob.glob(path_in + '*.xml')
    # for every result file, read the fracture node array from result filess, 
    # and calculate the angle of the (1) last segment added on each side and (2) average segment angle
    for name in names:
        tree = ET.parse(name)
        root = tree.getroot() #creates the element tree from xml file
    
        crackResults = root[4][6]
        numcracks = int(crackResults.get('nrCracks'))
        angles_end = np.zeros([numcracks,2])
        angles_avg = np.zeros([numcracks,1])
        
        # convert string data from xml to numerical nodes
        
        for j in range (0,numcracks):
            nodeData_str = crackResults[j][0].text.replace(' 0\n', '\n')
            nodeData_lst = nodeData_str.split('\n')
            nodeData_lst[-1] = nodeData_lst[-1][:-2] # erase last zero value
    
            nodeData_array = np.zeros([len(nodeData_lst), 2])
    
            for i in range(0,len(nodeData_lst)):
                nodeData_array[i] = np.fromstring(nodeData_lst[i],sep =' ')
            
            ang1 = SegmentAngle(nodeData_array[0],nodeData_array[2])
            ang2 = SegmentAngle(nodeData_array[-2],nodeData_array[-1])
            angles_end[j] = [ang1, ang2]
            angles_avg[j] = SegmentAngle(nodeData_array[0],nodeData_array[-1])
        
        # find ends that have not grown and set then to NaN
        angles_end = np.array(angles_end.flatten())
        if cnt == 1:
            angle_end_prev_step = seg_angles_all[0]
        if cnt > 0:
            if len(angles_end) == len(seg_angles_all[cnt-1]):
                bool_NoGrowth = np.equal(angle_end_prev_step, angles_end)
                angle_end_prev_step = angles_end
                angles_end = np.where(bool_NoGrowth == True, np.nan, angles_end)     
            else:
                raise Exception('ERROR, NUMBERS OF FRACURTES BETWEEN STEPS HAVE TO MATCH!')
                #angles_end = 
        seg_angles_all[cnt] = angles_end
        avg_angles_all[cnt] = angles_avg
        cnt += 1
    
    
    # calculate angle to initial orientation for each step
    seg_angles_DiffInit = {}
    seg_angles_DiffAvg = {}
    
    
    # calculate average angles in values > zero (i.e. fracture dip)
    
    abs_seg_angles_all = {}
    avg_err_seg = np.empty([len(seg_angles_all),3])
    avg_err_all = np.empty([len(seg_angles_all),1])
    for p in range (0, len(avg_err_seg)):
        abs_seg_angles_all[p] = np.abs(seg_angles_all[p])
        abs_avg_angles_all = np.abs(avg_angles_all[p])

        avg_err_seg[p,:] = [np.nanmean(abs_seg_angles_all[p]), np.nanstd(abs_seg_angles_all[p]), np.nanmedian(abs_seg_angles_all[p])]
        avg_err_all[p] = np.nanmean(abs_avg_angles_all)
    
    #prepare boxplot data 
    labels, data = abs_seg_angles_all.keys(), abs_seg_angles_all.values()
    fig, axs = plt.subplots(nrows=1, ncols=1, sharex=True)
    axs.errorbar(np.linspace(1,len(avg_err_seg),len(avg_err_seg)), avg_err_seg[:,0], yerr=avg_err_seg[:,1], fmt='o')
    #axs.boxplot(data)
    #axs.set_xticks(range(1, len(labels) + 1), labels)
    axs.set_title(path_in[35:], fontsize=18)
    axs.set_xlabel("Simulation Step", fontsize=18)
    axs.set_ylabel("Angle from horizontal (deg)", fontsize=18)
    axs.set_ylim([0, 90])
    #ax.set_title('Vert. symmetric')
        

    # ------------------ simple analysis
    #paths = ['/Volumes/PVPLAB2/OLE/roxol/RESULTS/15deg_aligned/isostress/',
    #         '/Volumes/PVPLAB2/OLE/roxol/RESULTS/15deg_aligned/extensional/10perc/',
    #         '/Volumes/PVPLAB2/OLE/roxol/RESULTS/15deg_aligned/compressional/10perc/',
    #         '/Volumes/PVPLAB2/OLE/roxol/RESULTS/15deg_aligned/unconfined/']
    
    #plt.figure(figsize=[20,20])
    #for path in paths:
    #    fname = path + 'crackPropagationData.csv'
    #    df=pd.read_csv(fname, sep=',',header=1)
    #    maxCrackID = list()
    
        
    #    plt.subplot(3,1,1)
    #    plt.ylabel('Total length (m)')
    #    plt.plot(df.values[:,-5])
    #    plt.legend(paths)
    #    plt.subplot(3,1,2)
    #    plt.ylabel('Average Angle of prop. crack elements (deg)')
    #    plt.plot(df.values[:,-1])
    #    plt.legend(paths)
    #    plt.subplot(3,1,3)
    #    plt.plot(df.values[:,-7])
    #    plt.ylabel('Number of propagated crack ends')
    #    plt.xlabel('Calculation Step')
    #    plt.legend(paths)
    return avg_err_seg
