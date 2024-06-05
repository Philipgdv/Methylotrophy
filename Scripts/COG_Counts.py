#!/usr/bin/python3

import glob
import numpy as np
import pandas as pd
import urllib.request
from ete3 import NCBITaxa

# Load Orthofinder data and emapper annotations
filepath = glob.glob('Data/input/*.emapper.annotations.*sv')[0]
emapper = pd.read_csv(filepath, sep ="\t", comment = "#", header = None)
emapper.columns = ["query","seed_ortholog","evalue","score","eggNOG_OGs","max_annot_lvl","COG_category","Description","Preferred_name","GOs","EC","KEGG_ko","KEGG_Pathway","KEGG_Module","KEGG_Reaction","KEGG_rclass","BRITE","KEGG_TC","CAZy","BiGG_Reaction","PFAMs"]

OFOGs = pd.read_csv("Data/OFResults/Orthogroups.GeneCount.tsv", sep ="\t", comment = "#", index_col = 0, header = 0)

OFOG_Annot = pd.DataFrame()
OFOG_Annot["OFOG"] = emapper["query"].str.split(".",expand=True)[0]
OFOG_Annot["COG"] = emapper["eggNOG_OGs"].str.split("@",expand=True)[0]
OFOGs = OFOGs.loc[OFOG_Annot.OFOG]
OFOGs = OFOGs.merge(OFOG_Annot, how= "left", left_on=None, right_on="OFOG", left_index=True, right_index=False)
OFOGs = OFOGs.set_index("COG")
OFOGs = OFOGs.drop(axis = 1, labels = ["Total", "OFOG"])
OFOGs = OFOGs.groupby(by=OFOGs.index, axis=0).sum() #some OFOGs correspond to the same COG, and need to be summed up

## Group Asgardarchaea by taxonomic sub group, taking the median gene count value for each. Used because of incomplete genome assemblies.
ProposedClass = pd.read_csv("Data/input/ProposedClassification.csv", sep =",", comment = "#", header = 0, index_col = "UPID")
data = OFOGs.T.merge(ProposedClass, how = "left", left_index=True, right_index=True)
OFOGs = data.groupby(data.iloc[:,-1]).median().T

# Retrieve EggNOG gene counts
urllib.request.urlretrieve("http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/1/1_members.tsv.gz", "Data/input/1_members.tsv.gz")
Root_OGs = pd.read_csv("Data/input/1_members.tsv.gz", sep ="\t", comment = "#", header = None, index_col = 1)
Root_OGs["list"] = Root_OGs[4].str.split(",", expand = False)
Root_OGs = Root_OGs["list"].explode().str.split(".", expand = True, n=1)
Root_OGs.columns = ["species","gene"]
Root_OGs = Root_OGs.reset_index()
Root_OGs.columns = ["COG","species","gene"]
Root_OGs = Root_OGs.groupby(["COG","species"]).count().unstack().fillna(0)
Root_OGs.columns = Root_OGs.columns.droplevel(0)

# Combine both Dataframes
OFOGs = OFOGs.reindex(Root_OGs.index, fill_value=0) #fill the dataframe with 0s for all other COGs not occuring in the OrthoFinder analysis
Root_OGs = pd.concat([Root_OGs, OFOGs], axis=1)

# Filter by taxonomy
ncbi = NCBITaxa()
Taxonomy = pd.DataFrame(index = Root_OGs.columns)
Taxonomy["Kingdom"] = "NaN"
Taxonomy["Order"] = "NaN"

for ID in Taxonomy.index:
    if ID.isnumeric():
        Taxonomy.Kingdom[ID] = ncbi.get_lineage(ID)[2]
        Taxonomy.Order[ID] = ncbi.get_lineage(ID)[3]
    else: 
        Taxonomy.Kingdom[ID] = 2157
        Taxonomy.Order[ID] = 1935183

TaxCount = pd.DataFrame(Taxonomy[Taxonomy.Kingdom != 2759].groupby("Order").size())
TaxCount["Name"] = ncbi.get_taxid_translator(TaxCount.index)

Root_OGs = Root_OGs.loc[:,Taxonomy.Kingdom != 2759] # Exclude eukaryotes

## Select only OGs spread over 2 or more taxonomic orders
Order = pd.DataFrame(index = Root_OGs.index, columns = Taxonomy.Order.unique())

for Ord in Taxonomy.Order.unique():
    Order[Ord] = Root_OGs.loc[:,Taxonomy.Order == Ord].sum(axis = 1)

OrderBool = Order > 0
Root_OGs = Root_OGs[OrderBool.sum(axis = 1) > 1]

# Save to files
Root_OGs.to_csv("Data/output/AllOFOG&eOGCounts.csv")

## Create a demo file
Sample = Taxonomy.groupby('Order').sample(5, replace= True) # Randomly pick 5 species per taxonomic order
SubsetSpecies = Sample[~Sample.index.duplicated(keep='first')].index.to_list() # Drop duplicates created for order's with fewer than 5 species in EggNOG
RefSpecies = ["Loki 4","Thor","574087","931626","264732","33035","1123288","903814","748727","545694","903818","243232","426368","192952","323259","304371","410358","456320","419665","339860"] # List the reference species used in the notebooks
DemoSpecies = RefSpecies + list(set(SubsetSpecies) - set(RefSpecies))# Merge both lists

SubsetGenes = Root_OGs.sample(100, replace= True).index.to_list() # Randomly pick gene families
RefGenes = pd.read_csv("Data/input/AllWLPGenes.csv", sep =";", comment = "#", header = 0).iloc[:,[0,1,6,7]].COG.to_list() # Add the WLP genes of interest
DemoGenes = RefGenes + list(set(SubsetGenes) - set(RefGenes)) # Merge both lists

Root_OGs.loc[Root_OGs.index.isin(DemoGenes), Root_OGs.columns.isin(DemoSpecies)].to_csv("Data/demo/OFOG&eOGCounts.csv") # Save to file
