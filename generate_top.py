import parmed as pmd
import sys

# Define standard masses and Lennard-Jones parameters for common atom types
standard_masses = {
    'H': 1.008,
    'C': 12.01,
    'N': 14.01,
    'O': 16.00,
    'P': 30.97,
    'S': 32.06,
    'F': 19.00,
    'Cl': 35.45,
    'Br': 79.90,
    'I': 126.90,
    # Add other standard atom types if necessary
}

lj_params = {
    'H': {'sigma': 0.1, 'epsilon': 0.067},
    'C': {'sigma': 0.34, 'epsilon': 0.457},
    'C.2': {'sigma': 0.34, 'epsilon': 0.457},
    'C.3': {'sigma': 0.34, 'epsilon': 0.457},
    'C.1': {'sigma': 0.34, 'epsilon': 0.457},
    'C.ar': {'sigma': 0.34, 'epsilon': 0.457},
    'C.cat': {'sigma': 0.34, 'epsilon': 0.457},
    'N': {'sigma': 0.31, 'epsilon': 0.65},
    'N.2': {'sigma': 0.31, 'epsilon': 0.65},
    'N.3': {'sigma': 0.31, 'epsilon': 0.65},
    'N.4': {'sigma': 0.31, 'epsilon': 0.65},
    'N.am': {'sigma': 0.31, 'epsilon': 0.65},
    'N.ar': {'sigma': 0.31, 'epsilon': 0.65},
    'N.pl3': {'sigma': 0.31, 'epsilon': 0.65},
    'O': {'sigma': 0.28, 'epsilon': 0.78},
    'O.2': {'sigma': 0.28, 'epsilon': 0.78},
    'O.3': {'sigma': 0.28, 'epsilon': 0.78},
    'O.co2': {'sigma': 0.28, 'epsilon': 0.78},
    'S': {'sigma': 0.35, 'epsilon': 0.8},
    'S.2': {'sigma': 0.35, 'epsilon': 0.8},
    'S.3': {'sigma': 0.35, 'epsilon': 0.8},
    'S.o': {'sigma': 0.35, 'epsilon': 0.8},
    'S.o2': {'sigma': 0.35, 'epsilon': 0.8},
    'P': {'sigma': 0.38, 'epsilon': 0.9},
    'F': {'sigma': 0.3, 'epsilon': 0.7},
    'Cl': {'sigma': 0.35, 'epsilon': 0.75},
    'Br': {'sigma': 0.37, 'epsilon': 0.85},
    'I': {'sigma': 0.4, 'epsilon': 0.9},
    'Si': {'sigma': 0.375, 'epsilon': 0.837},
    'Zn': {'sigma': 0.4, 'epsilon': 0.8},
    'Cu': {'sigma': 0.34, 'epsilon': 0.8},
    'Fe': {'sigma': 0.335, 'epsilon': 0.88},
    'Mg': {'sigma': 0.3, 'epsilon': 0.8},
    'Na': {'sigma': 0.33, 'epsilon': 0.5},
    'K': {'sigma': 0.45, 'epsilon': 0.3},
    # Add other LJ parameters if necessary
}

def get_element(atom_type):
    for element in standard_masses:
        if atom_type.startswith(element):
            return element
    return None

def guess_lj_params(atom_type):
    element = get_element(atom_type)
    if element:
        return lj_params[element]
    else:
        # Default values for unknown atoms
        return {'sigma': 0.3, 'epsilon': 0.5}

def set_masses_from_ligand(ligand):
    for atom in ligand.atoms:
        element = get_element(atom.type)
        if element:
            atom.mass = standard_masses[element]

def generate_topology():
    if len(sys.argv) != 2:
        print("Usage: generate_topology <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    ligand = pmd.load_file(input_file, structure=True)
    set_masses_from_ligand(ligand)
    gro_file = input_file.split('.')[0] + '.gro'
    itp_file = input_file.split('.')[0] + '.itp'
    prm_file = input_file.split('.')[0] + '.prm'
    ligand.save(gro_file)

    # Generate and save the ITP file
    with open(itp_file, 'w') as f:
        f.write('[ moleculetype ]\n')
        f.write('; Name            nrexcl\n')
        f.write('LIGAND            3\n\n')

        f.write('[ atoms ]\n')
        f.write('; nr    type    resnr   residue  atom   cgnr    charge    mass\n')
        for i, atom in enumerate(ligand.atoms):
            atom_type = f"L_{atom.type}"  # Prefix to avoid redefinition
            f.write(f'{i+1:<6} {atom_type:<6} 1       LIG   {atom.name:<4} {i+1:<6} {atom.charge:<8.4f} {atom.mass:<8.4f}\n')
        
        f.write('\n[ bonds ]\n')
        f.write('; ai    aj    funct\n')
        for bond in ligand.bonds:
            f.write(f'{bond.atom1.idx+1:<6} {bond.atom2.idx+1:<6} 1\n')

    # Generate and save the PRM file (Lennard-Jones format)
    with open(prm_file, 'w') as f:
        f.write('[ atomtypes ]\n')
        f.write(';name  at.num  mass     charge  ptype  sigma  epsilon\n')
        unique_atom_types = set()  # To avoid duplicate entries
        for atom in ligand.atoms:
            element = get_element(atom.type)  # Determine the element
            if element:
                atom_type = f"L_{atom.type}"  # Ensure unique atom type
                if atom_type not in unique_atom_types:
                    lj_param = lj_params.get(atom.type, guess_lj_params(atom.type))
                    sigma = lj_param['sigma']
                    epsilon = lj_param['epsilon']
                    mass = standard_masses[element]
                    f.write(f'{atom_type:<6} {atom.atomic_number:<8} {mass:<8} {atom.charge:<8.4f} A {sigma:<8.4f} {epsilon:<8.4f}\n')
                    unique_atom_types.add(atom_type)
            else:
                print(f'Warning: No LJ parameters found for atom type {atom.type}. Guessed values will be used.')
                lj_param = guess_lj_params(atom.type)
                sigma = lj_param['sigma']
                epsilon = lj_param['epsilon']
                mass = 0.0  # Default mass for unknown elements
                atom_type = f"L_{atom.type}"
                f.write(f'{atom_type:<6} {atom.atomic_number:<8} {mass:<8} {atom.charge:<8.4f} A {sigma:<8.4f} {epsilon:<8.4f}\n')

        f.write('\n[ bondtypes ]\n')
        f.write('; i     j      funct   length  force_constant\n')
        for bond in ligand.bonds:
            atom1_type = f"L_{bond.atom1.type}"
            atom2_type = f"L_{bond.atom2.type}"
            f.write(f'{atom1_type:<6} {atom2_type:<6} 1       0.1    1000\n')  # Replace with actual bond parameters

    print(f"Topology files generated: {gro_file}, {itp_file}, {prm_file}")

if __name__ == "__main__":
    generate_topology()
