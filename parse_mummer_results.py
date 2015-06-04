"""
This script parses the output of MUMmer genomic alignments
It extracts the coordinates of LYC4 scaffolds that are not aligned on the genome of S. lycopersicum Heinz1706
If not present on chromosome 8, then it extracts the scaffold coordinates
Ultimate goal: generate a BED file to filter .bam files generated from alignments of LA1777/LA2167/PI127826/F1/LA3935 mRNA-Seq data on
LYC4 scaffolds --> find expressed P450 --> give that to Ruy for cloning
"""
import natsort  
import os
import sys

input_file = sys.argv[1]
output_

with open(sys.argv[1],"r") as f:
	lignes = f.readlines()
	lignes = lignes[5:]
	print(lignes)

with open("aln.txt","r") as f:
	lines = f.readlines()
	lines = lines[5:]

######## parsing the MUMmer file ###########
# initialization of the lists_of_lists
list_of_lists = []
for line in lines:
	inner_list = line.strip() # strip() works on a string and return a string
	inner_list2 = inner_list.split("|") # split() works on a string and return a list
	list_of_lists.append(inner_list2)


# extraction as two lists of the coordinates on chromosome 8 (cultivated tomato) and on the genomic scaffolds of LYC4 (wild tomato)
chr8_coords = []
scaffolds_coords = []

for i in range(0,len(list_of_lists),1):
	chr8_coords.append(list_of_lists[i][0])
	scaffolds_coords.append(list_of_lists[i][1])
	
chr8 = []
scaffolds = []

for i in range(0,len(chr8_coords),1):
	chr8.append(chr8_coords[i].split())
	scaffolds.append(scaffolds_coords[i].split())


# Calculating gaps
# gap1 = distance between end of alignement i and start of alignment i+1 on chromosome 8 (S.lycopersicum)
# gap2 = distance between end of alignment i and start of alignment i+1 on scaffolds (S.habrochaites)
gap1 = []
gap2 = []
for i in range(0,len(chr8)-1,1):
	gap1.append(int(chr8[i+1][0]) - int(chr8[i][1]))
	gap2.append(int(scaffolds[i+1][0]) - int(scaffolds[i][1]))

# extracting interesting scaffolds coordinates
left = []
right = []
left_name = []
right_name = []

for i in range(0,len(gap1)-1,100):
	if abs(gap1[i]) < abs(gap2[i]):
		left.append(scaffolds[i][1])
		left_name.append(list_of_lists[i][-1].split()[-1])
		right.append(scaffolds[i+1][0])
		right_name.append(list_of_lists[i+1][-1].split()[-1])


######### final list ################
scaffolds_coords = []

# we first test if the scaffold names correspond to each other (since undesired gaps exist also between scaffolds)
for i in range(0,len(left_name),1):
	if left_name[i] == right_name[i]:
		scaffolds_coords.append(str(left_name[i]+"\t"+left[i]+"\t"+right[i]))
		scaffolds_coords.sort()
		natsort.natsorted(scaffolds_coords)

with open("chr8.bed","w") as fileout:
	for line in scaffolds_coords:
		if int(line.split("\t")[2]) > int(line.split("\t")[1]):
			fileout.write(line+"\n")
		else:
			fileout.write(line.split("\t")[0]+"\t"+line.split("\t")[2]+"\t"+line.split("\t")[1]+"\n")



# import os

# def get_filepaths(directory):
#     """
#     This function will generate the file names in a directory 
#     tree by walking the tree either top-down or bottom-up. For each 
#     directory in the tree rooted at directory top (including top itself), 
#     it yields a 3-tuple (dirpath, dirnames, filenames).
#     """
#     file_paths = []  # List which will store all of the full filepaths.

#     # Walk the tree.
#     for root, directories, files in os.walk(directory):
#         for filename in files:
#             # Join the two strings in order to form the full filepath.
#             filepath = os.path.join(root, filename)
#             file_paths.append(filepath)  # Add it to the list.

#     return file_paths  # Self-explanatory.

# # Run the above function and store its results in a variable.   
# full_file_paths = get_filepaths("/Users/johnny/Desktop/TEST")

# for f in full_file_paths:

#   if f.endswith(".dat"):

#     print f




