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

def flow_orientation_tensor(volFlowx, volFlowy):
    """ calculate orientation tensor for flow
        build tensor product of all 2D flow vectors, then calculate eigenvalues & vector
    """
    a11 = np.abs(volFlowx * volFlowx)
    a22 = np.abs(volFlowy * volFlowy)
    a12 = np.abs(volFlowx * volFlowy)
    Tensor = np.empty([2, 2])
    
    for i in range (0,len(a11)):
        T = np.array([[a11[i], a12[i]],[a12[i], a22[i]]])
        Tensor = Tensor + np.linalg.norm(T)
        
        Tensor = Tensor/len(a11+1)
        
        eigvalue,eigvector=np.linalg.eig(Tensor)
        
        idx = eigvalue.argsort()[::-1]
        return eigvalue[idx],eigvector[:,idx]
    

def flow_analysis(fpath_in,flow_max, flow_min, nstep, calcmode):
# =============================================================================
# Input parameters
#   fpath_in: path to roxol result xml files
#   flow_max/min: cut-off values for volume flow (i.e. defining outliers)
#   nstep: flow step interval (every nth result file represents a fluid flow step)
#   calcmode: use elements or nodes for calculations (default is nodes)
#    
# =============================================================================
    
    
    # volume flow as x,y,z is stored in the xml tree root[4][0][target_idx=18 for nodes, 9 for elements]
    target_idx = 18
    target_idx_el = 9
    
    modeldomain_extent = 0.22 # magnitude of extent of boundary from 0,0
    modeldomain_nodespacing = 0.00125
    
    #choose file path
    fpath = fpath_in+ '*.xml'
    files = glob.glob(fpath)
    
    flowsteps = int(np.floor(len(files)/nstep))
    
    cnt = 0
    outflow = np.zeros(flowsteps+1)
    outflow_x = np.zeros(flowsteps+1)
    outflow_y = np.zeros(flowsteps+1)
    
    for i in range(0,flowsteps):
        try:
            name = files[1+i*7]
            print(name)
            tree = ET.parse(name)
            root = tree.getroot() #creates the element tree from xml file
            
            
            #prop = np.empty([nrNodes,1])
            
            if calcmode == 'nodes':
                
                nrNodes = int(root[4][0].get('nrNodes'))
                nodeResults = root[4][0][target_idx].text
                
                volFlow = np.fromstring(nodeResults,sep ='\n')
                volFlow = np.where(volFlow>flow_max, np.nan, volFlow)
                volFlow = np.where(volFlow<flow_min, np.nan, volFlow)
                volFlowx =  volFlow[0::3]
                volFlowy =  volFlow[1::3]
                volFlowLen = np.sqrt(volFlowx ** 2 + volFlowy ** 2)
                volFlowDir = np.arctan2(volFlowy, volFlowx) * 180 / np.pi
                
                # find node coordinates along boundary between model and boundary domain (0.22 x 0.22 meters about 0,0)
                # NOTE: the following proceduce only works because the boundary domain has an irregularly spaced grid, while the model domain is regularly spaced!
                # for more complicated cases, you will need to find the coordinates differently
                
                nodeCoordinates_txt = root[4][0][0].text
                nodeCoordinates = np.fromstring(nodeCoordinates_txt,sep ='\n')
                nodeCoordinatesx = nodeCoordinates[0::2]
                nodeCoordinatesy = nodeCoordinates[1::2]
                
                # find boolian picking nodes along the boundary of the (inner) model domain
                md_xbound_0 = nodeCoordinatesx == -modeldomain_extent + modeldomain_nodespacing
                md_xbound_1 = nodeCoordinatesx == modeldomain_extent - modeldomain_nodespacing
                md_ybound_0 = nodeCoordinatesy == -modeldomain_extent + modeldomain_nodespacing
                md_ybound_1 = nodeCoordinatesy == modeldomain_extent - modeldomain_nodespacing
                
                
                outflow_x[i] = np.nansum(volFlowLen[md_xbound_0]) + np.nansum(volFlowLen[md_xbound_1])
                outflow_y[i] = np.nansum(volFlowLen[md_ybound_0]) + np.nansum(volFlowLen[md_ybound_1])
                outflow[i] = np.nansum(volFlowLen[md_xbound_0]) + np.nansum(volFlowLen[md_xbound_1]) + np.nansum(volFlowLen[md_ybound_0]) + np.nansum(volFlowLen[md_ybound_1]) 
                
                #eigval, eigvec = flow_orientation_tensor(volFlowx, volFlowy)
    
            
            # same flor elements, but picking only fractures. we do this assuming the matrix is impermeable and only fractures contribute
            elif calcmode == 'elements':
                nrElements = int(root[4][1].get('nrElements'))
                elementResults = root[4][1][target_idx_el].text
                
                volFlow = np.fromstring(elementResults,sep ='\n')
                volFlow = np.where(volFlow>flow_max, np.nan, volFlow)
                volFlow = np.where(volFlow<flow_min, np.nan, volFlow)
                
                # select by material
                elementMaterial = root[4][1][10].text     
                mat = np.fromstring(elementMaterial,sep ='\n')
                mat_crack = mat==3
                
                #volFlow = np.select(mat_crack,volFlow)
                
                volFlowx =  volFlow[0::3]
                volFlowy =  volFlow[1::3]
                
                volFlowx = volFlowx[mat_crack]
                volFlowy = volFlowy[mat_crack]
                
                volFlowLen = np.sqrt(volFlowx ** 2 + volFlowy ** 2)
                volFlowDir = np.arctan2(volFlowy, volFlowx) * 180 / np.pi
                

            
            plt.hist(volFlowDir)
            plt.plot(volFlowLen[md_ybound_0])
            plt.plot(volFlowLen[md_ybound_1])
            plt.plot(volFlowLen[md_xbound_0])
            plt.plot(volFlowLen[md_xbound_1])
            
            
            cnt += 1
           
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    
    return outflow, outflow_x, outflow_y              
    