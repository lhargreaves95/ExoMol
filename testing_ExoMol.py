# Testing functions used in ExoMol project

from fortranformat import FortranRecordWriter


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

def get_branch_exo(line):

    lower_j, upper_j = get_j_value_exo(line)

    if lower_j==upper_j:
        branch = 'Q'

    elif lower_j-1==upper_j:
        branch ='P'

    else:
        branch='R'

    return branch
def get_freq_exo(line):

    """
    Function stores frequency
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: frequency
    """
    frequency=line[7:15]

    return float(frequency)
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

def get_parity_exo(line):

    """
    Function gets upper parity of line
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: parity of upper state
    """

    upper_parity = str(line[117])
    lower_parity = str(line[128])


    return upper_parity,lower_parity

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

def get_id(line):

    """
    Function stores Molecule ID and Isotoplugle ID
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: molecule_id, iso_id
    """

    molecule_id = int(line[0:2])
    iso_id = int(line[2])

    return molecule_id, iso_id

def get_intensity(line):

    """
    Function stores intensity
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: intensity
    """

    intensity = float(line[16:25])

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

def get_energy_exo(line):

    """
    Function stores energy
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: energy
    """

    energy = float(line[46:55])

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

def get_global_qn(line):
    """
    Function stores global QN (non rigorous)
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: string_global_upper, string_global_lower

     """

    global_upper, global_lower = get_quantum_number_n_exo(line)
    string_global_lower = " ".join(str(x) for x in global_lower)
    string_global_upper = " ".join(str(x) for x in global_upper)

    return string_global_upper, string_global_lower

def get_local_qn(line):
    """
    Function stores local QN
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: local_upper_str, local_lower_str

     """

    local_lower, local_upper = get_j_value_exo(line)

    local_lower_str = str(local_lower)
    local_upper_str = str(local_upper)

    return local_upper_str, local_lower_str


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

def get_g(line):
    """
    Function stores g upper and g lower
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: g_upper, g_lower

    """

    g_upper = float(line[151:156])
    g_lower = float(line[158:163])

    return g_upper, g_lower

def set_hitran_intensity(intensity,line):
    """
    Function stores g upper and g lower
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: g_upper, g_lower

    """

    new_line = line[:16] + intensity + line[25:]

    return new_line

def set_hitran_einstein(einstein_coefficient,line):
    """
    Function replaces Einstein A coefficient
    :param line: input line from file that comes from HITRAN
    :return: new_line

    """

    new_line = line[:25] + einstein_coefficient + line[36:]

    return new_line

def set_hitran_energy(energy,line):
    """
    Function replaces energy
    :param line: input line from file that comes from HITRAN
    :return: new_line

    """

    new_line = line[:46] + energy + line[54:]

    return new_line


def local_qn(branch, localqn, parity):
    local_quantum = [branch,localqn, parity]

    string_local = branch+"" +localqn+parity+" "

    #string_local = " ".join(str(x) for x in local_quantum)


    return string_local


def default_hitran(ExoCrossline):

    """
    Function formats line into default HITRAN format
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: line in HITRAN format
    """

    # Following lines get parameters
    molecule_id, iso_id = get_id(ExoCrossline)

    frequency = get_freq_exo(ExoCrossline)

    intensity = get_intensity(ExoCrossline)

    einstein_coeff = get_einstein_coeff(ExoCrossline)

    broadening_air, broadeing_self = get_broadening(ExoCrossline)

    energy = get_energy_exo(ExoCrossline)

    n_air = get_n_air(ExoCrossline)

    delta_air = get_delta_air(ExoCrossline)

    global_upper, global_lower = get_global_qn(ExoCrossline)

    local_upper, local_lower = get_local_qn(ExoCrossline)

    branch = get_branch_exo(ExoCrossline)

    upper_parity, lower_parity = get_parity_exo(ExoCrossline)

    error_indices1, error_indices2, error_indices3, error_indices4, error_indices5, error_indices6 = get_error_indices(ExoCrossline)

    ref1, ref2, ref3, ref4, ref5, ref6 = get_ref(ExoCrossline)

    g_upper, g_lower = get_g(ExoCrossline)

    local_upper = str(local_upper)

    local_lower = local_lower

    # not sure of the format of the following line

    new_local_upper = local_qn(branch,local_upper,upper_parity)

    new_local_lower = local_qn(branch,local_lower,lower_parity)

    test1 = ' '
    test2 = ' '
    test3 = '10'
    test4 = 'e'
    # line mixing flag needs to be discusses

    line_mixing_flag=' '

    #newline = FortranRecordWriter('(I2,I1,F12.6,E10.3,E10.3,F5.4,F5.3,F10.4,F4.2,F8.6,A15,A15,A15,A15,6I1,6I2,A1,F7.1,F7.1)')
    newline = FortranRecordWriter(
        '(I2,I1,F12.6,E10.3,E10.3,F5.4,F5.3,F10.4,F4.2,F8.6,A15,A15,10X,A5,5X,A1,I3,A1,A5,6I1,6I2,A1,F7.1,F7.1)')

    line1 = molecule_id, iso_id, frequency, intensity, einstein_coeff, broadening_air, broadeing_self, energy, n_air,\
            delta_air, global_upper,global_lower,test1,branch,local_lower,lower_parity,test2,error_indices1, error_indices2,\
            error_indices3, error_indices4, error_indices5, error_indices6,ref1, ref2, ref3, ref4,\
            ref5, ref6, line_mixing_flag, g_upper,g_lower

    # #
    string1 = str(newline.write(line1))

    new_string = string1 + '\n'

    return new_string


testfile = '/Users/laurahargreaves/Documents/ExoMol/exomol_test.txt'
test_out ='test_out.txt'

test_line=[]

with open(testfile,'r') as in_fp:
    line = in_fp.readline()
    while(line):
        new_line = default_hitran(line)
        test_line.append(new_line)
        line = in_fp.readline()


with open(test_out,'w') as my_file:
    for row in test_line:
        print(row)
        my_file.write(row)



