#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:39:29 2019

@author: olerab
"""
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy

reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName("/Volumes/PVPLAB2/OLE/roxol/RESULTS/45deg_semialigned/compressional/1perc/simulatorResult_2.vtu")
reader.Update()
data = reader.GetOutput()