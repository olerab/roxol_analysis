# -*- coding: utf-8 -*-
"""
script extracting fracture node paths  from roxol(TM) result xml files

take a look here: https://docs.python.org/3/library/xml.etree.elementtree.html
and here: https://www.datacamp.com/community/tutorials/python-xml-elementtree
"""
# RESET ALL
from IPython import get_ipython
get_ipython().magic('reset -sf')

#import packages
import xml.etree.ElementTree as ET
import errno
import os
import os.path

#target = 'displacementVectors'
target = 'fracNodes'

files = []
start_dir = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random'
pattern   = "*.xml"

for dirpath, dirnames, filenames in os.walk(start_dir):
    for filename in [f for f in filenames if f.endswith(".xml")]:
        files.extend([os.path.join(dirpath, filename)])

#fpath_in = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/unconfined/*.xml'
#files = glob.glob(fpath_in)

min_x = -0.25
max_x = 0.25
min_y = -0.25
max_y = 0.25

# --------- loop through file names, build xml tree and extract nodes or displacement vectors from the correct position within root object/element
for name in files:
    try:
        tree = ET.parse(name)
        root = tree.getroot() #creates the element tree from xml file
        crackResults = root[4][6]
        numcracks = int(crackResults.get('nrCracks'))
        if target == 'fracNodes':
            fname_out = name[:-4] + '_fracNodes.txt'
            fid = open(fname_out, "w")
            print('writing fracture nodes to file: ', fname_out)
            
            for i in range(numcracks):
                crackNodes = crackResults[i][0].text
                crackNodes = crackNodes.replace('0\n', '')[:-2] + '\n'
                crackNodes = crackNodes.replace(' ', '\t')
                fid.write(crackNodes)      
        
        elif target == 'displacementVectors':
            fname_out = name[:-4] + '_dispVec.txt'
            fid = open(fname_out, "w")
            print('writing fracture displacement vectors to file: ', fname_out)
            
            for i in range(numcracks):
                dispVec = crackResults[i][1].text
                dispVec = dispVec.replace('0\n', '')[:-2] + '\n'
                dispVec = dispVec.replace('0;', '')
                dispVec = dispVec.replace(' ', '\t')
                fid.write(dispVec)
        else:
            raise Exception('No extraction target set - choose "fracNodes" or "displacementVectors"')
            
            
            
        #write edge points to center fracture network
        #if target == 'fracNodes':
            #fid.write('%5.2f\t%5.2f\n' % (min_x, min_y))
            #fid.write('%5.2f\t%5.2f\n' % (max_x, max_y))
        
        fid = fid.close()
    
        
    
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise





#fname_in = 'simulatorResult_0.xml'

#fpath_out = fpath_in
#fname_out = fname_in[:-4] + '.txt'

#file_in = fpath_in + fname_in
#file_out = fpath_out + fname_out




#playing around with the hierarchial XML data



# display attributes of each crack
#for crack in root.iter('crack'):
 #   print(crack.attrib)

#for crackResults in root.iter('crackResults'):
#    print(crackResults.get('nrCracks'))


# use xpath expressions to navigate to the cracks, then print the coordinate subelement for all cracks
#for crack in root.findall("./results/crackResults/crack"):
#    print(coordinates.text)
    
# 
# find number of cracks and loop through all cracks to display crack node coordinates

#for i in range(numcracks):
#    print(crackResults[i][0].text)
    
    
# write nodes for each crack into new variable tand use it to write FN node file
    
