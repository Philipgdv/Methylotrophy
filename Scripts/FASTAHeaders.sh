#!/bin/bash

#Rename each sequence fasta header to UPID_GeneName

cd Data/input/Proteomes

for f in *.fasta; do
  sed -i '' -e "s/^>/>${f%.fasta}./g" "${f}"
  sed -i '' -e '/^>/ s/ .*//' "${f}"
done

cd ..
cd ..
cd ..

#cut -d '|' -f1
cat Data/input/Proteomes/*.fasta >> Data/input/AllGenes.fasta
