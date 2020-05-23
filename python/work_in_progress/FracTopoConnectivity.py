#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 18:25:44 2020

@author: olerab
"""
# RESET ALL
from IPython import get_ipython
get_ipython().magic('reset -sf')

#import packages
import xml.etree.ElementTree as ET
import errno
import os
import os.path
import numpy as np
import glob

def FracTopoConnectivity(path_in, NX_init, NY_init):
               
    #path_in = '/Users/olerab/Documents/PhD/work_projects/geomechanical_modelling/roxol_analysis/isostress_backup/'
    filenames = sorted(glob.glob(path_in + '*.xml'))
    
    cnt = 0
    CL = []
    
    for name in filenames:             
        tree = ET.parse(name)
        root = tree.getroot() #creates the element tree from xml file
        crackResults = root[4][6]
        crackIndex = []
        
        
        # do everything for first result file
        for result in crackResults:
            crackIndex.append(int(result.get('index')))
        
        # find number of branches. initial only for first file
        NB = np.max(crackIndex)
        if cnt == 0:
            NB_init = NB
        
        NY = NY_init + NB - NB_init
        
        # calculate number of isolated nodes, lines and connections per line
        NI = 2*NB - 3*NY - 4*NX_init
        NL = 1/2*(NI + NY)
        CL.append(2*(NY + NX_init)/NL)

        cnt = cnt + 1

    return CL








"""
 ------- what needs to be done:




- IN GENERAL: THE WHOLE ANALYSIS SOFTWARE PACKAGE SHOULD BE WELDED INTO ONE FUNCTION/OBJECT
WHY? BECAUSE NOW FOR EVERY ANAYLYSIS WE REPEAT PARSING EVERY XML FILE, WHICH TAKES LOTS OF TIME.
GOAL SHOULD BE TO PARSE IT ONCE, RUN ALL CALCULATIONS AND BE DONE WITH IT.

ASK HAUKE IF THIS SHOULD BE DONE OBJECT BASED. GREAT OPPORTUNITY TO LEARN OBJECT-ORIENTED PROGRAMMING.

BUT: FINISH ALL ANALYSES FIRST!
"""