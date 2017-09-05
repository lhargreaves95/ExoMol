#!/usr/bin/env python

num_of_lines = 10000

filename= '/Users/laurahargreaves/Documents/ExoMol/HCN_ExoMol_HITRAN_03.dat'

with open(filename) as fin:
    fout = open('output0.txt',"w")
    for i,line in enumerate(fin):
        fout.write(line)
        if (i+1)%num_of_lines == 0:
            fout.close()
            fout = open("output%d.txt"%(i/num_of_lines+1),"w")

    fout.close()

smallFile = None


