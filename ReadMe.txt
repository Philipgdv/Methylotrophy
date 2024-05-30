This repository contains the data, scripts, and notebooks used in the paper,

Methylotrophic Acetyl-CoA Formation as the Pathway at the Origin of Life,
By Philip J. Gorter de Vries, Alex Toftgaard Nielsen, Alfred M. Spormann

1 - System Requirements:
The analysis was run locally on a computer with a 1,4 GHz Quad-Core Intel Core i5 running MacOS Sonoma 14.4.1
The software dependencies are:
	- snakemake 7.18.2
	- python 3.9.15 (including packages: numpy 1.23.5, pandas 1.5.2, scipy 1.10.1, scikit-learn 1.2.0, fastcluster 1.2.6, ete3 3.1.2)
	- Orthofinder 2.5.4
	- MAFFT v7.508
	- fasttree 2.1.11

2 - Installation guide
All packages can be installed with conda by running in the shell the command:
	conda install *insert package name*

The repository is filled with demo data, allowing to test the notebooks. The notebooks are:
	1_COG_Counts.ipynb
	2_COG_CountRefSpecies.ipynb
	3_COG_PresenceTaxa.ipynb
	4_JaccardCorrelation-TaxFilter.ipynb
	5_HierarchicalClustering.ipynb
	6_LGT_MSA&Tree.ipynb

If you wish to run the full analysis, change directory to the Methylotrophy folder and initiate it by running in the terminal (Where 1935183 is the taxon number of Asgardarchaea):
	python Scripts/Setup.py 1935183

Second, run the snakefile to run orthofinder.
	cd Data_1935183
	snakemake -j 4

The workflow will produce a FASTA file containing the sequences of one of each identified orthology group:
	/Methylotrophy/Data/OFResults/MultipleSequenceAlignments/OFOG_Representatives.fasta

Upload this file to http://eggnog-mapper.embl.de/ to link the found OrthoFinder groups to COG groups. Download the output as a csv or tsv file and move it to /Methylotrophy/Data/input/.

Then, the analyses in the notebooks can be run as described in the materials & methods section.

