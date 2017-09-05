# This python file hold all relevant functions required to match and replace lines in a new text file
# This file was created for the purpose of completeness to have all functions in one file


# Section 0

# This section should be used to store file names as variables:

# Input files

# Output files (there should be four output files, Final output file (mix of HITRAN and ExoMol lines), matched hitran lines,
# matched exomol lines and unmatched hitran lines


# Section 1: Getter methods for HITRAN and ExoMol

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

def get_branch_exo(line):

    lower_j, upper_j = get_j_value_exo(line)

    if lower_j==upper_j:
        branch = 'Q'

    elif lower_j-1==upper_j:
        branch ='P'

    else:
        branch='R'

    return branch



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

def set_ref():
    ref1 = 10
    ref2 = 4
    ref3 = 0
    ref4 = 0
    ref5 = 0
    ref6 = 0

    return ref1, ref2, ref3, ref4, ref5, ref6



def get_intensity(line):

    """
    Function stores intensity
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: intensity
    """

    intensity = float(line[16:25])

    return intensity


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


def get_g(line):
    """
    Function stores g upper and g lower
    :param line: input line from file that comes from ExoMol to HITRAN format (ExoCross)
    :return: g_upper, g_lower

    """

    g_upper = float(line[151:156])
    g_lower = float(line[158:163])

    return g_upper, g_lower


