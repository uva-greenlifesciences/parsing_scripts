"""
Parsing the ERCC sequences ERCC RNA Spike-In Mix catalog #4456740
"""

# read file content line by line
with open("ERCC.txt","r") as filin:
	lines = []
	for line in filin:
		lines.append(line.split("\t"))

header = str(lines[0][0]+"\t"+lines[0][1]+"\t"+lines[0][2]+"\t"+lines[0][3]+"\t"+lines[0][4]+"\n")
print header
print lines[0:2]

with open("ERCC.parsed.fasta","w") as outfile:
	for line in lines[1:]:
		outfile.write(">" + line[0]+"\n"+ line[4])
