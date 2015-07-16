"""
Addition of a column to the "seqdesign.txt" file that contains the left adapter + barcode + internal adapter sequence
This sequence will then be used by fastx_clipper to remove the adapter from the small RNA read sequence
Goal: facilitating the trimming of adapter sequences from small RNAs
"""

# importation of the table that links the barcode used (e.g. BC01) to the complete sequence to be removed
with open("barcodes.txt","r") as filin:
    barcodes = filin.readlines()

# reading the seqdesign file that contains sample id + barcode used + other informations
with open("seqdesign.txt","r") as filin:
    lines = filin.readlines()

# removal of hidden characters
newlines = []
newlines2 = []

for line in lines:
   	newlines.append(line.strip())

for line in newlines:
	newlines2.append(line.split("\t"))

# we make the correspondence between the barcode and its sequence
barcodes_split = []
for barcode in barcodes:
	barcodes_split.append(barcode.strip().split("\t"))

for i in range(1,len(newlines2),1):
	for j in range(1,len(barcodes_split),1):
		if newlines2[i][1] == barcodes_split[j][0]:
			newlines2[i].append(barcodes_split[j][1])

with open("seqdesign.modified.txt","w") as filout:
	for line in newlines2:
		for item in line:
			filout.write(item + "\t")

