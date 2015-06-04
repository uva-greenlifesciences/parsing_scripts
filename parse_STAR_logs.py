'''
Reads a star log file (final mapping results) and output:
1) the number of input reads 
2) the percentage of uniquely mapped reads
3) the percentage of reads mapped to too many loci
4) the percentage of reads unmapped (too many mismatches) 
'''

import re
import os

#### for one starlog file #######
filename_p = re.compile('\S+_Log.final.out') # creates a pattern object (compiled reg expression)
input_reads_p = re.compile('Number of input reads\s+\|\s+(.*)')
unique_reads_p = re.compile('Uniquely mapped reads %\s+\|\s+(.*)')
multiple_hits_p = re.compile('% of reads mapped to multiple loci\s+\|\s+(.*)')
input_reads=''
unique_reads=''
multiple_hits=''


with open("starlogs.parsed.txt", 'w') as outfile:
	outfile.write('Sample\tNumber of input reads\t% Uniquely mapped reads\t% of reads mapped to multiple loci\n')
	for file in os.listdir("./"):
		sample=filename_p.search(file) # pass the search method to the pattern object and returns matched object or None
		if sample:
			with open(file, 'r') as filin:
				for line in filin:
					if input_reads_p.search(line):
						input_reads=input_reads_p.search(line).group(1)
					elif unique_reads_p.search(line):
						unique_reads=unique_reads_p.search(line).group(1)
					elif multiple_hits_p.search(line):
						multiple_hits=multiple_hits_p.search(line).group(1)
			outfile.write('{0}\t{1}\t{2}\t{3}\n'.format(sample.group(),input_reads,unique_reads,multiple_hits))

# with open("starlogs.parsed.txt", 'w') as outfile:
# 	outfile.write('sample\tNumber of input reads\t% Uniquely mapped reads\t% of reads mapped to multiple loci\n')
# 	for samplefilename in os.listdir("./"):
# 		sample=filename_p.search(samplefilename)
# 		print sample
# 		with open(samplefilename, 'r') as file:
# 			for line in file:
# 				if input_reads_p.search(line):
# 					input_reads=input_reads_p.search(line)
# 				elif unique_reads_p.search(line):
# 					unique_reads=unique_reads_p.search(line)
# 				elif multiple_hits_p.search(line):
# 					multiple_hits=multiple_hits_p.search(line).group(1)
# 		outfile.write('{0}\t{1}\t{2}\t{3}\n'.format(sample,input_reads,unique_reads,multiple_hits))

