import sys
 
"""

[Usage]python get_these_sequences_from_this_fasta.py [file with gene ids] [fastafilename] > [outputfasta]
"""

def fasta2seqhash_and_genelist(geneseqfile):
	
	line        = geneseqfile.readline()
	currentgene = line[1:].strip()
	
	seq      =''
	gene_seq = {}
	line     = geneseqfile.readline()
	genelist = []
	while len(line)>0:
		if line[0]=='>':
			if gene_seq.has_key(currentgene) and gene_seq[currentgene] != seq: print 'key', currentgene, "already exists, with a different sequence! I will overwrite it. I suggest you will set keep_whole_header to 'True'"
			
			gene_seq[currentgene]=seq
			genelist.append(currentgene)
			#intialize new
			currentgene = line[1:].strip()
			seq         = ''
		else:
			#add this line to sequence
			seq += line.strip()
		line = geneseqfile.readline()
	
	#don't forget the last one :-)
	gene_seq[currentgene]=seq
	genelist.append(currentgene)
	
	return gene_seq, genelist
	
	

if __name__ == "__main__":
	if len(sys.argv) > 2:
		genelistfile  = sys.argv[1]
		fastafilename = sys.argv[2]
		
		selected_genes = set([])
		infile = open(genelistfile)
		lines  = infile.readlines()
		
		if len(lines) == 1: # Microsoft office screwed up file...
			infile.close()
			infile = open(genelistfile)
			lines  = infile.read().split('\r')
			
		for line in lines:
			selected_genes.add(line.strip())
	
		
		gene_seq, genelist = fasta2seqhash_and_genelist(open(fastafilename))
		for gene in genelist:
			if gene in selected_genes:
				print '>'+gene+'\n'+gene_seq[gene]
	else:
		print 'Please provide the file with selected fastaheaders, and the fastafile'
						
