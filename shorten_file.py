# This script will be used to shorten file used in the matching exercise

def get_freq_exo(line):

    """
    Function stores frequency
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: frequency
    """
    frequency=line[7:15]

    return float(frequency)

def get_freq_hitran(line):

    """
    Function stores frequency
    :param line: input line from file that is in exact HITRAN format
    :return: frequency
    """
    frequency = line[3:15]

    return float(frequency)

def get_isomer_exo(line):

    """

    :param line:
    :return:
    """

    isomer_no = int(line[90:91])

    return isomer_no

def get_lower_parity_hitran(line):

    """
    Function gets lower parity of line
    :param line: input line from file that is in exact HITRAN format
    :return: parity of lower state
    """
    lower_parity= str(line[121])

    return lower_parity

def get_quantum_number_n_hitran(line):

    """
    Function gets lowers quantum numbers n1",n2",n3",n4"
    :param line: input line that is in exact HITRAN format
    :return: lower and upper quantum numbers n1'/",n2'/",n3'/",n4'/"
    """

    # note to self need to account for blanjs

    upper = []
    lower = []

    QN_upper = line[75:82]
    QN_lower = line[90:97]

    upper_line=QN_upper.split()
    for c in upper_line:
        upper.append(int(c))

    lower_line=QN_lower.split()
    for c in lower_line:
        lower.append(int(c))

    return upper, lower

def delete_freq(cutoff,file):
    new_file = []
    output = 'new_HITRAN.txt'
    with open(file, 'r') as in_fp:
        line = in_fp.readline()
        while(line):
            if get_freq_hitran(line) < cutoff:
                print("append")
                new_file.append(line)
            line=in_fp.readline()

    with open(output,'w') as in_fp:
        for row in new_file:
            in_fp.write(row)
    return output

def delete_isomer(isomer,file):
    new_file=[]
    output = 'new_exomol.txt'
    with open(file, 'r') as in_fp:
        line = in_fp.readline()
        while (line):
            if get_isomer_exo(line) == isomer:
                print("append")
                new_file.append(line)
            line = in_fp.readline()

    with open(output, 'w') as in_fp:
        for row in new_file:
            in_fp.write(row)
    return output

def seperate_lines(file):

    with_parity=[]
    no_parity=[]

    output1 = 'HITRAN_parity.txt'
    output2 = 'HITRAN_no_parity.txt'

    with open(file,'r') as in_fp:
        line = in_fp.readline()
        while(line):
            if get_lower_parity_hitran(line) == 'e' or get_lower_parity_hitran(line) == 'f':
                with_parity.append(line)
            else:
                no_parity.append(line)
            line=in_fp.readline()

    with open(output1, 'w') as in_fp:
        for row in with_parity:
            in_fp.write(row)

    with open(output2, 'w') as in_fp:
        for row in no_parity:
            in_fp.write(row)

    return output1, output2

def when_l_is_zero(file):

    l_is_zero=[]
    l_is_not=[]

    output1 ='HITRAN_l_0.txt'
    output2 = 'HITRAN_l.txt'

    with open(file,'r') as in_fp:
        line = in_fp.readline()
        while(line):
            upper, lower = get_quantum_number_n_hitran(line)
            if lower[2]== 0:
                l_is_zero.append(line)
            else:
                l_is_not.append(line)
            line = in_fp.readline()

    with open(output1, 'w') as in_fp:
        for row in l_is_zero:
            in_fp.write(row)

    with open(output2, 'w') as in_fp:
        for row in l_is_not:
            in_fp.write(row)

    return output1, output2

def sort_file(file):
    column = []
    with open(file,'r') as in_fp:
        lines = in_fp.readlines()
    for line in lines:
        newline = line.split()
    print(lines)

    return lines



# delete_isomer(0,'exomol_cutoff.txt')
# delete_freq(4001,'HITRAN_data.txt')
# seperate_lines('new_HITRAN.txt')
#when_l_is_zero('HITRAN_no_parity.txt')

#
# def print_line(file):
#     with open(file, 'r') as in_fp:
#         line = in_fp.readline()
#         while(line):
#             print(line[90:110])
#             line= in_fp.readline()
#     return line
#
#
# print_line('exomol_test.txt')
