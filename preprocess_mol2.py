import parmed as pmd
import sys

def preprocess_ligand():
    if len(sys.argv) != 2:
        print("Usage: preprocess_ligand <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Load the ligand file (supports mol2 and pdb)
    if input_file.endswith('.mol2'):
        ligand = pmd.load_file(input_file, structure=True)
    elif input_file.endswith('.pdb'):
        ligand = pmd.load_file(input_file)
    else:
        raise ValueError('Unsupported file format. Please use PDB or mol2 format.')

    output_file = input_file.split('.')[0] + '_preprocessed.mol2'
    ligand.save(output_file)
    print(f"Ligand preprocessed and saved as {output_file}")
