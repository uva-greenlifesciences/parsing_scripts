"""
this little script replaces "U" in miRBase stem loop tomato precursor microRNA sequences with a "T"
"""

with open("sly_stemloop_mirbase_v21.fasta","r") as filin:
	lines = filin.readlines()

with open("sly_stemloop_mirbase_v21.t.replaced.fasta","w") as fileout:
	for i in range(0,len(lines),1):
		if i % 2 == 0:
			fileout.write(lines[i])
		else:
			fileout.write(lines[i].replace("U","T"))