# This python file hold all relevant functions required to match and replace lines in a new text file
# This file was created for the purpose of completeness to have all functions in one file

from fortranformat import FortranRecordWriter

# Section 0

# This section should be used to store file names as variables:

# Input files

# HITRAN data
filename_hitran = 'path to hitran file'
# Store contents of HITRAN data in a list
with open(filename_hitran, 'r') as in_fp:
 hitran_data = in_fp.readlines()

# ExoMol data

filename_exomol = 'path to exomol file'

# Output files (there should be four output files, Final output file (mix of HITRAN and ExoMol lines), matched hitran lines,
# matched exomol lines and unmatched hitran lines

output_final= 'final_output.txt'
output_unmatched = 'unmatched_hitran_lines.txt'

# Files of matched lines: to check intensity and energy
match_hitran = 'matched_hitran.txt'
match_exo = 'matched_exo.txt'



# Section 1: This section contains getter functions for HITRAN and ExoMol lines
# A getter function for each parameter in ExoMol
# Getter functions for parameters of HITRAN which need to be checked

# Section 1a: Getter methods

def get_id(line):

    """
    Function stores Molecule ID and Isotoplugle ID
    :param line: input line from file that comes from either ExoCross or HITRAN line
    :return: molecule_id, iso_id
    """

    molecule_id = int(line[0:2])
    iso_id = int(line[2])

    return molecule_id, iso_id

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

def get_intensity_exo(line):

    intensity = float(line[16:26])

    return intensity

def get_intensity_hitran(line):

    intensity = float(line[16:26])

    return intensity

def get_einstein_coeff(line):

    """
    Function stores einstein A coefficient
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: einstein A coefficient
    """

    einstein_coeff = float(line[26:35])

    return einstein_coeff

def get_broadening(line):

    """
    Function stores broadening parameters
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: broadening_air, broadening_self
    """

    broadening_air = float('0.' + line[36:39])
    broadening_self = float(line[40:45])

    return broadening_air, broadening_self

def set_broadening(air,self):

    """
    Function sets broadening parameters
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: broadening_air, broadening_self
    """

    broadening_air = air
    broadening_self = self

    return broadening_air, broadening_self


def get_exo_energy(line):

    energy = float(line[47:54])

    return energy

def get_hitran_energy(line):

    energy = float(line[47:54])

    return energy

def get_n_air(line):

    """
    Function stores n air
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: n air
    """

    n_air = float(line[55:59])

    return n_air

def get_delta_air(line):

    """
    Function stores delta air
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: delta air

    """

    delta_air = float(line[59:67])

    return delta_air

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

def get_global_qn(line):
    """
    Function stores global QN (non rigorous) as strings (required for Fortran formatting)
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: string_global_upper, string_global_lower

     """

    global_upper, global_lower = get_quantum_number_n_exo(line)
    string_global_lower = " ".join(str(x) for x in global_lower)
    string_global_upper = " ".join(str(x) for x in global_upper)

    return string_global_upper, string_global_lower



def get_j_value_exo(line):
    """
    Function gets upper and lower J values
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: upper and lower J quantum numbers
    """
    try:
        upper_j = line[112:114]
        lower_j = line[123:125]
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


def get_branch_exo(line):

    lower_j, upper_j = get_j_value_exo(line)

    if lower_j==upper_j:
        branch = 'Q'

    elif lower_j-1==upper_j:
        branch ='P'

    else:
        branch='R'

    return branch

def get_branch_hitran(line):

    """
    Function gets branch type
    :param line: input line that is in exact HITRAN format
    :return: branch type(P,Q,R)
    """
    branch = line[117]


    return str(branch)


def get_parity_exo(line):

    """
    Function gets upper parity of line
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: parity of upper state
    """

    upper_parity = str(line[117])
    lower_parity = str(line[128])


    return upper_parity,lower_parity

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

# Section 1.b Error and references for ExoMol line
# This section contains getter and setter methods for the error indices and references
# The input file

def get_error_indices(line):
    """
    Function stores error indices
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: error_indices1, error_indices2, error_indices3, error_indices4, error_indices5, error_indices6

    """

    error_indices1 = int(line[130])
    error_indices2 = int(line[131])
    error_indices3 = int(line[132])
    error_indices4 = int(line[133])
    error_indices5 = int(line[134])
    error_indices6 = int(line[135])

    return error_indices1, error_indices2, error_indices3, error_indices4, error_indices5, error_indices6

def set_error():
    """
    Function sets error indices
    :param l
    :return: error_indices1, error_indices2, error_indices3, error_indices4, error_indices5, error_indices6

    """

    error_indices1 = 2
    error_indices2 = 5
    error_indices3 = 0
    error_indices4 = 0
    error_indices5 = 0
    error_indices6 = 0

    return error_indices1, error_indices2, error_indices3, error_indices4, error_indices5, error_indices6


def get_ref(line):

    """
    Function stores references
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: ref1, ref2, ref3, ref4, ref5, ref6
    """
    references = line[137:149]
    references = references.split()
    ref1 = int(references[0])
    ref2 = int(references[1])
    ref3 = int(references[2])
    ref4 = int(references[3])
    ref5 = int(references[4])
    ref6 = int(references[5])


    return ref1, ref2, ref3, ref4, ref5, ref6

def set_ref():
    ref1 = 10
    ref2 = 4
    ref3 = 0
    ref4 = 0
    ref5 = 0
    ref6 = 0

    return ref1, ref2, ref3, ref4, ref5, ref6


def get_local_qn(line):
    """
    Function stores local rigourous quantum numbers (J',J")
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: local_upper_str, local_lower_str

     """

    local_lower, local_upper = get_j_value_exo(line)

    local_lower_str = str(local_lower)
    local_upper_str = str(local_upper)

    return local_upper_str, local_lower_str


def get_g(line):
    """
    Function stores g upper and g lower
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: g_upper, g_lower

    """

    g_upper = float(line[151:156])
    g_lower = float(line[158:163])

    return g_upper, g_lower

## Section 2: This section contains code that defaults ExoMol line to HITRAN format
# This code uses the function FortranFormatWriter from the FortranFormat library
# The function allows the user to write lines in Fortran format
# Format for each molecule can be found in the 2004 HITRAN paper
# Local quantum numbers format are dependent on the molecule


def default_hitran(ExoCrossline):

    """
    Function formats line into default HITRAN format
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: line in HITRAN format
    """

    # Following lines get parameters
    molecule_id, iso_id = get_id(ExoCrossline)

    frequency = get_freq_exo(ExoCrossline)

    intensity = get_intensity_exo(ExoCrossline)

    einstein_coeff = get_einstein_coeff(ExoCrossline)

    broadening_air, broadeing_self = get_broadening(ExoCrossline)

    energy = get_exo_energy(ExoCrossline)

    n_air = get_n_air(ExoCrossline)

    delta_air = get_delta_air(ExoCrossline)

    global_upper, global_lower = get_global_qn(ExoCrossline)

    local_upper, local_lower = get_local_qn(ExoCrossline)

    branch = get_branch_exo(ExoCrossline)

    upper_parity, lower_parity = get_parity_exo(ExoCrossline)

    error_indices1, error_indices2, error_indices3, error_indices4, error_indices5, error_indices6 = set_error()

    ref1, ref2, ref3, ref4, ref5, ref6 = set_ref()

    g_upper, g_lower = get_g(ExoCrossline)

    space1 = ' '
    space2 = ' '

    line_mixing_flag=' '

    newline = FortranRecordWriter(
        '(I2,I1,F12.6,E10.3,E10.3,F5.4,F5.3,F10.4,F4.2,F8.6,A15,A15,10X,A5,5X,A1,I3,A1,A5,6I1,6I2,A1,F7.1,F7.1)')

    # Set up line with chosen parameters (order and type are important)

    line1 = molecule_id, iso_id, frequency, intensity, einstein_coeff, broadening_air, broadeing_self, energy, n_air,\
            delta_air, global_upper,global_lower,space1,branch,local_lower,lower_parity,space2,error_indices1, error_indices2,\
            error_indices3, error_indices4, error_indices5, error_indices6,ref1, ref2, ref3, ref4,\
            ref5, ref6, line_mixing_flag, g_upper,g_lower

    # #
    string1 = str(newline.write(line1))

    new_string = string1 + '\n'

    return new_string

# Section 3: Code to check if parameters match

# Section 3.1 Functions to check a given set of parameters
# Counters are included to keep track of line no of matched hitran lines

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

def check_frequency_oneDp(frequency_hitran,frequency_exomol):

    """
    Function checks whether frequency in HITRAN and exomol match to 1 dp
    :param frequency_hitran:
    :param frequency_exomol:
    :return: True if frequency matches to 2dp, otherwise false
    """

    if round(frequency_hitran,1) == round(frequency_exomol,1):
        return True
    else:
        return False

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

def check_match_param_relaxed(query_upper_j,query_lower_j,query_lower_parity,query_upper_parity,query_frequency,query_lower_QN,
                      query_upper_QN,dataset):
    """
    Function checks whether parameters are equal - relaxed frequency requirements
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
    for row in dataset:
        #use hitran functions here to obtain parameters
        ref_lower_j, ref_upper_j = get_J_value_hitran(row)
        ref_lower_parity = get_lower_parity_hitran(row)
        ref_upper_parity = get_upper_parity_hitran(ref_lower_parity,row)
        ref_frequency = get_freq_hitran(row)
        ref_upper_qn, ref_lower_qn = get_quantum_number_n_hitran(row)
        if ref_lower_j==query_lower_j and ref_upper_j==query_upper_j:
            if ref_lower_parity == query_lower_parity and ref_upper_parity == query_upper_parity:
                if check_frequency_oneDp(ref_frequency,query_frequency) == True:
                    if ref_upper_qn == query_upper_QN and ref_lower_qn==query_lower_QN:
                        return row, counter
        counter = counter + 1

    return False, counter

def get_line_no(list):

    line_number =[]

    for i in range(0,len(list),1):
        line_number.append(i)
    return line_number

# Section 3.2: Check parametes and set up lists
# This section runs the matching functions
# Checks if HITRAN line is in ExoMol file- if so adds to list
# Also keeps track of matched ExoMol lines

new_exmol = []

# Line no of matched HITRAN lines
matched_hitran = []

# List of matched lines
match_hitran_line = []
match_exo_line = []

with open(filename_exomol,'r') as in_fp:
    line = in_fp.readline()
    while(line):
        try:
            # Get ExoMol parameters that are used in matching
            lower_j, upper_j = get_j_value_exo(line)
            upper_parity, lower_parity = get_parity_exo(line)
            frequency = get_freq_exo(line)
            upper_qn, lower_qn = get_quantum_number_n_exo(line)
            newline, counter = check_match_param_relaxed(upper_j,lower_j,lower_parity,upper_parity,frequency,lower_qn,upper_qn,hitran_data)
        except TypeError:
            print("Line has different format")
            pass
        if newline:
            # Append HITRAN line if it matches ExoMol line (instead of ExoMol line)
            new_exmol.append(newline)
            matched_hitran.append(counter)
            match_hitran_line.append(newline)
            match_exo_line.append(line)
            # Print statements for the purpose of debugging
            print("line replaced")
        else:
            # Append ExoMol line if there is no match
            newline1 = default_hitran(line)
            new_exmol.append(newline1)
        line = in_fp.readline()


# Section 4: Make new files of matched and unmatched lines
# Section 4.1:

# Store as output file
with open(output_final, 'w') as my_file:
    for row in new_exmol:
        my_file.write(row)

with open(match_hitran, 'w') as my_file:
    for row in match_hitran_line:
        my_file.write(row)

with open(match_exo, 'w') as my_file:
    for row in match_exo_line:
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

    unmatched_hitran = sorted(set(hitran_no) - set(matched_hitran))

    return unmatched_hitran


unmatched_hitran = get_unmatched(hitran_data,matched_hitran)

def get_unmatched_lines(fullist,unmatched_list_no):

    unmatched_list = []
    counter = 0
    for row in fullist:
        for num in unmatched_list_no:
            if counter == num:
                unmatched_list.append(row)
        counter = counter +1
    return unmatched_list

def make_file(filename,list):
    with open(filename,'w') as new_file:
        for row in list:
            new_file.write(row)
    return filename

list=get_unmatched_lines(hitran_data,unmatched_hitran)

make_file(output_unmatched,list)
