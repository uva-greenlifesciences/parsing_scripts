import sys
from Bio import SeqIO


"""
To clean sequences: remove duplicate sequences, remove too short sequences and remove sequences with too many unknown nucleotides "N"
python sequence_cleaner.py Aip_coral.fasta 10 10
"""

def sequence_cleaner(fasta_file):
    #create our hash table to add the sequences
    sequences={}
 
    #Using the biopython fasta parse we can read our fasta input
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        #Take the current sequence
        sequence=str(seq_record.seq).upper()
        if sequence not in sequences:
            sequences[sequence]=seq_record.id
       #If It is already in the hash table, We're just gonna concatenate the ID of the current sequence to another one that is already in the hash table
        else:
        	sequences[sequence]+="_"+seq_record.id
 
 
    #Write the clean sequences
 
    #Create a file in the same directory where you ran this script
    output_file=open("clear_"+fasta_file,"w+")
    #Just Read the Hash Table and write on the file as a fasta format
    for sequence in sequences:
            output_file.write(">"+sequences[sequence]+"\n"+sequence+"\n")
    output_file.close()

sequence_cleaner(sys.argv[1])