#!/usr/bin/env python

from fortranformat import FortranRecordWriter

import testing_ExoMol as tE


# Filenames in HITRAN format
filename_hitran = '/Users/laurahargreaves/Documents/ExoMol/new_HITRAN.txt'
filename_exomol = '/Users/laurahargreaves/Documents/ExoMol/new_exomol.txt'

output_final= 'new_file.txt'
output_unmatched = 'unmatched.txt'

# Store contents of ExoMol data (that is in HITRAN format from ExoCross)
with open(filename_hitran, 'r') as in_fp:
    hitran_data = in_fp.readlines()


def get_freq_hitran(line):

    """
    Function stores frequency
    :param line: input line from file that is in exact HITRAN format
    :return: frequency
    """
    frequency = line[3:15]


    return float(frequency)

def get_freq_exo(line):

    """
    Function stores frequency
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: frequency
    """
    frequency=line[3:15]

    return float(frequency)

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

def get_quantum_number_n_exo(line):

    """
    Function gets lowers quantum numbers n1",n2",n3",n4"
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return:lower and upper quantum numbers n1'/",n2'/",n3'/",n4'/"
    """
    upper=[]
    lower=[]

    QN_upper =line[73:87]
    upper_line=QN_upper.split()
    for c in upper_line:
        upper.append(int(c))

    QN_lower = line[93:107]
    lower_line = QN_lower.split()
    for c in lower_line:
        lower.append(int(c))


    return upper, lower

def get_branch_hitran(line):

    """
    Function gets branch type
    :param line: input line that is in exact HITRAN format
    :return: branch type(P,Q,R)
    """
    branch = line[117]


    return str(branch)

def get_j_value_exo(line):

    """
    Function gets upper and lower J values
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: upper and lower J quantum numbers
    """
    try:
        upper_j=line[112:114]
        lower_j=line[123:125]
        return int(lower_j), int(upper_j)
    except ValueError:
        pass


def get_J_value_hitran(line):

    """
    Function gets upper and lower J values
    :param line: input line from file that is in exact HITRAN format
    :return: upper and lower J values
    """

    branch = get_branch_hitran(line) # To determine selection rules

    lower_J = int(line[119]+line[120])

    if branch == 'P':
        upper_J=lower_J-1
    elif branch == 'R':
        upper_J=lower_J+1
    else:
        upper_J=lower_J

    return int(lower_J), int(upper_J)

def get_lower_parity_hitran(line):

    """
    Function gets lower parity of line
    :param line: input line from file that is in exact HITRAN format
    :return: parity of lower state
    """
    parity= str(line[121])

    if parity == 'f':
        lower_parity = 'f'
    else:
        lower_parity='e'


    return lower_parity

def get_upper_parity_hitran(lower_parity,line):

    """
    Function gets upper parity of line
    :param line: input line from file that is in exact HITRAN format
    :param lower_parity: parity of lower state
    :return: parity of upper state
    """

    # get type of branch to determine selection rules
    branch = get_branch_hitran(line)

    # Selection rules
    if branch == 'Q' and lower_parity == 'f':
        upper_parity = 'e'

    elif branch == 'Q' and lower_parity == 'e':
        upper_parity = 'f'
    else:
        upper_parity = lower_parity


    return upper_parity

def get_parity_exo(line):

    """
    Function gets upper parity of line
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: parity of upper state
    """

    upper_parity = str(line[117])
    lower_parity = str(line[128])


    return upper_parity,lower_parity


def check_frequency(frequency_hitran,frequency_exomol):

    """
    Function checks whether frequency in HITRAN and exomol match to 2 dp
    :param frequency_hitran:
    :param frequency_exomol:
    :return: True if frequency matches to 2dp, otherwise false
    """

    if round(frequency_hitran,2) == round(frequency_exomol,2):
        return True
    else:
        return False

def check_j(j_hitran,j_exo):

    """
    Function checks whether j states are equal (unused as of 26/07/17)
    :param j_hitran:
    :param j_exo:
    :return: True if equal, false if not
    """

    if j_hitran== j_exo:
        return True
    else:
        return False

def check_parity(parity_hitran,parity_exo):

    """
    Function checks whether parity are equal (unused as of 26/07/17)
    :param parity_hitran:
    :param parity_exo:
    :return: True if equal, false if not
    """

    if parity_hitran == parity_exo:
        return True
    else:
        return False

def get_branch_exo(line):

    lower_j, upper_j = get_j_value_exo(line)

    if lower_j==upper_j:
        branch = 'Q'

    elif lower_j-1==upper_j:
        branch ='P'

    else:
        branch='R'

    return branch

def get_isomer_exo(line):

    """

    :param line:
    :return:
    """

    isomer_no = int(line[90:92])
    print(isomer_no)

    return isomer_no

def get_line_no(list):

    line_number =[]

    for i in range(0,len(list),1):
        line_number.append(i)
    return line_number


def check_match_param(query_upper_j,query_lower_j,query_lower_parity,query_upper_parity,query_frequency,query_lower_QN,
                      query_upper_QN,dataset):
    """
    Function checks whether parameters are equal
    :param query_upper_j: ExoMol upper J state
    :param query_lower_j: ExoMol lower J state
    :param query_lower_parity: ExoMol lower parity state
    :param query_upper_parity: ExoMol upper parity state
    :param query_frequency: ExoMol frequency
    :param query_lower_QN: ExoMol lower QN
    :param query_upper_QN: ExoMol upper QN
    :param dataset: HITRAN data set
    :return:
    """

    counter = 0
    matched_hitran = []
    for row in dataset:
        #use hitran functions here to obtain parameters
        ref_lower_j, ref_upper_j = get_J_value_hitran(row)
        ref_lower_parity = get_lower_parity_hitran(row)
        ref_upper_parity = get_upper_parity_hitran(ref_lower_parity,row)
        ref_frequency = get_freq_hitran(row)
        ref_upper_qn, ref_lower_qn = get_quantum_number_n_hitran(row)
        if ref_lower_j==query_lower_j and ref_upper_j==query_upper_j:
            if ref_lower_parity == query_lower_parity and ref_upper_parity == query_upper_parity:
                if check_frequency(ref_frequency,query_frequency) == True:
                    if ref_upper_qn == query_upper_QN and ref_lower_qn==query_lower_QN:
                        return row, counter
        counter = counter + 1

    return False, counter



new_exmol = []
matched_hitran = []
unmatched_hitran =[]

with open(filename_exomol,'r') as in_fp:
    line = in_fp.readline()
    while(line):
        try:
            # Get ExoMol parameters that are used in matching
            lower_j, upper_j = get_j_value_exo(line)
            upper_parity, lower_parity = get_parity_exo(line)
            frequency = get_freq_exo(line)
            upper_qn, lower_qn = get_quantum_number_n_exo(line)
            newline, counter = check_match_param(upper_j,lower_j,lower_parity,upper_parity,frequency,lower_qn,upper_qn,hitran_data)

        except TypeError:
            print("Line has different format")
            pass
        if newline:
            # Append HITRAN line if it matches ExoMol line (instead of ExoMol line)
            new_exmol.append(newline)
            matched_hitran.append(counter)
            # Print statements for the purpose of debugging
            print(newline)
            print("line replaced")
        else:
            # Append ExoMol line if there is no match
            newline1 = tE.default_hitran(line)
            new_exmol.append(newline1)
        line = in_fp.readline()

print(matched_hitran)
# Store as output file
with open(output_final, 'w') as my_file:
    for row in new_exmol:
        my_file.write(row)


def get_unmatched(hitran_data,matched_hitran):
    """
    Function gets number of lines of HITRAN data which do not match ExoMol data base
    :param hitran_data:
    :param matched_hitran:
    :return: List of line numbers where
    """
    full_hitran=[]

    for row in hitran_data:
        full_hitran.append(row)

    hitran_no= get_line_no(full_hitran)

    unmatched_hitran = set(hitran_no) - set(matched_hitran)

    return unmatched_hitran


unmatched_hitran = get_unmatched(hitran_data,matched_hitran)

print(unmatched_hitran)

# with open(output_unmatched,'w') as un:
#     for row in unmatched_hitran:
#         #print(row)
#         un.write(row)