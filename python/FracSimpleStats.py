#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 17:26:36 2019

@author: olerab
"""


# ------------------ simple analysis
paths = ['/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress/',
         '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/10perc/',
         '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/compressional/10perc/']
    
plt.figure(figsize=[20,20])
for path in paths:
    fname = path + 'crackPropagationData.csv'
    df=pd.read_csv(fname, sep=',',header=1)
    maxCrackID = list()
    
        
    plt.subplot(3,1,1)
    plt.ylabel('Total length (m)')
    plt.plot(df.values[:,-5])
    plt.legend(paths)
    plt.subplot(3,1,2)
    plt.ylabel('Average Angle of prop. crack elements (deg)')
    plt.plot(df.values[:,-1])
    plt.legend(paths)
    plt.subplot(3,1,3)
    plt.plot(df.values[:,-7])
    plt.ylabel('Number of propagated crack ends')
    plt.xlabel('Calculation Step')
    plt.legend(paths)