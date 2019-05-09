#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:27:20 2019

@author: olerab
"""
import matplotlib.pyplot as plt
from FracArea import *

def main():
    
    fpath_in_fracNodes = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/compressional/100perc/*_fracNodes.txt'
    fpath_in_dispVec = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/compressional/100perc/*_dispVec.txt'
    frac_area = FracArea(fpath_in_fracNodes, fpath_in_dispVec)
    return frac_area
    
    
if __name__ == "__main__":
    main()