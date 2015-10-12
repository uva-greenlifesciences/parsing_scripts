"""
This script:
1/ parses the hairpin and mature microRNAs from miRBase to keep only the Viridiplantae species microRNAs (with
the exception of Solanum lycopersicum).
2/ It collapses sequences to obtain non-redundant hairpin and mature microRNA sequences for Viridiplantae
3/ It then verifies that the non-redundant Viridiplantae miRNA sequences are not in the S.lycopersicum miRNA sequences.
4/
5/ Build the subsquent 

It 
It subsequently builds the corresponding Bowtie2 indexes
"""


import os
import glob
import re
from subprocess import call
from Bio.Seq import Seq, Alphabet, IUPAC
from Bio import SeqIO
from Bio.Alphabet import IUPAC
from Bio.SeqRecord import SeqRecord

############################## Inputs ######################################################################
# Directory to output Bowtie2 index
DIR = "/home/mgalland/data/02_refs/miRBase_v21/"

# original miRBase files (all microRNAs in miRBase)
HAIRPIN = "hairpin.fa"
MATURE = "mature.fa"

# original miRBase files for Solanum lycopersicum
HAIRPIN_SLY = "sly_stemloop_mirbase_v21.fasta"
MATURE_SLY = "sly_mature_mirbase_v21.fasta"

# correspondence between organism short name and phylogeny
ORGANISMS = "organisms.txt"

# final desired file for hairpin and mature miRNA file
MATURE_FINAL = "sly_and_viridiplantae.mature.fa"
HAIRPIN_FINAL = "sly_and_viridiplantae.hairpin.fa"

 
############### Utilities & functions #####################################
# function to remove redundancy in fasta files
def sequence_cleaner(fasta_file,min_length=0,por_n=100):
    #create our hash table to add the sequences
    sequences={}
 
    #Using the biopython fasta parse we can read our fasta input
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        #Take the current sequence
        sequence=str(seq_record.seq).upper()
        #Check if the current sequence is according to the user parameters
        if (len(sequence)>=min_length and (float(sequence.count("N"))/float(len(sequence)))*100<=por_n):
       # If the sequence passed in the test "is It clean?" and It isnt in the hash table , the sequence and Its id are going to be in the hash
            if sequence not in sequences:
                sequences[sequence]=seq_record.id
       #If It is already in the hash table, We're just gonna concatenate the ID of the current sequence to another one that is already in the hash table
            else:
                sequences[sequence]+="_"+seq_record.id
 
    #Write the clean sequences
 
    #Create a file in the same directory where you ran this script
    output_file=open("collapsed."+fasta_file,"w+")
    #Just Read the Hash Table and write on the file as a fasta format
    for sequence in sequences:
            output_file.write(">"+sequences[sequence]+"\n"+sequence+"\n")
    output_file.close()


########################################### Pipeline ########################
files = [HAIRPIN,MATURE]
sly_files = [HAIRPIN_SLY,MATURE_SLY]

# clean any left over files containing viridiplantae
for f in glob.glob(DIR + "viridiplantae"):
	os.remove(f)
# search for files that matches Bowtie2 index + remove them
bowtie_index_files = [f for f in os.listdir("./") if re.search("bt2$",f)] 
for f in bowtie_index_files:
	os.remove(f)

# filter organisms to keep viridiplantae
with open(ORGANISMS,"r") as filin:
	lines = filin.readlines()
	new_lines = [line.strip() for line in lines]
	viridiplantae_wo_sly = [l for l in new_lines if "Viridiplantae" in l and "Solanum lycopersicum" not in l]
	species = [v[0:4].strip() for v in viridiplantae_wo_sly]	

# import global miRBase files
# filter with Viridiplantae species that are not S.lycopersicum
# convert to IUPACUnambiguousRNA and then back transcribe to DNA
# remove sequence redundancy
for f in files:
	with open(f,"r") as filin, open(str(f.split(".")[0] + ".viridiplantae.wo_sly.fasta"),"w") as fileout:
		records = []
		for record in SeqIO.parse(filin,"fasta"):
			for specie in species:
				if specie in record.id[0:3]:
					record.seq = Seq(str(record.seq),IUPAC.unambiguous_rna)
					record.seq = record.seq.back_transcribe()
					records.append(record)
				else:
					pass
		SeqIO.write(records,fileout,"fasta")

for f in files:
	sequence_cleaner(str(f.split(".")[0] + ".viridiplantae.wo_sly.fasta")) 

# get mature and hairpin miRNA sequences for Solanum lycopersicum records in two lists (to filter them from Viridiplantae file)
if len(sly_files) > 2:
	print("check that you have only one mature miRNA and one precursor miRNA miRBase files for Solanum lycopersicum")
else:
	for sly_f in sly_files:
		if "mature" in sly_f:	
			with open(sly_f,"r") as infile:
				sly_mature_seqs = []		
				for record in SeqIO.parse(infile,"fasta"):
					record.seq = Seq(str(record.seq),IUPAC.unambiguous_rna)
					record.seq = record.seq.back_transcribe()
					sly_mature_seqs.append(str(record.seq))
		elif "hairpin" or "stemloop" in sly_f:
			with open(sly_f,"r") as infile:
				sly_hairpin_seqs = []
				for record in SeqIO.parse(infile,"fasta"):
					record.seq = Seq(str(record.seq),IUPAC.unambiguous_rna)
					record.seq = record.seq.back_transcribe()
					sly_hairpin_seqs.append(str(record.seq))
		else:
			print("check that file name for Solanum lycopersicum contains 'mature' or 'hairpin/stemloop'")	

# Collapse mature and hairpin miRNA sequences for Viridiplantae (excluding Solanum lycopersicum) 
collapsed_files = [str("collapsed."+f.split(".")[0] + ".viridiplantae.wo_sly.fasta") for f in files if f.endswith(".fasta") or f.endswith(".fa")]
collapsed_names = [f.split(".fasta")[0] for f in collapsed_files]

for i in list(range(0,len(collapsed_files),1)):
	if "mature" in collapsed_files[i]:
		with open(collapsed_files[i],"r") as filin, open(str(collapsed_names[i] + ".filtered.fasta"),"w") as fileout:
			records = []	
			for record in SeqIO.parse(filin,"fasta"):
				if str(record.seq) in sly_mature_seqs:
					pass
				else:
					records.append(record)
			SeqIO.write(records,fileout,"fasta")
	if "hairpin" or "stemloop" in collapsed_files[i]:
		with open(collapsed_files[i],"r") as filin, open(str(collapsed_names[i] + ".filtered.fasta"),"w") as fileout:
			records = []	
			for record in SeqIO.parse(filin,"fasta"):
				if str(record.seq) in sly_mature_seqs:
					pass
				else:
					records.append(record)
			SeqIO.write(records,fileout,"fasta")

# Concatenate Solanum lycopersicum miRBase and all other plant Viridiplantae species non-reundant miRBase records in two fasta files (hairpin + mature)
collapsed_and_filtered_files = [collapsed_name + ".filtered.fasta" for collapsed_name in collapsed_names]

final_files = [MATURE_FINAL,HAIRPIN_FINAL]

for f in collapsed_and_filtered_files:
	if "mature" in f:
		call("cat " + MATURE_SLY + " " + f + " > " + MATURE_FINAL,shell=True)
	if "hairpin" in f:
		call("cat " + HAIRPIN_SLY + " " + f + " > " + HAIRPIN_FINAL,shell=True)
				 

# Create bowtie-2 indexes for viridiplantae
for f in final_files:
	call("bowtie2-build --quiet" +  " " + f + " " + f,shell=True)



