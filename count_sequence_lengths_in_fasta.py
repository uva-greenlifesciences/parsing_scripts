"""
This script is aimed at counting and plotting the length distribution of sequences in a fasta file
"""

from Bio import SeqIO 

for record in SeqIO.parse(open("sly_stemloop_mirbase_v21.t.replaced.fasta","rU"),"fasta"):
    print record.id
    print record.seq


