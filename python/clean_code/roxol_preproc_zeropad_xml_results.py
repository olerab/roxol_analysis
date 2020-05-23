#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 14:53:41 2020

This script takes roxol (or if edited any other) file of format result_number.xml
and zeropads the result number. This ensures correct order during analysis

@author: olerab
"""

import os
import os.path

def FracOrientation(path_in):
    
    pattern   = ".xml"

    # grab all filenames and zero-pad them to be able to sort them later
    for dirpath, dirnames, filenames in os.walk(path_in):
        for filename in [f for f in filenames if f.endswith(pattern)]:
            prefix, num = filename[:-4].split('_')
            num = num.zfill(4)
            new_filename = prefix + "_" + num + ".xml"
            os.rename(os.path.join(path_in, filename), os.path.join(path_in, new_filename))
            
    print("all xml result filenames in ", path_in, "zero-padded!")
            