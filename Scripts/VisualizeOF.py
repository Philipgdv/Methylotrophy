#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

OGs = pd.read_table("Data/OFResults/Orthogroups.tsv", sep = "\t", index_col = 0).notnull().astype('int')
OGs_lone = pd.read_table("Data/OFResults/Orthogroups_UnassignedGenes.tsv", index_col = 0).notnull().astype('int')

OGs = pd.concat([OGs,OGs_lone])

OGs.sum(1).value_counts().plot.bar()
plt.savefig('Data/output/OFOG_Prevalance.png')

# OGs = pd.read_table("Data/OFResults/Orthogroups.GeneCount.tsv", sep = "\t")#, index_col = 0)
# OGs = OGs.drop("Total",axis=1)
#
# SpCount = OGs.shape[1]
#
# OGs_lone = pd.read_table("Data/OFResults/Orthogroups_UnassignedGenes.tsv", index_col = 0).notnull().astype('int')
# OGs = pd.concat([OGs,OGs_lone])
#
# plt.rcParams['axes.spines.right'] = False
# plt.rcParams['axes.spines.top'] = False
#
# OGsMeta = pd.DataFrame(index=OGs.index)
# OGsMeta["DistCount"] = "NaN"
# OGsMeta.DistCount = SpCount - OGs.eq(0).sum(axis=1)
# OGsMeta
#
# Counts = OGsMeta.DistCount.value_counts().sort_index()
#
# plt.figure(figsize=(10, 5))
# plt.bar(Counts.index,Counts, align="center")#, width = 0.5)
# plt.title("Binned OGs by prevalence in species")
# plt.yscale("log")
# plt.axis([-0.99, SpCount+0.99, 0.1, 20000])
# plt.xlabel("Species in OG")
# plt.ylabel("OG count")
#
# plt.savefig('Data/output/OFOG_Prevalance.png')
