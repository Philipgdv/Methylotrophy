#!/bin/bash

#Rename each sequence fasta header to UPID_GeneName

cd Data/OFResults/MultipleSequenceAlignments

rm OFOG_Representatives.fasta

for f in *.fa; do
  awk "/^>/ {n++} n>1 {exit} {print}" "${f}" | sed 's/-//g' >> ${f%.fa}_tmp.txt #OG0000000
  sed -i '' -e "s/^>/>${f%.fa}./g" "${f%.fa}_tmp.txt"
done

cat *_tmp.txt >> OFOG_Representatives.fasta
rm *_tmp.txt

sed -i '' -e '/^$/d' OFOG_Representatives.fasta

# Move all alignments to new separate folders to add the database alignments
find Data/OFResults/MultipleSequenceAlignments/*.fa -prune -type f -exec \
  sh -c 'mkdir -p "${0%.fa}" && mv "$0" "${0%.fa}"' {} \;

cd ../../..
