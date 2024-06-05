#!/usr/bin/python3

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from os.path import join
import ftplib
import urllib3
import sys

TaxID = sys.argv[1]

if TaxID == "Demo":
    print("You are running on a demo dataset comprised only of two genome assemblies: UP000324665 & UP000321408")
    SpIndex = pd.read_csv("https://rest.uniprot.org/proteomes/search?query=(taxonomy_id:1935183)&fields=upid%2Corganism%2Corganism_id%2Cprotein_count%2Cgenome_assembly&&format=tsv&size=500", sep="\t", index_col = 'Proteome Id')
    mask =["UP000324665","UP000321408"]
    SpIndex = SpIndex.loc[mask]

else:
    SpIndex = pd.read_csv(f"https://rest.uniprot.org/proteomes/search?query=(taxonomy_id:{TaxID})&fields=upid%2Corganism%2Corganism_id%2Cprotein_count%2Cgenome_assembly&&format=tsv&size=500", sep="\t", index_col = 'Proteome Id')
    if SpIndex.empty: print("Error, wrong taxID, there are no species listed. Please enter a valid NCBI taxID")
    else: print(f"Assessing quality of {len(SpIndex)} genome assemblies belonging to TaxID {TaxID}")
    

SpIndex.rename(columns={'Genome assembly ID':'Assembly'}, inplace=True)
SpIndex["AssemblyFullName"] = "NaN"
SpIndex["SeqLen"] = "NaN"
SpIndex["Contigs"] = "NaN"

i = 0
for PID in SpIndex.index:
    i = i + 1
    try:
        ftp = ftplib.FTP('ftp.ncbi.nlm.nih.gov', 'anonymous', 'password')
        ftp.cwd(f'genomes/all/GCA/{SpIndex.loc[PID,"Assembly"][4:7]}/{SpIndex.loc[PID,"Assembly"][7:10]}/{SpIndex.loc[PID,"Assembly"][10:13]}/')
        if len(ftp.nlst()) == 1:
            print(PID,SpIndex.loc[PID,"Assembly"], f"Progress {round(i/len(SpIndex.index)*100,1)}%")
            SpIndex.loc[PID,"AssemblyFullName"] = ftp.nlst()[0]
            url = f'https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/{SpIndex.loc[PID,"Assembly"][4:7]}/{SpIndex.loc[PID,"Assembly"][7:10]}/{SpIndex.loc[PID,"Assembly"][10:13]}/{SpIndex.loc[PID,"AssemblyFullName"]}/{SpIndex.loc[PID,"AssemblyFullName"]}_assembly_stats.txt'
            stats = pd.read_csv(url, comment = "#", sep = "\t", header = None)
            stats = stats[stats.iloc[:,0] == "all"].set_index(4).iloc[:,-1]
            SpIndex.loc[PID,"SeqLen"] = stats["total-length"]
            if stats["contig-count"] > 0:
                SpIndex.loc[PID,"Contigs"] = stats["contig-count"]
        else:
            print("More than one assembly")
        print(f'\t Assembly is {SpIndex.loc[PID,"SeqLen"]} bp long and consists of {SpIndex.loc[PID,"Contigs"]} Contigs')
        ftp.close()
    except:
        pass

    SpIndex[["Contigs","SeqLen"]] = SpIndex[["Contigs","SeqLen"]].replace("NaN",1).astype(int)

    plt.figure(figsize=(10, 5))
    plt.title("Assembly Quality Assesment")
    plt.scatter(SpIndex["Contigs"],SpIndex["SeqLen"]/1000000)
    plt.hlines(1,0,1000, linewidth = 0.5)
    plt.vlines(300,0,10, linewidth = 0.5)
    plt.xlabel(r'Contig count')
    plt.ylabel(r'Total sequence length ($10^6$ bp)')
    plt.axis([0, 550, 0, 5.5])

    plt.savefig('Data/output/AssemblyQC.png')

    SpIndex_CutOff = SpIndex[SpIndex["SeqLen"] > 1000000]
    SpIndex_CutOff = SpIndex_CutOff[SpIndex_CutOff["Contigs"] < 300]

    SpIndex_CutOff.to_csv("Data/input/SpeciesIndexDF.tsv", sep="\t", index = True)
    SpIndex_CutOff.reset_index()["Proteome Id"].to_csv("Data/input/UPIDs.txt", sep='\n', index=False, header=False)
