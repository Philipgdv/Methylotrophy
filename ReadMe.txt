This repository contains the data, scripts, and notebooks used in the paper,

Methylotrophy at the Origin of Life,
By Philip J. Gorter de Vries, Alex Toftgaard Nielsen, Alfred M. Spormann

In order to run the scripts, the user needs to have installed python and snakemake and change directory to the repository.

Initiate the folder by running in the terminal (Where 1935183 is the taxon number of Asgardarchaea):
	python Scripts/Setup.py 1935183

Second, run the snakefile to run orthofinder.
	snakemake -j 4

Then, the analyses in the notebooks can be run as described in the materials & methods section.