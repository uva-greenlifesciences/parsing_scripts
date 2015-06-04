"""
This script removes "NNNNN" from fasta files and keep them formated with 60 nucleotides per line)
Usage: python removes_NNN_from_fasta.py [input file] [outputfasta]
"""

import sys
from Bio import SeqIO

filin = open(sys.argv[1],'r')
#filout = open(sys.argv[2],'w')

for record in SeqIO.parse(filin,'fasta'):
  filteredSeq = str(record.seq).replace('n','')
  outputLines = [filteredSeq[i:i+60] for i in range(0, len(filteredSeq), 60)]

  print ">" + record.id
  for outputLine in outputLines:
    print outputLine
