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

delete_isomer(0,'exomol_cutoff.txt')
delete_freq(4001,'HITRAN_data.txt')


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
