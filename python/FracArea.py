# -*- coding: utf-8 -*-
# RESET ALL
#from IPython import get_ipython
#get_ipython().magic('reset -sf')
import glob
import errno
import numpy as np
import matplotlib.pyplot as plt


def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


def FracArea(fpath_in_fracNodes, fpath_in_dispVec):    
    """
    Created on Tue May  7 15:22:48 2019
    
    calculates area of polygons created from combined roxol crack nodes and displacement vectors,
    i.e. in effect fracture area
    
    @author: olerab
    """   
    files_fracNodes = glob.glob(fpath_in_fracNodes)
    files_dispVec = glob.glob(fpath_in_dispVec)
    
    if len(files_fracNodes)!=len(files_dispVec):
        raise Exception('Error, need same number of files containing "fracNodes" and "displacementVectors"')
    
    cnt = 0
    frac_area_lib = {}
    frac_area = list()
    frac_area_max = list()
    frac_area_min = list()
    frac_area_avg = list()
    frac_area_med = list()
    frac_area_std = list()
    # read frac nodes and displacement vectors, and  store them as doubles
            #create figure for boxplots
    fig0 = plt.figure(figsize=(10,5))
    ax0 = fig0.add_subplot(111)
    for cnt in range (0,len(files_fracNodes)):
        #fnodes = np.genfromtxt(fracNodeFile, delimiter = "\t")
        file_fracNodes = open(files_fracNodes[cnt],'r')
        i = 0
        fracNodes = {}
        for line in file_fracNodes:
            data = line.split()
            fracNodes[i] = np.array(np.float_(data))
            i += 1
        file_fracNodes.close()
            
        #fnodes = np.genfromtxt(fracNodeFile, delimiter = "\t")
        file_dispVec = open(files_dispVec[cnt],'r')
        i = 0
        dispVec = {}
        for line in file_dispVec:
            data = line.split()
            dispVec[i] = np.array(np.float_(data))
            i += 1
        file_dispVec.close()
    
            
        # build polygon nodes by combining frac nodes and displacement vectors
        polyNodes = {}
        polyarea = list()
     
        #extract pairwise displacement vectors
        

    
        for j in range(0,len(fracNodes)):
            disp1 = np.empty_like(fracNodes[j])
            disp2 = np.empty_like(fracNodes[j])
            disp1[0::2] = dispVec[j][0::4]
            disp1[1::2] = dispVec[j][1::4]
            disp2[0::2] = dispVec[j][2::4]
            disp2[1::2] = dispVec[j][3::4]
            
            #for k in range (0,len(fracNodes[j])):
            polyNodes[j] = np.append(fracNodes[j] + disp1, np.flip(fracNodes[j] + disp2))
            polyNodesx = np.append(polyNodes[j][0:len(fracNodes[j]):2], polyNodes[j][len(fracNodes[j])+1::2])
            polyNodesy = np.append(polyNodes[j][1:len(fracNodes[j]):2], polyNodes[j][len(fracNodes[j])::2])
            polyarea.append(PolyArea(polyNodesx,polyNodesy))
            # plot polygons
            # plt.show() # if you need...
            #plt.plot(polyNodesx,polyNodesy)
        
        
        
        
        frac_area_max.append(np.max(polyarea))
        frac_area_min.append(np.min(polyarea))
        frac_area_avg.append(np.mean(polyarea))
        frac_area_med.append(np.median(polyarea))
        frac_area_std.append(np.std(polyarea))
        frac_area.append(np.sum(polyarea))
        frac_area_lib[cnt] = frac_area
        
        
        #line, = ax2.plot(frac_area, lw=2)
        if cnt % 5 == 0:
            ax0.boxplot(frac_area_avg, positions = [float(cnt)/5])
            ax0.set_title(fpath_in_fracNodes[35:-16], fontsize=18)
            ax0.set_xlabel("Simulation Step", fontsize=18)
            ax0.set_ylabel("Mean Fracture Area", fontsize=18)
            ax0.set_xlim(-0.5, cnt/5+0.5)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.show()
    
    
    
    #plotting
    
    # -------------------- total fracture area at each step
    fig1 = plt.figure(figsize=(10,5))
    ax1 = fig1.add_subplot(111)
    line, = ax1.plot(frac_area, lw=2, marker='o', color='mediumvioletred')

    ax1.set_title(fpath_in_fracNodes[35:-16], fontsize=18)
    ax1.set_xlabel("Simulation Step", fontsize=18)
    ax1.set_ylabel("Total Fracture Area", fontsize=18)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.grid(True)
    plt.show()
    
    # --------------------- max, min, mean, standard deviation at each step
    fig2 = plt.figure(figsize=(10,5))
    ax2 = fig2.add_subplot(111)
    #line, = ax2.plot(frac_area, lw=2)
    
    ax2.errorbar(np.linspace(0,len(frac_area_avg),len(frac_area_avg)),frac_area_avg, yerr=frac_area_std, fmt='o', color='mediumvioletred')

    ax2.set_title(fpath_in_fracNodes[35:-16], fontsize=18)
    ax2.set_xlabel("Simulation Step", fontsize=18)
    ax2.set_ylabel("Mean Fracture Area", fontsize=18)
    
    ax2.plot(frac_area_med, lw=2, marker='o', color='red')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.grid(True)
    plt.show()
    
    
    
    
    
    # return fracture area value
    return frac_area


    
    
    
    
    
    
    
    
    
    
    
    
