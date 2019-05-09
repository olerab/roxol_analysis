# -*- coding: utf-8 -*-
# RESET ALL
#from IPython import get_ipython
#get_ipython().magic('reset -sf')

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))




def FN_area(fpath_in_fracNodes, fpath_in_dispVec):    
"""
Created on Tue May  7 15:22:48 2019

calculates area of polygons created from combined roxol crack nodes and displacement vectors,
i.e. in effect fracture area

@author: olerab
"""
        
    fpath_in_fracNodes = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress/*_fracNodes.txt'
    fpath_in_dispVec = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/isostress/*_dispVec.txt'
    
    files_fracNodes = glob.glob(fpath_in_fracNodes)
    files_dispVec = glob.glob(fpath_in_dispVec)
    
    if len(files_fracNodes)!=len(files_dispVec):
        raise Exception('Error, need same number of files containing "fracNodes" and "displacementVectors"')
    
    
    cnt = 0
    FracArea = list()
    # read frac nodes and displacement vectors, and  store them as doubles
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
    
        #plt.figure()
    
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
            #plt.plot(polyNodesx,polyNodesy)
        
        # plot polygons
        # plt.show() # if you need...
        FracArea.append(np.sum(polyarea))
        return FracArea


    
    
    
    
    
    
    
    
    
    
    
    
