# This file will look at matched lines

import math

match_hitran = 'matched_hitran.txt'
match_exo = 'matched_exo.txt'

def get_intensity_hitran(line):

    intensity = float(line[16:26])

    return intensity

def get_hitran_energy(line):

    energy = float(line[47:54])

    return energy

def get_intensity_exo(line):

    intensity = float(line[16:26])

    return intensity

def get_exo_energy(line):

    energy = float(line[47:54])

    return energy

def magnitude(x):
    return int(math.log10(x))
def round_energy(x):
    return int(round(x))

# Store contents of ExoMol data (that is in HITRAN format from ExoCross)
with open(match_hitran, 'r') as in_fp:
    hitran_data = in_fp.readlines()

with open(match_exo,'r') as in_fp:
    exo_data = in_fp.readlines()

def check_intensity_energy(list1,list2):

    for i in range(len(list1)):
        for ii in range(len(list2)):
            if i == ii:
                if magnitude(get_intensity_hitran(list1[i]))==magnitude(get_intensity_exo(list2[ii])) and \
                                round(get_hitran_energy(list1[i]))==round(get_exo_energy(list2[ii])):
                    print("true")

    return

check_intensity_energy(hitran_data,exo_data)





