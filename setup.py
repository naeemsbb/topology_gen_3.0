from setuptools import setup, find_packages

setup(
    name='topology_genrator',
    version='3.0',
    packages=find_packages(),
    install_requires=[
        'parmed',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'preprocess_ligand=topology_gen.preprocess_mol2:preprocess_ligand',
            'generate_topology=topology_gen.generate_top:generate_topology',
        ],
    },
    author='Naeem Mahmood Ashraf and Arslan Hamdi',
    author_email='naeem.sbb@pu.edu.pk',
    description='A package to preprocess ligand files and generate topology files for GROMACS.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com//naeemsbb/ligand_processor',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
