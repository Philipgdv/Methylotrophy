configfile: "config.yaml"

import pandas as pd
UPIDs = pd.read_csv("Data/input/SpeciesIndexDF.tsv", sep="\t").iloc[:,0]

EggNOG_Kingdoms  = {"2759":"eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2759/2759_raw_algs.tar",
                    "2157":"eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2157/2157_raw_algs.tar"}

KingdomTaxIDs = EggNOG_Kingdoms.keys()

rule all:
    input:
        expand("Data/input/Proteomes/{UPID}.fasta", UPID = UPIDs),
        "Data/input/Proteomes/AllGenes.fasta",
        "Data/OFResults/Orthogroups.tsv",
        "Data/OFResults/MultipleSequenceAlignments/OFOG_Representatives.fasta"

rule download_UP:
    output: expand("Data/input/Proteomes/{UPID}.fasta.gz", UPID = UPIDs)
    shell: "python Scripts/DownloadProteome.py"

rule gunzip_UP:
    input: "Data/input/Proteomes/{UPID}.fasta.gz"
    output: "Data/input/Proteomes/{UPID}.fasta"
    shell: "gunzip Data/input/Proteomes/{wildcards.UPID}.fasta.gz"

rule GatherFASTAs:
    input: expand("Data/input/Proteomes/{UPID}.fasta", UPID = UPIDs)
    output: "Data/input/Proteomes/AllGenes.fasta"
    shell: "Scripts/FASTAHeaders.sh"

rule orthofinder:
	input: expand("Data/input/Proteomes/{UPID}.fasta", UPID = UPIDs)
	output: "Data/OFResults/Orthogroups.tsv",'Data/OFResults/Orthogroups_UnassignedGenes.tsv'
	threads: 8
	shell: "bash Scripts/run_orthofinder.sh {threads}"

rule VisulaizeOF_results:
    input: "Data/OFResults/Orthogroups.tsv", 'Data/OFResults/Orthogroups_UnassignedGenes.tsv'
    output: "Data/output/OFOG_Prevalance.png"
    shell: "python Scripts/VisualizeOF.py"

rule OFOG_Representatives:
    input: "Data/OFResults/Orthogroups.tsv"
    output: "Data/OFResults/MultipleSequenceAlignments/OFOG_Representatives.fasta"
    shell: "Scripts/OFOG_Representatives.sh"