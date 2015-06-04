#!/usr/bin/env python
from Bio import SeqIO
for current_seq in SeqIO.parse("LA1777_transcript.filtered.fa", "fasta"):
    if current_seq.seq.tostring() != '':
        print ">", current_seq.id, "\n", current_seq.seq.tostring()