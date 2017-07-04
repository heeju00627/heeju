# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 04:00:15 2017

@author: heeju
"""

import os
import sys

path_dir = sys.argv[1]
file_list = os.listdir(path_dir)
fna_list = []

## .fna 파일만
for file in file_list:
    ext = os.path.splitext(file)[-1]
    if (ext == '.fna'):
        fna_list.append(file)

fna_list.sort()
print(fna_list)

for file in fna_list:
    with open(file, 'r') as contig:
        name = contig.readline()
        print(name)
        ##k = int(size.split(" ")[0])
        #l = int(size.split(" ")[1])
        #n = int(bm.readline().split("%")[1])
        
        #for i in range(n):
        #    cord = bm.readline().split("\n")[0]
        #    cord = cord.split("\t")
        #    x.append(int(cord[1]))
        #    y.append(int(cord[2]))