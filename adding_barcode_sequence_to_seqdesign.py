"""
Testing pandas for adding the adapter+barcode sequence as a last column
"""

# Import libraries
import pandas as pd
import os

# importing data
seqdesign = pd.read_csv("seqdesign.txt",sep="\t")
barcodes = pd.read_csv("barcodes.txt",sep="\t")

# merging seqdesign with barcodes to get the sequence
seqdesign_with_barcodes = pd.merge(seqdesign,barcodes,on="Barcode",how="inner") # inner = inner join --> use intersection of keys from both data frame
seqdesign_with_barcodes.to_csv("seqdesign_with_barcodes_seqs.txt",sep="\t",index=False)