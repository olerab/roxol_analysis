# -*- coding: utf-8 -*-
"""
script extracting fracture node paths  from roxol(TM) result xml files

take a look here: https://docs.python.org/3/library/xml.etree.elementtree.html
and here: https://www.datacamp.com/community/tutorials/python-xml-elementtree
"""
import xml.etree.ElementTree as ET

# specify and read xml file






fpath_in = '/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/unconfined/'
fname_in = 'simulatorResult_0.xml'

fpath_out = fpath_in
fname_out = fname_in[:-4] + '.txt'

file_in = fpath_in + fname_in
file_out = fpath_out + fname_out

tree = ET.parse(file_in)
root = tree.getroot() #creates the element tree


#playing around with the hierarchial XML data

# print all elements in the tree according to hierarchy
[elem.tag for elem in root.iter()]

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
numcracks = int(crackResults.get('nrCracks'))
#for i in range(numcracks):
#    print(crackResults[i][0].text)
    
    
# write nodes for each crack into new variable tand use it to write FN node file
    
fid = open(file_out, "w")
    
for i in range(numcracks):
    crackNodes = crackResults[i][0].text
    crackNodes = crackNodes.replace('0\n', '')[:-2] + '\n'
    crackNodes = crackNodes.replace(' ', '\t')
    fid.write(crackNodes)
    
fid = fid.close()