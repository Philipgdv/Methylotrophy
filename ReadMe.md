# Methylotrophic Origin of Life

This repository contains the scripts and notebooks used in used in the manuscript:

Methylotrophic Acetyl-CoA Formation as the Pathway at the Origin of Life,
By Philip J. Gorter de Vries, Alex Toftgaard Nielsen, Alfred M. Spormann

- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Instructions](#instructions)
- [License](#license)

# System Requirements
## Hardware requirements
The code requires only a standard computer with enough RAM to support the in-memory operations. The analysis was run locally on a laptop computer with a 1,4 GHz Quad-Core Intel Core i5 running MacOS Sonoma 14.4.1

## Software requirements
### OS Requirements
This code is supported for *macOS*, it has been tested on the following systems: macOS: Sonoma (14.4.1)

### Command line tools
```
snakemake 7.18.2
python 3.9.15
Orthofinder 2.5.4
MAFFT v7.508
fasttree 2.1.11
```

### Python Dependencies
The included notebooks mainly depend on the Python packages:

```
numpy 1.23.5 
pandas 1.5.2 
scipy 1.10.1
scikit-learn 1.2.0 
fastcluster 1.2.6
ete3 3.1.2
```

# Installation Guide:

All packages can be installed with conda by running in the shell the command (replacing *PackageName*):
```
conda install *PackageName*
```
To run the code in the jupyter notebooks, run (replacing *EnvironmentName*): 
```
conda install -c anaconda ipykernel
python -m ipykernel install --user --name= *EnvironmentName*
```

# Instructions:

The repository consists of a series of scripts that will combine user-selected genomes with genomes of the EggNOG database to create a single dataframe of gene counts per species per orthologous gene group. This dataframe is used for various analyses and visualizations in the jupyter notebooks. The graphical abstract shows how these notebooks are used in the manuscript.

![alt text](https://github.com/Philipgdv/Methylotrophy/blob/main/Figures/GraphicalAbstract.png?raw=true)

## Run on the demo data

The repository is filled with demo data, allowing to test the notebooks. The demo file is a subset of the full dataframe The notebooks are:
```
1_COG_CountRefSpecies.ipynb
2_COG_PresenceTaxa.ipynb
3_COG_Clustering.ipynb
4_LGT_MSA&Tree.ipynb
```

## Run the full analysis

If you wish to run the full analysis and recreate the full dataframe, run the following steps:

### 1 - Initiate 
Change directory to the Methylotrophy folder & initiate it by running in the terminal (Where 1935183 is the taxon number of Asgardarchaea):
```
cd /Methylotrophy
python Scripts/Setup.py 1935183
```

### 2 - Snakefile
run the snakefile to run OrthoFinder
```
snakemake -j 4
```

### 3 - Mapping
the workflow will produce a FASTA file containing the sequences of one of each identified orthology group find the file at: 
```
/Methylotrophy/Data/OFResults/MultipleSequenceAlignments/OFOG_Representatives.fasta 	
```
Upload this file to http://eggnog-mapper.embl.de/ to link the found OrthoFinder groups to COG groups. Download the output as a csv or tsv file and move it to /Methylotrophy/Data/input/

### 4 - Combining Counts
Run a python script to download all COGs from EggNOG at root level and link the identified OrthoFinder orthologous groups to them, creating a count matrix
```
python Scripts/COG_counts.py
```

### 5 - Analyses
Run the analyses in the notebooks, as described in the materials & methods section.

# License

This project is covered under the **Apache 2.0 License**.
