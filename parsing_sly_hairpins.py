"""
This script takes a fasta file and look for "Solanum lycopersicum" within the headers. If present
then it extracts the header + associated fasta sequence"
"""

with open("hairpin.fa","r") as filin:
	lines = filin.readlines()

with open("hairpin.sly.fa","w") as fileout:
	for i in range(0,len(lines)-1,1):
		if "Solanum lycopersicum" in lines[i]:
			fileout.write(lines[i] + lines[i+1])

