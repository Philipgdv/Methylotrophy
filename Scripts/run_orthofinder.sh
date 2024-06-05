#!/bin/bash

threads=$1
orthofinder -t $threads -a $threads -oa -M msa -f Data/input/Proteomes
# mkdir -p tmp
find Data/input/Proteomes -name 'Orthogroups.tsv' -exec cp {} Data/OFResults \;
find Data/input/Proteomes -name 'Orthogroups.GeneCount.tsv' -exec cp {} Data/OFResults \;
find Data/input/Proteomes -name 'Orthogroups_UnassignedGenes.tsv' -exec cp {} Data/OFResults \;
find Data/input/Proteomes -name 'MultipleSequenceAlignments' -exec cp -R {} Data/OFResults \;
find Data/input/Proteomes -name 'Gene_Trees' -exec cp -R {} Data/OFResults \;

rm -r Data/input/Proteomes/OrthoFinder