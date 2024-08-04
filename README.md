# topology_gen_3.0
Toplogt gernator is updated version of ligand processor. This is a Python package designed to preprocess ligand files and generate necessary topology files for GROMACS simulations. This package supports ligand files in PDB and mol2 formats, and outputs the required `.itp`, `.gro`, and `.prm` files for small ligands.

## Features

- Preprocess ligand files in PDB or mol2 format.
- Generate topology files (`.itp`, `.gro`, `.prm`) for GROMACS.

## Installation

You can install the Ligand Processor package using pip:

```sh

pip install topology_genrator

Usage
Preprocess Ligand File
To preprocess a ligand file, use the preprocess_ligand command. This command will take a ligand file in mol2 format and generate a preprocessed mol2 file.

preprocess_ligand <name_of_your_ligand.mol2>

Example:
preprocess_ligand lig.mol2

This command will generate a file lig_preprocessed.mol2.

Generate Topology Files
Once you have the preprocessed ligand file, you can generate the topology files for GROMACS using the generate_topology command:

generate_topology <name_preprocessed.mol2>

Example:
generate_topology lig_preprocessed.mol2

This command will generate the following files:

lig.gro: GROMACS coordinate file.
lig.itp: GROMACS topology file.
lig.prm: Parameter file with Lennard-Jones parameters.

Dependencies
parmed: This package is required to handle the ligand files. It can be installed via pip.

pip install parmed

Contributing
Contributions are welcome! Please feel free to submit a Pull Request on the GitHub repository

License
This project is licensed under the MIT License.

Contact
For any questions or feedback, please contact  naeem.sbb@pu.edu.pk
