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

def SegmentLength(x1,x2,y1,y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)


def FracArea(fpath_in_fracNodes, fpath_in_dispVec, plotting = False, norm_by_len = False):    
    """
    Created on Tue May  7 15:22:48 2019
    
    calculates area of polygons created from combined roxol crack nodes and displacement vectors,
    i.e. in effect fracture area
    
    inputs: 
        fpath_in_fracNodes: file path for fracture nodes in format (x0 y0 x1 y1 ... for node coordinates) per fracture, and of the form " path + '*_fracNodes.txt' "
        fpath_in_dispVec:   file path for fracture displacement Vectors in format (dx00 dy00 dx01 dy01 dx10 dy10 dx11 dy11 ... for bidirectional node displacement) per fracture, and of the form " path + '*_dispVec.txt' "
        plotting: True/False input. displays plots or not. Standard: False
        norm_by_len = True/False input. normalizes fracture area by respective fracture length or not. Standard: True
    
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
    frac_length = list()
    # read frac nodes and displacement vectors, and  store them as doubles
            #create figure for boxplots

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
    
        # calculate length of each fracture in a result step to normalize area at a later stage 
        fraclen = list()    
        for i in range(0,len(fracNodes)):
            segments = list()
            for k in range(0,int(len(fracNodes[i])/2-2)):
                segments.append(SegmentLength(fracNodes[i][2*k],fracNodes[i][2*k+2],fracNodes[i][2*k+1],fracNodes[i][2*k+3]))
            
            fraclen.append(np.sum(segments))
        
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
            
            # calculate polunomial area, normalizeby the length (if desired)
            polyarea.append(PolyArea(polyNodesx,polyNodesy))
            
            # plot polygons
            # if you need...
            #plt.plot(polyNodesx,polyNodesy)
        
        #plt.show()
        
        frac_area_max.append(np.max(polyarea))
        frac_area_min.append(np.min(polyarea))
        frac_area_avg.append(np.mean(polyarea))
        frac_area_med.append(np.median(polyarea))
        frac_area_std.append(np.std(polyarea))
        if norm_by_len == True:
            frac_area.append(np.sum(polyarea)/np.sum(fraclen))
        else:
            frac_area.append(np.sum(polyarea))
        frac_area_lib[cnt] = frac_area
        frac_length.append(np.sum(fraclen))
    
    
    #plotting
    if plotting == True:
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
        fig1.savefig(fpath_in_fracNodes[:-15] + 'plot_TotalFracArea.png')
        
        # --------------------- max, min, mean, standard deviation at each step
        fig2 = plt.figure(figsize=(10,5))
        ax2 = fig2.add_subplot(111)
        #line, = ax2.plot(frac_area, lw=2)
        ax2.errorbar(np.linspace(0,len(frac_area_avg)-1,len(frac_area_avg)),frac_area_avg, yerr=[frac_area_min, frac_area_max], fmt='o', color='mediumvioletred')
    
        ax2.set_title(fpath_in_fracNodes[35:-16], fontsize=18)
        ax2.set_xlabel("Simulation Step", fontsize=18)
        ax2.set_ylabel("Mean Fracture Area", fontsize=18)
        
        ax2.plot(frac_area_med, lw=2, marker='o', color='red')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.grid(True)
        plt.show()
        fig2.savefig(fpath_in_dispVec[:-13] + 'plot_MeanMaxFracArea.png')
    else:
        print('PLOTTING DISABLED. use arg plotting = True to show plots')
    

    
    # return fracture area value
    return frac_area, frac_length


    
    
    
    
    
    
    
    
    
    
    
    
