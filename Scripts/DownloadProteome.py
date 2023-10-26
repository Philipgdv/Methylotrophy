#!/usr/bin/python3

import pandas as pd
import os
from os.path import join
import sys
import urllib3

# Download proteome FASTA files using Uniprot API
#PID = str(sys.argv[1])
folder_path = join((os.getcwd()),"Data/input")
http = urllib3.PoolManager()

SpIndex = pd.read_csv(join(folder_path, "SpeciesIndexDF.tsv"), sep = "\t", index_col = 0)

if not os.path.exists(join(folder_path,'Proteomes')):
    os.makedirs(join(folder_path,'Proteomes'))
    print("The Proteome directory is created")

for PID in SpIndex.index:
    file = f'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/{SpIndex.loc[PID,"Assembly"][4:7]}/{SpIndex.loc[PID,"Assembly"][7:10]}/{SpIndex.loc[PID,"Assembly"][10:13]}/{SpIndex.loc[PID,"AssemblyFullName"]}/{SpIndex.loc[PID,"AssemblyFullName"]}_protein.faa.gz'
    r = http.request('GET',file)#f'https://rest.uniprot.org/uniprotkb/stream?compressed=true&format=fasta&query=%28proteome%3A{UPID}%29'
    open(join(folder_path,"Proteomes",f"{PID}.fasta.gz"), "wb").write(r.data)
    print("Downloading..." + PID)
