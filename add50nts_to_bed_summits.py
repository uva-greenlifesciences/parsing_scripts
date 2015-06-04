"""
This very little script takes a bed file (with the summit nucleotide position) and substract/add 50 nts to the start/end coordinate of the peak respectively)
Usage: python add50nts_to_bed_summits.py [input_file] [output_file]
"""
import sys

fileout = open(sys.argv[2],"w")

# creating three empty lists to receive the id + new coordinates
identifier = []
start_minus_50 = []
end_plus_50 = []

# reading the initial bed summit file that contains peak coordinates
list_of_lists = []
for line in open(sys.argv[1],"r"):
	list_of_lists.append(line.strip().split("\t")) # adding the results as a list that contains sublists (each sublist = one line)

# for each sublist (=line of original file), we substract or add 50 nucleotides --> new coordinates are sent to initialized lists
for sublist in list_of_lists:
	identifier.append(sublist[0])
	start_minus_50.append(int(sublist[1])-50)
	end_plus_50.append(int(sublist[2])+50)
	#print sublist

# we write to a tab delimited file 
for i in range(0,len(list_of_lists),1):
	fileout.write(identifier[i]+"\t"+str(start_minus_50[i])+"\t"+str(end_plus_50[i])+"\n")

