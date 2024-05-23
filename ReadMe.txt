This repository contains the data, scripts, and notebooks used in the paper,

Methylotrophy at the Origin of Life,
By Philip J. Gorter de Vries, Alex Toftgaard Nielsen, Alfred M. Spormann

In order to run the scripts, the user needs to have installed python and snakemake and change directory to the repository.

Initiate the folder by running in the terminal (Where 1935183 is the taxon number of Asgardarchaea):
	python Scripts/Setup.py 1935183

Second, run the snakefile to run orthofinder.
	snakemake -j 4

Then, the analyses in the notebooks can be run as described in the materials & methods section.

1 - System Requirements:
The analysis was run locally on a computer with a 1,4 GHz Quad-Core Intel Core i5 running MacOS Sonoma 14.4.1
The software dependencies are:
	- snakemake 7.18.2
	- python 3.9.15 (including packages: numpy 1.23.5, pandas 1.5.2, scipy 1.10.1, scikit-learn 1.2.0, fastcluster 1.2.6, ete3 3.1.2)
	- Orthofinder 2.5.4
	- MAFFT v7.508
	- fasttree 2.1.11

All packages can be installed with conda, which takes no more than an hour to set everything up.

2 - 
