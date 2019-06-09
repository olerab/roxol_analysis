#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:23:31 2019
Script to extract topology parameter omega (see Kobchenko et al 2013) from a roxol-generated fracture pattern
@author: olerab
"""
# for every result folder, chose the final result file, and read the fracture node array from the xml
# then identify dead ends and connections inside of a given area (i.e. excluding fractues connecting to the boundary/boundary domain (if applicable))
# and calculate omega according to Kobchenko et al 2013

from IPython import get_ipython
get_ipython().magic('reset -sf')

# ---- import modules
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import glob



paths_in = ['/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/extensional/5perc/']

for path_in in paths_in:
    names = glob.glob(path_in + '*.xml')
    name = names[-1] # pick last result file
    tree = ET.parse(name)
    root = tree.getroot() #creates the element tree from xml file
    
    crackResults = root[4][6]
    numcracks = int(crackResults.get('nrCracks'))
    nodeData_dict_noends = {}
    nodeData_dict_ends = list()
    for j in range (0,numcracks):
        nodeData_str = crackResults[j][0].text.replace(' 0\n', '\n')
        nodeData_lst = nodeData_str.split('\n')
        nodeData_lst[-1] = nodeData_lst[-1][:-2] # erase last zero value

        nodeData_array = np.zeros([len(nodeData_lst), 2])
    
        for i in range(0,len(nodeData_lst)):
            nodeData_array[i] = np.fromstring(nodeData_lst[i],sep =' ')
            nodeData_dict_noends[j] = nodeData_array[1:-2]
            nodeData_dict_ends.append(nodeData_array[0])
            nodeData_dict_ends.append(nodeData_array[0])
            
#    for k in range (0,numcracks):
        