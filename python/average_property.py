#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:56:16 2019

@author: olerab
"""
# RESET ALL
from IPython import get_ipython
get_ipython().magic('reset -sf')

#import packages
import xml.etree.ElementTree as ET
import errno
import glob
import numpy as np
import matplotlib.pyplot as plt

target = 'porepressure'
# define realistic maximum and minimum to avoid numerical outliers skewing the result
target_max = 8e+7
target_min = 0

files = []
start_dir = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress'
pattern   = ".xml"


if target == 'porepressure':
    target_idx = 16

fpath = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress/*xml'
files = glob.glob(fpath)

avgprop = np.zeros([len(files),])
cnt = 0
for name in files:
    try:
        tree = ET.parse(name)
        root = tree.getroot() #creates the element tree from xml file
        
        nrNodes = int(root[4][0].get('nrNodes'))
        nodeResults = root[4][0][target_idx].text
        #prop = np.empty([nrNodes,1])
        
        prop = np.fromstring(nodeResults,sep ='\n')
        #prop = np.where(prop>target_max, np.nan, prop)
        prop = np.where(prop<target_min, np.nan, prop)
        avgprop[cnt] = np.nanmean(prop)/nrNodes
        cnt += 1
        
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise