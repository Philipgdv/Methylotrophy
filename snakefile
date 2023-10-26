configfile: "config.yaml"

TaxonID=config["TaxonID"]

#UPID_OOI    = open("Data/input/UPID_OOI.txt", "r").read
#UPIDs       = open("Data/input/UPIDs.txt", "r").read.split("\n")
#TaxonID        = config["TaxonID"]

import pandas as pd
UPIDs = pd.read_csv("Data/input/SpeciesIndexDF.tsv", sep="\t").iloc[:,0]

#UPIDs = list(filter(None, open("Data/input/UPIDs.txt", "r").read().split("\n")))

#EggNOG_Kingdoms  = {"2":"eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2/2_raw_algs.tar",
EggNOG_Kingdoms  = {"2759":"eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2759/2759_raw_algs.tar",
                    "2157":"eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2157/2157_raw_algs.tar"}

KingdomTaxIDs = EggNOG_Kingdoms.keys()

rule all:
    input:
        expand("Data/input/Proteomes/{UPID}.fasta", UPID = UPIDs),
        "Data/input/AllGenes.fasta",
        'Data/output/AssemblyQC.png',
        "Data/OFResults/Orthogroups.tsv",
        "Data/OFResults/MultipleSequenceAlignments/OFOG_Representatives.fasta"#"Data/output/OFOG_Prevalance.png"
#        "Data/input/Proteomes/OrthoFinder/Results_OF/Orthogroups/Orthogroups.tsv"
#        expand("Data/input/EggNOG/{TaxID}/*.raw_alg.faa.gz", TaxID=KingdomTaxIDs)#expand("Data/input/EggNOG/{TaxID}.tar", TaxID=KingdomTaxIDs)

rule Setup:
    output: 'Data/output/AssemblyQC.png','Data/input/UPID_OOI.txt','Data/input/TaxonID.txt'
    params: TaxonID=config["TaxonID"]
    script: "python Scripts/Setup.py {params.TaxonID}"

rule download_UP:
    output: expand("Data/input/Proteomes/{UPID}.fasta.gz", UPID = UPIDs)
    shell: "python Scripts/DownloadProteome.py"

rule gunzip_UP:
    input: "Data/input/Proteomes/{UPID}.fasta.gz"
    output: "Data/input/Proteomes/{UPID}.fasta"
    shell: "gunzip Data/input/Proteomes/{wildcards.UPID}.fasta.gz"

rule GatherFASTAs:
    input: expand("Data/input/Proteomes/{UPID}.fasta", UPID = UPIDs)
    output: "Data/input/AllGenes.fasta"
    shell: "Scripts/FASTAHeaders.sh"

rule orthofinder:
	input: expand("Data/input/Proteomes/{UPID}.fasta", UPID = UPIDs)
	output: "Data/OFResults/Orthogroups.tsv",'Data/OFResults/Orthogroups_UnassignedGenes.tsv'
	threads: 50
#	conda: "envs/ortho.yaml"
#	log: "log_of.txt"
	shell: "bash Scripts/run_orthofinder.sh {threads}"#" > {log}"

rule VisulaizeOF_results:
    input: "Data/OFResults/Orthogroups.tsv", 'Data/OFResults/Orthogroups_UnassignedGenes.tsv'
    output: "Data/output/OFOG_Prevalance.png"
    shell: "python Scripts/VisualizeOF.py"

rule OFOG_Representatives:
    input: "Data/OFResults/Orthogroups.tsv"
    output: "Data/OFResults/MultipleSequenceAlignments/OFOG_Representatives.fasta"
    shell: "Scripts/OFOG_Representatives.sh"

#orthofinder -f Data/input/Proteomes/UP000070043.fasta Data/input/Proteomes/UP000070149.fasta -n OrthoFinder -oa

#rule download_EggNOG:
#    output: expand("Data/input/EggNOG/{TaxID}/*.raw_alg.faa.gz", TaxID=KingdomTaxIDs)
#    params: download_link = lambda w: EggNOG_Kingdoms[w.KingdomTaxIDs]
#    shell: "wget -qO- {params.download_link} |  tar xvz -C Data/input/EggNOG/{}"
#    shell: "curl -L {params.download_link} | tar -xf"# -o {output}"

#rule EggNOG_untar:
#    input: expand("Data/input/EggNOG/{TaxID}/*.raw_alg.faa.gz", UPID=UPIDs)#"Data/input/EggNOG/{TaxIDs}.tar"
#    output: "Data/input/EggNOG/{TaxIDs}.tar"
#    shell: "tar -xf {input}"
#rule untar_EggNOG:
#    input: "Data/input/EggNOG/{TaxIDs}.tar"
#    output: "Data/input/EggNOG/{TaxIDs}.fasta"
#    shell: "tar -xz {input} > {output}"

#rule download_EggNOG:
#    params:
#        url = "eggnog5.embl.de/download/eggnog_5.0/per_tax_level/{TaxIDs}/{TaxIDs}_raw_algs.tar",#, KingdomTaxIDs = ["2","2759","2157"])
#    output:
#        EggNOG = "Data/input/EggNOG/{TaxIDs}.tar", TaxIDs = KingdomTaxIDs),#config["KingdomTaxIDs"])
#    shell:
#        "curl {params.url} > {output.EggNOG}"

#rule download_UP:
#    output: "Data/input/Proteomes/{wildcards.UPID}.fasta.gz"
#    shell: "python Scripts/DownloadProteomes.py {UPID_OOI} {TaxonID}"

#rule gunzip_UP:
#    input: "Data/input/Proteomes/{wildcards.UPID}.fasta.gz"
#    output: "Data/input/Proteomes/{wildcards.UPID}.fasta"
#    shell: "gunzip {input} > {ouput}"

#rule GatherFASTAs:
#    input: "Data/input/Proteomes/{wildcards.UPID}.fasta"
#    output: "Data/input/AllGenes.fasta"
#    shell: "Scripts/FASTAHeaders.sh"

#rule initialize:
#    output:
#        UPID_OOI = "Data/input/UPID_OOI.txt",
#        TaxonID = "Data/input/TaxonID.txt"
#    shell: "Scripts/prompt.sh"

#rule UPID_list:
#    input:
#        UPID_OOI = "Data/input/UPID_OOI.txt",
#        TaxonID = "Data/input/TaxonID.txt"
#    output:
        #FASTAS = expand("Data/input/Proteomes/{n}.fasta", n=links.keys()),
#        QPlot = "Data/output/AssemblyQuality.png",
#        list = "Data/input/UPIDs.txt" #Something wrong here!
#    shell: "python Scripts/DownloadProteomes.py {input.UPID_OOI} {input.TaxonID}"





#def read_TaxonUPID_output():
#    with open('Data/input/UPIDs.txt') as f:
#        UPIDs = [UPIDs for UPIDs in f.read().split('\n') if len(UPIDs) > 0]  # we dont want empty lines
#        return expand("{UPID}", UPID=UPIDs)

#rule downloadUPIDs:
#    input: read_TaxonUPID_output()
#    shell: "curl https://rest.uniprot.org/uniprotkb/stream?query=proteome:{input}&format=fasta&compressed=false&includeIsoform=true | gunzip -c > {UPID}.fasta"

#IDS, = glob_wildcards("Data/input/Proteomes/{UPIDs}.fasta")
#rule all:
#    input:  expand("Data/input/Proteomes/{UPIDs}.fasta", id=UPIDs)
#glob_wildcards("Data/RawReads/{UPIDs}.fasta")

#rule GatherFASTAs:
#    input: "Data/input/Proteomes/*.fasta"
#    output: "Data/input/AllGenes.fasta"
#    shell: "Scripts/FASTAHeaders.sh"

#rule DwnldEggNOG
#    input: "2","2157","2759"
#    output
#    shell: http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2/2_raw_algs.tar
#    http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2759/2759_raw_algs.tar
#    http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/2157/2157_raw_algs.tar

#rule report:
#    input:"Data/input/Proteomes/*.fasta"
#    output:"report.txt"
#    shell: "ls Data/input/Proteomes/ >> report.txt"
