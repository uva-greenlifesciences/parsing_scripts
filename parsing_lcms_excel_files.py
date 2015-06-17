"""
This script takes all LC-MS files produced by Ruy Kortbeek (acylsugars) and output one tabular file per sample with all the
compounds organized in three columns
"""

import os

for file_present in os.listdir("./"):
	if file_present.endswith(".txt"):
		with open(file_present,"r") as filin:
			filin_content = filin.read()
			filin_splitted = filin_content.split("\r")
			lines_as_a_list = []
			for line in filin_splitted[1:]: # we do not read the first line
				lines_as_a_list.append(line.split("\t")) 
			samples = [] # getting sample names in a specific list
			for line in lines_as_a_list:
				samples.append(line[0])
			for sample in samples: # creating as many output files as there are different samples + each molecular compound is on a different line
				with(open("{0}.txt".format(sample),"w")) as output:
					output.write("Sample"+"\t"+"File"+"\t"+"Product_ion"+"\t"+"RT"+"\t"+"Area"+"\n")
					for line in lines_as_a_list:
						for i in range(5,len(line),3):
							if line[0] == sample:
								output.write(line[0]+"\t"+line[1]+"\t"+line[i]+"\t"+line[i+1]+"\t"+line[i+2]+"\n")	
					
							


